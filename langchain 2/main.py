
from __future__ import print_function
from pydantic import BaseModel
from typing import Optional
from fastapi import Body, FastAPI
from config import getNewmail, getResponsemail
from langchain.assistant.ai_assistant import AIAssistant
import uvicorn
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError


import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



app = FastAPI(
    title="API",
    description="",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
)
import os

os.environ["OPENAI_API_KEY"] = "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"

class UserInput(BaseModel):
    query: str
    content: Optional[str] = None

app.add_middleware(SessionMiddleware, secret_key='!secret')
config = Config('.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.get('/')
async def home(request: Request):
    user = request.session.get('user')
    if user is not None:
        email = user['email']
        html = (
            f'<pre>Email: {email}</pre><br>'
            '<a href="/docs">documentation</a><br>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')

@app.get('/login', tags=['authentication'])  # Tag it as "authentication" for our docs
async def login(request: Request):
    # Redirect Google OAuth back to our application
    redirect_uri = request.url_for('auth')

    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')

@app.get('/logout', tags=['authentication'])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)

    return RedirectResponse(url='/')

async def get_user(request: Request) -> Optional[dict]:
    user = request.session.get('user')
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=403, detail='Could not validate credentials.')

    return None

@app.route('/openapi.json')
async def get_open_api_endpoint(request: Request, user: Optional[dict] = Depends(get_user)):  # This dependency protects our endpoint!
    response = JSONResponse(get_openapi(title='FastAPI', version=1, routes=app.routes))
    return response


@app.get('/docs', tags=['documentation'])  # Tag it as "documentation" for our docs
async def get_documentation(request: Request, user: Optional[dict] = Depends(get_user)):  # This dependency protects our endpoint!
    response = get_swagger_ui_html(openapi_url='/openapi.json', title='Documentation')
    return response

def gmail_create_draft(email):
    creds, _ = google.auth.default()
    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()
        message.set_content('This is automated draft mail')
        message['To'] = 'gduser1@workspacesamples.dev'
        message['From'] = email
        message['Subject'] = 'Automated draft'
        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {
            'message': {
                'raw': encoded_message
            }
 
        }
        # pylint: disable=E1101
        draft = service.users().drafts().create(userId="me",
                                                body=create_message).execute()

        print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None

    return draft


@app.post('/draft', tags=["draft"])
def query(request:Request):
    try:
        user = request.session.get('user')
        email = user["email"]
        gmail_create_draft(email)
    except Exception as e:
        return {"error": str(e)}



@app.post('/query', tags=["query"])
def query(input: UserInput = Body(examples=getNewmail)):
    try:
        ai = AIAssistant(query=input.query, content=input.content)
        status, response = ai.execute_utility()
        if status == True:
            return {
                "response": response
            }
        else:
            return {
                "message": "No response found"
            }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
