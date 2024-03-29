@echo off

python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
deactivate
copy .env.example .env