FROM python:alpine3.17
WORKDIR ./app
RUN pip install requests
RUN pip install flask
RUN pip install flask_restful
COPY main.py .
COPY model.py .
COPY collection.py .
EXPOSE 8000 # remove becuase this is only for docker to docker container
ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=8000
CMD ["flask", "run", "--host=0.0.0.0"]