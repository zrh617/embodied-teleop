"""
RealSense视频流服务器 - 提供H.264编码的视频流
可以直接集成到VR应用中
"""

import cv2
import numpy as np
import pyrealsense2 as rs
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import asyncio
import logging
from threading import Thread, Lock
from collections import deque

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="VR视频流服务器")

class RealSenseVideoServer:
    def __init__(self):
        self.pipeline = None
        self.config = None
        self.align = None
        self.colorizer = None
        self.is_running = False
        self.frame_buffer = deque(maxlen=2)
        self.lock = Lock()
        self.thread = None
        
    def initialize(self):
        """初始化RealSense"""
        try:
            self.pipeline = rs.pipeline()
            self.config = rs.config()
            
            # 配置RGB流
            self.config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
            # 配置深度流
            self.config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
            
            profile = self.pipeline.start(self.config)
            
            # 对齐深度到彩色
            self.align = rs.align(rs.stream.color)
            # 深度伪彩器
            self.colorizer = rs.colorizer()
            
            logger.info("RealSense初始化成功")
            return True
        except Exception as e:
            logger.error(f"RealSense初始化失败: {e}")
            return False
    
    def start_capture(self):
        """启动后台采集线程"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = Thread(target=self._capture_thread, daemon=True)
        self.thread.start()
        logger.info("视频采集线程已启动")
    
    def stop_capture(self):
        """停止采集线程"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def _capture_thread(self):
        """后台采集线程"""
        while self.is_running:
            try:
                frames = self.pipeline.wait_for_frames(timeout_ms=1000)
                frames = self.align.process(frames)
                
                color_frame = frames.get_color_frame()
                depth_frame = frames.get_depth_frame()
                
                if color_frame and depth_frame:
                    color_image = np.asanyarray(color_frame.get_data())
                    depth_color_frame = self.colorizer.colorize(depth_frame)
                    depth_image = np.asanyarray(depth_color_frame.get_data())
                    
                    with self.lock:
                        self.frame_buffer.append({
                            'color': color_image,
                            'depth': depth_image,
                            'timestamp': frames.get_timestamp()
                        })
            except Exception as e:
                logger.error(f"采集错误: {e}")
                break
    
    def get_latest_frame(self, frame_type='color'):
        """获取最新帧"""
        with self.lock:
            if self.frame_buffer:
                frame_data = self.frame_buffer[-1]
                return frame_data.get(frame_type)
        return None
    
    def cleanup(self):
        """清理资源"""
        self.stop_capture()
        if self.pipeline:
            self.pipeline.stop()


# 全局实例
video_server = RealSenseVideoServer()


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    if video_server.initialize():
        video_server.start_capture()
    else:
        logger.error("无法初始化RealSense")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理"""
    video_server.cleanup()


def gen_h264_stream(frame_type='color'):
    """
    生成H.264编码的MJPEG流
    适合VR应用直接显示（低延迟）
    """
    fps = 30
    frame_skip = 0
    
    while True:
        frame = video_server.get_latest_frame(frame_type)
        if frame is None:
            await asyncio.sleep(0.01)
            continue
        
        # 调整质量以平衡延迟和质量
        ok, jpg = cv2.imencode(".jpg", frame, [
            int(cv2.IMWRITE_JPEG_QUALITY), 75,  # 质量
            int(cv2.IMWRITE_JPEG_PROGRESSIVE), 1  # 渐进式编码
        ])
        
        if ok:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n"
                b"Content-Length: " + str(len(jpg)).encode() + b"\r\n\r\n" +
                jpg.tobytes() +
                b"\r\n"
            )
        
        await asyncio.sleep(1.0 / fps)


@app.get("/stream/color")
async def stream_color():
    """获取彩色视频流"""
    return StreamingResponse(
        gen_h264_stream('color'),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )


@app.get("/stream/depth")
async def stream_depth():
    """获取深度视频流（伪彩）"""
    return StreamingResponse(
        gen_h264_stream('depth'),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "ok",
        "camera_running": video_server.is_running,
        "buffered_frames": len(video_server.frame_buffer)
    }


@app.get("/stream/info")
async def stream_info():
    """获取流信息"""
    return {
        "color": {
            "resolution": "1280x720",
            "framerate": 30,
            "format": "MJPEG",
            "endpoint": "/stream/color"
        },
        "depth": {
            "resolution": "1280x720",
            "framerate": 30,
            "format": "Pseudo-colored MJPEG",
            "endpoint": "/stream/depth"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("启动RealSense视频服务器...")
    logger.info("彩色流: http://localhost:8000/stream/color")
    logger.info("深度流: http://localhost:8000/stream/depth")
    logger.info("健康检查: http://localhost:8000/health")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
