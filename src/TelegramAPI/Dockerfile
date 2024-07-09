# Usa un'immagine base leggera di Debian
FROM debian:stable
ENV API_ID ID
ENV API_HASH HASH

# Installa le dipendenze necessarie
RUN apt-get update && apt-get install -y \
    make \
    git \
    zlib1g-dev \
    libssl-dev \
    gperf \
    php-cli \
    cmake \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Clona il repository
RUN git clone --recursive https://github.com/tdlib/telegram-bot-api.git /telegram-bot-api

# Imposta il directory di lavoro nell'immagine
WORKDIR /telegram-bot-api

# Crea il directory di build
RUN mkdir build

# Entra nel directory di build
WORKDIR /telegram-bot-api/build

# Compila il progetto
RUN cmake -DCMAKE_BUILD_TYPE=Release ..

# Installa il progetto
RUN cmake --build . --target install

# Torna alla directory principale del progetto
WORKDIR /telegram-bot-api

# Comando predefinito per avviare l'applicazione
#CMD ["./tdlib"]
# ./build/telegram-bot-api --local --api-id=$API_ID --api-hash=$API_HASH --dir=/data/telegram-api --http-port=8880
#CMD ["./build/telegram-bot-api", "--local", "--api-id=$API_ID", "--api-hash=$API_HASH", "--dir=$DATADIR", "--http-port=$PORT"]
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]