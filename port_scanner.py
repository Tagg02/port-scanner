#!/usr/bin/env python3
"""
Simple TCP port scanner (educational).
Only scan systems you own or have explicit permission to test.
"""

from __future__ import annotations
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="TCP port scanner (permission-only)."
    )
    parser.add_argument("target", help="Target hostname or IP address")
    parser.add_argument(
        "-p", "--ports",
        default="1-1024",
        help="Port range (e.g. 1-1024) or comma list (e.g. 22,80,443). Default: 1-1024"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=0.6,
        help="Socket timeout in seconds (default: 0.6)"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"Target: {args.target}")
    print(f"Ports:  {args.ports}")
    print(f"Timeout:{args.timeout}s")


if __name__ == "__main__":
    main()
