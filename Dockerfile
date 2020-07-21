FROM       python:3
LABEL      maintainer="Mohammed Nauman Siddique <@m_nsiddique>"

RUN        apt update && apt install -y r-base && rm -rf /var/lib/apt/lists/*

WORKDIR    /app
COPY       requirements.txt ./
RUN        pip install -r requirements.txt
COPY       . ./
RUN        chmod +x *.py

ENTRYPOINT ["./main.py"]
