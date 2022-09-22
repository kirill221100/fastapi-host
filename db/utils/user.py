from sqlalchemy.orm import Session
from ..models.user_model import UserModel
from core.hashing import Hasher


def check_if_user_exists(username: str, db: Session):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user:
        return True


def get_user(username: str, db: Session):
    return db.query(UserModel).filter(UserModel.username == username).first()


def add_new_user(username: str, password: str, db: Session):
    if not check_if_user_exists(username, db):
        user = UserModel(username=username, password_hash=Hasher.get_password_hash(password))
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
