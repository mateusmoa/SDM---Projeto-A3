# Compilação das Escolhas Técnicas e Justificativas da Aplicação UniTask

Este documento detalha as escolhas técnicas identificadas na aplicação UniTask, com base na análise do código-fonte fornecido, incluindo o `Dockerfile`, `docker-compose.yml` e `requirements.txt`. Para cada escolha, será apresentada uma justificativa, destacando os benefícios e, quando aplicável, as considerações ou alternativas.

## 1. Linguagem de Programação: Python

A aplicação UniTask é desenvolvida em Python, conforme evidenciado pelos arquivos `requirements.txt` e a estrutura do projeto. A imagem base do Dockerfile (`python:3.11-slim`) também confirma essa escolha.

### Justificativa:

Python é uma linguagem de programação de alto nível, interpretada e de propósito geral, conhecida por sua simplicidade e legibilidade. Sua vasta coleção de bibliotecas e frameworks, como o Flask utilizado nesta aplicação, acelera o desenvolvimento e oferece soluções robustas para diversas necessidades. A comunidade ativa e a grande quantidade de recursos disponíveis facilitam a resolução de problemas e a manutenção do código. Além disso, a portabilidade do Python permite que a aplicação seja executada em diferentes sistemas operacionais com poucas ou nenhuma modificação.

## 2. Framework Web: Flask

O framework Flask é utilizado para construir a aplicação web, conforme listado no `requirements.txt` (`Flask==3.1.1`).

### Justificativa:

Flask é um microframework web para Python, o que significa que ele fornece apenas o essencial para construir aplicações web, sem impor muitas dependências ou escolhas de design. Isso o torna leve, flexível e ideal para projetos menores ou para desenvolvedores que preferem ter mais controle sobre os componentes que utilizam. Sua simplicidade e facilidade de aprendizado permitem um rápido desenvolvimento de protótipos e APIs RESTful. A modularidade do Flask também facilita a integração com outras bibliotecas e ferramentas, como o Flask-SQLAlchemy para interação com o banco de dados.

## 3. ORM (Object-Relational Mapper): Flask-SQLAlchemy

A aplicação utiliza Flask-SQLAlchemy para gerenciar a interação com o banco de dados, conforme indicado no `requirements.txt` (`Flask-SQLAlchemy==3.1.1`).

### Justificativa:

Flask-SQLAlchemy é uma extensão do Flask que simplifica o uso do SQLAlchemy, um poderoso ORM para Python. Um ORM permite que os desenvolvedores interajam com o banco de dados usando objetos Python, em vez de escrever SQL puro. Isso abstrai a complexidade das operações de banco de dados, tornando o código mais legível, fácil de manter e menos propenso a erros de SQL. A integração com o Flask é fluida, proporcionando uma maneira conveniente de definir modelos de dados, realizar consultas e gerenciar transações, o que acelera o desenvolvimento e melhora a produtividade.

## 4. Banco de Dados: SQLite

A presença do arquivo `database.db` e a configuração no `Dockerfile` (`COPY database.db .`) indicam que a aplicação utiliza SQLite como banco de dados.

### Justificativa:

SQLite é um sistema de gerenciamento de banco de dados relacional que se destaca por ser leve, sem servidor e autôônomo. Ele armazena o banco de dados em um único arquivo no sistema de arquivos, o que o torna extremamente fácil de configurar e usar, sem a necessidade de um processo de servidor separado. Essa característica é particularmente útil para aplicações pequenas, protótipos, desenvolvimento local e testes, onde a simplicidade e a portabilidade são prioritárias. A ausência de um servidor de banco de dados dedicado simplifica a implantação e reduz a sobrecarga de recursos.

### Considerações e Alternativas:

Embora o SQLite seja excelente para cenários específicos, ele possui limitações para aplicações em produção que exigem alta concorrência, escalabilidade ou recursos avançados de gerenciamento de banco de dados. Para ambientes de produção, especialmente em configurações Docker, é **altamente recomendado considerar a migração para um banco de dados mais robusto, como PostgreSQL ou MySQL**. Esses bancos de dados oferecem melhor desempenho em cenários de múltiplos usuários, recursos de replicação, backup e recuperação mais avançados, e são mais adequados para ambientes distribuídos e de alta disponibilidade. A documentação fornecida (`Plano para Dockerizar o Banco de Dados UniTask (SQLite).md`) já sugere essa consideração, o que é um bom indicativo de que essa limitação foi reconhecida.

## 5. Containerização: Docker

A aplicação é containerizada usando Docker, conforme evidenciado pelo `Dockerfile` e `docker-compose.yml`.

### Justificativa:

Docker é uma plataforma de containerização que permite empacotar aplicações e suas dependências em contêineres isolados. Essa abordagem garante que a aplicação funcione de forma consistente em diferentes ambientes, desde o desenvolvimento até a produção, eliminando problemas de "funciona na minha máquina". Os contêineres são leves, portáteis e eficientes em termos de recursos, facilitando a implantação, o escalonamento e o gerenciamento da aplicação. A containerização com Docker simplifica o processo de setup para novos desenvolvedores, padroniza o ambiente de execução e melhora a confiabilidade da implantação.

## 6. Orquestração de Contêineres: Docker Compose

O arquivo `docker-compose.yml` é utilizado para definir e executar a aplicação Docker multi-contêiner.

### Justificativa:

Docker Compose é uma ferramenta para definir e executar aplicações Docker multi-contêiner. Com um único arquivo YAML, é possível configurar todos os serviços da aplicação, suas redes e volumes, e iniciá-los com um único comando (`docker-compose up`). Isso simplifica significativamente o gerenciamento de ambientes de desenvolvimento e teste complexos, onde a aplicação pode depender de vários serviços (como um banco de dados, um cache, etc.). O Docker Compose facilita a replicação do ambiente de produção em máquinas de desenvolvimento, garantindo consistência e reduzindo a complexidade da configuração manual.


