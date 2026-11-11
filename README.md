# Tita Bot 🐈💤

Una gatita con actitud de princesa, una siesta interrumpida y acceso a Gemini.  
Tita está para charlar... aunque primero te va a hacer sentir un poquito culpable por despertarla.

## ¿Qué hace?

- Te saluda con toda la energía de alguien a quien sacaron de la quinta siesta.
- Contesta tus mensajes usando Gemini 3.1 Flash Lite y una personalidad bien rioplatense.
- Recuerda los últimos mensajes de la charla para no contestar como si cada mensaje fuera el primero.
- Si algo falla, se queja en vez de fingir que entendió. Bastante sensata, la michi.

## Qué necesitás

- Python 3.10 o superior.
- Un bot de Telegram y su token.
- Una clave de API de Gemini.

## Preparar el proyecto

Desde la carpeta del proyecto, creá y activá un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalá las dependencias:

```bash
pip install -r requirements.txt
```

Creá un archivo `.env` junto a `tita.py`:

```env
TELEGRAM_TOKEN=tu_token_de_telegram
GEMINI_API_KEY=tu_clave_de_gemini
```

No compartas estas claves ni subas `.env` a GitHub. ¡Tita es chusma, pero tus secretos no son para ella!

El archivo `personalidad.txt` contiene el prompt de Tita y forma parte del repositorio. Las claves de Telegram y Gemini no: mantenelas únicamente en tu `.env` local y nunca las publiques.

## A despertar a Tita

```bash
python tita.py
```

En Telegram, buscá tu bot y mandale `/start`. Para apagarlo, volvé a la terminal y apretá `Ctrl+C`.

## Si Tita no contesta

Mirá la terminal donde está corriendo: ahí se registran los errores de Telegram o Gemini. El acceso gratuito de Gemini tiene límites de uso y puede saturarse (error 503); cambiar a un modelo más liviano no garantiza disponibilidad permanente. Si pasa, probá de nuevo más tarde.

## Nota de convivencia

Tita puede ser cortante, quejosa y bastante dramática con sus siestas. Es parte del personaje; no es nada personal. 🐾
