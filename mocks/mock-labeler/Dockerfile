FROM python:3.8-alpine

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 2002

ENTRYPOINT [ "python" ]

CMD [ "labeler.py" ]