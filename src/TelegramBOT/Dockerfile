# Usa un'immagine di base di Python
FROM --platform=$BUILDPLATFORM python:3.10-slim

# Imposta il work directory nel container
WORKDIR /app

# Copia i file nel container
COPY Classes Classes
COPY Models Models
COPY Helpers Helpers
COPY MainTelegramBOT.py MainTelegramBOT.py
COPY requirements.txt .

# Installa le dipendenze del progetto
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Comando per avviare l'applicazione
CMD ["python3", "MainTelegramBOT.py"]
