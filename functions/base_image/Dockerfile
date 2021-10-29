FROM fnproject/python:3.8.5

RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade --no-cache-dir pip wheel setuptools && \
    pip3 install --target /python/ --no-cache-dir -r requirements.txt \ 
    git+https://github.com/openghg/openghg.git@devel#egg=openghg

COPY webscrape /python/webscrape
RUN python3 -m compileall /python/webscrape/*

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
