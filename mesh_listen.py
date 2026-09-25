#!/usr/bin/env python3
"""
mesh_listen.py — Escucha tráfico REAL de la red Meshtastic mundial vía el
broker MQTT público y decodifica los paquetes del canal por defecto.

Instalación (Mac, ~1 min):
    python3 -m pip install --user paho-mqtt meshtastic cryptography

Uso:
    python3 mesh_listen.py            # todo el mundo
    python3 mesh_listen.py MX         # solo nodos que suben con región MX
    python3 mesh_listen.py US         # etc.

Ctrl+C para salir.
"""
import sys
from datetime import datetime

import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from meshtastic.protobuf import mesh_pb2, mqtt_pb2, portnums_pb2, telemetry_pb2

BROKER = "mqtt.meshtastic.org"
PORT = 1883
USER, PASSWORD = "meshdev", "large4cats"

# Filtro opcional por región (segmento del topic: msh/<REGION>/...)
REGION = sys.argv[1].upper() if len(sys.argv) > 1 else None
TOPIC = f"msh/{REGION}/#" if REGION else "msh/#"

# Clave del canal por defecto ("AQ==" expandida a 16 bytes)
DEFAULT_KEY = bytes.fromhex("d4f1bb3a20290759f0bcffabcf4e6901")

stats = {"paquetes": 0, "texto": 0, "posicion": 0, "nodeinfo": 0, "telemetria": 0, "otros": 0}


def node_id(n: int) -> str:
    return f"!{n:08x}"


def decrypt(packet: mesh_pb2.MeshPacket) -> bytes | None:
    """AES-CTR con nonce = packet_id (8 bytes LE) + from (4 bytes LE) + 4 ceros."""
    nonce = packet.id.to_bytes(8, "little") + getattr(packet, "from").to_bytes(4, "little") + bytes(4)
    cipher = Cipher(algorithms.AES(DEFAULT_KEY), modes.CTR(nonce))
    dec = cipher.decryptor()
    return dec.update(packet.encrypted) + dec.finalize()


def describe(data: mesh_pb2.Data) -> tuple[str, str]:
    p = data.portnum
    if p == portnums_pb2.TEXT_MESSAGE_APP:
        return "texto", f'💬 "{data.payload.decode("utf-8", "replace")}"'
    if p == portnums_pb2.POSITION_APP:
        pos = mesh_pb2.Position()
        pos.ParseFromString(data.payload)
        return "posicion", f"📍 lat={pos.latitude_i / 1e7:.4f} lon={pos.longitude_i / 1e7:.4f}"
    if p == portnums_pb2.NODEINFO_APP:
        u = mesh_pb2.User()
        u.ParseFromString(data.payload)
        try:
            hw = mesh_pb2.HardwareModel.Name(u.hw_model)
        except ValueError:
            hw = str(u.hw_model)
        return "nodeinfo", f"🪪 {u.long_name!r} ({u.short_name}) hw={hw}"
    if p == portnums_pb2.TELEMETRY_APP:
        t = telemetry_pb2.Telemetry()
        t.ParseFromString(data.payload)
        if t.HasField("device_metrics"):
            d = t.device_metrics
            return "telemetria", f"🔋 bat={d.battery_level}% V={d.voltage:.2f} util={d.channel_utilization:.1f}%"
        if t.HasField("environment_metrics"):
            e = t.environment_metrics
            return "telemetria", f"🌡️ {e.temperature:.1f}°C hum={e.relative_humidity:.0f}%"
        return "telemetria", "📈 telemetría"
    try:
        return "otros", f"({portnums_pb2.PortNum.Name(p)})"
    except ValueError:
        return "otros", f"(portnum {p})"


def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"✅ Conectado a {BROKER}. Suscrito a {TOPIC}\n")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    env = mqtt_pb2.ServiceEnvelope()
    try:
        env.ParseFromString(msg.payload)
    except Exception:
        return  # JSON u otro formato: lo ignoramos
    pkt = env.packet
    if not pkt.HasField("encrypted"):
        return
    try:
        data = mesh_pb2.Data()
        data.ParseFromString(decrypt(pkt))
    except Exception:
        return  # canal con otra clave: no lo podemos leer (¡así debe ser!)
    if data.portnum == 0:
        return

    kind, text = describe(data)
    stats["paquetes"] += 1
    stats[kind] += 1

    # topic: msh/<REGION>/[<subtopic>/]2/e/<canal>/<gateway>
    parts = msg.topic.split("/")
    region = parts[1] if len(parts) > 1 else "?"
    hops_hint = f"hops={pkt.hop_start - pkt.hop_limit}/{pkt.hop_start}" if pkt.hop_start else ""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {region:<4} {node_id(getattr(pkt, 'from'))} → {node_id(pkt.to)} "
          f"vía {env.gateway_id:<10} {hops_hint:<10} {text}")


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(USER, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    print(f"Conectando a {BROKER}:{PORT} ...")
    client.connect(BROKER, PORT, 60)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n📊 Resumen:", ", ".join(f"{k}={v}" for k, v in stats.items()))


if __name__ == "__main__":
    main()
