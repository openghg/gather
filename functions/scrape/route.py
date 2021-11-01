from io import BytesIO
from fdk.context import InvokeContext
from fdk.response import Response
from traceback import format_exc
import json
import os

from webscrape.handlers import scrape_handler


async def handle_invocation(ctx: InvokeContext, data: BytesIO) -> Response:
    """The endpoint for the function. This handles the POST request and passes it through
    to the handler

    Note: this handler should only be used for testing purposes. All function calls
    in a production system should go though Acquire so that data is encrypted in transit.

    Args:
        ctx: Invoke context. This is passed by Fn to the function
        data: Data passed to the function by the user
    Returns:
        dict: Dictionary of return data
    """
    headers = ctx.Headers()

    try:
        # There's no point doing all the processing just find we
        # don't have a token
        _ = os.environ["GIT_TOKEN"]
        # Get the authorization headers
        auth_key = headers["authorization"]
        # Read valid keys JSON from env variable
        key_data = json.loads(os.environ["VALID_KEYS"])
        valid_keys = key_data["keys"]
        # Read args
        post_data = json.loads(data.getvalue())
    except Exception:
        error_str = str(format_exc())
        return Response(ctx=ctx, response_data=error_str)

    if auth_key not in valid_keys:
        ctx.SetResponseHeaders({"Authorisation": "Denied"}, 403)
        return Response(ctx=ctx, response_data=error_str)

    # This handles the calls to each of the network pipelines
    result = scrape_handler(args=post_data)

    return Response(ctx=ctx, response_data=result)
