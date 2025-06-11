# Use uma imagem Python oficial como imagem base
FROM python:3.11-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo de dependências
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o diretório src e o arquivo do banco de dados para o diretório de trabalho
COPY src/ ./src
COPY database.db .

# Exponha a porta que a aplicação Flask usa
EXPOSE 5000

# Defina variáveis de ambiente (opcional, pode ser feito no docker-compose)
# ENV FLASK_APP=src/main.py
# ENV FLASK_RUN_HOST=0.0.0.0
ENV SECRET_KEY=uma-chave-secreta-padrao-mas-use-env-no-compose

# Comando para rodar a aplicação
CMD ["python", "src/main.py"]

