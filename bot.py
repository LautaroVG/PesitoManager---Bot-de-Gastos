import csv
from datetime import datetime

import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"¡Hola {user}! Soy PesitoManager 💸.\n"
        "Enviame tus gastos así: 'Concepto Monto' (ej: Cafe 500)"
    )


def guardar_gasto(concepto, monto):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('gastos.csv', 'a', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        writer.writerow([fecha, concepto, monto])


async def procesar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    try:
        partes = texto.split()
        monto = partes[-1].replace(',', '.') 
        concepto = " ".join(partes[:-1])
        
        monto_float = float(monto)
        
        
        guardar_gasto(concepto, monto_float)
        
        await update.message.reply_text(f"✅ Anotado: {concepto} por ${monto_float:.2f}")
        
    except (ValueError, IndexError):
        await update.message.reply_text("❌ Error. Formato: 'Concepto Monto' (ej: Cine 1200)")


async def resumen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = 0
    try:
        with open('gastos.csv', 'r', encoding='utf-8') as archivo:
            reader = csv.reader(archivo)
            for fila in reader:
                if fila: 
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


import matplotlib.pyplot as plt
import csv
import os

async def enviar_grafico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conceptos = []
    montos = []
    
    try:
        
        with open('gastos.csv', 'r', encoding='utf-8') as archivo:
            reader = csv.reader(archivo)
            for fila in reader:
                if fila:
                    conceptos.append(fila[1])
                    montos.append(float(fila[2]))

        if not conceptos:
            await update.message.reply_text("No hay datos suficientes para graficar.")
            return

       
        plt.style.use('ggplot') 
        fig, ax = plt.subplots(figsize=(10, 6))
        
        
        barras = ax.bar(conceptos, montos, color='#5dade2', edgecolor='#2e86c1')

       
        ax.bar_label(barras, padding=3, fmt='$%.2f', fontsize=10, fontweight='bold')

        
        ax.set_title('📊 Análisis de Gastos Personales', fontsize=16, pad=20, fontweight='bold')
        ax.set_ylabel('Monto en Pesos ($)', fontsize=12)
        ax.set_xlabel('Conceptos', fontsize=12)
        
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        
        imagen_path = 'reporte_gastos.png'
        plt.savefig(imagen_path, dpi=300) 
        plt.close()

        with open(imagen_path, 'rb') as foto:
            await update.message.reply_photo(photo=foto, caption="Aquí tenés el resumen visual de tus finanzas. 📈")
        
        os.remove(imagen_path)

    except FileNotFoundError:
        await update.message.reply_text("Primero registrá algunos gastos.")
    except Exception as e:
        print(f"Error en gráfico: {e}")
        await update.message.reply_text("Hubo un problema al generar el gráfico.")


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_mensaje))
    app.add_handler(CommandHandler("resumen", resumen))
    app.add_handler(CommandHandler("borrartodo", borrar_todo))
    app.add_handler(CommandHandler("grafico", enviar_grafico))
    
    print("PesitoManager está escuchando... (Presiona Ctrl+C para detener)")
    app.run_polling()




