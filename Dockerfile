FROM       python:3
LABEL      maintainer="Mohammed Nauman Siddique <@naumansiddiqui4>"

RUN        apt update && apt install -y r-base && rm -rf /var/lib/apt/lists/*

WORKDIR    /app
COPY       requirements.txt ./
RUN        pip install -r requirements.txt
COPY       . ./
RUN        chmod +x *.py

ENTRYPOINT ["./followerscript.sh"]
