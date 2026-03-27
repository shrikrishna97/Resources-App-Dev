# WSL Setup Commands

This document gives a general set of commands to install and run Redis, Celery, and MailHog in WSL for a Flask app.

## 1. Create and activate virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

## 2. Install Python packages

```bash
pip install Flask Flask-SQLAlchemy Flask-JWT-Extended Flask-CORS Flask-Caching celery redis
```

## 3. requirements.txt

Your `requirements.txt` should contain:

```txt
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Flask-CORS
Flask-Caching
celery
redis
```

`MailHog` should not be added to `requirements.txt` because it is not a Python package.

## 4. Install Redis in WSL

```bash
sudo apt update
sudo apt install -y redis-server
```

## 5. Run Redis server

```bash
redis-server
```

## 6. Install MailHog in WSL

```bash
sudo apt update
sudo apt install -y golang-go
go install github.com/mailhog/MailHog@latest
```

## 7. Run MailHog

```bash
~/go/bin/MailHog
```

MailHog UI:

```text
http://localhost:8025
```

## 8. Run Flask app

```bash
python3 app.py
```

## 9. Run Celery worker

```bash
celery -A celery_worker.celery_app worker --loglevel=info
```

## 10. Run Celery beat

```bash
celery -A celery_worker.celery_app beat --loglevel=info
```

## 11. Full command summary

### Install

```bash
python3 -m venv env
source env/bin/activate
pip install Flask Flask-SQLAlchemy Flask-JWT-Extended Flask-CORS Flask-Caching celery redis
sudo apt update
sudo apt install -y redis-server golang-go
go install github.com/mailhog/MailHog@latest
```

### Run

```bash
python3 app.py
```

```bash
redis-server
```

```bash
celery -A celery_worker.celery_app worker --loglevel=info
```

```bash
celery -A celery_worker.celery_app beat --loglevel=info
```

```bash
~/go/bin/MailHog
```