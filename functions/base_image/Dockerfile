FROM fnproject/python:3.8-dev as build-stage

RUN apt-get update && apt-get install git -y

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip wheel setuptools && \
    pip3 install --target /python/ -r requirements.txt && \
    pip3 install --target /python/ git+https://github.com/openghg/openghg.git@devel#egg=openghg && \
    pip3 install --target /python/ git+https://github.com/openghg/acquire.git@devel#egg=acquire

COPY webscrape /python/webscrape
RUN python3 -m compileall /python/webscrape/*

FROM fnproject/python:3.8.5

COPY --from=build-stage /python/ /python/
ENV PYTHONPATH=/python
ENV OPENGHG_PATH="/tmp/tmp_store"
ENV ACQUIRE_HOST="localhost:8080"

ENTRYPOINT ["bash"]

# WORKDIR /function


# COPY route.py /function/
# ENV OPENGHG_PATH="/tmp/tmp_store"
# ENV ACQUIRE_HOST="localhost:8080"
# ENV PYTHONPATH=/python
# # Become the $FN_USER so that nothing runs as root
# USER $FN_USER

# ENTRYPOINT ["/python/bin/fdk", "/function/route.py", "handle_invocation"]
