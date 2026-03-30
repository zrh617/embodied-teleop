package com.xr.teleop.xr

import android.util.Log
import java.util.concurrent.Executors
import java.util.concurrent.ScheduledFuture
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
        .connectTimeout(5, TimeUnit.SECONDS)
        .build()

    @Volatile
    private var webSocket: WebSocket? = null

    @Volatile
    private var destroyed = false

    private val reconnectExecutor = Executors.newSingleThreadScheduledExecutor()
    private var reconnectFuture: ScheduledFuture<*>? = null

    fun connect() {
        destroyed = false
        doConnect()
    }

    private fun doConnect() {
        if (destroyed) return
        if (webSocket != null) return

        Log.i(TAG, "connecting to $url")
        val request = Request.Builder().url(url).build()
        webSocket = client.newWebSocket(
            request,
            object : WebSocketListener() {
                override fun onOpen(webSocket: WebSocket, response: Response) {
                    Log.i(TAG, "WebSocket connected: $url")
                    reconnectFuture?.cancel(false)
                    reconnectFuture = null
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
                    this@XrWsClient.webSocket = null
                    scheduleReconnect()
                }

                override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                    Log.e(TAG, "failed: ${t.message}")
                    this@XrWsClient.webSocket = null
                    scheduleReconnect()
                }
            },
        )
    }

    private fun scheduleReconnect() {
        if (destroyed) return
        if (reconnectFuture != null && !reconnectFuture!!.isDone) return
        Log.i(TAG, "reconnecting in ${RECONNECT_DELAY_MS}ms...")
        reconnectFuture = reconnectExecutor.schedule({
            webSocket = null
            doConnect()
        }, RECONNECT_DELAY_MS, TimeUnit.MILLISECONDS)
    }

    fun sendState(state: XrControllerState): Boolean {
        val payload = state.toJsonString()
        val sent = webSocket?.send(payload) ?: false
        if (!sent) {
            Log.w(TAG, "send skipped; socket not connected")
        }
        return sent
    }

    /** 暂停时保持连接（Quest onPause 不断开）*/
    fun pause() {
        // 保持 WS 连接，什么都不做
        Log.i(TAG, "pause() called — keeping WS alive")
    }

    /** 真正销毁时才断开 */
    fun disconnect() {
        destroyed = true
        reconnectFuture?.cancel(false)
        reconnectFuture = null
        webSocket?.close(1000, "bye")
        webSocket = null
        reconnectExecutor.shutdown()
    }

    companion object {
        private const val TAG = "XrWsClient"
        const val DEFAULT_URL = "ws://10.20.213.58:8765"
        private const val RECONNECT_DELAY_MS = 2000L
    }
}
