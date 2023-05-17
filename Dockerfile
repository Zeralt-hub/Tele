# Se usa una imagen base de Python
FROM python:3.8-slim-buster

# Se establece un directorio de trabajo
WORKDIR /app

# Se copian los requerimientos de la aplicación
COPY requirements.txt .

# Se instalan los requerimientos de nuestra aplicación
RUN pip install -r requirements.txt

# Se copia el resto del código de aplicación
COPY . .

# Se expone el puerto en el que se ejecutará nuestra aplicación
EXPOSE 5000

# Comando para iniciar la aplicación usando Gunicorn
CMD ["gunicorn", "-b", ":5000", "tele2:app"]