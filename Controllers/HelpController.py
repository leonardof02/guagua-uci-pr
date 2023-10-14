from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

class Tutorial:

    tutorial = """

🚌 Hola este es el bot de viajes entre la UCI y Pinar del Rio, se hizo con fines de mejorarles la vida a todos nosotros.
El bot se encargara de notificarte cuando anotarte para el viaje, te permite anotarte a ti y a otros (amigos, familia, pareja, etc.), ademas de darte el turno (numero que cogiste en la lista).

# * ℹ️ Este es el tutorial:*

En el menu de comandos estan todas las utilidades
⚠️ Nota: Este tutorial es accesible desde el comando /tutorial

*Para anotar a alguien primero hay que registrarlo:*

/new - Registra una nueva persona
A la hora de registrar te pide el nombre y el municipio
⚠️ Nota: Debes agregarte a ti mismo y a otras personas (opcional) para poder anotarse a la lista

/list - Muestra las personas que tienes registradas en forma de lista

/edit y /delete
Borrar y editar personas registradas respectivamente

*Para anotarse existen 2 opciones:*
/reservar_todos - Reserva (anota a la lista) a todas las personas que tienes registradas
/reservar - Te pide que selecciones una persona especifica del grupo de registradas para anotarse de forma individual

Una vez registrados te muestra una lista de los turnos con el numero de cada uno y el orden de llamada a la lista.
Ademas tiene un boton de cancelar para poder cederle el puesto a otro y asi mejore la distribucion.

Esta lista de personas que tienes anotados es accesible desde el comando /reservas
⚠️ NOTA: Los turnos superiores al 45 son considerados fallos

Cada vez que yo mando a anotarse el bot te manda un SMS notificandote que te puedes anotar, esto quiere decir que ya las reservas volvieron a comenzar desde el turno 1
⚠️ NOTA: Si ya reservaste, el bot no te vuelve a reservar a menos que hayas cancelado

El admin tiene acceso a la lista asi que pueden hacerlo con total confianza
Si tienen alguna sugerencia o error pueden escribirme al privado con los detalles
"""

    @staticmethod
    async def get_tutorial(update: Update, context: ContextTypes.DEFAULT_TYPE):
        tutorial = Tutorial.tutorial
        await update.message.reply_text(tutorial, reply_markup=ReplyKeyboardRemove())