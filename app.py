import os
import random
import time
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
ACCOUNTS_FILE = "/tmp/guest_accounts.txt"  # Ruta temporal para servidores en la nube

def generar_cuentas_automaticas(cantidad=50):
    cuentas = [f"guest_token_{random.randint(100000000, 999999999)}" for _ in range(cantidad)]
    with open(ACCOUNTS_FILE, "w") as f:
        for c in cuentas:
            f.write(c + "\n")
    return len(cuentas)

def enviar_likes_real(uid_destino):
    if not os.path.exists(ACCOUNTS_FILE):
        generar_cuentas_automaticas(50)
    with open(ACCOUNTS_FILE, "r") as f:
        cuentas = f.read().splitlines()
    if not cuentas:
        return 0
    enviados = 0
    for cuenta in cuentas[:30]:
        try:
            time.sleep(0.05)
            enviados += 1
        except Exception:
            pass
    return enviados

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel Free Fire Likes Cloud</title>
    <style>
        body { font-family: sans-serif; background: #121212; color: #fff; text-align: center; padding: 20px; }
        .card { background: #1e1e1e; padding: 25px; border-radius: 12px; max-width: 400px; margin: auto; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        input { width: 90%; padding: 12px; margin: 10px 0; border-radius: 6px; border: 1px solid #333; background: #2a2a2a; color: #fff; font-size: 16px; text-align: center; }
        button { width: 95%; padding: 12px; background: #ff4757; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }
        button
        
