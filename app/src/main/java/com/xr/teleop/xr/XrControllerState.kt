package com.xr.teleop.xr

import java.util.concurrent.atomic.AtomicLong
import org.json.JSONObject

data class Vec2(
    val x: Float = 0f,
    val y: Float = 0f,
)

data class Vec3(
    val x: Float = 0f,
    val y: Float = 0f,
    val z: Float = 0f,
)

data class Quat(
    val x: Float = 0f,
    val y: Float = 0f,
    val z: Float = 0f,
    val w: Float = 1f,
)

data class Buttons(
    val primary: Boolean = false,
    val secondary: Boolean = false,
    val thumbstickClick: Boolean = false,
    val menu: Boolean = false,
    val system: Boolean = false,
)

data class HeadState(
    val pos: Vec3,
    val rot: Quat,
)

data class ControllerState(
    val connected: Boolean = true,
    val pos: Vec3,
    val rot: Quat,
    val thumbstick: Vec2 = Vec2(),
    val trigger: Float = 0f,
    val squeeze: Float = 0f,
    val buttons: Buttons = Buttons(),
)

data class XrControllerState(
    val type: String = "xr_controller_state",
    val tsMs: Long,
    val seq: Long,
    val head: HeadState,
    val left: ControllerState,
    val right: ControllerState,
) {
    fun toJsonString(): String {
        return JSONObject()
            .put("type", type)
            .put("ts_ms", tsMs)
            .put("seq", seq)
            .put("head", head.toJson())
            .put("left", left.toJson())
            .put("right", right.toJson())
            .toString()
    }
}

private val sequenceGenerator = AtomicLong(0L)

fun createTestXrControllerState(tsMs: Long = System.currentTimeMillis()): XrControllerState {
    return XrControllerState(
        tsMs = tsMs,
        seq = sequenceGenerator.incrementAndGet(),
        head = HeadState(
            pos = Vec3(0f, 1.5f, 0.2f),
            rot = Quat(0f, 0f, 0f, 1f),
        ),
        left = ControllerState(
            connected = true,
            pos = Vec3(-0.2f, 1.2f, 0.4f),
            rot = Quat(0f, 0f, 0f, 1f),
            thumbstick = Vec2(0f, 0f),
            trigger = 0f,
            squeeze = 0f,
            buttons = Buttons(
                primary = false,
                secondary = false,
                thumbstickClick = false,
                menu = false,
            ),
        ),
        right = ControllerState(
            connected = true,
            pos = Vec3(0.2f, 1.2f, 0.4f),
            rot = Quat(0f, 0f, 0f, 1f),
            thumbstick = Vec2(0f, 0f),
            trigger = 0f,
            squeeze = 0f,
            buttons = Buttons(
                primary = false,
                secondary = false,
                thumbstickClick = false,
                system = false,
            ),
        ),
    )
}

private fun HeadState.toJson(): JSONObject {
    return JSONObject()
        .put("pos", pos.toJson())
        .put("rot", rot.toJson())
}

private fun ControllerState.toJson(): JSONObject {
    return JSONObject()
        .put("connected", connected)
        .put("pos", pos.toJson())
        .put("rot", rot.toJson())
        .put("thumbstick", thumbstick.toJson())
        .put("trigger", trigger)
        .put("squeeze", squeeze)
        .put("buttons", buttons.toJson())
}

private fun Vec2.toJson(): JSONObject {
    return JSONObject()
        .put("x", x)
        .put("y", y)
}

private fun Vec3.toJson(): JSONObject {
    return JSONObject()
        .put("x", x)
        .put("y", y)
        .put("z", z)
}

private fun Quat.toJson(): JSONObject {
    return JSONObject()
        .put("x", x)
        .put("y", y)
        .put("z", z)
        .put("w", w)
}

private fun Buttons.toJson(): JSONObject {
    return JSONObject()
        .put("primary", primary)
        .put("secondary", secondary)
        .put("thumbstick_click", thumbstickClick)
        .put("menu", menu)
        .put("system", system)
}
