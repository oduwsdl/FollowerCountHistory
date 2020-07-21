FROM       python:3
LABEL      maintainer="Mohammed Nauman Siddique <@naumansiddiqui4>"

RUN        apt update && apt install -y r-base && rm -rf /var/lib/apt/lists/* && docker container run -d --name=memgator-server -p 1208:1208 oduwsdl/memgator --contimeout=10s server

WORKDIR    /app
COPY       requirements.txt ./
RUN        pip install -r requirements.txt
COPY       . ./
RUN        chmod +x *.py

ENTRYPOINT ["./main.py"]
