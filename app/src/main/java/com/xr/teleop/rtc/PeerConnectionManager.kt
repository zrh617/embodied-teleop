package com.xr.teleop.rtc

import android.view.Surface
import com.xr.teleop.codec.CodecConfig
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

data class PeerConnectionSnapshot(
    val connected: Boolean = false,
    val decoderMimeType: String = "",
    val decoderAttached: Boolean = false
)

class PeerConnectionManager {
    private val _snapshot = MutableStateFlow(PeerConnectionSnapshot())
    val snapshot: StateFlow<PeerConnectionSnapshot> = _snapshot.asStateFlow()

    fun configureVideo(codecConfig: CodecConfig) {
        _snapshot.update {
            it.copy(decoderMimeType = codecConfig.mimeType)
        }
    }

    fun attachDecoderSurface(surface: Surface?) {
        _snapshot.update {
            it.copy(decoderAttached = surface != null)
        }
    }

    fun markConnected(connected: Boolean) {
        _snapshot.update {
            it.copy(connected = connected)
        }
    }
}
