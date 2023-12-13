from aiohttp import web
from pydantic import ValidationError

from models import ChatModel
from client import answer_chatgpt, answer_gigachat
from exceptions import ChatGPTException, GigaChatException

routes = web.RouteTableDef()


@routes.post('/chatgpt/')
async def chatgpt_view(request):
    data = await request.json()
    try:
        validated_data = ChatModel(**data)
    except ValidationError:
        return web.HTTPBadRequest(text="Validation error from fields")
    try:
        answer = await answer_chatgpt(validated_data.model_dump())
    except ChatGPTException:
        return web.HTTPNotAcceptable(text="Error from ghatgpt request")
    return web.json_response(answer)


@routes.post('/gigachat/')
async def gigachat_view(request):
    data = await request.json()
    try:
        validated_data = ChatModel(**data)
    except ValidationError:
        return web.HTTPBadRequest(text="Validation error from fields")
    try:
        answer = await answer_gigachat(validated_data.model_dump())
    except GigaChatException:
        return web.HTTPNotAcceptable(text="Error from gigachat request")
    return web.json_response(answer)


async def web_app():
    app = web.Application()
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    web.run_app(web_app())
