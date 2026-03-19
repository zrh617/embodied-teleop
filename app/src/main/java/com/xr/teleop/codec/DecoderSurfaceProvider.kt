package com.xr.teleop.codec

import android.view.Surface

interface DecoderSurfaceProvider {
    fun acquireDecoderSurface(): Surface?
    fun releaseDecoderSurface()
}
