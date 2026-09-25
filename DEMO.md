# 🎤 Guión de demo — copiar y pegar por slide

Comandos listos para pegar durante la presentación. Cada bloque = un momento.
Presenta desde la carpeta del proyecto con el `venv` activado.

> **Antes de nada, en cada terminal nueva:**
> ```bash
> cd ~/Desktop/workspace/meshtastic
> source venv/bin/activate
> ```
> En Windows: `venv\Scripts\activate` y usa `python` en vez de `python3`.

---

## ✅ Pre-vuelo (hazlo ANTES de presentar, en privado)

Que no te falle nada en vivo: instala dependencias y comprueba que hay señal.

```bash
cd ~/Desktop/workspace/meshtastic
source venv/bin/activate
pip install -r requirements.txt
```

Prueba rápida de que llega tráfico real (déjalo 10 s y corta con Ctrl+C):

```bash
python3 mesh_listen.py MX
```

Si ves líneas con 📍/🔋/🌡️, estás listo. **Ctrl+C** para cortar.

---

## 🛰️ Slide 1 — "Esto es tráfico REAL de la red mundial"

🎤 *"Cada línea es un paquete que un radio LoRa físico emitió ahora mismo, en algún*
*lugar de México, y que llegó por la red mesh sin internet ni SIM."*

```bash
python3 mesh_listen.py MX
```

Deja correr unos segundos. Señala una posición 📍 o una telemetría 🌡️.
**Ctrl+C** muestra el resumen y cierra.

---

## 💬 Slide 2 — "Nosotros podemos chatear igual, sin hardware"

Chat de grupo en dos terminales. **No hace falta montar nada** (usa un broker
público gratis; los mensajes van cifrados).

**Terminal 1:**
```bash
python3 mesh_chat.py "Irwing"
```

**Terminal 2** (otra ventana):
```bash
python3 mesh_chat.py "Ana"
```

🎤 Escribe en una, aparece en la otra. *"Mismo formato que los radios reales, pero*
*por software y cifrado extremo a extremo."* **Ctrl+C** en cada una para salir.

> 💡 Si el WiFi del lugar es inestable, usa un broker local (más fiable en vivo):
> abre una 3.ª terminal con `./start-broker.sh` y en las otras dos antepon
> `MESH_BROKER=127.0.0.1` al comando.

---

## 🔒 Slide 3 — "Está cifrado: sin la clave, es ruido"

🎤 *"El broker y cualquier tercero solo ven texto cifrado. Solo quien tiene la clave*
*del grupo lee los mensajes."* Muestra la clave del grupo en el código:

```bash
grep -n "MESH_KEY" mesh_chat.py
```

(Opcional) Enseña que un oyente de la red mundial NO puede leer estos mensajes:
solo ve paquetes que no puede descifrar.

---

## 🚀 Slide 4 — "Así se une CUALQUIERA" (lo que hará tu equipo)

🎤 *"Cuatro comandos y estás dentro."*

```bash
git clone https://github.com/Irwingduran/meshtastic.git
cd meshtastic
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 mesh_chat.py "TuNombre"
```

---

## 🤖 Slide 5 — "¿No eres técnico? Que lo haga una IA"

🎤 *"Abres el repo con Claude Code o Cursor y le dices una frase."*

Muestra el archivo y la frase mágica:

```bash
open AGENTE.md          # macOS  (Windows: start AGENTE.md)
```

> Frase para la IA:
> **"Lee el archivo `AGENTE.md` y sigue las instrucciones para ayudarme a unirme al chat."**

---

## 🌐 Slide 6 — "Tres formas de conectarse, todas gratis"

🎤 Cierre con las opciones según necesidad:

| Necesitas… | Broker | Cómo |
|------------|--------|------|
| Probar rápido | Público (`broker.hivemq.com`) | Nada que instalar, ya es el default |
| Grupo privado estable | HiveMQ Cloud free | Ver `HIVEMQ.md` (usuario/contraseña + TLS) |
| Control total / sin internet | Tu propio `mosquitto` | `./start-broker.sh` |

Repo: **https://github.com/Irwingduran/meshtastic**

---

## 🧯 Si algo falla en vivo

| Síntoma | Arreglo rápido |
|---------|----------------|
| `ConnectionRefusedError` | Broker local caído/no arrancado, o sin internet. Usa el broker público (quita `MESH_BROKER`). |
| El listener no muestra nada | Usa filtro de región (`MX`), nunca el modo mundial (`msh/#`) que el broker corta. |
| No se ven los mensajes entre terminales | Confirma que las dos usan el mismo broker (ambas sin `MESH_BROKER`, o ambas con la misma IP). |
| Emojis raros en Windows | Ya está resuelto en el código; usa Windows Terminal si puedes. |
