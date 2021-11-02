FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /what_to_eat_today
COPY requirements.txt /what_to_eat_today/
RUN pip install -r requirements.txt
COPY . /what_to_eat_today/