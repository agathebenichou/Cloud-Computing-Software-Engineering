FROM python:alpine3.17

WORKDIR ./meals

RUN pip install requests
RUN pip install flask
RUN pip install flask_restful

COPY main.py .
COPY model.py .
COPY collection.py .

ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=5001
CMD ["flask", "run", "--host=0.0.0.0"]