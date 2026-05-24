from flask import Flask, request, send_file, jsonify
import edge_tts
import asyncio
import uuid
import os

app = Flask(__name__)

AUDIO_FOLDER = "audios"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

async def generar_audio(texto, voz, archivo):
    tts = edge_tts.Communicate(
        text=texto,
        voice=voz,
        rate="-5%",
        pitch="-10Hz"
    )
    await tts.save(archivo)

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/style.css")
def css():
    return send_file("style.css")

@app.route("/script.js")
def js():
    return send_file("script.js")

@app.route("/convertir", methods=["POST"])
def convertir():
    data = request.json
    texto = data.get("texto", "")
    voz = data.get("voz", "es-ES-AlvaroNeural")

    if not texto.strip():
        return jsonify({"error": "Escribe un texto"}), 400

    nombre = f"{uuid.uuid4()}.mp3"
    ruta = os.path.join(AUDIO_FOLDER, nombre)

    asyncio.run(generar_audio(texto, voz, ruta))

    return send_file(ruta, as_attachment=True, download_name="voz.mp3")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)