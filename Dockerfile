FROM python:3.10

WORKDIR /home/app/
COPY . /home/app/
RUN pip install -r ./requirements.txt

CMD [ "python3", "app.py"]