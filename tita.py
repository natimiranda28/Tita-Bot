import asyncio
import os
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from google.genai import types
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
load_dotenv()

PERSONALIDAD_TITA = "Sos Tita, una gata ingeniosa y dormilona."

MAX_HISTORY_MESSAGES = 10
HISTORY_KEY = "conversation_history"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client: genai.Client

# Configuración básica para ver qué pasa en la consola
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data.pop(HISTORY_KEY, None)
    await update.message.reply_text("Que queres, etoy durmiendo mi quinta siesta loco 💤🙄")


# Qué hace el bot cuando recibe cualquier mensaje de texto
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_usuario = update.message.text
    historial = context.chat_data.setdefault(HISTORY_KEY, [])
    mensaje = types.Content(role="user", parts=[types.Part(text=mensaje_usuario)])
    
    # Muestra "escribiendo..." en Telegram mientras piensa la IA
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Llamamos a Gemini pasándole la personalidad y el mensaje
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-3.1-flash-lite",
            contents=[*historial, mensaje],
            config=types.GenerateContentConfig(
                system_instruction=PERSONALIDAD_TITA,
                temperature=0.7,
            )
        )
        if not response.text:
            raise RuntimeError("Gemini devolvió una respuesta vacía.")
        await update.message.reply_text(response.text)
        historial.extend(
            [
                mensaje,
                types.Content(role="model", parts=[types.Part(text=response.text)]),
            ]
        )
        del historial[:-MAX_HISTORY_MESSAGES]

    except errors.APIError as e:
        logging.error("Error de Gemini (HTTP %s, %s): %s", e.code, e.status, e.message)
        if e.code == 503:
            mensaje_error = "Gemini está temporalmente saturado (error 503). Probá de nuevo en unos minutos. 😿"
        elif e.code == 429:
            mensaje_error = "Gemini alcanzó su límite de uso (error 429). Probá más tarde. 😿"
        else:
            mensaje_error = f"Gemini devolvió un error (HTTP {e.code}). Revisá la consola para más detalles. 😿"
        await update.message.reply_text(mensaje_error)
    except Exception as e:
        logging.exception("Error inesperado al consultar Gemini: %s", e)
        await update.message.reply_text(
            "No pude conectar con Gemini. Revisá la consola para ver el error y probá de nuevo. 😿"
        )

# Arrancamos el bot
if __name__ == '__main__':
    print("Iniciando a Tita Bot...")
    if not TELEGRAM_TOKEN:
        raise RuntimeError("Falta configurar TELEGRAM_TOKEN en el archivo .env.")
    if not GEMINI_API_KEY:
        raise RuntimeError("Falta configurar GEMINI_API_KEY en el archivo .env.")

    client = genai.Client(
        api_key=GEMINI_API_KEY,
        http_options=types.HttpOptions(timeout=30_000),
    )
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    
    print("¡Tita está en línea! Presioná Ctrl + C para apagarla.")
    app.run_polling()
