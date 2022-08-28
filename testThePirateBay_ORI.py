from tpblite import TPB
# Customize your search
from tpblite import CATEGORIES, ORDERS

# Create a TPB object with a domain name
# t = TPB('https://tpb.party')

# Or create a TPB object with default domain
t = TPB()


## To print all available categories, use the classmethod printOptions
#CATEGORIES.printOptions()
## Or just a subset of categories, like VIDEO
#CATEGORIES.VIDEO.printOptions()
## Similarly for the sort order
# ORDERS.printOptions()

## Quick search for torrents, returns a Torrents object
# torrents = t.search('flac pink floyd')

## See how many torrents were found
# print('There were {0} torrents found.'.format(len(torrents)))

## Iterate through list of torrents and print info for Torrent object
# for torrent in torrents:
#     print(torrent)

torrents = t.search('flac pink floyd 24bit', page=0, order=ORDERS.NAME.DES, category=CATEGORIES.AUDIO.FLAC)

# See how many torrents were found
print('There were {0} torrents found.'.format(len(torrents)))
# Iterate through list of torrents and print info for Torrent object
for torrent in torrents:
    print(torrent)

# Get the most seeded torrent based on a filter
# torrent = torrents.getBestTorrent(min_seeds=30, min_filesize='500 MiB', max_filesize='20 GiB')

# Or select a particular torrent by indexing
torrent = torrents[0]

# Get the magnet link for a torrent
print(torrent.magnetlink)


# Get the url link for a torrent
print(torrent.url)


