# Cyphercon 9 Badge TV B Gone

## Credits

Ported the code from https://github.com/bikeNomad/micropython-tv-b-gone to the Cyphercon 9 Badge.

Mostly this is Claude slop with me fixing it, but it does work. At least on the hotel room TV. Your mileage may vary. 

## Usage

* Push sw1 to start a run
* Push sw2 to cancel a run

## Installation

1. Back up the code and files on your badge: 
```
mpremote ls
mpremote cp :main.py main.py
etc.
```

2. Run badge-update.sh (or the commands in there)