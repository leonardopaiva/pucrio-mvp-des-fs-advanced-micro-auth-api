from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request, jsonify
from flask_cors import CORS
from schemas import (
    LoginSchema,
    RegistrationSchema,
    ConfirmSignUpSchema,
    ResetPasswordSchema,
    TokenResponseSchema,
    ErrorSchema,
    ProtectedInputSchema,
    RefreshSchema
)
from services.cognito_service import (
    authenticate_user,
    verify_token,
    reset_user_password,
    sign_up_user,
    confirm_sign_up,
    refresh_user
)

info = Info(title="API Auth com Cognito", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para documentação
home_tag = Tag(name="Documentação", description="Redireciona para a documentação")
auth_tag = Tag(name="Autenticação", description="Endpoints para autenticação com Cognito")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para a documentação OpenAPI."""
    return redirect('/openapi')

@app.post('/login', tags=[auth_tag],
          responses={
              "200": TokenResponseSchema,
              "401": ErrorSchema,
              "400": ErrorSchema
          })
def login(body: LoginSchema):
    """Realiza a autenticação com o Amazon Cognito e retorna os tokens e dados do usuário."""
    username = body.username
    password = body.password
    auth_response = authenticate_user(username, password)
    if "error" in auth_response:
        return jsonify({
            "status": "error",
            "msg": auth_response["error"],
            "data": {}
        }), 401

    id_token = auth_response.get("IdToken")
    payload = verify_token(id_token)
    if not payload:
        return jsonify({
            "status": "error",
            "msg": "Erro ao decodificar o token",
            "data": {}
        }), 401

    user_data = {
        "AccessToken": auth_response.get("AccessToken"),
        "IdToken": id_token,
        "RefreshToken": auth_response.get("RefreshToken"),
        "ExpiresIn": auth_response.get("ExpiresIn"),
        "TokenType": auth_response.get("TokenType"),
        "email": payload.get("email"),
        "name": payload.get("name"),
        "username": payload.get("sub")  # UUID do usuário
    }
    return jsonify({
        "status": "ok",
        "msg": "Login realizado com sucesso.",
        "data": user_data
    }), 200

@app.post('/reset-password', tags=[auth_tag],
          responses={
              "200": {"description": "Senha resetada com sucesso."},
              "400": ErrorSchema
          })
def reset_password(body: ResetPasswordSchema):
    """Reseta a senha do usuário a partir do email informado."""
    email = body.email
    result = reset_user_password(email)
    if "error" in result:
        return jsonify({
            "status": "error",
            "msg": result["error"],
            "data": {}
        }), 400
    return jsonify({
        "status": "ok",
        "msg": "Senha resetada com sucesso.",
        "data": {}
    }), 200

@app.post('/sign-up', tags=[auth_tag],
          responses={
              "200": {"description": "Usuário registrado com sucesso."},
              "400": ErrorSchema
          })
def sign_up(body: RegistrationSchema):
    """Registra um novo usuário no Cognito."""
    username = body.username
    password = body.password
    email = body.email
    name = body.name
    sign_up_response = sign_up_user(username, password, email, name)
    if "error" in sign_up_response:
        return jsonify({
            "status": "error",
            "msg": sign_up_response["error"],
            "data": {}
        }), 400
    return jsonify({
        "status": "ok",
        "msg": "Cadastro realizado com sucesso. Por favor, verifique seu email, copie o código de confirmação e complete o processo de verificação.",
        "data": {}
    }), 200

@app.post('/confirm-sign-up', tags=[auth_tag],
          responses={
              "200": {"description": "Usuário confirmado com sucesso."},
              "400": ErrorSchema
          })
def confirm_sign_up_route(body: ConfirmSignUpSchema):
    """Confirma o cadastro do usuário com o código de verificação recebido por email."""
    username = body.username
    confirmation_code = body.confirmation_code
    session = body.session  # opcional
    result = confirm_sign_up(username, confirmation_code, session)
    if "error" in result:
        return jsonify({
            "status": "error",
            "msg": result["error"],
            "data": {}
        }), 400
    return jsonify({
        "status": "ok",
        "msg": "Confirmação realizada com sucesso! Agora faça login.",
        "data": {}
    }), 200

@app.post('/refresh-token', tags=[auth_tag],
          responses={
              "200": TokenResponseSchema,
              "401": ErrorSchema,
              "400": ErrorSchema
          })
def refresh_token(body: RefreshSchema):
    """
    Renova os tokens utilizando o refresh token via Cognito.
    """
    username = body.username
    refresh_response = refresh_user(username, body.refreshToken)
    if "error" in refresh_response:
        return jsonify({
            "status": "error",
            "msg": refresh_response["error"],
            "data": {}
        }), 401
    new_tokens = {
        "AccessToken": refresh_response.get("AccessToken"),
        "IdToken": refresh_response.get("IdToken", ""),
        "RefreshToken": body.refreshToken,
        "ExpiresIn": refresh_response.get("ExpiresIn"),
        "TokenType": refresh_response.get("TokenType")
    }
    return jsonify({
        "status": "ok",
        "msg": "Token refreshed successfully.",
        "data": new_tokens
    }), 200

@app.post('/protected', tags=[auth_tag],
          responses={
              "200": TokenResponseSchema,
              "401": ErrorSchema
          })
def protected(body: ProtectedInputSchema):
    """Endpoint protegido que exige um token válido do Cognito."""
    auth_header = request.headers.get("Authorization")
    if not auth_header and body.token:
        auth_header = f"Bearer {body.token}"
    if not auth_header:
        return jsonify({
            "status": "error",
            "msg": "Authorization header missing",
            "data": {}
        }), 401
    parts = auth_header.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        return jsonify({
            "status": "error",
            "msg": "Authorization header must be Bearer token",
            "data": {}
        }), 401
    token_value = parts[1]
    payload = verify_token(token_value)
    if not payload:
        return jsonify({
            "status": "error",
            "msg": "Invalid or expired token",
            "data": {}
        }), 401
    return jsonify({
        "status": "ok",
        "msg": "Acesso autorizado",
        "data": {"user": payload}
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
