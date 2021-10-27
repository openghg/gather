FROM openghg/pipeline-base:latest

COPY route.py /function/

ENTRYPOINT ["/python/bin/fdk", "/function/route.py", "handle_invocation"]
