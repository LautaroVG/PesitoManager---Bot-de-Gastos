import csv
from datetime import datetime

import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Configuración de seguridad
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Configurar logs (para ver errores en la terminal)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 2. Comando de inicio
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"¡Hola {user}! Soy PesitoManager 💸.\n"
        "Enviame tus gastos así: 'Concepto Monto' (ej: Cafe 500)"
    )

# Función para guardar en el archivo
def guardar_gasto(concepto, monto):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('gastos.csv', 'a', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        writer.writerow([fecha, concepto, monto])


async def procesar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    try:
        partes = texto.split()
        monto = partes[-1].replace(',', '.') # Por si ponen coma en vez de punto
        concepto = " ".join(partes[:-1])
        
        monto_float = float(monto)
        
        # GUARDAR LOS DATOS
        guardar_gasto(concepto, monto_float)
        
        await update.message.reply_text(f"✅ Anotado: {concepto} por ${monto_float:.2f}")
        
    except (ValueError, IndexError):
        await update.message.reply_text("❌ Error. Formato: 'Concepto Monto' (ej: Cine 1200)")

# NUEVO COMANDO: /resumen
async def resumen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = 0
    try:
        with open('gastos.csv', 'r', encoding='utf-8') as archivo:
            reader = csv.reader(archivo)
            for fila in reader:
                if fila: # Evita líneas vacías
                    total += float(fila[2])
        
        await update.message.reply_text(f"📊 Tu gasto total acumulado es: ${total:.2f}")
    except FileNotFoundError:
        await update.message.reply_text("Aún no tenés gastos registrados.")


async def borrar_todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists('gastos.csv'):
        os.remove('gastos.csv')
        await update.message.reply_text("🗑️ Historial eliminado. ¡Cuenta reiniciada!")
    else:
        await update.message.reply_text("No hay ningún archivo de gastos para borrar.")

# 4. Lanzar el bot  
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_mensaje))
    app.add_handler(CommandHandler("resumen", resumen))
    app.add_handler(CommandHandler("borrartodo", borrar_todo))
    
    print("PesitoManager está escuchando... (Presiona Ctrl+C para detener)")
    app.run_polling()




