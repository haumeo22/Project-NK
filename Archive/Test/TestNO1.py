import asyncio, websockets, json, uuid, os

# ── CONFIG ─────────────────────────────────────────────────────────────
TOKEN_PATH   = "C:/Users/haume/Documents/Active/Programming/NeuroKaylie/scripts/Token.txt"
PLUGIN_NAME  = "NeuroKaylie"
DEVELOPER    = "Doctor Anthony"
VTS_URI      = "ws://127.0.0.1:8001"
EXPR_FILE    = "hoodie.exp3.json"  # your expression

# ── TOKEN UTILITIES ────────────────────────────────────────────────────
def save_token(token: str):
    with open(TOKEN_PATH, "w") as f:
        f.write(token)

def load_token():
    if os.path.exists(TOKEN_PATH):
        return open(TOKEN_PATH, "r").read().strip()
    return None

# ── VTS AUTH FLOW ───────────────────────────────────────────────────────
async def authenticate(ws, token: str) -> bool:
    req = {
        "apiName":"VTubeStudioPublicAPI","apiVersion":"1.0",
        "messageType":"AuthenticationRequest","requestID":str(uuid.uuid4()),
        "data": {"pluginName":PLUGIN_NAME,"pluginDeveloper":DEVELOPER,"authenticationToken":token}
    }
    await ws.send(json.dumps(req))
    resp = json.loads(await ws.recv())
    return resp["data"].get("authenticated", False)

async def request_new_token(ws) -> str:
    req = {
        "apiName":"VTubeStudioPublicAPI","apiVersion":"1.0",
        "messageType":"AuthenticationTokenRequest","requestID":str(uuid.uuid4()),
        "data": {"pluginName":PLUGIN_NAME,"pluginDeveloper":DEVELOPER}
    }
    await ws.send(json.dumps(req))
    resp = json.loads(await ws.recv())
    token = resp["data"]["authenticationToken"]
    save_token(token)
    print(f"[TOKEN] New token saved: {token}")
    return token

# ── MAIN FLOW & EXPRESSION ──────────────────────────────────────────────
async def main():
    # 1) Open single WS connection
    ws = await websockets.connect(VTS_URI)
    
    # 2) Try existing token
    token = load_token()
    if token:
        print("[TOKEN] Loaded saved token.")
        if not await authenticate(ws, token):
            print("[TOKEN] Invalid token, fetching new one…")
            token = await request_new_token(ws)
            if not await authenticate(ws, token):
                raise RuntimeError("Auth failed after new token.")
    else:
        # No token file → request and auth
        token = await request_new_token(ws)
        if not await authenticate(ws, token):
            raise RuntimeError("Auth failed after initial token.")

    print("✅ Authenticated! Triggering expression…")

    # 3) Send ExpressionActivationRequest
    expr_req = {
        "apiName":"VTubeStudioPublicAPI","apiVersion":"1.0",
        "messageType":"ExpressionActivationRequest","requestID":str(uuid.uuid4()),
        "data": {"expressionFile": EXPR_FILE, "active": True}
    }
    await ws.send(json.dumps(expr_req))
    resp = await ws.recv()
    print(f"[EXPRESSION RESPONSE] {resp}")

    # 4) Clean up
    await ws.close()

if __name__ == "__main__":
    asyncio.run(main())
