#!/bin/bash
echo "BUILD START"

# Mostrar información del sistema
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Instalar dependencias
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear directorio de archivos estáticos
mkdir -p staticfiles_build
mkdir -p staticfiles_build/static

# Recopilar archivos estáticos
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Verificar que se creó el directorio
ls -la staticfiles_build/

echo "BUILD END"
