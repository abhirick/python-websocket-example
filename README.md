# Python WebSocket Server — Quick Start & Protocol Explanation

This guide shows how to set up and test the Python WebSocket server and explains the WebSocket handshake and message flow at the protocol level.

---

# 1️⃣ Setup Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install websockets
```

Run the server:

```bash
python server.py
```

Server starts on:

```
ws://localhost:8765
```

---

# 2️⃣ Test client using wscat

Install wscat:

```bash
npm install -g wscat
```

Connect to the server:

```bash
wscat -c ws://localhost:8765
```

You’ll see:

```json
{"type":"welcome","message":"Connected to Python WebSocket server"}
```

Send a message:

```
hello
```

Server response:

```json
{"type":"echo","received":"hello"}
```

---

# 3️⃣ End‑to‑end WebSocket handshake (wire‑level)

When the client connects:

```bash
wscat -c ws://localhost:8765
```

The client sends an HTTP Upgrade request:

```http
GET / HTTP/1.1
Host: localhost:8765
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==
Sec-WebSocket-Version: 13
```

## What these headers mean

* **Upgrade: websocket** → request protocol switch
* **Connection: Upgrade** → hop‑by‑hop upgrade signal
* **Sec-WebSocket-Key** → random client nonce
* **Sec-WebSocket-Version** → WebSocket protocol version

---

# 4️⃣ Server handshake response

The Python `websockets` library automatically returns:

```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: HSmrc0sMlYUkAGmm5OPpG2HaGWk=
```

## How `Sec-WebSocket-Accept` is computed

```
base64( SHA1( client_key + GUID ) )
```

GUID constant defined by the WebSocket spec:

```
258EAFA5-E914-47DA-95CA-C5AB0DC85B11
```

👉 This proves the server understands the WebSocket protocol.

After this response:

**HTTP is finished.**
The connection becomes raw WebSocket frames.

---

# 5️⃣ After handshake — data frames

When you type in the client:

```
hello
```

The client sends a WebSocket frame:

```
FIN = 1
opcode = 1 (text)
payload = "hello"
```

The Python server receives it via:

```python
async for message in ws:
```

So:

```
message = "hello"
```

The server responds with another WebSocket text frame:

```
opcode = 1
payload = {"type":"echo","received":"hello"}
```

No HTTP headers are used anymore — only WebSocket frames.

---

# 6️⃣ Full lifecycle summary

```
TCP connect
→ HTTP Upgrade request
→ 101 Switching Protocols
→ Bidirectional WebSocket frames
→ Close frame
→ TCP close
```

---

# 7️⃣ Key takeaways

* WebSocket starts as HTTP, then upgrades
* After upgrade → persistent bidirectional channel
* Messages are frames, not HTTP requests
* Python `websockets` handles handshake automatically
* Your handler processes frames asynchronously

---

**You now have a working Python WebSocket server and understand the full protocol flow end‑to‑end.**
