FROM python:3.11-buster

USER root
RUN apt update && apt upgrade -y
RUN useradd -m -p fast_api fast_api && mkdir /opt/api && chown -R fast_api:fast_api /opt/api
ADD requirements.txt ./

USER fast_api

RUN pip install --user -r ./requirements.txt
WORKDIR /opt/api
ADD ./ ./

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]