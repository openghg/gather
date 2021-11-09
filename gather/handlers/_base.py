from io import BytesIO
from fdk.context import InvokeContext
from fdk.response import Response
from traceback import format_exc
from pandas import Timestamp
import json
import os

import gather.pipeline as pipeline
from gather.utils import git_commit


def base_handler(ctx: InvokeContext, data: BytesIO, function: str) -> Response:
    """The endpoint for the function. This handles the POST request and passes it through
    to the handler

    Args:
        ctx: Invoke context. This is passed by Fn to the function.
        data: Data passed to the function by the caller
        function: Name of function to route this data to
    Returns:
        dict: Dictionary of return data
    """
    headers = ctx.Headers()

    try:
        auth_key = headers["authorization"]
        # There's no point doing all the processing just find we
        # don't have a token
        _ = os.environ["GIT_TOKEN"]
        # Quick and dirty auth key lookup
        # Load the valid authentication keys from
        key_data = json.loads(os.environ["VALID_KEYS"])
        valid_keys = key_data["keys"]

        if auth_key not in valid_keys:
            raise KeyError("Invalid authorisation key.")

        # Get the pipeline function that will process the data
        fn_to_call = getattr(pipeline, name=function)
    except Exception:
        error_str = str(format_exc())
        return Response(ctx=ctx, response_data=error_str)

    run_success = True

    try:
        raw_data = data.getvalue()
        result = fn_to_call(data=raw_data)
        now_str = str(Timestamp.now())
        result[function] = f"{function} run success at - {now_str}"
    except Exception:
        run_success = False
        error_str = str(format_exc())
        result[function] = f"Did not run - {error_str}"

    if run_success:
        repo_url = "github.com/openghg/dashboard_data"
        now_str = str(Timestamp.now())
        commit_msg = f"Automated commit of {function} data at {now_str}"

        commit(repo_url=repo_url, processed_data=result, commit_msg=commit_msg)

    return Response(ctx=ctx, response_data=result)
