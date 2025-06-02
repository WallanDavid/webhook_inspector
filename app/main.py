# app/main.py

from fastapi import FastAPI, Request, Depends, WebSocket, WebSocketDisconnect, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
import json
import secrets

from app.db import get_db, engine, Base
from app.models import Webhook

app = FastAPI()
security = HTTPBasic()
USERNAME = "admin"
PASSWORD = "senha123"

connections: List[WebSocket] = []

def autenticar(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/webhook")
async def receive_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    data = await request.json()
    event = data.get("event", "unknown")
    payload = json.dumps(data, ensure_ascii=False)

    webhook = Webhook(event=event, payload=payload)
    db.add(webhook)
    await db.commit()

    # Enviar para todos os clientes WebSocket
    for conn in connections:
        await conn.send_text(payload)

    return {"message": "Webhook armazenado com sucesso"}

@app.get("/")
async def home():
    return {"status": "API Webhook Inspector rodando com SQLite e WebSocket"}

@app.get("/messages", response_class=HTMLResponse)
async def show_webhooks(
    db: AsyncSession = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(autenticar)
):
    result = await db.execute(select(Webhook))
    webhooks = result.scalars().all()

    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Webhook Inspector</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 text-gray-800">
        <div class="container mx-auto py-8 px-4">
            <h1 class="text-3xl font-bold mb-6 text-center">📡 Webhooks Recebidos</h1>
            <ul id="webhooks" class="space-y-4">
    """
    for webhook in webhooks:
        html += f"""
            <li class="bg-white p-4 rounded-lg shadow">
                <p class="text-sm font-medium text-indigo-600 mb-2">Evento: <strong>{webhook.event}</strong></p>
                <pre class="text-sm bg-gray-100 p-3 rounded overflow-auto">{webhook.payload}</pre>
            </li>
        """
    html += """
            </ul>
        </div>

        <script>
            const ws = new WebSocket("ws://" + location.host + "/ws");
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                const list = document.getElementById("webhooks");
                const item = document.createElement("li");
                item.className = "bg-white p-4 rounded-lg shadow";
                item.innerHTML = `
                    <p class="text-sm font-medium text-indigo-600 mb-2">
                        Evento: <strong>${data.event}</strong>
                    </p>
                    <pre class="text-sm bg-gray-100 p-3 rounded overflow-auto">${JSON.stringify(data, null, 2)}</pre>
                `;
                list.prepend(item);
            };
        </script>
    </body>
    </html>
    """

    return html

@app.get("/messages/export", response_class=JSONResponse)
async def export_webhooks(
    db: AsyncSession = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(autenticar)
):
    result = await db.execute(select(Webhook))
    webhooks = result.scalars().all()

    export_data = [
        {
            "id": webhook.id,
            "event": webhook.event,
            "payload": json.loads(webhook.payload)
        }
        for webhook in webhooks
    ]

    return export_data

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # mantém a conexão viva
    except WebSocketDisconnect:
        connections.remove(websocket)
