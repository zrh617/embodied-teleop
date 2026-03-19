package com.xr.teleop.rtc

data class StreamStats(
    val decodeFps: Float = 0f,
    val endToEndLatencyMs: Float = 0f,
    val packetLossRatio: Float = 0f
)

class StatsCollector {
    private var latestStats = StreamStats()

    fun update(stats: StreamStats) {
        latestStats = stats
    }

    fun snapshot(): StreamStats = latestStats
}
