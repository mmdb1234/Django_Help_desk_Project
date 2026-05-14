FROM docker.arvancloud.ir/python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE Base_Tiket_Sup.settings

RUN rm -rf /etc/apt/sources.list.d/* && \
    cat > /etc/apt/sources.list << EOF
deb http://mirror.arvancloud.ir/debian bullseye main non-free contrib
deb http://mirror.arvancloud.ir/debian bullseye-updates main non-free contrib
deb http://mirror.arvancloud.ir/debian-security bullseye-security main non-free contrib
EOF

RUN apt-get update -o Acquire::Check-Valid-Until=false && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app/
WORKDIR /app

RUN python manage.py collectstatic --noinput --clear

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "Base_Tiket_Sup.asgi:application"]