## Plano para Dockerizar o Banco de Dados UniTask (SQLite)

- [X] **Passo 1: Criar Dockerfile para a Aplicação Flask**
    - Definir imagem base Python.
    - Configurar diretório de trabalho.
    - Copiar `requirements.txt` e instalar dependências.
    - Copiar código-fonte da aplicação (`src`, `database.db`).
    - Expor a porta 5000.
    - Definir comando de execução (`python src/main.py`).

- [X] **Passo 2: Criar docker-compose.yml**
    - Definir serviço `app` para a aplicação Flask.
    - Configurar build a partir do Dockerfile.
    - Mapear porta `5000:5000`.
    - Definir volume nomeado para persistir `database.db`.
    - Mapear o volume nomeado para `/app/database.db` (ou caminho correspondente no container).
    - (Opcional) Mapear código-fonte para desenvolvimento.
    - Definir variáveis de ambiente (ex: `SECRET_KEY`).

- [X] **Passo 3: Ajustar Configuração da Aplicação**
    - Modificar `SQLALCHEMY_DATABASE_URI` em `src/main.py` para apontar para o caminho do banco dentro do container (ex: `sqlite:////app/database.db`).
    - Garantir que `SECRET_KEY` seja lida de variável de ambiente.

- [S] **Passo 4: Construir e Validar** (Pulado - Docker não disponível no ambiente)
    - Construir a imagem Docker usando `docker-compose build`.
    - Iniciar os containers com `docker-compose up`.
    - Verificar logs e acessar a aplicação para confirmar funcionamento.
    - Testar persistência do banco (criar dados, parar/reiniciar container, verificar dados).

- [X] **Passo 5: Preparar Entrega**
    - Organizar arquivos (`Dockerfile`, `docker-compose.yml`, código modificado).
    - Escrever instruções de uso.
    - Enviar arquivos e instruções ao usuário.
