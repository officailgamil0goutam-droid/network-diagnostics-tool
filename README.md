# Network Diagnostics Tool

A lightweight Python command-line tool that performs a quick first-pass
health check on a machine's network connectivity — the kind of check an
IT support technician runs before escalating a "no internet" or "slow
connection" ticket.

## What it checks
- **Connectivity** — pings reliable external hosts (Google DNS, Cloudflare)
- **DNS resolution** — confirms hostnames resolve correctly
- **Local network info** — reports hostname and local IP address
- **Summary report** — pass/fail overview so you can immediately see
  whether the issue is DNS, connectivity, or local configuration

## Why I built this
While troubleshooting connectivity issues, I found myself running the same
few manual checks (ping, nslookup, ipconfig) every time. This script
automates that first-pass triage into a single command, and prints a clear
summary of what's working and what isn't — useful for quickly narrowing
down whether a problem is local, DNS-related, or a broader connectivity
issue.

## Usage
```bash
python net_diagnose.py
```

## Example output
```
==================================================
NETWORK DIAGNOSTICS TOOL
==================================================
  Host      : DESKTOP-XXXX
  Local IP  : 192.168.1.14
  OS        : Windows 10

==================================================
CONNECTIVITY CHECK
==================================================
  Google DNS (8.8.8.8)           -> REACHABLE
  Cloudflare (1.1.1.1)           -> REACHABLE

==================================================
DNS RESOLUTION CHECK
==================================================
  www.google.com                 -> resolved to 142.250.xx.xx (12.3 ms)
  github.com                     -> resolved to 140.82.xx.xx (15.1 ms)

==================================================
SUMMARY
==================================================
  [OK] Ping 8.8.8.8 (Google DNS)
  [OK] Ping 1.1.1.1 (Cloudflare)
  [OK] DNS: google.com
  [OK] DNS: github.com

  All checks passed — connectivity looks healthy.
```

## Requirements
- Python 3.x (no external libraries — uses only the standard library)

## Possible next steps
- Add traceroute output for failed connectivity checks
- Export results to a log file for ticket documentation
- Add a Wi-Fi signal strength check
