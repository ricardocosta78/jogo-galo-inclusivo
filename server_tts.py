"""
╔══════════════════════════════════════════════════════════════════╗
║  Jogo do Galo – Servidor TTS  (Microsoft Neural PT-PT)          ║
║  Usa edge-tts para vozes Microsoft Fernanda / Raquel Neural     ║
╠══════════════════════════════════════════════════════════════════╣
║  Instalação:                                                     ║
║    pip install flask edge-tts                                    ║
║                                                                  ║
║  Execução:                                                       ║
║    python server_tts.py                                          ║
║    → Abre http://localhost:5050 no Microsoft Edge               ║
╚══════════════════════════════════════════════════════════════════╝
"""

import asyncio
import io
import os
import threading
import webbrowser
from pathlib import Path

from flask import Flask, jsonify, request, send_file, send_from_directory

# ── Tenta importar edge-tts ──────────────────────────────────────
try:
    import edge_tts
    EDGE_TTS_OK = True
except ImportError:
    EDGE_TTS_OK = False
    print("[AVISO] edge-tts não instalado. Execute:  pip install edge-tts")
    print("        O servidor arranca na mesma, mas sem voz neural.")

app = Flask(__name__)

# ── CORS: permite pedidos de qualquer origem (file:// incluído) ──
@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route("/api/tts",    methods=["OPTIONS"])
@app.route("/api/status", methods=["OPTIONS"])
@app.route("/api/voices", methods=["OPTIONS"])
def cors_preflight():
    return "", 204

# ── Configuração de voz ──────────────────────────────────────────
# Preferências: Raquel > Fernanda > Helia > Duarte
VOICE_PREFS = [
    "pt-PT-RaquelNeural",     # Voz neural feminina – padrão
    "pt-PT-FernandaNeural",   # Alternativa feminina neural
    "pt-PT-HeliaNeural",      # Edge v3
    "pt-PT-DuarteNeural",     # Masculino
]

SELECTED_VOICE = VOICE_PREFS[0]   # padrão; pode ser alterado via /api/voices

# Diretório do HTML
BASE_DIR = Path(__file__).parent


# ═══════════════════════════════════════════════════════════════════
#  ROTAS
# ═══════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    """Serve o ficheiro HTML principal."""
    html_path = BASE_DIR / "index.html"
    if not html_path.exists():
        return "Ficheiro index.html não encontrado.", 404
    return send_from_directory(str(BASE_DIR), "index.html")


@app.route("/api/tts", methods=["POST"])
def tts():
    """
    POST /api/tts
    Body JSON: { "text": "...", "voice": "pt-PT-FernandaNeural" }
    Devolve: audio/mpeg (MP3)
    """
    if not EDGE_TTS_OK:
        return jsonify({"error": "edge-tts não instalado"}), 503

    data  = request.get_json(force=True)
    text  = data.get("text", "").strip()
    voice = data.get("voice", SELECTED_VOICE)

    if not text:
        return jsonify({"error": "texto vazio"}), 400

    try:
        audio_bytes = asyncio.run(_generate_audio(text, voice))
        return send_file(
            io.BytesIO(audio_bytes),
            mimetype="audio/mpeg",
            as_attachment=False,
        )
    except Exception as e:
        print(f"[TTS ERRO] {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/voices", methods=["GET"])
def list_voices():
    """Lista vozes pt-PT disponíveis no edge-tts."""
    if not EDGE_TTS_OK:
        return jsonify({"error": "edge-tts não instalado", "voices": []})

    voices = asyncio.run(_get_pt_voices())
    return jsonify({"voices": voices, "current": SELECTED_VOICE})


@app.route("/api/voice", methods=["POST"])
def set_voice():
    """Altera a voz ativa. Body: { "voice": "pt-PT-FernandaNeural" }"""
    global SELECTED_VOICE
    data  = request.get_json(force=True)
    voice = data.get("voice", "")
    if voice:
        SELECTED_VOICE = voice
        return jsonify({"ok": True, "voice": SELECTED_VOICE})
    return jsonify({"error": "voz inválida"}), 400


@app.route("/api/status", methods=["GET"])
def status():
    """Estado do servidor."""
    return jsonify({
        "edge_tts": EDGE_TTS_OK,
        "voice": SELECTED_VOICE,
        "prefs": VOICE_PREFS,
    })


# ═══════════════════════════════════════════════════════════════════
#  HELPERS ASYNC
# ═══════════════════════════════════════════════════════════════════

async def _generate_audio(text: str, voice: str) -> bytes:
    """Gera áudio MP3 com edge-tts e devolve bytes."""
    communicate = edge_tts.Communicate(text, voice, rate="-18%", volume="+0%")
    buf = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    return buf.getvalue()


async def _get_pt_voices() -> list:
    """Devolve lista de vozes PT disponíveis."""
    all_voices = await edge_tts.list_voices()
    return [
        {"name": v["ShortName"], "gender": v["Gender"], "locale": v["Locale"]}
        for v in all_voices
        if v["Locale"].startswith("pt-PT")
    ]


# ═══════════════════════════════════════════════════════════════════
#  ARRANQUE
# ═══════════════════════════════════════════════════════════════════

def open_browser():
    """Abre o Edge/browser após 1 segundo."""
    import time
    time.sleep(1.2)
    # Tenta Microsoft Edge primeiro
    try:
        edge = webbrowser.get("windows-default")
        edge.open("http://localhost:5050")
    except Exception:
        webbrowser.open("http://localhost:5050")


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 5050

    print("=" * 62)
    print("  Jogo do Galo Acessível – Servidor TTS Neural")
    print("=" * 62)
    print(f"  URL:   http://{HOST}:{PORT}")
    print(f"  Voz:   {SELECTED_VOICE}")
    print(f"  TTS:   {'edge-tts OK ✓' if EDGE_TTS_OK else 'edge-tts NÃO instalado ✗'}")
    print()
    if not EDGE_TTS_OK:
        print("  INSTALAR:  pip install edge-tts flask")
        print()
    print("  Prima  Ctrl+C  para parar o servidor.")
    print("=" * 62)

    # Abre o browser automaticamente
    threading.Thread(target=open_browser, daemon=True).start()

    app.run(host=HOST, port=PORT, debug=False)
