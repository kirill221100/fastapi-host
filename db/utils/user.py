from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user_model import UserModel
from core.hashing import Hasher


async def check_if_user_exists(username: str, db: AsyncSession):
    user = await db.execute(select(UserModel).filter(UserModel.username == username))
    if user.scalars().first():
        return True


async def get_user(username: str, db: AsyncSession):
    user = await db.execute(select(UserModel).filter(UserModel.username == username))
    return user.scalars().first()


async def add_new_user(username: str, password: str, db: AsyncSession):
    if not await check_if_user_exists(username, db):
        user = UserModel(username=username, password_hash=Hasher.get_password_hash(password))
        db.add(user)
        await db.commit()
        print(user, 8888)
        #await db.refresh(user)
        return user
