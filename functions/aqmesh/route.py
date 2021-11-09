from io import BytesIO
from fdk.context import InvokeContext
from fdk.response import Response

from gather.handlers import base_handler


async def handle_invocation(ctx: InvokeContext, data: BytesIO) -> Response:
    """The endpoint for the function. This handles the POST request and passes it through
    to the handler

    Args:
        ctx: Invoke context. This is passed by Fn to the function
        data: Data passed to the function by the user
    Returns:
        dict: Dictionary of return data
    """
    return base_handler(ctx=ctx, data=data, function="aqmesh")
