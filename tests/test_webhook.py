import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_webhook_flow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # 1. Enviar um webhook
        payload = {"event": "teste.evento", "data": {"nome": "Exemplo"}}
        response = await client.post("/webhook", json=payload)
        assert response.status_code == 200
        assert response.json() == {"message": "Webhook armazenado com sucesso"}

        # 2. Exportar webhooks com autenticação HTTP Basic
        auth = ("admin", "senha123")
        export = await client.get("/messages/export", auth=auth)
        assert export.status_code == 200
        export_json = export.json()
        assert isinstance(export_json, list)
        assert any(item["event"] == "teste.evento" for item in export_json)
