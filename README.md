# Mesh Chat — kit sin hardware

Escucha la red **Meshtastic** mundial y **chatea en grupo** con tus compañeros,
todo por software (sin radios LoRa), usando el mismo formato cifrado que los
nodos reales.

> 🤖 **¿No eres técnico?** Abre [`AGENTE.md`](AGENTE.md): está escrito para que un
> asistente de IA (Claude Code, Cursor…) haga todo el setup por ti. Solo tienes que
> decirle _"lee AGENTE.md y ayúdame a unirme al chat"_.
>
> 🎤 **¿Vas a presentarlo?** En [`DEMO.md`](DEMO.md) tienes un guión con los comandos
> listos para copiar y pegar, uno por slide.

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

### 2. Entra al chat (¡sin montar nada!)

Por defecto el chat usa un **broker MQTT público gratuito** (`broker.hivemq.com`),
así que **no necesitas hospedar ningún servidor**. Solo corre:

```bash
python3 mesh_chat.py "TuNombre"
```

> 🔒 Tus mensajes van **cifrados** con la clave del grupo. El broker público y
> cualquier otro solo ven **texto cifrado**; únicamente quien tenga tu `MESH_KEY`
> puede leerlos.

*(Opcional)* Si prefieres tu propio broker (más privado, ver
[Hospedar tu propio broker](#-opcional-hospedar-tu-propio-broker)):

```bash
MESH_BROKER=127.0.0.1 python3 mesh_chat.py "Irwing"
```

*(Opcional)* Para un **grupo privado gratis con usuario/contraseña + TLS**, mira
[`HIVEMQ.md`](HIVEMQ.md).

> 🪟 **En Windows** funciona igual, con dos cambios: usa **`python`** (no `python3`)
> y activa el entorno con **`venv\Scripts\activate`**. El camino normal (broker
> público) no necesita variables de entorno: solo `python mesh_chat.py "TuNombre"`.
> Si necesitas pasar variables (broker propio o HiveMQ), la sintaxis es distinta:
> ```powershell
> # PowerShell
> $env:MESH_BROKER="127.0.0.1"; python mesh_chat.py "Ana"
> ```
> ```bat
> REM cmd.exe
> set MESH_BROKER=127.0.0.1 && python mesh_chat.py "Ana"
> ```

### 3. ¡Chatea!

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

## 📡 (Opcional) Hospedar tu propio broker

**No hace falta** para chatear: por defecto se usa el broker público gratuito. Pero
si quieres un broker propio (más privado, o para una red sin internet), **una**
persona lo corre y comparte su IP; los demás la ponen en `MESH_BROKER`.

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

> ℹ️ **Sobre los brokers.** Un broker MQTT **genérico** (como el `broker.hivemq.com`
> que usamos por defecto, o el tuyo propio) reenvía cualquier mensaje: sirve para el
> chat. El broker **de Meshtastic** (`mqtt.meshtastic.org`) es especial —
> **no reenvía** mensajes inyectados en canales propios (solo puentea nodos reales),
> así que sirve para *escuchar* la red mundial pero no para chatear entre ustedes.

---

## 👂 Escuchar la red mundial (opcional)

Sin configurar nada, mira tráfico **real** de nodos Meshtastic de todo el mundo:

```bash
source venv/bin/activate
python3 mesh_listen.py MX     # solo región MX (recomendado)
python3 mesh_listen.py US     # solo región US
python3 mesh_listen.py        # todo el mundo (ver nota)
```

Cada línea es un paquete real que un nodo LoRa emitió y un gateway subió a MQTT.
**Ctrl+C** muestra un resumen.

> ⚠️ **Usa siempre un filtro de región** (`MX`, `US`, …). El modo "todo el mundo"
> (`msh/#`) suele hacer que el broker público de Meshtastic **corte la conexión**
> por ser una suscripción demasiado amplia (se queda reconectando sin recibir nada).

---

## ⚙️ Configuración del grupo

Lo que forma "el grupo" son dos cosas que **todos deben compartir**: el nombre de
**canal** y la **clave**. Están al inicio de `mesh_chat.py` y se pueden sobrescribir
por variables de entorno:

| Variable | Por defecto | Qué es |
|----------|-------------|--------|
| `MESH_BROKER`  | `broker.hivemq.com` | IP/host del broker MQTT (público gratis por defecto) |
| `MESH_PORT`    | `1883` | Puerto del broker (`8883` con TLS) |
| `MESH_REGION`  | `MX` | Segmento de región del topic |
| `MESH_CHANNEL` | `KimeDemo` | Nombre del canal (grupo) |
| `MESH_KEY`     | *(clave del repo)* | Clave AES de 16 bytes en hex |
| `MESH_USER`    | *(vacío)* | Usuario del broker (p. ej. HiveMQ Cloud) |
| `MESH_PASS`    | *(vacío)* | Contraseña del broker |
| `MESH_TLS`     | *(off)* | `1` para conexión cifrada TLS (HiveMQ Cloud) |

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
