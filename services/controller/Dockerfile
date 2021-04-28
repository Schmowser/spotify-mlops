FROM python:3.8-alpine

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 9000

ENTRYPOINT [ "python" ]

CMD [ "controller.py" ]