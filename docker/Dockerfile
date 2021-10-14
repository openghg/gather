FROM fnproject/python:3.8-dev as build-stage

RUN apt-get update && apt-get install git -y

# pip 20.2.4 is the version before the new resolver was introduced
RUN pip3 install pip==20.2.4 wheel setuptools && \
    pip3 install --target /python/ git+https://github.com/openghg/openghg.git@devel#egg=openghg-devel


ADD route.py /function/
WORKDIR /function

RUN python3 -m compileall /python/openghg/*

ENV PYTHONPATH=/python
ENV OPENGHG_CLOUD=1
# Become the $FN_USER so that nothing runs as root
USER $FN_USER

ENTRYPOINT ["/python/bin/fdk", "/function/route.py", "handle_invocation"]
