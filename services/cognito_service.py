import os
import hmac
import hashlib
import base64
import boto3
from botocore.exceptions import ClientError
from jose import jwt, JWTError
import requests

# Carregar configurações do Cognito a partir das variáveis de ambiente
COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID = os.environ.get("COGNITO_APP_CLIENT_ID")
COGNITO_APP_CLIENT_SECRET = os.environ.get("COGNITO_APP_CLIENT_SECRET")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
COGNITO_ISSUER = f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"

# Cria o cliente boto3 para o Cognito
client = boto3.client('cognito-idp', region_name=AWS_REGION)

def get_secret_hash(username: str) -> str:
    """
    Calcula o SECRET_HASH utilizando HMAC-SHA256.
    """
    message = username + COGNITO_APP_CLIENT_ID

    print(' ****** Username *******')
    print("Username:", username)
    # print("Client ID:", COGNITO_APP_CLIENT_ID)
    # print("Message:", message)


    dig = hmac.new(
        COGNITO_APP_CLIENT_SECRET.encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()

def authenticate_user(username: str, password: str) -> dict:
    """
    Autentica o usuário utilizando o fluxo USER_PASSWORD_AUTH do Cognito,
    enviando também o SECRET_HASH.
    """
    try:
        print("XXXXXX Username:", username)
        #print("XXXXXXpassword:", password)

        auth_parameters = {
            'USERNAME': username,
            'PASSWORD': password,
            'SECRET_HASH': get_secret_hash(username)
        }
        response = client.initiate_auth(
            ClientId=COGNITO_APP_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters=auth_parameters
        )
        return response.get("AuthenticationResult", response)
    except ClientError as e:
        return {"error": e.response["Error"]["Message"]}

def reset_user_password(username: str) -> dict:
    """
    Envia uma solicitação para resetar a senha de um usuário no Cognito.
    """
    try:
        response = client.admin_reset_user_password(
            UserPoolId=COGNITO_USER_POOL_ID,
            Username=username
        )
        return {"message": "Password reset requested successfully."}
    except ClientError as e:
        return {"error": e.response["Error"]["Message"]}

def sign_up_user(username: str, password: str, email: str, name: str) -> dict:
    """
    Registra um novo usuário no Cognito.
    """
    try:
        response = client.sign_up(
            ClientId=COGNITO_APP_CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'name', 'Value': name}
            ],
            SecretHash=get_secret_hash(username)
        )
        return response
    except ClientError as e:
        return {"error": e.response["Error"]["Message"]}

def confirm_sign_up(username: str, confirmation_code: str, session: str = None) -> dict:
    """
    Confirma o cadastro de um usuário no Cognito utilizando o código de verificação.
    """
    try:
        params = {
            'ClientId': COGNITO_APP_CLIENT_ID,
            'Username': username,
            'ConfirmationCode': confirmation_code,
            'SecretHash': get_secret_hash(username)
        }
        if session:
            params['Session'] = session

        response = client.confirm_sign_up(**params)
        return {"message": "User confirmed successfully."}
    except ClientError as e:
        return {"error": e.response["Error"]["Message"]}

def get_cognito_jwk():
    """
    Recupera as chaves públicas do Cognito para validação dos tokens JWT.
    """
    jwks_url = f"{COGNITO_ISSUER}/.well-known/jwks.json"
    response = requests.get(jwks_url)
    response.raise_for_status()
    return response.json()

def verify_token(token: str) -> dict:
    """
    Verifica e decodifica o token JWT usando as chaves públicas do Cognito.
    """
    try:
        jwks = get_cognito_jwk()
        headers = jwt.get_unverified_header(token)
        kid = headers.get("kid")
        key = None
        for jwk in jwks["keys"]:
            if jwk["kid"] == kid:
                key = jwk
                break
        if key is None:
            return None
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=COGNITO_APP_CLIENT_ID,
            issuer=COGNITO_ISSUER
        )
        return payload
    except JWTError:
        return None
    except Exception:
        return None

def refresh_user(username: str, refresh_token: str) -> dict:
    """
    Renews the tokens using the refresh token via Cognito.
    """
    try:
        auth_parameters = {
            'REFRESH_TOKEN': refresh_token,
            'SECRET_HASH': get_secret_hash(username),
            'USERNAME': username
        }
        response = client.initiate_auth(
            ClientId=COGNITO_APP_CLIENT_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters=auth_parameters
        )
        return response.get("AuthenticationResult", response)
    except ClientError as e:
        return {"error": e.response["Error"]["Message"]}
