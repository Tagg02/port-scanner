#!/usr/bin/env python3
"""
Simple TCP port scanner (educational).
Only scan systems you own or have explicit permission to test.
"""

from __future__ import annotations
import argparse


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

    # validate
    valid: list[int] = []
    for p in sorted(ports):
        if 1 <= p <= 65535:
            valid.append(p)
        else:
            raise ValueError(f"Invalid port: {p} (must be 1-65535)")
    if not valid:
        raise ValueError("No ports provided")
    return valid


def main() -> None:
    args = parse_args()
    try:
        ports = parse_ports(args.ports)
    except ValueError as e:
        raise SystemExit(f"Error: {e}")

    print(f"Target:  {args.target}")
    print(f"Ports:   {ports[0]}..{ports[-1]} ({len(ports)} total)")
    print(f"Timeout: {args.timeout}s")


if __name__ == "__main__":
    main()
