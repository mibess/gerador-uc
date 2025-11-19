# 1. Imagem Base: Começamos com uma imagem oficial do Python 3.10
FROM python:3.10-slim

# 2. Diretório de Trabalho: Define o local padrão dentro do contêiner
WORKDIR /app

# 3. Copia de Dependências: Copia o requirements.txt primeiro
# (Isso otimiza o cache do Docker)
COPY requirements.txt .

# 4. Instalação: Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Criação de usuário não-root
RUN useradd -m appuser
USER appuser

# 6. Cópia do Código: Copia o resto do seu projeto para o contêiner
# Ajuste de permissões para o usuário não-root
COPY --chown=appuser:appuser . .

# 7. Comando de Execução: Como o contêiner deve iniciar
# Use 'gunicorn' para rodar a app na porta 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]