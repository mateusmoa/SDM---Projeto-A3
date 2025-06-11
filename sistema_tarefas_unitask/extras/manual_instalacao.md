# Manual de Instalação da Aplicação UniTask

Este manual fornece instruções detalhadas para a instalação e execução da aplicação UniTask utilizando Docker e Docker Compose. Ele aborda os pré-requisitos, o processo de configuração e as etapas para iniciar a aplicação.

## 1. Pré-requisitos

Para instalar e executar a aplicação UniTask, você precisará ter os seguintes softwares instalados em seu sistema:

*   **Docker:** Uma plataforma para desenvolver, enviar e executar aplicações usando contêineres. Você pode baixar e instalar o Docker Desktop (que inclui o Docker Engine, Docker CLI e Docker Compose) para Windows, macOS ou Linux a partir do site oficial do Docker [1].

*   **Docker Compose:** Uma ferramenta para definir e executar aplicações Docker multi-contêiner. O Docker Compose geralmente vem incluído com o Docker Desktop. Se você estiver em Linux e instalou o Docker Engine separadamente, pode ser necessário instalar o Docker Compose manualmente [2].

Certifique-se de que o Docker e o Docker Compose estejam funcionando corretamente antes de prosseguir. Você pode verificar as instalações abrindo um terminal e executando os seguintes comandos:

```bash
docker --version
docker-compose --version
```

Ambos os comandos devem retornar a versão instalada do respectivo software.

## 2. Estrutura do Projeto

Após descompactar o arquivo fornecido, você encontrará uma estrutura de diretórios semelhante a esta:

```
DOCKERESQLITE/
└── DOCKER E SQLITE/
    └── sistema_tarefas_unitask/
        ├── Dockerfile
        ├── database.db
        ├── docker-compose.yml
        ├── env.example
        ├── main.py
        ├── requirements.txt
        ├── src/
        │   ├── models/
        │   ├── routes/
        │   ├── static/
        │   └── templates/
        └── extras/
            ├── Documentação do Sistema de Gerenciamento de Tarefas (UniTask).md
            └── instrucoes_uso_sistema_tarefas.md
```

O diretório principal da aplicação é `sistema_tarefas_unitask`.

## 3. Instalação e Execução

Siga os passos abaixo para instalar e executar a aplicação UniTask:

### Passo 3.1: Navegar até o Diretório do Projeto

Abra um terminal ou prompt de comando e navegue até o diretório `sistema_tarefas_unitask`:

```bash
cd /caminho/para/DOCKERESQLITE/DOCKER\ E\ SQLITE/sistema_tarefas_unitask
```

Substitua `/caminho/para/DOCKERESQLITE` pelo caminho real onde você descompactou o arquivo.

### Passo 3.2: Construir e Iniciar os Contêineres

No diretório `sistema_tarefas_unitask`, execute o seguinte comando para construir a imagem Docker da aplicação e iniciar o contêiner:

```bash
docker-compose up --build -d
```

*   `docker-compose up`: Inicia os serviços definidos no `docker-compose.yml`.
*   `--build`: Força a reconstrução da imagem Docker. Isso é útil na primeira vez que você executa ou se houver alterações no `Dockerfile` ou `requirements.txt`.
*   `-d`: Executa os contêineres em modo "detached" (segundo plano), liberando o terminal.

Este processo pode levar alguns minutos na primeira execução, pois o Docker precisará baixar a imagem base do Python e instalar as dependências.

### Passo 3.3: Verificar o Status dos Contêineres

Você pode verificar se o contêiner está em execução com o seguinte comando:

```bash
docker-compose ps
```

Você deverá ver o serviço `app` com o status `Up`.

### Passo 3.4: Acessar a Aplicação

Uma vez que o contêiner esteja em execução, a aplicação UniTask estará acessível em seu navegador web. Abra seu navegador e navegue para:

```
http://localhost:5000
```

Você deverá ver a página de login ou a interface principal da aplicação UniTask.

## 4. Parando e Removendo os Contêineres

Para parar os contêineres sem removê-los, no diretório `sistema_tarefas_unitask`, execute:

```bash
docker-compose stop
```

Para parar e remover os contêineres, redes e volumes criados pelo `docker-compose up`, execute:

```bash
docker-compose down
```

*   `docker-compose down`: Para e remove os contêineres, redes e volumes definidos no `docker-compose.yml`.

## 5. Considerações Adicionais

### 5.1. Variáveis de Ambiente

O arquivo `docker-compose.yml` inclui uma variável de ambiente `SECRET_KEY`. Para ambientes de produção, é **altamente recomendado** gerenciar essa chave de forma segura, por exemplo, usando um arquivo `.env` separado (conforme sugerido pelo `env.example` no projeto) ou um sistema de gerenciamento de segredos.

### 5.2. Persistência de Dados (Banco de Dados SQLite)

Atualmente, o banco de dados SQLite (`database.db`) é copiado para o contêiner. Isso significa que, se o contêiner for removido (por exemplo, com `docker-compose down`), todos os dados do banco de dados serão perdidos. Para garantir a persistência dos dados, especialmente em ambientes de produção, é **crucial implementar um volume Docker para o arquivo `database.db`**.

Um exemplo de como você poderia modificar seu `docker-compose.yml` para persistir o banco de dados seria:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data # Mapeia um diretório local 'data' para '/app/data' no contêiner
    environment:
      SECRET_KEY: 'sua-chave-secreta-aqui-ou-use-env-file'

volumes:
  data: # Define um volume nomeado para persistência
```

Neste exemplo, você precisaria ajustar seu `Dockerfile` e o código da aplicação para que o `database.db` seja criado ou acessado dentro do diretório `/app/data` no contêiner. Alternativamente, você pode mapear diretamente o arquivo `database.db` se ele já existir e você quiser persistir as alterações:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - ./database.db:/app/database.db # Mapeia o arquivo local database.db para o contêiner
    environment:
      SECRET_KEY: 'sua-chave-secreta-aqui-ou-use-env-file'
```

**Recomendação:** Para ambientes de produção, considere migrar de SQLite para um banco de dados mais robusto como PostgreSQL ou MySQL, que são mais adequados para ambientes Docker e oferecem melhor persistência e escalabilidade.

## 6. Referências

[1] Docker Desktop: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
[2] Install Docker Compose: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)


