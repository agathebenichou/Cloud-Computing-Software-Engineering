FROM python:alpine3.17

WORKDIR ./diets

RUN pip install requests
RUN pip install flask
RUN pip install flask_restful
RUN pip install pymongo

COPY main.py .
COPY model.py .
COPY collection.py .

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5002

CMD ["flask", "run"]
