# 💸 PesitoManager - Telegram Bot

Asistente personal de finanzas para Telegram desarrollado con **Python**. Permite registrar gastos diarios, generar resúmenes totales y visualizar estadísticas mediante gráficos.

## ✨ Características
- **Registro rápido:** Enviá `Concepto Monto` y el bot lo guarda automáticamente.
- **Reportes:** Comando `/resumen` para ver el total acumulado.
- **Visualización:** Comando `/grafico` para generar un reporte visual con Matplotlib.
- **Seguridad:** Manejo de credenciales mediante variables de entorno.

## 🛠️ Tecnologías
- [Python 3.10+](https://www.python.org/)
- [python-telegram-bot](https://python-telegram-bot.org/) - Interacción con la API de Telegram.
- [Pandas / CSV](https://pandas.pydata.org/) - Almacenamiento de datos.
- [Matplotlib](https://matplotlib.org/) - Generación de gráficos.

## 🚀 Instalación
1. Clonar el repo.
2. Crear un archivo `.env` con tu `TELEGRAM_TOKEN`.
3. Instalar dependencias: `pip install -r requirements.txt`.
4. Ejecutar `python bot.py`.