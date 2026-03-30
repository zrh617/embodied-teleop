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

fun parseXrControllerStateJson(json: String): XrControllerState {
    val root = JSONObject(json)

    fun parseVec2(obj: JSONObject): Vec2 = Vec2(
        x = obj.optDouble("x", 0.0).toFloat(),
        y = obj.optDouble("y", 0.0).toFloat(),
    )

    fun parseVec3(obj: JSONObject): Vec3 = Vec3(
        x = obj.optDouble("x", 0.0).toFloat(),
        y = obj.optDouble("y", 0.0).toFloat(),
        z = obj.optDouble("z", 0.0).toFloat(),
    )

    fun parseQuat(obj: JSONObject): Quat = Quat(
        x = obj.optDouble("x", 0.0).toFloat(),
        y = obj.optDouble("y", 0.0).toFloat(),
        z = obj.optDouble("z", 0.0).toFloat(),
        w = obj.optDouble("w", 1.0).toFloat(),
    )

    fun parseButtons(obj: JSONObject): Buttons = Buttons(
        primary = obj.optBoolean("primary", false),
        secondary = obj.optBoolean("secondary", false),
        thumbstickClick = obj.optBoolean("thumbstick_click", false),
        menu = obj.optBoolean("menu", false),
        system = obj.optBoolean("system", false),
    )

    fun parseController(obj: JSONObject): ControllerState = ControllerState(
        connected = obj.optBoolean("connected", false),
        pos = parseVec3(obj.optJSONObject("pos") ?: JSONObject()),
        rot = parseQuat(obj.optJSONObject("rot") ?: JSONObject()),
        thumbstick = parseVec2(obj.optJSONObject("thumbstick") ?: JSONObject()),
        trigger = obj.optDouble("trigger", 0.0).toFloat(),
        squeeze = obj.optDouble("squeeze", 0.0).toFloat(),
        buttons = parseButtons(obj.optJSONObject("buttons") ?: JSONObject()),
    )

    return XrControllerState(
        type = root.optString("type", "xr_controller_state"),
        tsMs = root.optLong("ts_ms", System.currentTimeMillis()),
        seq = root.optLong("seq", sequenceGenerator.incrementAndGet()),
        head = HeadState(
            pos = parseVec3(root.optJSONObject("head")?.optJSONObject("pos") ?: JSONObject()),
            rot = parseQuat(root.optJSONObject("head")?.optJSONObject("rot") ?: JSONObject()),
        ),
        left = parseController(root.optJSONObject("left") ?: JSONObject()),
        right = parseController(root.optJSONObject("right") ?: JSONObject()),
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
