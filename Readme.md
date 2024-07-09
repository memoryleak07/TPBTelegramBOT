# Builds
[![tpb-telegrambot image release](https://github.com/memoryleak07/TPBTelegramBOT/actions/workflows/telegram-bot-release.yml/badge.svg)](https://github.com/memoryleak07/TPBTelegramBOT/actions/workflows/telegram-bot-release.yml)

# How to use TelegramBot

### add bot to docker-compose
```docker-compose
version: '3'

services:
  telegram-bot:
    image: tpb-telegram-bot:latest
    depends_on:
      - telegram-bot-api
    volumes:
      - $LOCAL_DESTINATION_PATH:/data
    environment:
      - LOG_LEVEL=$LOG_LEVEL
      - BOT_TOKEN=$BOT_TOKEN
      - BASE_FILE_URL=$BASE_FILE_URL
      - API_BASE_URL=$API_BASE_URL
      - READ_TIMEOUT=$READ_TIMEOUT
      - QBITTORENT_URL=$QBITTORENT_URL
      - QBITTORENT_USERNAME=$QBITTORENT_USERNAME
      - QBITTORENT_PASSWORD=$QBITTORENT_PASSWORD
      - IS_LOCAL_API=$IS_LOCAL_API
      - DESTINATION_PATH=$DESTINATION_PATH
      - USERS_WITHE_LIST=$USERS_WITHE_LIST
      - GET_INTERNAL_USAGE=$GET_INTERNAL_USAGE
      - TELEGRAM_DOWNLOAD_DATA_FILE_PATH=$TELEGRAM_DOWNLOAD_DATA_FILE_PATH
      - LOCAL_TELEGRAM_DOWNLOAD_DATA_FILE_PATH=$LOCAL_TELEGRAM_DOWNLOAD_DATA_FILE_PATH
```
### Variabili da configurare nell'enviroment

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

### Elenco comandi per configurazione in **BotFather**

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

# How to use Telegram API

### Use container
Per avviarlo può essere utilizzato il seguente `docker-compose`

```docker-compose
version: '3'

services:
  telegram-bot-api:
    image: tpb-telegram-api:latest
    container_name: telegram-bot-api
    environment:
      - API_ID=1234561
      - API_HASH=1234567
    ports:
      - 8880:8080
    volumes:
      - data:/data
    # command: ./build/telegram-bot-api --local --api-id=$API_ID --api-hash=$API_HASH --dir=/data/telegram-api --http-port=8880

volumes:
  data:
```
### Build and install Telegram API on Raspberry Pi

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
