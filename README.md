# Python TCP Port Scanner

A simple TCP connect port scanner built in Python to demonstrate network enumeration fundamentals.

⚠️ Only scan systems you own or have explicit permission to test.

## Features
- Target host/IP input
- Port ranges (`1-1024`) or comma lists (`22,80,443`)
- Configurable timeout
- Multithreaded scanning for speed
- Clear open-port reporting

## Usage

Scan common ports:
```bash
python3 port_scanner.py 127.0.0.1 -p 1-1024
