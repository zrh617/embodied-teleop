package com.xr.teleop.rtc

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

enum class SignalingState {
    IDLE,
    CONNECTING,
    CONNECTED,
    CLOSED
}

class SignalingClient {
    private val _state = MutableStateFlow(SignalingState.IDLE)
    val state: StateFlow<SignalingState> = _state.asStateFlow()

    fun connect(endpoint: String) {
        _state.value = if (endpoint.isBlank()) SignalingState.IDLE else SignalingState.CONNECTING
    }

    fun markConnected() {
        _state.value = SignalingState.CONNECTED
    }

    fun close() {
        _state.value = SignalingState.CLOSED
    }
}
