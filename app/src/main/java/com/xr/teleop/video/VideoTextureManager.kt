package com.xr.teleop.video

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.Log
import com.xr.teleop.NativeBridge
import kotlinx.coroutines.*
import java.io.BufferedInputStream
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL

/**
 * Pulls a MJPEG stream (multipart/x-mixed-replace) from a server and pushes
 * each decoded JPEG frame into the native renderer via NativeBridge.
 *
 * Usage:
 *   val mgr = VideoTextureManager(context)
 *   mgr.startStream("http://192.168.1.100:8000", "color")
 *   // later:
 *   mgr.stopStream()
 *   mgr.cleanup()
 */
class VideoTextureManager(private val context: Context) {

    interface FrameCallback {
        fun onFrame(bitmap: Bitmap)
        fun onError(message: String)
    }

    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())
    private var streamJob: Job? = null
    private var frameCallback: FrameCallback? = null

    @Volatile private var running = false

    companion object {
        private const val TAG = "VideoTextureManager"
        private const val CONNECT_TIMEOUT_MS = 5_000
        private const val READ_TIMEOUT_MS = 10_000
        private const val MJPEG_BOUNDARY_PREFIX = "--"
        private const val JPEG_SOI = 0xFF.toByte()
        private const val JPEG_SOI2 = 0xD8.toByte()
    }

    fun setFrameCallback(cb: FrameCallback) {
        frameCallback = cb
    }

    /**
     * Start streaming from [baseUrl]/[streamType].
     * e.g. baseUrl="http://192.168.1.100:8000", streamType="color"
     * Stops any previously running stream first.
     */
    fun startStream(baseUrl: String, streamType: String = "color") {
        stopStream()
        running = true
        val url = "$baseUrl/$streamType"
        Log.i(TAG, "Starting MJPEG stream from $url")
        streamJob = scope.launch {
            runStream(url)
        }
    }

    fun stopStream() {
        running = false
        streamJob?.cancel()
        streamJob = null
        Log.i(TAG, "Stream stopped")
    }

    fun cleanup() {
        stopStream()
        scope.cancel()
    }

    // -------------------------------------------------------------------------

    private suspend fun runStream(url: String) {
        while (running && isActive) {
            try {
                connectAndReadMjpeg(url)
            } catch (e: CancellationException) {
                break
            } catch (e: Exception) {
                Log.e(TAG, "Stream error: ${e.message}")
                frameCallback?.onError(e.message ?: "unknown error")
                if (running) {
                    delay(2_000)  // retry after 2 s
                }
            }
        }
    }

    private fun connectAndReadMjpeg(url: String) {
        val conn = (URL(url).openConnection() as HttpURLConnection).apply {
            connectTimeout = CONNECT_TIMEOUT_MS
            readTimeout = READ_TIMEOUT_MS
            requestMethod = "GET"
            connect()
        }

        try {
            if (conn.responseCode != 200) {
                throw IOException("HTTP ${conn.responseCode} from $url")
            }

            val contentType = conn.contentType ?: ""
            val input = BufferedInputStream(conn.inputStream, 65536)

            if (contentType.contains("multipart")) {
                readMjpegMultipart(input)
            } else {
                // Single JPEG or raw stream — decode once
                val bytes = input.readBytes()
                decodeAndPush(bytes)
            }
        } finally {
            conn.disconnect()
        }
    }

    /**
     * Parse a standard MJPEG multipart/x-mixed-replace stream.
     * Each part looks like:
     *   --boundary\r\n
     *   Content-Type: image/jpeg\r\n
     *   Content-Length: N\r\n
     *   \r\n
     *   <jpeg bytes>
     */
    private fun readMjpegMultipart(input: BufferedInputStream) {
        val buf = ByteArray(65536)
        val accumulator = ArrayList<Byte>(65536)

        while (running) {
            val bytesRead = input.read(buf)
            if (bytesRead < 0) break

            for (i in 0 until bytesRead) {
                accumulator.add(buf[i])
            }

            // Scan for JPEG SOI (0xFF 0xD8) ... EOI (0xFF 0xD9)
            val data = accumulator.toByteArray()
            var soiIdx = -1
            var eoiIdx = -1

            var i = 0
            while (i < data.size - 1) {
                if (data[i] == JPEG_SOI && data[i + 1] == JPEG_SOI2) {
                    soiIdx = i
                }
                if (soiIdx >= 0 && data[i] == 0xFF.toByte() && data[i + 1] == 0xD9.toByte()) {
                    eoiIdx = i + 2
                    break
                }
                i++
            }

            if (soiIdx >= 0 && eoiIdx > soiIdx) {
                val jpegBytes = data.copyOfRange(soiIdx, eoiIdx)
                decodeAndPush(jpegBytes)
                // Keep bytes after EOI
                val remaining = data.copyOfRange(eoiIdx, data.size)
                accumulator.clear()
                remaining.forEach { accumulator.add(it) }
            }

            // Prevent unbounded growth
            if (accumulator.size > 2_000_000) {
                Log.w(TAG, "Accumulator overflow, resetting")
                accumulator.clear()
            }
        }
    }

    private fun decodeAndPush(jpegBytes: ByteArray) {
        val bitmap = BitmapFactory.decodeByteArray(jpegBytes, 0, jpegBytes.size)
            ?: run {
                Log.w(TAG, "Failed to decode JPEG (${jpegBytes.size} bytes)")
                return
            }

        // Ensure ARGB_8888 format for pixel extraction
        val argbBitmap = if (bitmap.config == Bitmap.Config.ARGB_8888) {
            bitmap
        } else {
            bitmap.copy(Bitmap.Config.ARGB_8888, false).also { bitmap.recycle() }
        }

        val w = argbBitmap.width
        val h = argbBitmap.height
        val pixels = IntArray(w * h)
        argbBitmap.getPixels(pixels, 0, w, 0, 0, w, h)
        argbBitmap.recycle()

        if (NativeBridge.isLibraryLoaded()) {
            NativeBridge.nativeUpdateVideoFrame(pixels, w, h)
        }

        frameCallback?.onFrame(
            BitmapFactory.decodeByteArray(jpegBytes, 0, jpegBytes.size)
                ?: return
        )
    }
}
