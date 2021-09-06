FROM python:slim

RUN pip install requests

COPY ["src", "/"]

ENTRYPOINT [ "/entrypoint.sh" ]
