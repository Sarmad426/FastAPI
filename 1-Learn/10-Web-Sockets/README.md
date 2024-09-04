# Web Sockets

WebSockets are a communication protocol that enables full-duplex (two-way) communication between a client (typically a web browser) and a server over a single, long-lived connection. Unlike traditional HTTP requests, where the client must initiate communication each time it wants to send or receive data, WebSockets allow both the client and server to send messages at any time, making real-time communication much more efficient.

**Use Cases:**

1. **Real-time Updates**: Ideal for applications that require instant updates, like stock tickers, live sports scores, or real-time notifications.
  
2. **Chat Applications**: WebSockets are commonly used in chat apps, where users expect to see messages appear immediately after they are sent.

3. **Online Gaming**: Multiplayer games use WebSockets to keep players' states synchronized in real-time.

4. **Collaborative Tools**: Tools like Google Docs use WebSockets to allow multiple users to edit documents simultaneously, with changes reflected instantly.

5. **IoT Devices**: WebSockets can be used to maintain continuous communication between IoT devices and servers for real-time data monitoring and control.

Learn more at: <https://github.com/Sarmad426/Tech-Concepts/blob/master/Back-end/Web-Sockets/Readme.md>

Install web sockets in your virtual environment.

```bash
pip install websockets
```

**Production:**

For production we might have a framework like React, Vue or svelte.

```py
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

```

Docs: <https://fastapi.tiangolo.com/advanced/websockets/>
