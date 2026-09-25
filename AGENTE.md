# 🤖 Únete al chat con ayuda de una IA

Este archivo está escrito para que **una inteligencia artificial** (un "agente")
haga por ti toda la parte técnica. Tú no necesitas saber programar.

---

## 👤 Si eres una persona (lee esto primero)

1. Instala un asistente de IA que pueda usar tu terminal. Cualquiera de estos sirve:
   - **Claude Code** (recomendado) — https://claude.com/claude-code
   - **Cursor** — https://cursor.com
   - o cualquier asistente con acceso a la terminal de tu computadora.
2. Abre esta carpeta con ese asistente.
3. Escríbele **exactamente** esto:

   > **Lee el archivo `AGENTE.md` y sigue las instrucciones para ayudarme a unirme al chat. Explícame cada paso en palabras simples y pregúntame lo que necesites.**

4. El asistente hará el resto: instalar todo, configurar y abrir el chat. Cuando te
   pregunte, respóndele con normalidad (por ejemplo tu nombre, o la dirección del
   broker que te haya pasado tu organizador).

Eso es todo. El resto de este archivo son las instrucciones para la IA. 👇

---

## 🤖 Si eres el agente de IA, sigue este runbook

**Tu objetivo:** dejar a esta persona (probablemente NO técnica) dentro del chat de
grupo `mesh_chat.py`, funcionando. Sé amable, explica cada paso en lenguaje simple,
y **pregunta antes de instalar o de cualquier acción que no sea reversible**. No
hagas `git push` ni cambies la clave del grupo salvo que te lo pidan.

### Paso 0 — Contexto
- Repositorio: `https://github.com/Irwingduran/meshtastic.git`
- El chat necesita: Python 3.9+ y las dependencias de `requirements.txt`.
- **No hace falta montar un broker:** por defecto usa uno público gratuito
  (`broker.hivemq.com`) y los mensajes van cifrados. El camino normal es solo
  instalar y ejecutar.
- Detecta el sistema operativo (macOS / Linux / Windows) y adapta los comandos.

### Paso 1 — Python
- Comprueba: `python3 --version` (debe ser 3.9 o mayor).
- Si no existe, guía la instalación:
  - macOS: `brew install python` (si no hay Homebrew: https://brew.sh)
  - Linux: `sudo apt install python3 python3-venv python3-pip` (o el gestor que aplique)
  - Windows: descarga desde https://python.org y marca "Add to PATH".

### Paso 2 — Obtener el proyecto
- Si YA estás dentro de la carpeta del repo (ves `mesh_chat.py`), continúa.
- Si no, clónalo y entra:
  ```bash
  git clone https://github.com/Irwingduran/meshtastic.git
  cd meshtastic
  ```

### Paso 3 — Entorno e instalación de dependencias
```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Verifica que no haya errores de instalación antes de seguir.

### Paso 4 — Pregunta el nombre
**¿Con qué nombre quiere aparecer en el chat?** (ej. "Ana"). Con eso basta para el
camino normal (broker público). El Paso 5 es **opcional**.

### Paso 5 — (Opcional) Broker propio
Solo si la persona quiere su **propio** broker (más privado, o red sin internet).
NO es necesario para chatear. Si lo pide:
```bash
brew install mosquitto        # macOS (una vez). Linux: sudo apt install mosquitto
./start-broker.sh --lan       # abre el broker a la red local e imprime la IP a compartir
```
- Deja ese broker corriendo en su propia terminal (Ctrl+C lo apaga).
- Que **comparta la IP que imprime el script** con los demás, y todos usen
  `MESH_BROKER=<esa-IP>`.

### Paso 6 — Entrar al chat
En una terminal con el `venv` activado. **Camino normal (broker público, gratis):**
```bash
python3 mesh_chat.py "<NOMBRE>"
```
Si usan un broker propio, antepongan su dirección:
```bash
MESH_BROKER=<IP-DEL-BROKER> python3 mesh_chat.py "<NOMBRE>"
```

### Paso 7 — Explícale cómo usarlo
Dile, en palabras simples:
- "Escribe tu mensaje y pulsa **Enter** para enviarlo."
- "Los mensajes de los demás aparecen solos."
- "Para salir, pulsa **Ctrl+C**."

### Solución de problemas (para ti, el agente)
| Síntoma | Qué hacer |
|---------|-----------|
| `ConnectionRefusedError: [Errno 61]` | Con broker público: revisa la conexión a internet (o el puerto 1883 bloqueado en su red — probar hotspot). Con broker propio: confirma la IP o móntalo (Paso 5). |
| No ve mensajes de otros | Confirma que todos usan el **mismo** broker, el mismo `MESH_CHANNEL` y la misma `MESH_KEY` (valores por defecto en `mesh_chat.py`). |
| `mosquitto: command not found` | Instálalo (`brew install mosquitto`) o usa `./start-broker.sh`, que busca el binario. |
| Error de `pip` / módulos | Asegúrate de haber activado el `venv` antes de instalar y de ejecutar. |

### Reglas para ti
- Explica en lenguaje simple **antes** de correr cada comando.
- Pide confirmación antes de instalar software.
- No modifiques `MESH_KEY` ni `MESH_CHANNEL` salvo petición expresa.
- Nunca hagas `git push` ni publiques nada sin que te lo pidan.
- Si algo falla dos veces, explica claramente qué pasó y pregunta cómo seguir en
  vez de insistir con lo mismo.
