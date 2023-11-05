from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

class Tutorial:

    # Text in Markdown
    tutorial = """

🚌 Tutorial bot GUAGUA UCI / PR

En el menu de comandos estan todas las utilidades
💡 Nota: Este tutorial es accesible desde el comando /tutorial

*Para anotar a alguien primero hay que registrarlo, este paso es obligatiorio*
🟥 Se registra una sola vez, el bot guarda el usuario creado.

/nueva\_persona - Registra una nueva persona
A la hora de registrar te pide el nombre y el puente donde te recogen/te bajas
💡 Nota: Debes agregarte a ti mismo (obligatorio) y a otras personas (opcional) para poder anotarse a la lista

/mis\_personas - Muestra las personas que tienes registradas en forma de lista

/editar\_persona y /borrar\_persona
Editar y borrar personas registradas respectivamente

*Para anotarse existen 2 opciones:*
/reservar\_todos - Reserva (anota a la lista) a todas las personas que tienes registradas
/reservar - Te pide que selecciones una persona especifica del grupo de registradas para anotarse de forma individual

/ver\_lista - Para ver la lista hasta el momento en formato .txt
Una vez registrados te muestra una lista de los turnos con el numero de cada uno y el orden de llamada a la lista.
Ademas tiene un boton de cancelar para poder cederle el puesto a otro y asi mejore la distribucion.

Esta lista de personas que tienes anotados es accesible desde el comando /reservas
⚠️ NOTA: Los turnos superiores al 50 son considerados fallos

Cada vez que yo mando a anotarse el bot te manda un SMS notificandote que te puedes anotar, esto quiere decir que ya las reservas volvieron a comenzar desde el turno 1
⚠️ NOTA: Si ya reservaste, el bot no te vuelve a reservar a menos que hayas cancelado


Si tienen alguna sugerencia o error pueden escribirme al privado con los detalles
"""

    @staticmethod
    async def get_tutorial(update: Update, context: ContextTypes.DEFAULT_TYPE):
        tutorial = Tutorial.tutorial
        await update.message.reply_markdown(tutorial, reply_markup=ReplyKeyboardRemove())