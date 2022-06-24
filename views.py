from aiohttp import web
from models import UserModel, UserValidationModel, AdvertisementModel, AdvertisementValidationModel
from utils import get_password_hash
from asyncpg.exceptions import UniqueViolationError


async def check_health(request: web.Request):
    return web.json_response({'status': 'OK'})


class UserView(web.View):
    async def get(self):
        user_id = int(self.request.match_info['user_id'])
        user = await UserModel.get(user_id)
        if user is None:
            return web.json_response({'error': 'not found'}, status=404)
        user_data = user.to_dict()
        user_data.pop('password')
        return web.json_response(user_data)

    async def post(self):
        json_data = await self.request.json()
        json_data_validated = UserValidationModel(**json_data).dict()
        try:
            json_data_validated['password'] = get_password_hash(json_data_validated['password'])
            new_user = await UserModel.create(**json_data_validated)
        except UniqueViolationError:
            return web.json_response({'error': 'already exists'}, status=400)
        return web.json_response(new_user.to_dict())


class AdvertisementView(web.View):
    async def get(self):
        advertisement_id = int(self.request.match_info['ad_id'])
        advertisement = await AdvertisementModel.get(advertisement_id)
        if advertisement is None:
            return web.json_response({'error': 'not found'}, status=404)
        ad_data = advertisement.to_dict()
        return web.json_response(ad_data)

    async def post(self):
        json_data = await self.request.json()
        json_data_validated = AdvertisementValidationModel(**json_data).dict()
        new_ad = await AdvertisementModel.create(**json_data_validated)
        return web.json_response(new_ad.to_dict())

    async def delete(self):
        advertisement_id = int(self.request.match_info['ad_id'])
        advertisement = await AdvertisementModel.get(advertisement_id)
        if advertisement is None:
            return web.json_response({'error': 'not found'}, status=404)
        await advertisement.delete()
        return web.json_response({}, status=204)
