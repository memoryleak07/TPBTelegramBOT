# Modifiche

Aggiunto all'head la possibilità di effettuare il download di documenti, musica e video condividendo il media previa scelta della directory di download sul dispositivo di destinazione.</br>
Per effettuare il download di media superiori ai 20MB è necessario utilizzare API locali.

# Installazione e compilazione API

I seguenti comandi consentono il download dal repository dell'API Telegram e la compilazione su Raspberry pi.

```bash
sudo apt-get install make git zlib1g-dev libssl-dev gperf php-cli cmake clang libc++-dev libc++abi-dev
git clone --recursive https://github.com/tdlib/telegram-bot-api.git
cd telegram-bot-api
mkdir build
cd build
CXXFLAGS="-stdlib=libc++" CC=/usr/bin/clang CXX=/usr/bin/clang++ cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=../tdlib ..
cmake --install . --target prepare_cross_compiling
``` 

# Elenco comandi per configurazione in **BotFather**

Di seguito l'elenco dei comandi da utilizzare per la configurazione del bot in **BotFather**

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
| READ_TIMEOUT         |              | Timeout del download dei file scaricati tramite telegram. Utilizzando API avviate in locale settare a None| 5.0                               |
| QBITTORENT_URL       |      SI      | Indirizzo client QBittorrent                                         |                                   |
| QBITTORENT_USERNAME  |              | Username per l'accesso al client QBittorrent                         |                                   |
| QBITTORENT_PASSWORD  |              | Password per l'accesso al client QBittorrent                         |                                   |
| IS_LOCAL_API         |              | Indica se le API di telegram sono avviate in locale                  | False                             |
| EXTERNAL_MEMORY_PATH |              | Path dell'HDD esterno utilizzato per ottenere lo spazio Disponibile  |                                   |

Per eseguire il bot al di fuori di un Docker, è possibile aggiungere un file `.env` nel path di esecuzione per non configurare le variabili a livello di sistema operativo.
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
EXTERNAL_MEMORY_PATH=<EXTERNAL_MEMORY_PATH>
```