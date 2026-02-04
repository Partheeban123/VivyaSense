"""
WebSocket handler for real-time video streaming
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
import asyncio
import cv2
import base64

from core.logger import log
from services.video_service import video_processor


class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, stream_id: str):
        """Connect a client to a stream"""
        await websocket.accept()
        if stream_id not in self.active_connections:
            self.active_connections[stream_id] = set()
        self.active_connections[stream_id].add(websocket)
        log.info(f"Client connected to stream: {stream_id}")
    
    def disconnect(self, websocket: WebSocket, stream_id: str):
        """Disconnect a client from a stream"""
        if stream_id in self.active_connections:
            self.active_connections[stream_id].discard(websocket)
            if not self.active_connections[stream_id]:
                del self.active_connections[stream_id]
        log.info(f"Client disconnected from stream: {stream_id}")
    
    async def send_frame(self, stream_id: str, data: dict):
        """Send frame to all connected clients"""
        if stream_id not in self.active_connections:
            return

        # Create a copy of the set to avoid "Set changed size during iteration" error
        connections_copy = list(self.active_connections[stream_id].copy())
        disconnected = set()

        for connection in connections_copy:
            try:
                await connection.send_json(data)
            except Exception as e:
                log.error(f"Error sending frame to {stream_id}: {type(e).__name__}: {str(e)}")
                disconnected.add(connection)

        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection, stream_id)
    
    async def broadcast(self, stream_id: str, message: str):
        """Broadcast message to all clients"""
        if stream_id not in self.active_connections:
            return
        
        for connection in self.active_connections[stream_id]:
            try:
                await connection.send_text(message)
            except Exception:
                pass


manager = ConnectionManager()


async def handle_stream_websocket(websocket: WebSocket, stream_id: str):
    """Handle WebSocket connection for video streaming"""
    await manager.connect(websocket, stream_id)
    
    try:
        # Callback for video processor
        async def frame_callback(data):
            """Send frame data to connected clients"""
            frame = data.get('frame')
            if frame is not None:
                # Encode frame to JPEG
                _, buffer = cv2.imencode('.jpg', frame)
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # Send to clients
                await manager.send_frame(stream_id, {
                    'type': 'frame',
                    'stream_id': stream_id,
                    'frame': frame_base64,
                    'detections': data.get('detections', []),
                    'frame_number': data.get('frame_number', 0)
                })
        
        # Wait for messages from client
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
                message = json.loads(data)
                
                if message.get('action') == 'start':
                    # Start processing stream
                    stream_url = message.get('stream_url')
                    detection_types = message.get('detection_types', ['ppe', 'fall', 'fire'])
                    confidence = message.get('confidence', 0.5)

                    log.info(f"Starting stream {stream_id}: {stream_url}")
                    log.info(f"Detection types: {detection_types}, Confidence: {confidence}")

                    # Start processing in background
                    asyncio.create_task(
                        video_processor.process_rtsp_stream(
                            stream_url,
                            detection_types,
                            frame_callback,
                            stream_id,
                            confidence
                        )
                    )

                    await manager.broadcast(stream_id, json.dumps({
                        'type': 'status',
                        'message': 'Stream started'
                    }))
                
                elif message.get('action') == 'stop':
                    # Stop processing stream
                    video_processor.stop_stream(stream_id)
                    await manager.broadcast(stream_id, json.dumps({
                        'type': 'status',
                        'message': 'Stream stopped'
                    }))
            
            except asyncio.TimeoutError:
                # Send heartbeat
                await websocket.send_json({'type': 'heartbeat'})
            except json.JSONDecodeError:
                log.error("Invalid JSON received")
    
    except WebSocketDisconnect:
        log.info(f"WebSocket disconnected normally for stream: {stream_id}")
        manager.disconnect(websocket, stream_id)
        video_processor.stop_stream(stream_id)
    except Exception as e:
        log.error(f"WebSocket error for {stream_id}: {type(e).__name__}: {str(e)}")
        manager.disconnect(websocket, stream_id)
        video_processor.stop_stream(stream_id)

