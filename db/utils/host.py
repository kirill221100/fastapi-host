from sqlalchemy.orm import Session
from ..models.host_model import HostModel
from ..models.user_model import UserModel
from .user import get_user
from routes.forms.host import HostForm


def get_host(db: Session, route: str):
    return db.query(HostModel).filter(HostModel.route == route).first()


def delete_host(db: Session, route: str):
    host = get_host(db, route)
    db.delete(host)
    db.commit()
    return True


def update_host(db: Session, hostform: HostForm, url: str):
    host = get_host(db, url)
    if host:
        host.name = hostform.site_name
        host.data = hostform.site_content
        host.route = hostform.url
        db.commit()
        db.refresh(host)
        return True




def get_all_hosts(db: Session, username: str):
    return db.query(HostModel).join(UserModel).filter(UserModel.username == username).all()


def create_host(db: Session, hostform: HostForm, username: str):
    if not get_host(db, hostform.url):
        user = get_user(username, db)
        host = HostModel(name=hostform.site_name, data=hostform.site_content, route=hostform.url, user=user)
        db.add(host)
        db.commit()
        db.refresh(host)
        return host

