from aiohttp import web
from app import app
from views import UserView, AdvertisementView, check_health

app.add_routes([
    web.get('/check', check_health),
    web.post('/users', UserView),
    web.get('/users/{user_id:\d+}', UserView),
    web.post('/ads', AdvertisementView),
    web.get('/ads/{ad_id:\d+}', AdvertisementView),
    web.delete('/ads/{ad_id:\d+}', AdvertisementView),
])
