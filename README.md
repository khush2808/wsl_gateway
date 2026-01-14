# WSL Gateway

A simple Python gateway server that forwards requests from your Windows network to your WSL FastAPI server.

## Usage

1. Make sure your FastAPI server in WSL is running and bound to `0.0.0.0:8000`
2. Run the gateway on Windows:

```cmd
python wsl_gateway\gateway.py 8000 localhost 8000
```

This will:
- Listen on `0.0.0.0:8000` (accessible from your network)
- Forward requests to `localhost:8000` (your WSL FastAPI server)

## Access your API

From other devices on your network, use your Windows machine's IP:
```
http://<WINDOWS_IP>:8000
```

## Finding your Windows IP

Run in Windows Command Prompt:
```cmd
ipconfig
```
Look for your WiFi adapter's IPv4 address.

## Custom ports

To use different ports:
```cmd
python wsl_gateway\gateway.py <external_port> <wsl_host> <wsl_port>
```

Example:
```cmd
python wsl_gateway\gateway.py 8080 localhost 3000
```