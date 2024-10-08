from typing import Any, Awaitable, Callable
from .answer_codes import error_404
from .routes import mean_route, fibonacci_route, factorial_route

async def app(scope: dict[str, Any],
        receive: Callable[[], Awaitable[dict[str, Any]]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
) -> None:
    if scope["type"] == "lifespan":
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return
    if scope["type"] == "http":
        if scope["method"] == "GET":
            if scope["path"] == "/factorial":
                await factorial_route(scope, send)
                return

            if scope["path"].split("/")[1] == "fibonacci":
                await fibonacci_route(scope, send)
                return

            if scope["path"] == "/mean":
                await mean_route(scope, receive, send)
                return
        await error_404(send)
