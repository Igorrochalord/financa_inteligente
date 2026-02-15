FROM python:3.10-slim

WORKDIR /app

# Dependências de sistema (necessário para compilar algumas libs python)
RUN apt-get update && apt-get install -y build-essential curl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]