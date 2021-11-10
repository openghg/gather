import io
from fdk.context import InvokeContext

from gather.handlers import base_handler
import gather.pipeline as pipeline

# We need to patch the import of git_commit in the _base.py file
import gather.handlers._base as base
from pandas import Timestamp


def test_base_handler(monkeypatch):
    def mock_git(repo_url, processed_data, commit_msg):
        return None

    def mock_crds(data):
        return {"test": "data"}

    def mock_timestamp():
        return "2021-01-01T00:00:00"

    monkeypatch.setattr(base, "git_commit", mock_git)
    monkeypatch.setattr(pipeline, "run_crds", mock_crds)
    monkeypatch.setattr(Timestamp, "now", mock_timestamp)

    monkeypatch.setenv("VALID_KEYS", '{"keys": ["valid-test-key-123"]}')
    monkeypatch.setenv("GIT_TOKEN", "test-token")

    ctx = InvokeContext(
        app_id="1",
        app_name="gather_test",
        fn_id="test-id",
        fn_name="test-name",
        call_id=123,
        headers={"authorization": "valid-test-key-123"},
    )

    bin_data = io.BytesIO(b"1234")
    response = base_handler(ctx=ctx, data=bin_data, function="run_crds")
    response_data = response.response_data

    assert response_data == {
        "run_crds": "run_crds run success at - 2021-01-01T00:00:00"
    }

    ctx = InvokeContext(
        app_id="1",
        app_name="gather_test",
        fn_id="test-id",
        fn_name="test-name",
        call_id=123,
        headers="nonsense_here",
    )

    response = base_handler(ctx=ctx, data=bin_data, function="run_crds")
    assert response.status_code == 500

    ctx = InvokeContext(
        app_id="1",
        app_name="gather_test",
        fn_id="test-id",
        fn_name="test-name",
        call_id=123,
        headers={"authorization": "valid-test-key-123"},
    )

    def mock_crds(data):
        raise TypeError("CRDS process error")

    monkeypatch.setattr(pipeline, "run_crds", mock_crds)

    response = base_handler(ctx=ctx, data=bin_data, function="run_crds")

    assert response.status_code == 500

    response_headers = response.context().GetResponseHeaders()

    assert response_headers["function_process_error"] == "CRDS process error"

    monkeypatch.setenv("VALID_KEYS", '{"keys": ["valid-test-key-321"]}')
    response = base_handler(ctx=ctx, data=bin_data, function="run_crds")
    assert response.status_code == 500
    response_headers = response.context().GetResponseHeaders()

    assert response_headers["function_setup_error"] == "'Invalid authorisation key.'"

    monkeypatch.delenv("GIT_TOKEN")
    response = base_handler(ctx=ctx, data=bin_data, function="run_crds")
    assert response.status_code == 500
    response_headers = response.context().GetResponseHeaders()
    assert response_headers["function_setup_error"] == "'GIT_TOKEN'"
