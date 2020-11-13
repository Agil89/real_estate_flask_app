from python:3.8.0-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . .

EXPOSE 5000

ENV FLASK_APP="app.py"

CMD [ "flask", "run" , "-h", "0.0.0.0", "-p", "5000"]





# from alpine:latest

# RUN apk add --no-cache python3-dev \
#     && pip3 install --upgrade pip

# WORKDIR /app

# COPY . /app

# RUN pip3 --no-cache-dir install -r requirements.txt

# EXPOSE 5000

# ENTRYPOINT ["python3"]
# CMD ["app.py"]