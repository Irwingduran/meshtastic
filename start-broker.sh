#!/usr/bin/env bash
# Arranca el broker MQTT local para el chat.
#
#   ./start-broker.sh          # solo esta máquina (127.0.0.1)
#   ./start-broker.sh --lan    # abierto a tu red local (0.0.0.0) para que otros entren
#
# Déjalo corriendo en su propia terminal. Ctrl+C para apagarlo.
set -euo pipefail
cd "$(dirname "$0")"

# Encuentra el binario de mosquitto (PATH, Homebrew ARM o Intel)
MOSQ=""
for c in mosquitto /opt/homebrew/opt/mosquitto/sbin/mosquitto /usr/local/opt/mosquitto/sbin/mosquitto /usr/sbin/mosquitto; do
  if command -v "$c" >/dev/null 2>&1 || [ -x "$c" ]; then MOSQ="$c"; break; fi
done
if [ -z "$MOSQ" ]; then
  echo "❌ No encontré 'mosquitto'. Instálalo con:  brew install mosquitto" >&2
  exit 1
fi

CONF="mosquitto.conf"
if [ "${1:-}" = "--lan" ]; then
  # Config temporal abierta a la LAN
  CONF="$(mktemp -t mosq-lan.XXXX.conf)"
  printf 'listener 1883 0.0.0.0\nallow_anonymous true\n' > "$CONF"
  IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "<tu-IP>")
  echo "🌐 Broker abierto a la red. Que los demás usen:  MESH_BROKER=$IP python3 mesh_chat.py \"Nombre\""
fi

echo "📡 Iniciando broker con $MOSQ ($CONF)…  (Ctrl+C para salir)"
exec "$MOSQ" -c "$CONF"
