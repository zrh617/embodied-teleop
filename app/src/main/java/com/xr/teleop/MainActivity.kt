package com.xr.teleop

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import com.xr.teleop.ui.AppStateStore
import com.xr.teleop.ui.theme.XRTeleoperationTheme

class MainActivity : ComponentActivity() {
    private val appStateStore = AppStateStore()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        try {
            if (!NativeBridge.isLibraryLoaded()) {
                Log.e(TAG, "Native library failed to load")
                appStateStore.updateSessionPhase("native-lib-load-failed")
            } else {
                val initialized = NativeBridge.nativeInit(this)
                appStateStore.updateSessionPhase(
                    if (initialized) "native-ready" else "native-init-failed"
                )
                refreshStatus()
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error initializing native bridge: ${e.message}", e)
            appStateStore.updateSessionPhase("native-init-error")
        }

        setContent {
            val uiState by appStateStore.uiState.collectAsState()
            XRTeleoperationTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    TeleopRoot(
                        phase = uiState.sessionPhase,
                        nativeStatus = uiState.nativeStatus,
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }

    override fun onResume() {
        super.onResume()
        try {
            if (NativeBridge.isLibraryLoaded()) {
                NativeBridge.nativeOnResume()
            }
            appStateStore.updateSessionPhase("foreground")
            refreshStatus()
        } catch (e: Exception) {
            Log.e(TAG, "Error in onResume: ${e.message}", e)
        }
    }

    override fun onPause() {
        try {
            if (NativeBridge.isLibraryLoaded()) {
                NativeBridge.nativeOnPause()
            }
            appStateStore.updateSessionPhase("background")
            refreshStatus()
        } catch (e: Exception) {
            Log.e(TAG, "Error in onPause: ${e.message}", e)
        }
        super.onPause()
    }

    override fun onDestroy() {
        try {
            if (NativeBridge.isLibraryLoaded()) {
                NativeBridge.nativeRequestExit()
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error in onDestroy: ${e.message}", e)
        }
        super.onDestroy()
    }

    private fun refreshStatus() {
        try {
            if (NativeBridge.isLibraryLoaded()) {
                appStateStore.updateNativeStatus(NativeBridge.nativeGetStatus())
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error refreshing status: ${e.message}", e)
        }
    }

    companion object {
        private const val TAG = "MainActivity"
    }
}

@Composable
private fun TeleopRoot(
    phase: String,
    nativeStatus: String,
    modifier: Modifier = Modifier
) {
    Box(modifier = modifier.fillMaxSize()) {
        Text(
            text = "Quest Teleop\nphase=$phase\n\n$nativeStatus",
            style = MaterialTheme.typography.bodyLarge
        )
    }
}