# from fdk import fixtures
# import pytest
# import json
# # Our aqmesh function handler
# from aqmesh.route import handle_invocation

# import aqmesh.route as route

# @pytest.mark.asyncio
# async def test_parse_request_without_data(monkeypatch):
#     def mock_handler(ctx, data, function):
#         return '{"data": "some_data"}'

#     monkeypatch.setattr(route, "base_handler", mock_handler)

#     call = await fixtures.setup_fn_call(handle_invocation)

#     content, status, headers = await call

#     assert status == 200
#     assert json.loads(content) == {"data": "some_data"}
