package com.xr.teleop.codec

data class CodecConfig(
    val mimeType: String = "video/avc",
    val width: Int = 1920,
    val height: Int = 1080,
    val lowLatency: Boolean = true
)
