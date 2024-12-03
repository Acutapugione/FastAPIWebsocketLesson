from typing import Annotated
from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)


app = FastAPI()


@app.get("")
def index():
    return {"cover page": 1}


async def get_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@app.websocket("/mama_mila_dupu")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Annotated[str, Depends(get_token)],
):
    await websocket.accept()

    try:
        while 1:

            data = await websocket.receive_text()  # receive_bytes()
            if not data:
                raise WebSocketException(
                    code=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA,
                    reason="Empty payload",
                )
            print(data)

            await websocket.send_text(data=data.lower())
            await websocket.send_text(f"Message text was: {data}, for token: {token}")
    except WebSocketException as we:
        await websocket.send_text(f"Connection closed for {we.reason}")
        await websocket.close()
        print(f"{we}")
    except WebSocketDisconnect:
        print("Disconnected")
