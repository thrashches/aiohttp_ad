from aiohttp import web
from gino import Gino
import config

app = web.Application()

db = Gino()


async def init_orm(app):
    print('Application started!')
    await db.set_bind(config.PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()
    print('Application stopped!')


app.cleanup_ctx.append(init_orm)
