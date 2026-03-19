package com.xr.teleop.ui

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

data class AppUiState(
    val sessionPhase: String = "boot",
    val nativeStatus: String = "waiting-for-native"
)

class AppStateStore {
    private val _uiState = MutableStateFlow(AppUiState())
    val uiState: StateFlow<AppUiState> = _uiState.asStateFlow()

    fun updateSessionPhase(phase: String) {
        _uiState.update { current ->
            current.copy(sessionPhase = phase)
        }
    }

    fun updateNativeStatus(status: String) {
        _uiState.update { current ->
            current.copy(nativeStatus = status)
        }
    }
}
