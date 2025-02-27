# Usa uma imagem base do Python
FROM python:3.10-slim

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
COPY . .

# Exponha a porta 8080 (ou 5000, se preferir)
EXPOSE 8080

# Comando para iniciar o Gunicorn, rodando a aplicação Flask
CMD ["gunicorn", "--workers", "2", "--timeout", "300", "--bind", "0.0.0.0:8080", "run:app"]



