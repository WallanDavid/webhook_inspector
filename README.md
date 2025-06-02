# 📡 Webhook Inspector

![coverage](https://img.shields.io/badge/coverage-69%25-yellow)
![status](https://img.shields.io/badge/status-em%20desenvolvimento-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-informational)
![FastAPI](https://img.shields.io/badge/framework-FastAPI-green)

> Ferramenta didática para **inspecionar, visualizar e armazenar webhooks recebidos via POST**. Ideal para testar APIs externas ou como projeto de estudo com FastAPI + WebSocket + SQLite.

---

## 🚀 Funcionalidades

- ✅ Receber webhooks JSON via `POST /webhook`
- ✅ Visualizar todos os webhooks em tempo real via `/messages`
- ✅ Exportar histórico via `/messages/export` (formato JSON)
- ✅ Autenticação básica (`admin/senha123`)
- ✅ Testes automatizados com `pytest`
- ✅ Cobertura de testes `69%`
- ✅ WebSocket para exibição ao vivo
- ✅ Banco de dados com SQLite via SQLAlchemy
- ✅ Pronto para Docker (opcional)

---

## 🧪 Tecnologias usadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/)
- [WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [pytest](https://docs.pytest.org/)
- [httpx](https://www.python-httpx.org/)
- SQLite

---

## 📦 Instalação local

### 1. Clonar o projeto

```bash
git clone https://github.com/seu-usuario/webhook_inspector.git
cd webhook_inspector
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  ← Linux/macOS
pip install -r requirements.txt
