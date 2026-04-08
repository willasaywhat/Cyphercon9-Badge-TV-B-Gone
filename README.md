# Cyphercon 9 Badge TV B Gone

## Credits

Ported the code from https://github.com/bikeNomad/micropython-tv-b-gone to the Cyphercon 9 Badge.

Mostly this is Claude slop with me fixing it, but it does work. At least on the hotel room TV. Your mileage may vary. 

## Usage

* Push sw1 to start a run
* Push sw2 to cancel a run

## Power / Sleep Modes

The badge has a three-tier sleep system to extend battery life:

| Tier | Trigger | Behaviour | Wake |
|------|---------|-----------|------|
| **Light poll** | Always | CPU halts between button checks (`machine.lightsleep`) instead of busy-waiting | Automatic |
| **Display sleep** | 30 s idle | LCD turns off, CPU drops to 48 MHz | Press SW1 |

The timeout is a configurable constant near the top of `main.py`:

```python
_IDLE_TIMEOUT_MS = 30_000   # 30 s → display-off light sleep
```

## Installation

1. Back up the code and files on your badge: 
```
mpremote ls
mpremote cp :main.py main.py
etc.
```

2. Run badge-update.sh (or the commands in there)