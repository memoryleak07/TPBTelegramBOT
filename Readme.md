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

```bash
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