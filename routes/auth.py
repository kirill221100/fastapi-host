from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db.db_setup import get_db
from db.utils.user import add_new_user, get_user
from .forms.user import UserForm
from core.hashing import Hasher

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get('/login')
async def login_get(request: Request):
    if request.session.get('username'):
        return RedirectResponse(request.url_for('main_get'), status_code=303)
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/login')
async def login_post(request: Request, db: Session = Depends(get_db)):
    if request.session.get('username'):
        return RedirectResponse(request.url_for('main_get'), status_code=303)
    form = UserForm(request)
    await form.load_data()
    user = get_user(form.username, db)
    if user and Hasher.verify_password(form.password, user.password_hash):
        request.session['username'] = user.username
        return RedirectResponse(request.url_for('main_get'), status_code=303)
    return templates.TemplateResponse('login.html', {'request': request, 'msg': 'Incorrect login or password'})


@router.get('/register')
async def register_get(request: Request):
    if request.session.get('username'):
        return RedirectResponse(request.url_for('main_get'), status_code=303)
    return templates.TemplateResponse('register.html', {'request': request})


@router.post('/register')
async def register_post(request: Request, db: Session = Depends(get_db)):
    if request.session.get('username'):
        return RedirectResponse(request.url_for('main_get'), status_code=303)
    form = UserForm(request)
    await form.load_data()
    user = add_new_user(form.username, form.password, db)
    if user:
        request.session['username'] = user.username
        return RedirectResponse(request.url_for('main_get'), status_code=303)
    return templates.TemplateResponse('register.html', {'request': request, 'msg': 'Username is already exists'})


@router.get('/logout')
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(request.url_for('login_get'))