# 🔐 Grupo privado con HiveMQ Cloud (gratis, con usuario/contraseña + TLS)

El broker público por defecto (`broker.hivemq.com`) funciona sin registro, pero es
**compartido y anónimo**: cualquiera podría conectarse al mismo broker (aunque solo
vería tus mensajes cifrados, no su contenido).

Si quieres un broker **solo tuyo**, con **usuario/contraseña y cifrado TLS**, y
**sin pagar**, usa el tier gratuito de **HiveMQ Cloud**. Da hasta 100 conexiones,
suficiente para un equipo.

---

## 1. Crea el clúster gratuito (una vez, ~5 min)

1. Entra a **https://www.hivemq.com/mqtt-cloud-broker/** y crea una cuenta.
2. Elige el plan **"Serverless" (Free)** y crea el clúster.
3. Cuando esté listo, anota del panel:
   - **Cluster URL / Host** — algo como `abc123def456.s1.eu.hivemq.cloud`
   - **Port** — `8883` (TLS)
4. Ve a **Access Management → Credentials** y crea un **usuario y contraseña**
   (por ejemplo `equipo` / una contraseña fuerte). Este user/pass lo compartes con
   tu grupo.

---

## 2. Cada persona se conecta así

Con el `venv` activado, define las variables de entorno del clúster y entra al chat:

```bash
export MESH_BROKER="abc123def456.s1.eu.hivemq.cloud"   # tu Cluster URL
export MESH_PORT=8883
export MESH_TLS=1
export MESH_USER="equipo"
export MESH_PASS="la-contraseña-del-grupo"

python3 mesh_chat.py "TuNombre"
```

O todo en una línea:

```bash
MESH_BROKER="abc123def456.s1.eu.hivemq.cloud" MESH_PORT=8883 MESH_TLS=1 \
MESH_USER="equipo" MESH_PASS="la-contraseña" python3 mesh_chat.py "TuNombre"
```

**En Windows** (usa `python`, no `python3`):

```powershell
# PowerShell
$env:MESH_BROKER="abc123def456.s1.eu.hivemq.cloud"
$env:MESH_PORT="8883"; $env:MESH_TLS="1"
$env:MESH_USER="equipo"; $env:MESH_PASS="la-contraseña"
python mesh_chat.py "TuNombre"
```

```bat
REM cmd.exe
set MESH_BROKER=abc123def456.s1.eu.hivemq.cloud
set MESH_PORT=8883
set MESH_TLS=1
set MESH_USER=equipo
set MESH_PASS=la-contraseña
python mesh_chat.py "TuNombre"
```

> 💡 Para no reescribir esto cada vez, guarda esas líneas `export ...` en un archivo
> `.env-grupo` y ejecútalo con `source .env-grupo` antes de entrar al chat. **No lo
> subas al repositorio** (contiene la contraseña).

---

## 3. Dos capas de seguridad

Con HiveMQ Cloud tienes **doble candado**:

1. **TLS + usuario/contraseña** → nadie entra al broker sin las credenciales.
2. **Cifrado de la app** (`MESH_KEY`) → aunque alguien entrara, solo vería ruido.

Para máxima privacidad, además genera tu propia `MESH_KEY` (ver README) y no uses
la que viene en el repo.

---

## ¿Cuándo usar cada opción?

| Necesitas… | Usa |
|------------|-----|
| Probar rápido, sin registro | Broker público por defecto (`broker.hivemq.com`) |
| Grupo estable y privado, gratis | **HiveMQ Cloud** (esta guía) |
| Control total / red sin internet | Tu propio `mosquitto` (ver README) |

## Solución de problemas

| Síntoma | Arreglo |
|---------|---------|
| Se conecta pero se desconecta al instante | Falta `MESH_TLS=1` (HiveMQ Cloud exige TLS) o el puerto no es `8883`. |
| `Not authorized` / rechaza conexión | Usuario o contraseña incorrectos, o no creados en *Access Management*. |
| Error de certificado TLS | Actualiza `certifi`: `pip install --upgrade certifi`. |
