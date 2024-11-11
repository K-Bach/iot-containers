#FROM alpine:3.8
#RUN apk add --update python python-dev py-pip py-requests build-base
FROM alpine:3.8

RUN apk add --no-cache python3 python3-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install requests && \
    pip3 install ez_setup && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 1987
ENTRYPOINT ["python"]
CMD ["camera.py"]
