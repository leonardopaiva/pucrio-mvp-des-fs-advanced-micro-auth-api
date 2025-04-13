import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import app as app_module
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_login_success(client, monkeypatch):
    # Simula uma autenticação bem-sucedida
    def fake_authenticate_user(username, password):
        return {
            "IdToken": "fake_id_token",
            "AccessToken": "fake_access",
            "RefreshToken": "fake_refresh",
            "ExpiresIn": 3600,
            "TokenType": "Bearer"
        }
    # Patch na função do módulo app (já importada a partir de services.cognito_service)
    monkeypatch.setattr(app_module, "authenticate_user", fake_authenticate_user)

    def fake_verify_token(token):
        return {"email": "user@example.com", "name": "User", "sub": "uuid-123"}
    monkeypatch.setattr(app_module, "verify_token", fake_verify_token)

    data = {"username": "user", "password": "password"}
    response = client.post("/login", json=data)
    assert response.status_code == 200, f"Status code retornado: {response.status_code}"
    result = response.get_json()
    assert result["status"] == "ok"
    assert "AccessToken" in result["data"]

def test_login_failure(client, monkeypatch):
    # Simula falha na autenticação
    def fake_authenticate_user(username, password):
        return {"error": "Incorrect username or password."}
    monkeypatch.setattr(app_module, "authenticate_user", fake_authenticate_user)

    data = {"username": "invalido", "password": "errado"}
    response = client.post("/login", json=data)
    assert response.status_code == 401
    result = response.get_json()
    assert result["status"] == "error"
    assert result["msg"] == "Incorrect username or password."

def test_reset_password(client, monkeypatch):
    # Simula um cenário de reset de senha com sucesso
    def fake_reset_user_password(email):
        return {}  # Resposta sem erros
    monkeypatch.setattr(app_module, "reset_user_password", fake_reset_user_password)

    data = {"email": "usuario@example.com"}
    response = client.post("/reset-password", json=data)
    assert response.status_code == 200, f"Status code retornado: {response.status_code}"
    result = response.get_json()
    assert result["status"] == "ok"
    assert result["msg"] == "Senha resetada com sucesso."

def test_sign_up_missing_field(client):
    # Testa envio de payload incompleto (campo obrigatório ausente)
    data = {
        "username": "usuario",
        # "password" ausente
        "email": "usuario@example.com",
        "name": "Nome do Usuário"
    }
    response = client.post("/sign-up", json=data)
    assert response.status_code == 422

def test_refresh_token_success(client, monkeypatch):
    # Simula um refresh token bem-sucedido
    def fake_refresh_user(username, refreshToken):
        return {
            "AccessToken": "new_fake_access",
            "IdToken": "new_fake_id",
            "ExpiresIn": 7200,
            "TokenType": "Bearer"
        }
    monkeypatch.setattr(app_module, "refresh_user", fake_refresh_user)

    data = {"username": "user", "refreshToken": "fake_refresh"}
    response = client.post("/refresh-token", json=data)
    assert response.status_code == 200, f"Status code retornado: {response.status_code}"
    result = response.get_json()
    assert result["status"] == "ok"
    tokens = result["data"]
    assert tokens["AccessToken"] == "new_fake_access"
    assert tokens["IdToken"] == "new_fake_id"
    assert tokens["RefreshToken"] == "fake_refresh"
    assert tokens["ExpiresIn"] == 7200
    assert tokens["TokenType"] == "Bearer"
