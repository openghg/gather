from io import BytesIO
from fdk.context import InvokeContext
from fdk.response import Response
from traceback import format_exc
import json
import os

from webscrape.handlers import data_handler


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
        auth_key = headers["authorization"]
        # Quick and dirty auth key lookup
        # Load the valid authentication keys from
        key_data = json.loads(os.environ["VALID_KEYS"])
        valid_keys = key_data["keys"]
    except KeyError:
        error_str = str(format_exc())
        return Response(ctx=ctx, response_data=error_str)

    if auth_key not in valid_keys:
        ctx.SetResponseHeaders({"Authorisation": "Denied"}, 403)
        return Response(ctx=ctx, response_data=error_str)

    raw_data = data.getvalue()
    result = data_handler(data=raw_data)

    return Response(ctx=ctx, response_data=result)
