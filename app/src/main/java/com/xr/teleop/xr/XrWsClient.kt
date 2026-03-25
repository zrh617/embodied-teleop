package com.xr.teleop.xr

import android.util.Log
import java.util.concurrent.TimeUnit
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.WebSocket
import okhttp3.WebSocketListener

class XrWsClient(
    private val url: String = DEFAULT_URL,
) {
    private val client = OkHttpClient.Builder()
        .pingInterval(10, TimeUnit.SECONDS)
        .build()

    @Volatile
    private var webSocket: WebSocket? = null

    fun connect() {
        if (webSocket != null) {
            return
        }

        val request = Request.Builder()
            .url(url)
            .build()

        webSocket = client.newWebSocket(
            request,
            object : WebSocketListener() {
                override fun onOpen(webSocket: WebSocket, response: Response) {
                    Log.i(TAG, "WebSocket connected: $url")
                }

                override fun onMessage(webSocket: WebSocket, text: String) {
                    Log.i(TAG, "recv: $text")
                }

                override fun onClosing(webSocket: WebSocket, code: Int, reason: String) {
                    Log.w(TAG, "closing: $code $reason")
                    webSocket.close(1000, null)
                }

                override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                    Log.w(TAG, "closed: $code $reason")
                }

                override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                    Log.e(TAG, "failed", t)
                }
            },
        )
    }

    fun sendState(state: XrControllerState): Boolean {
        val payload = state.toJsonString()
        val sent = webSocket?.send(payload) ?: false
        if (!sent) {
            Log.w(TAG, "send skipped; socket not connected yet")
        }
        return sent
    }

    fun disconnect() {
        webSocket?.close(1000, "bye")
        webSocket = null
    }

    companion object {
        private const val TAG = "XrWsClient"
        const val DEFAULT_URL = "ws://192.168.147.131:8765"
    }
}
