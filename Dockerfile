# Usa uma imagem oficial do Python
FROM python:3.13

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala o Poetry globalmente
RUN pip install --no-cache-dir poetry

# Copia os arquivos do projeto para dentro do container
COPY pyproject.toml poetry.lock /app/

# Instala dependências do projeto sem criar ambiente virtual
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

# Copia todo o restante do código para dentro do container
COPY . /app

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "ftt.app:app", "--host", "0.0.0.0", "--port", "8000"]
