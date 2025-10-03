#!/bin/bash

echo "Atualizando o pip..."
pip install --upgrade pip

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Instalando python-dotenv (caso não esteja no requirements.txt)..."
pip install python-dotenv

echo "Verificando e instalando gunicorn..."
pip show gunicorn || pip install gunicorn

echo "Aplicando migrações do banco de dados..."
python manage.py migrate

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput


echo "Build concluído com sucesso!"