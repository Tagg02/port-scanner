#!/usr/bin/env python3
"""
Simple TCP port scanner (educational).
Only scan systems you own or have explicit permission to test.
"""

from __future__ import annotations
import argparse
import socket
import time


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TCP port scanner (permission-only).")
    parser.add_argument("target", help="Target hostname or IP address")
    parser.add_argument(
        "-p", "--ports",
        default="1-1024",
        help="Port range (e.g. 1-1024) or comma list (e.g. 22,80,443). Default: 1-1024",
    )
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=0.6,
        help="Socket timeout in seconds (default: 0.6)",
    )
    return parser.parse_args()


def parse_ports(spec: str) -> list[int]:
    spec = spec.strip()
    ports: set[int] = set()

    if "-" in spec and "," not in spec:
        start_s, end_s = spec.split("-", 1)
        start, end = int(start_s), int(end_s)
        if start > end:
            start, end = end, start
        for p in range(start, end + 1):
            ports.add(p)
    else:
        parts = [p.strip() for p in spec.split(",") if p.strip()]
        for part in parts:
            ports.add(int(part))

    valid: list[int] = []
    for p in sorted(ports):
        if 1 <= p <= 65535:
            valid.append(p)
        else:
            raise ValueError(f"Invalid port: {p} (must be 1-65535)")
    if not valid:
        raise ValueError("No ports provided")
    return valid


def scan_port(target: str, port: int, timeout: float) -> bool:
    """Return True if TCP connect succeeds (port likely open)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            return s.connect_ex((target, port)) == 0
        except socket.gaierror:
            raise SystemExit("Error: Could not resolve target hostname")
        except OSError:
            return False


def main() -> None:
    args = parse_args()
    try:
        ports = parse_ports(args.ports)
    except ValueError as e:
        raise SystemExit(f"Error: {e}")

    print("TCP Port Scanner (permission-only)")
    print(f"Target:  {args.target}")
    print(f"Ports:   {ports[0]}..{ports[-1]} ({len(ports)} total)")
    print(f"Timeout: {args.timeout}s")
    print("-" * 40)

    start = time.time()
    open_ports: list[int] = []

    for p in ports:
        if scan_port(args.target, p, args.timeout):
            open_ports.append(p)
            print(f"[OPEN] {p}")

    elapsed = time.time() - start
    print("-" * 40)
    if open_ports:
        print(f"Open ports: {', '.join(map(str, open_ports))}")
    else:
        print("No open ports found in the selected range.")
    print(f"Scan time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
