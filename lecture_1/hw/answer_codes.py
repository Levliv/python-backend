import json


async def error_422(send):
    await send(
        {
            "type": "http.response.start",
            "status": 422,
            "headers": [(b"content-type", b"text/plain")],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": b'json.dumps({"error": "Unprocessable Entity"})',
        }
    )
    return


async def error_400(send):
    await send(
        {
            "type": "http.response.start",
            "status": 400,
            "headers": [(b"content-type", b"text/plain")],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": json.dumps({"error": "Bad Request"}).encode("utf-8"),
        }
    )
    return


async def error_404(send):
    await send(
        {
            "type": "http.response.start",
            "status": 404,
            "headers": [(b"content-type", b"text/plain")],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": json.dumps({"error": "Not Found"}).encode("utf-8"),
        }
    )
    return


async def result_send(send, func, value):
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'plain/text'],
        ],
    })
    result = await func(value)
    await send({
        'type': 'http.response.body',
        'body': json.dumps({"result": result}).encode('utf-8'),
    })
    return