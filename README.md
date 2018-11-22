## Introduction
Utility for easily connecting to wireless networks from the command line

## Requirements

### System Utilities
- ifconfig
- iw

### Python packages
- urwid

## Installation
### Ubuntu/Debian
```
sudo apt update
sudo apt install ifconfig iw
pip install -u requirements.txt
```

### FreeBSD
```
pkg update
pkg install ifconfig iw
pip install -u requirements.txt
```

## Usage
```
python main.py
```