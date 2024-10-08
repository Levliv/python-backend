from .math import factorial, fibonacci, mean
import json
from urllib.parse import parse_qs
from .answer_codes import error_400, error_422, result_send

async def factorial_route(scope, send):
    value = 0
    try:
        value = int(parse_qs(scope["query_string"].decode())["n"][0])
    except Exception:
        await error_422(send)
        return
    if value < 0:
        await error_400(send)
    else:
        await result_send(send, factorial, value)
    return


async def fibonacci_route(scope, send):
    value = 0
    try:
        value = int(scope["path"].split("/")[2])
    except Exception:
        await error_422(send)
        return
    if value < 0:
        await error_400(send)
    else:
        await result_send(send, fibonacci, value)
    return


async def mean_route(scope, receive, send):
    body = b""
    more_body = True

    while more_body:
        message = await receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)
    try:
        values = json.loads(body)
        if len(values) == 0:
            await error_400(send)
            return
    except Exception:
        await error_422(send)
        return
    if not all(
        [isinstance(value, float) or isinstance(value, int) for value in values]
    ):
        await error_422(send)
        return
    await result_send(send, mean, values)
    return