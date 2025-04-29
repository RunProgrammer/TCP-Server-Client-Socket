# 🔌 Python TCP Client-Server Messaging App

This project is a simple **multi-threaded TCP client-server messaging system** built using Python's `socket` and `threading` libraries. It allows multiple clients to connect to a single server and exchange simple text messages using a custom fixed-size header protocol.

---

## 📌 Features

- ✅ Multi-threaded server to handle multiple clients concurrently  
- ✅ Fixed-size header to handle variable-length messages  
- ✅ Graceful disconnection handling  
- ✅ Clean and modular client-server structure  
- ✅ Easily expandable for chat, file transfers, etc.

---

## 📁 Project Structure

```
.
├── server.py     # Server-side code
└── client.py     # Client-side code
```

---

## 🚀 How It Works

### 🖥️ Server

- Listens on a specified port and IP address.
- Accepts multiple client connections using threads.
- Each message is sent with a fixed-size header (128 bytes) indicating the length of the actual message.
- Disconnects cleanly when receiving a special message (`!DISCONNECT!`).

### 💬 Client

- Connects to the server using the server's IP and port.
- Sends a message length as a header, followed by the actual message.
- Can send multiple messages, including a disconnect signal.

---

## 🔧 Usage

### 1. Start the Server

Make sure the IP and port are correctly set.

```bash
python server.py
```

### 2. Run the Client (in another terminal or device on the same network)

Update the `SERVER` IP in `client.py` to match your server machine.

```bash
python client.py
```

---

## 🛠 Configuration

- `HEADER`: Size (in bytes) of the fixed-length header used to send message lengths.
- `PORT`: Change if the default port is in use.
- `SERVER`: Replace with the server’s local IP (`ipconfig` on Windows or `ifconfig`/`ip a` on Linux/Mac).

---

## 🧠 Concepts Covered

- Socket programming (`AF_INET`, `SOCK_STREAM`)
- Message framing with fixed-size headers
- Threaded client handling with `threading.Thread`
- Basic protocol design (`!DISCONNECT!` flag)

---

## 📌 Future Improvements

- Broadcast messages to all clients (chat-style)
- Message acknowledgment and retries
- Logging and error handling
- GUI with Tkinter or web sockets via Flask + React

---

## 🧑‍💻 Author

**Tarun N**
Feel free to fork, modify, and contribute! 🚀🔗🔥

---
