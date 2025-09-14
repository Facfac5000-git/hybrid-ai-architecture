# Infraestructura de WebSocket para FastAPI (comentado para activación futura)
# Descomentar y mover a main.py para habilitar WebSocket

# from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# from fastapi.responses import HTMLResponse
#
# router = APIRouter()
#
# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             # Procesar mensaje recibido y emitir respuesta
#             await websocket.send_text(f"Echo: {data}")
#     except WebSocketDisconnect:
#         pass

# Para activar:
# 1. Mover este código a main.py o endpoints.py
# 2. Agregar router.include_router(router) en main.py
# 3. Instalar 'websockets' si es necesario: poetry add websockets
