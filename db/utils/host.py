from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from ..models.host_model import HostModel
from ..models.user_model import UserModel
from .user import get_user
from routes.forms.host import HostForm


async def get_host(db: AsyncSession, route: str):
    host = await db.execute(select(HostModel).filter(HostModel.route == route).options(selectinload(HostModel.user)))
    return host.scalars().first()


async def delete_host(db: AsyncSession, route: str):
    host = await get_host(db, route)
    await db.delete(host)
    await db.commit()
    return True


async def update_host(db: AsyncSession, hostform: HostForm, url: str):
    host = await get_host(db, url)
    if host:
        host.name = hostform.site_name
        host.data = hostform.site_content
        host.route = hostform.url
        await db.commit()
        #await db.refresh(host)
        return True


async def get_all_hosts(db: AsyncSession, username: str):
    hosts = await db.execute(select(HostModel).join(UserModel).filter(UserModel.username == username))
    return hosts.scalars().all()


async def create_host(db: AsyncSession, hostform: HostForm, username: str):
    if not await get_host(db, hostform.url):
        user = await get_user(username, db)
        host = HostModel(name=hostform.site_name, data=hostform.site_content, route=hostform.url, user=user)
        db.add(host)
        await db.commit()
        #await db.refresh(host)
        return host

