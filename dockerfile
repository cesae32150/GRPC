# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia todos los archivos del directorio local al contenedor
COPY pokemons_pb2_grpc.py .
COPY pokemons_pb2.py .
COPY pokemons_service.py .
COPY pokemons.proto .
COPY server.py .

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto si tu aplicación lo usa (cambia si es necesario)
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "server.py"]
