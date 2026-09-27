from fastapi import FastAPI, Request, status

app = FastAPI()

@app.post("/webhook")
async def handle_webhook(request: Request):
    # Acknowledge receipt quickly to prevent timeouts from the sender
    payload = await request.json()
    
    # Process your data here
    print(f"Received webhook event: {payload}")
    
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)