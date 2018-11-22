## Introduction
Utility for easily connecting to wireless networks from the command line
<p align="center">
  <img width="600" src="https://aniquetahir.github.io/wconnect/example.svg">
</p>


## Requirements

### System Utilities
- ifconfig
- iw

### Python packages
- urwid

## Installation
### Ubuntu/Debian/Raspbian
```
sudo apt update
sudo apt install ifconfig iw wireless-tools
pip3 install -r requirements.txt
```

## Usage
```
python3 main.py
```

## Releases
You can run `wconnect` without installing python by downloading the binaries in the [Releases](https://github.com/aniquetahir/wconnect/releases)