# Mesh Chat — kit sin hardware

Escucha la red **Meshtastic** mundial y **chatea en grupo** con tus compañeros,
todo por software (sin radios LoRa), usando el mismo formato cifrado que los
nodos reales.

Dos herramientas:

| Script | Qué hace |
|--------|----------|
| `mesh_chat.py`  | Chat de grupo: envías y recibes mensajes cifrados con quien comparta el canal + la clave. |
| `mesh_listen.py`| Escucha **solo lectura** del tráfico real de la red mundial vía el broker público. |

---

## 🚀 Unirse al chat en 4 pasos

### 1. Clona e instala

```bash
git clone <URL-DEL-REPO> mesh-chat
cd mesh-chat
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> Necesitas **Python 3.9+**. En Mac: `brew install python`.

### 2. Consigue la dirección del broker

Para chatear, **todos se conectan al mismo broker MQTT**. Una persona lo hospeda
(ver [Hospedar el broker](#-hospedar-el-broker)) y comparte su **IP**. Si sois
todos en la misma máquina de pruebas, el broker es `127.0.0.1`.

### 3. Entra al chat

```bash
MESH_BROKER=<IP-DEL-BROKER> python3 mesh_chat.py "TuNombre"
```

Ejemplo en tu propia máquina:

```bash
MESH_BROKER=127.0.0.1 python3 mesh_chat.py "Irwing"
```

### 4. ¡Chatea!

Escribe y pulsa **Enter** para enviar. Los mensajes de los demás aparecen solos.
**Ctrl+C** para salir.

```
✅ Conectado como Irwing (!0fda20e5) en canal 'KimeDemo'.
   Escribe un mensaje y pulsa Enter. Ctrl+C para salir.

> hola a todos 👋
[10:32:04] !77a1b2c3: ¡hola Irwing!
> 
```

---

## 📡 Hospedar el broker

El chat necesita **un** broker MQTT que todos alcancen. **Una** persona lo corre y
comparte su IP; los demás la ponen en `MESH_BROKER`.

```bash
brew install mosquitto      # una vez

# En tu red local (LAN) — los demás usan tu IP:
./start-broker.sh --lan

# Solo en esta máquina (para probar con 2 terminales):
./start-broker.sh
```

Deja esa terminal abierta (muestra el log del broker). **Ctrl+C** lo apaga.

- **Misma oficina / WiFi:** `--lan` basta; comparte la IP que imprime el script.
- **Gente remota (internet):** hospeda el broker en un VPS con IP pública (mismo
  `mosquitto -c mosquitto.conf` con `listener 1883 0.0.0.0`). Para uso serio,
  añade usuario/contraseña y TLS — hoy va **anónimo**, pensado para demos.

> ℹ️ **¿Por qué no el broker público de Meshtastic?** `mqtt.meshtastic.org` sirve
> para *escuchar* la red mundial, pero **no reenvía** mensajes inyectados en
> canales propios (está para puentear nodos reales). Para chatear entre ustedes
> necesitan su propio broker.

---

## 👂 Escuchar la red mundial (opcional)

Sin configurar nada, mira tráfico **real** de nodos Meshtastic de todo el mundo:

```bash
source venv/bin/activate
python3 mesh_listen.py        # todo el mundo (mucho tráfico)
python3 mesh_listen.py MX     # solo región MX
python3 mesh_listen.py US     # solo región US
```

Cada línea es un paquete real que un nodo LoRa emitió y un gateway subió a MQTT.
**Ctrl+C** muestra un resumen.

---

## ⚙️ Configuración del grupo

Lo que forma "el grupo" son dos cosas que **todos deben compartir**: el nombre de
**canal** y la **clave**. Están al inicio de `mesh_chat.py` y se pueden sobrescribir
por variables de entorno:

| Variable | Por defecto | Qué es |
|----------|-------------|--------|
| `MESH_BROKER`  | `mqtt.meshtastic.org` | IP/host del broker MQTT |
| `MESH_PORT`    | `1883` | Puerto del broker |
| `MESH_REGION`  | `MX` | Segmento de región del topic |
| `MESH_CHANNEL` | `KimeDemo` | Nombre del canal (grupo) |
| `MESH_KEY`     | *(clave del repo)* | Clave AES de 16 bytes en hex |

**Para crear tu propio grupo privado**, genera una clave nueva y repártela solo a
quien quieras que entre:

```bash
python3 -c "import os; print(os.urandom(16).hex())"
```

Cámbiala en `mesh_chat.py` (`MESH_KEY`) o pásala por entorno a todos:

```bash
export MESH_CHANNEL="MiEquipo"
export MESH_KEY="tu_clave_de_32_hex"
```

---

## 🔒 Seguridad (léelo)

- Los mensajes van **cifrados** (AES-CTR). Sin la clave correcta, el broker y
  cualquier tercero solo ven ruido.
- **La clave que viene en este repo es pública** (está en el código): sirve para la
  demo, **no para nada confidencial**. Para un grupo real, genera tu propia clave y
  compártela por un canal seguro, fuera del repositorio.
- El broker de ejemplo va **sin autenticación**. Para producción: usuario/contraseña
  y TLS en `mosquitto.conf`.
- Tu `node ID` (`!a1b2c3d4`) se deriva de tu nombre; no lleva datos personales.

---

## 🧩 Solución de problemas

| Síntoma | Causa / arreglo |
|---------|-----------------|
| `ConnectionRefusedError: [Errno 61]` | No hay broker escuchando. Arranca `./start-broker.sh` y usa la IP correcta en `MESH_BROKER`. |
| No veo mensajes de otros | ¿Todos con el **mismo** `MESH_CHANNEL` y `MESH_KEY`? ¿Todos apuntando al **mismo** broker? |
| No salen líneas en `mesh_listen.py` | La región puede tener poco tráfico; prueba sin filtro o con `US`. |
| `mosquitto: command not found` | `brew install mosquitto`, o usa `./start-broker.sh` (busca el binario solo). |
| Puerto 1883 bloqueado | Usa otra red (p. ej. hotspot del celular) o cambia el puerto con `MESH_PORT`. |

---

## 📂 Estructura del repo

```
mesh-chat/
├── mesh_chat.py       # cliente de chat (enviar + recibir)
├── mesh_listen.py     # escucha de solo lectura de la red mundial
├── mosquitto.conf     # config del broker local
├── start-broker.sh    # arranca el broker (encuentra mosquitto solo)
├── requirements.txt   # dependencias de Python
└── README.md
```

## 🔗 Recursos

- Mapa mundial en vivo: https://meshtastic.liamcottle.net
- Web client oficial: https://client.meshtastic.org
- Docs: https://meshtastic.org/docs · Discord: https://discord.gg/meshtastic
