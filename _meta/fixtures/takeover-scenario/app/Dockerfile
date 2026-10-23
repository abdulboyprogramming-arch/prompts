FROM python:3.12-slim
WORKDIR /srv
COPY . /srv
RUN pip install -r app/requirements.txt
EXPOSE 8080
CMD python app/main.py
