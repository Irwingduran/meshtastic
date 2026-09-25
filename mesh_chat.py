#!/usr/bin/env python3
"""
mesh_chat.py — Chat de grupo compatible con Meshtastic sobre MQTT.

Varias personas pueden mensajearse SI comparten el mismo CANAL + la misma CLAVE.
Cada quien corre este script con su propio nombre; escribe y pulsa Enter para
enviar. Los mensajes de los demás aparecen solos.

Instalación (una vez):
    python3 -m pip install --user paho-mqtt meshtastic cryptography

Uso:
    python3 mesh_chat.py "Irwing"        # entra al chat como "Irwing"
    python3 mesh_chat.py "Ana" GDL       # nombre corto opcional (2do arg)

Para que ELLOS entren:
    1. Comparte este archivo.
    2. Que TODOS usen el MISMO CHANNEL y la MISMA KEY de abajo.
    3. Cada quien lo corre con su propio nombre.

Ctrl+C para salir.
"""
import os
import sys
import threading
from datetime import datetime

import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from meshtastic.protobuf import mesh_pb2, mqtt_pb2, portnums_pb2

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DEL GRUPO — esto es lo que "ellos" deben compartir contigo
# ─────────────────────────────────────────────────────────────────────────────
# Por defecto usamos un broker MQTT público GRATIS (sin registro, en internet).
# Como los mensajes van cifrados con la KEY del grupo, el broker solo ve ruido.
BROKER = os.environ.get("MESH_BROKER", "broker.hivemq.com")
PORT = int(os.environ.get("MESH_PORT", "1883"))
REGION = os.environ.get("MESH_REGION", "MX")      # segmento del topic

# Credenciales:
#  - Si defines MESH_USER/MESH_PASS (p. ej. para HiveMQ Cloud), se usan esas.
#  - Si no, y el broker es el de Meshtastic, se usan las públicas de Meshtastic.
#  - Si no, conexión anónima (brokers públicos como broker.hivemq.com).
if os.environ.get("MESH_USER"):
    USER, PASSWORD = os.environ["MESH_USER"], os.environ.get("MESH_PASS", "")
elif "meshtastic.org" in BROKER:
    USER, PASSWORD = "meshdev", "large4cats"
else:
    USER, PASSWORD = None, None

# TLS: actívalo con MESH_TLS=1 (obligatorio en HiveMQ Cloud, puerto 8883).
USE_TLS = os.environ.get("MESH_TLS", "").lower() in ("1", "true", "yes")

# ↓↓↓ CAMBIEN ESTO ENTRE TODOS (mismo canal + misma clave = mismo grupo privado) ↓↓↓
CHANNEL = os.environ.get("MESH_CHANNEL", "KimeDemo")
KEY = bytes.fromhex(os.environ.get("MESH_KEY", "65d237cc6194e3f9818be50b9ed6e877"))  # 16 bytes
# ↑↑↑ Genera una clave nueva con:  python3 -c "import os;print(os.urandom(16).hex())"
# ─────────────────────────────────────────────────────────────────────────────

TOPIC_SUB = f"msh/{REGION}/#"

# Identidad: node id estable derivado del nombre (para que tu "!id" no cambie)
NAME = sys.argv[1] if len(sys.argv) > 1 else f"user-{os.getpid()}"
SHORT = (sys.argv[2] if len(sys.argv) > 2 else NAME[:4]).upper()
MY_NODE = (int.from_bytes(NAME.encode(), "little") * 2654435761 & 0xFFFFFFFF) or 0x1234
MY_ID = f"!{MY_NODE:08x}"
BROADCAST = 0xFFFFFFFF


def channel_hash(name: str, key: bytes) -> int:
    """Hash de canal de Meshtastic: XOR de los bytes del nombre y de la clave."""
    h = 0
    for b in name.encode():
        h ^= b
    for b in key:
        h ^= b
    return h & 0xFF


CH_HASH = channel_hash(CHANNEL, KEY)


def crypt(payload: bytes, packet_id: int, from_node: int) -> bytes:
    """AES-CTR: cifra y descifra son la misma operación (nonce = id + from + ceros)."""
    nonce = packet_id.to_bytes(8, "little") + from_node.to_bytes(4, "little") + bytes(4)
    cipher = Cipher(algorithms.AES(KEY), modes.CTR(nonce))
    c = cipher.encryptor()
    return c.update(payload) + c.finalize()


def send(client: mqtt.Client, text: str) -> None:
    """Construye Data(texto) → cifra → MeshPacket → ServiceEnvelope → publica."""
    data = mesh_pb2.Data(portnum=portnums_pb2.TEXT_MESSAGE_APP, payload=text.encode())

    pkt = mesh_pb2.MeshPacket()
    setattr(pkt, "from", MY_NODE)          # 'from' es palabra reservada en Python
    pkt.to = BROADCAST
    pkt.id = int.from_bytes(os.urandom(4), "little") or 1
    pkt.channel = CH_HASH
    pkt.hop_limit = 3
    pkt.hop_start = 3
    pkt.encrypted = crypt(data.SerializeToString(), pkt.id, MY_NODE)

    env = mqtt_pb2.ServiceEnvelope(packet=pkt, channel_id=CHANNEL, gateway_id=MY_ID)
    topic = f"msh/{REGION}/2/e/{CHANNEL}/{MY_ID}"
    client.publish(topic, env.SerializeToString())


def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe(TOPIC_SUB)
    print(f"✅ Conectado como {NAME} ({MY_ID}) en canal '{CHANNEL}'.")
    print("   Escribe un mensaje y pulsa Enter. Ctrl+C para salir.\n")


def on_message(client, userdata, msg):
    env = mqtt_pb2.ServiceEnvelope()
    try:
        env.ParseFromString(msg.payload)
    except Exception:
        return
    pkt = env.packet
    if not pkt.HasField("encrypted"):
        return
    from_node = getattr(pkt, "from")
    if from_node == MY_NODE:
        return  # es mi propio eco
    try:
        data = mesh_pb2.Data()
        data.ParseFromString(crypt(pkt.encrypted, pkt.id, from_node))
    except Exception:
        return  # otra clave/canal: no es de nuestro grupo
    if data.portnum != portnums_pb2.TEXT_MESSAGE_APP:
        return  # solo mostramos texto en este chat
    ts = datetime.now().strftime("%H:%M:%S")
    text = data.payload.decode("utf-8", "replace")
    print(f"\r[{ts}] !{from_node:08x}: {text}\n> ", end="", flush=True)


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if USER:
        client.username_pw_set(USER, PASSWORD)
    if USE_TLS:
        client.tls_set()  # usa los certificados CA del sistema
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_start()  # red en hilo de fondo; el hilo principal lee el teclado

    try:
        while True:
            text = input("> ")
            if text.strip():
                send(client, text)
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Saliendo.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
