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
- El chat necesita: Python 3.9+, las dependencias de `requirements.txt`, y la
  dirección de un **broker MQTT** al que todos se conectan.
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

### Paso 4 — Pregunta a la persona DOS cosas
1. **¿Con qué nombre quiere aparecer en el chat?** (ej. "Ana")
2. **¿Le dieron una dirección (IP) del broker?**
   - **Sí** → úsala en `MESH_BROKER`.
   - **No sabe / ella es quien organiza** → ve al Paso 5 para hospedar el broker.

### Paso 5 — (Solo si esta persona hospeda el broker)
El chat necesita UN broker que todos alcancen. Si esta persona es quien lo monta:
```bash
brew install mosquitto        # macOS (una vez). Linux: sudo apt install mosquitto
./start-broker.sh --lan       # abre el broker a la red local e imprime la IP a compartir
```
- Deja ese broker corriendo en su propia terminal (Ctrl+C lo apaga).
- Dile a la persona que **comparta la IP que imprime el script** con los demás.
- Para gente por internet (no misma red), hay que hospedarlo en un VPS con IP
  pública; avísale que eso requiere un paso extra y ofrécele ayuda si lo desea.

### Paso 6 — Entrar al chat
En una terminal (con el `venv` activado), usando la IP del broker y el nombre:
```bash
MESH_BROKER=<IP-DEL-BROKER> python3 mesh_chat.py "<NOMBRE>"
```
Si la persona hospeda el broker en su propia máquina, `MESH_BROKER=127.0.0.1`.

### Paso 7 — Explícale cómo usarlo
Dile, en palabras simples:
- "Escribe tu mensaje y pulsa **Enter** para enviarlo."
- "Los mensajes de los demás aparecen solos."
- "Para salir, pulsa **Ctrl+C**."

### Solución de problemas (para ti, el agente)
| Síntoma | Qué hacer |
|---------|-----------|
| `ConnectionRefusedError: [Errno 61]` | No hay broker en esa dirección. Confirma la IP con la persona, o monta el broker (Paso 5). |
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
