FROM openghg/pipeline-base:latest

COPY route.py /function/
USER $FN_USER

ENTRYPOINT ["/python/bin/fdk", "/function/route.py", "handle_invocation"]
