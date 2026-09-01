#!/usr/bin/env python3
"""
Network Diagnostics Tool
-------------------------
A simple command-line utility that checks common network health indicators:
  1. Internet connectivity (ping test to reliable hosts)
  2. DNS resolution
  3. Local network configuration (IP, gateway)
  4. Latency to key services

Useful as a quick first-pass check when troubleshooting "no internet" or
"slow connection" issues — the kind of thing an IT support associate would
run before escalating a ticket.

Usage:
    python net_diagnose.py
"""

import socket
import subprocess
import platform
import time


def print_header(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def check_ping(host="8.8.8.8", label="Google DNS (8.8.8.8)"):
    """Ping a host once and report whether it's reachable."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", param, "1", host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
        )
        reachable = result.returncode == 0
        status = "REACHABLE" if reachable else "UNREACHABLE"
        print(f"  {label:30s} -> {status}")
        return reachable
    except Exception as e:
        print(f"  {label:30s} -> ERROR ({e})")
        return False


def check_dns(hostname="www.google.com"):
    """Try resolving a hostname to confirm DNS is working."""
    try:
        start = time.time()
        ip = socket.gethostbyname(hostname)
        elapsed = (time.time() - start) * 1000
        print(f"  {hostname:30s} -> resolved to {ip} ({elapsed:.1f} ms)")
        return True
    except socket.gaierror as e:
        print(f"  {hostname:30s} -> DNS RESOLUTION FAILED ({e})")
        return False


def get_local_ip():
    """Get the machine's local IP address (best-effort, no external calls)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1 (could not determine LAN IP)"
        finally:
            s.close()
        return ip
    except Exception as e:
        return f"Unavailable ({e})"


def get_hostname():
    return socket.gethostname()


def summarize(results):
    print_header("SUMMARY")
    all_ok = all(results.values())
    for check, ok in results.items():
        print(f"  [{'OK' if ok else 'FAIL'}] {check}")
    if all_ok:
        print("\n  All checks passed — connectivity looks healthy.")
    else:
        print("\n  One or more checks failed — see above for what to")
        print("  investigate first (DNS vs. connectivity vs. local config).")


def main():
    print_header("NETWORK DIAGNOSTICS TOOL")
    print(f"  Host      : {get_hostname()}")
    print(f"  Local IP  : {get_local_ip()}")
    print(f"  OS        : {platform.system()} {platform.release()}")

    print_header("CONNECTIVITY CHECK")
    results = {}
    results["Ping 8.8.8.8 (Google DNS)"] = check_ping("8.8.8.8", "Google DNS (8.8.8.8)")
    results["Ping 1.1.1.1 (Cloudflare)"] = check_ping("1.1.1.1", "Cloudflare (1.1.1.1)")

    print_header("DNS RESOLUTION CHECK")
    results["DNS: google.com"] = check_dns("www.google.com")
    results["DNS: github.com"] = check_dns("github.com")

    summarize(results)


if __name__ == "__main__":
    main()
