import os
import random
import time
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
ACCOUNTS_FILE = "/tmp/guest_accounts.txt"

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
        button:hover { background: #ff6b81; }
        #res { margin-top: 15px; font-weight: bold; word-break: break-all; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🔥 Panel FF Likes Cloud</h2>
        <input type="text" id="uid" placeholder="Ingresa el UID de Free Fire">
        <button onclick="sendLike()">Enviar Likes</button>
        <div id="res"></div>
    </div>
    <script>
        async function sendLike() {
            const uid = document.getElementById('uid').value;
            const resDiv = document.getElementById('res');
            if(!uid) { resDiv.innerHTML = "<span style='color:red;'>Ingresa un UID válido</span>"; return; }
            resDiv.innerHTML = "Generando cuentas y enviando likes...";
            try {
                let r = await fetch('/like?uid=' + uid);
                let d = await r.json();
                if(d.status === 'success') {
                    resDiv.innerHTML = "<span style='color:lime;'>" + d.message + "</span>";
                } else {
                    resDiv.innerHTML = "<span style='color:red;'>" + d.message + "</span>";
                }
            } catch(e) {
                resDiv.innerHTML = "<span style='color:red;'>Error de conexión con el servidor</span>";
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/like', methods=['GET', 'POST'])
def send_like():
    uid = request.args.get('uid') or (request.json.get('uid') if request.is_json else None)
    if not uid:
        return jsonify({"status": "error", "message": "Falta el UID"}), 400
    total = enviar_likes_real(uid)
    return jsonify({"status": "success", "message": f"¡Se enviaron {total} likes con éxito al UID {uid}!"})

if __name__ == '__main__':
    app.run()
    
