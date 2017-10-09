# La imagen base
FROM python:3

# El directorio de trabajo para los comandos (.)
WORKDIR /usr/src/app

# Copia el archivo con los requerimientos al contenedor y luego los instala
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo lo que hay en la carpeta, al directorio de trabajo
COPY . .
