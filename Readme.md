# Modifiche

Aggiunto all'head la possibilità di effettuare il download di documenti, musica e video condividendo il media previa scelta della directory di download sul dispositivo di destinazione.</br>
Per effettuare il download di media superiori ai 20MB è necessario utilizzare API locali.

# Installazione e compilazione API

### Per Raspberry Pi
I seguenti comandi consentono il download dal repository [API Telegram](https://github.com/tdlib/telegram-bot-api.git) e la compilazione su Raspberry Pi.

```bash
sudo apt-get install make git zlib1g-dev libssl-dev gperf php-cli cmake clang libc++-dev libc++abi-dev
git clone --recursive https://github.com/tdlib/telegram-bot-api.git
cd telegram-bot-api
mkdir build
cd build
CXXFLAGS="-stdlib=libc++" CC=/usr/bin/clang CXX=/usr/bin/clang++ cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=../tdlib ..
cmake --install . --target prepare_cross_compiling
```

### Immagine Docker
Per generare un immagine docker si può utilizzare il seguente `Dockerfile`

```Dockerfile
# Usa un'immagine base leggera di Debian
FROM debian:stable

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
CMD ["./tdlib"]
```

Per avviarlo può essere utilizzato il seguente `docker-compose`

```docker-compose
version: '3'

services:
  telegram-bot:
    image: telegram-bot-api:latest
    ports:
      - 8880:8880
    volumes:
      - $TELEGRAM_DATA_PATH:/data
    command: ./build/telegram-bot-api --local --api-id=$API_ID --api-hash=$API_HASH --dir=/data --http-port=8880
```

che necessita delle seguenti variabili, che si ottengono dalla pagina Telegram dedicata [guida](https://core.telegram.org/api/obtaining_api_id#obtaining-api-id), caricabili utilizzando un `.env` file

```
API_ID=<id>
API_HASH=<hash>
TELEGRAM_DATA_PATH=<telegram_data_path>
```

# Elenco comandi per configurazione in **BotFather**

Di seguito l'elenco dei comandi da utilizzare per la configurazione del bot in [BotFather](https://t.me/BotFather).

```
start - Start
dwtelegram - To run section Telegram download
search - To run Torrent download
space - Space on disks
prev - Precedent command
setname - Change name of file in download list
space - Show raspy memory space
next - Next state
dwlist - Download list
end - Close handler
magnet - Download torrent by magnet link
qbittorrent - View qBittorrent command
```

# Variabili da configurare nell'enviroment

Di seguito l'elenco delle variabili da configurare nell'environment, per il debug utilizzare il file `.vscode/launch.json`.

| Key                  | Obbligatorio | Descrizione                                                          | Default value                     |
|----------------------|:------------:|----------------------------------------------------------------------|-----------------------------------|
| BOT_TOKEN            |      SI      | Token generato con [BotFather](https://t.me/BotFather)               |                                   |
| LOG_LEVEL            |              | Livello di logging                                                   | ERROR                             |
| BASE_FILE_URL        |              | Directory di salvataggio dei file scaricati tramite telegram         | https://api.telegram.org/file/bot |
| API_BASE_URL         |              | Endpoint delle API telegram                                          | https://api.telegram.org/bot      |
| READ_TIMEOUT         |              | Timeout del download dei file scaricati tramite telegram. Utilizzando API avviate in locale settare a None| 5.0 |
| QBITTORENT_URL       |      SI      | Indirizzo client QBittorrent                                         |                                   |
| QBITTORENT_USERNAME  |              | Username per l'accesso al client QBittorrent                         |                                   |
| QBITTORENT_PASSWORD  |              | Password per l'accesso al client QBittorrent                         |                                   |
| IS_LOCAL_API         |              | Indica se le API di telegram sono avviate in locale                  | False                             |
| DESTINATION_PATH     |      SI      | Path di salvataggio dei file scaricati tramite telegram. Attraverso tale path si ottine anche lo spazio di archiviazione: disponibile, usato e totale | |
| USERS_WITHE_LIST     |              | Lista di username autorizzati all'utilizzo del bot separati da virgola. Se non vengono specificati l'accesso è autorizzato a tutti | |
| GET_INTERNAL_USAGE   |              | Indica se ottenere le info di archiviazione della memoria interna    | False |
| TELEGRAM_DOWNLOAD_DATA_FILE_PATH | SI | Indica il path di salvataggio del file `data.dict` utilizzato per la storicizzazione dei file da scaricare tramite telegram | |

Per eseguire il bot al di fuori di un Docker, è possibile aggiungere un file `.env` nel path di esecuzione, per non configurare le variabili a livello di sistema operativo.
Di seguito un esempio del file.

```
BOT_TOKEN=<BOT_TOKEN>
LOG_LEVEL=<LOG_LEVEL>
BASE_FILE_URL=<BASE_FILE_URL>
API_BASE_URL=<API_BASE_URL>
READ_TIMEOUT=None
QBITTORENT_URL=<QBITTORENT_URL>
QBITTORENT_USERNAME=<QBITTORENT_USERNAME>
QBITTORENT_PASSWORD=<QBITTORENT_PASSWORD>
IS_LOCAL_API=True
DESTINATION_PATH=<DESTINATION_PATH>
USERS_WITHE_LIST=<USER_LIST_SEPARATED_FROM_COMMA>
GET_INTERNAL_USAGE=False
TELEGRAM_DOWNLOAD_DATA_FILE_PATH=<TELEGRAM_DOWNLOAD_DATA_FILE_PATH>
```
