FROM python:slim

RUN pip install requests

COPY ["src", "/"]

RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
