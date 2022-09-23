from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db.db_setup import get_db
from db.utils.host import create_host, get_host, get_all_hosts, delete_host, update_host
from .forms.host import HostForm

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get('/')
async def main_get(request: Request, db: Session = Depends(get_db)):
    pages = []
    if request.session.get('username'):
        pages = get_all_hosts(db, request.session.get('username'))
    return templates.TemplateResponse('main.html', {'request': request, 'pages': pages})


@router.get('/create')
async def create_get(request: Request):
    if not request.session.get('username'):
        return RedirectResponse(request.url_for('login_get'), status_code=303)
    return templates.TemplateResponse('create.html', {'request': request})


@router.post('/create')
async def create_post(request: Request, db: Session = Depends(get_db)):
    if not request.session.get('username'):
        return RedirectResponse(request.url_for('login_get'), status_code=303)
    form = HostForm(request)
    await form.load_data()
    await form.is_valid()
    if not form.errors:
        if create_host(db, form, request.session.get('username')):
            return RedirectResponse(request.url_for('main_get'), status_code=303)
        return templates.TemplateResponse('create.html', {'request': request, 'msg': 'Route already exists'})
    return templates.TemplateResponse('create.html', {'request': request, 'msg': form.errors[0]})


@router.get('/site/{url:path}')
async def site(request: Request, url: str, db: Session = Depends(get_db)):
    host = get_host(db, url)
    if not host:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return templates.TemplateResponse('site.html', {'request': request, 'content': host.data})


@router.get('/delete/{url:path}')
async def delete(request: Request, url: str, db: Session = Depends(get_db)):
    host = get_host(db, url)
    if host.user.username != request.session.get('username'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't delete others' sites")
    delete_host(db, url)
    return RedirectResponse(request.url_for('main_get'), status_code=303)


@router.get('/update/{url:path}')
async def update_get(request: Request, url: str, db: Session = Depends(get_db)):
    host = get_host(db, url)
    if host.user.username != request.session.get('username'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't edit others' sites")
    return templates.TemplateResponse('update.html', {'request': request, 'host': host})


@router.post('/update/{url:path}')
async def update_post(request: Request, url: str, db: Session = Depends(get_db)):
    host = get_host(db, url)
    if host.user.username != request.session.get('username'):
        return RedirectResponse(request.url_for('main_get'), status_code=303)
    form = HostForm(request)
    await form.load_data()
    await form.is_valid()
    if not form.errors:
        if update_host(db, form, url):
            return RedirectResponse(request.url_for('main_get'), status_code=303)
        return templates.TemplateResponse('update.html', {'request': request, 'host': host, 'msg': 'Route already exists'})
    return templates.TemplateResponse('update.html', {'request': request, 'host': host, 'msg': form.errors[0]})
