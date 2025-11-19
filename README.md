# knowledge-search-poc

## Initial setup
1. Create `secure.py` beside this README with your OpenAI key  
   `KEY = "sk-..."`  
2. Create a folder named `knowledge-base/` and drop the PDFs you want to chat with.

## Local development (no Poetry)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Log in at `/login/`, upload PDFs at `/upload/`, then ask questions in `/chat/`.

## Docker
```
docker compose up --build
```
Make sure `secure.py`, `requirements.txt`, and your `knowledge-base/` folder are in the build context. Use env vars such as `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` for domain configuration.