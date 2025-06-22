# Usa uma imagem base do Python
FROM python:3.10-slim

# Garante que o pip esteja instalado
RUN apt update && apt install -y python3-pip

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

#ENV SECRET_KEY=AmberlyqueriaS3erohalo
#ENV DATABASE_URL=postgresql://postgres:V0lBaT3rComAcaraNoposte@db:5432/biblioteca

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o container
COPY requirements.txt requirements.txt

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o container
COPY config.py .
COPY app/static/ /app/static/
COPY . .
COPY postgres/conf/postgresql.conf /postgresql.conf

# Exponha a porta 8080 (ou 5000, se preferir)
EXPOSE 8080

# Comando para iniciar o Gunicorn, rodando a aplicação Flask
CMD ["gunicorn", "--workers", "2", "--timeout", "300", "--bind", "0.0.0.0:8080", "run:app"]



