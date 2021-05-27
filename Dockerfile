FROM python
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt