FROM python:3.8-alpine

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 2001

ENTRYPOINT [ "python" ]

CMD [ "caller.py" ]