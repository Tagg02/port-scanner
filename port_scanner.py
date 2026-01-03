#!/usr/bin/env python3
"""
Simple TCP port scanner (educational).
Only scan systems you own or have explicit permission to test.
"""

from __future__ import annotations
import argparse
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


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
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=150,
        help="Number of threads (default: 150)",
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


def scan_port(target: str, port: int, timeout: float) -> tuple[int, bool]:
    """Return (port, is_open)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            ok = s.connect_ex((target, port)) == 0
            return port, ok
        except socket.gaierror:
            raise SystemExit("Error: Could not resolve target hostname")
        except OSError:
            return port, False


def main() -> None:
    args = parse_args()
    try:
        ports = parse_ports(args.ports)
    except ValueError as e:
        raise SystemExit(f"Error: {e}")

    if args.workers < 1 or args.workers > 2000:
        raise SystemExit("Error: workers must be between 1 and 2000")

    print("TCP Port Scanner (permission-only)")
    print(f"Target:   {args.target}")
    print(f"Ports:    {ports[0]}..{ports[-1]} ({len(ports)} total)")
    print(f"Timeout:  {args.timeout}s")
    print(f"Workers:  {args.workers}")
    print("-" * 40)

    start = time.time()
    open_ports: list[int] = []

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = [ex.submit(scan_port, args.target, p, args.timeout) for p in ports]
        for fut in as_completed(futures):
            port, is_open = fut.result()
            if is_open:
                open_ports.append(port)
                print(f"[OPEN] {port}")

    open_ports.sort()
    elapsed = time.time() - start

    print("-" * 40)
    if open_ports:
        print(f"Open ports: {', '.join(map(str, open_ports))}")
    else:
        print("No open ports found in the selected range.")
    print(f"Scan time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
