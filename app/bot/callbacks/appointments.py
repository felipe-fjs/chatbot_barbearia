from app.bot import bot, delete_message
from app.bot.callbacks import  return_menu
from app.bot.handlers import start
from app.model import now_br
from app.model.Appointment import Appointment, AppointmentStatus, get_free_appointments, update_appointment, get_appointment, get_client_last_appointment
from app.model.Client import get_client, Client
from app.model.Admin import  get_admin
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import time

week_days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


def my_appointment(call: CallbackQuery):
    delete_message(call.message)
    chat_id = call.message.chat.id
    print(chat_id)

    client: Client = get_client(chat_id)

    if client != None:

        your_appointment  = get_client_last_appointment(client.chat_id)

        if your_appointment and your_appointment.hour.day > now_br().day:

            buttons = InlineKeyboardMarkup()
            buttons.row(InlineKeyboardButton("Cancelar agendamento", callback_data=f"appointment_cancel_{your_appointment.id}"))
            return_menu(buttons, call)

            text = f"Seu próximo corte foi marcado para: \n  * Dia: {your_appointment.hour.strftime('%d/%m/%Y')}"
            text += f"\nHora: {your_appointment.hour.strftime('%H:%M')}"
            
            bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons)
            return

    message = bot.send_message(chat_id=chat_id, text="Nenhum agendamento ativo foi encontrado!")
    time.sleep(3)
    start(message=message)

def appointments_days(call: CallbackQuery):
    delete_message(call.message)
    buttons = InlineKeyboardMarkup()

    appoints = get_free_appointments()
    if appoints:
        for appoints_day in appoints:
            if len(appoints_day) >= 1:
                data = f"appointments_day_{appoints_day[0].hour.weekday()}"

                text = f"{week_days[appoints_day[0].hour.weekday()]}"
                buttons.row(InlineKeyboardButton(text=text, callback_data=data))

                    
        text = """✨ “Esses são os dias que temos horários disponíveis para você.
    Escolha o que ficar melhor na sua agenda e seguimos para os horários ⏰.”"""
        return_menu(buttons, call)

        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=buttons)
        return
    
    return_menu(buttons)
    text = """🚫 Ops! Agenda cheia por aqui…

Infelizmente não temos mais horários disponíveis para esta semana.
✂️ Mas pode ficar tranquilo: novas vagas serão abertas na sexta-feira, a partir das 6h da manhã.

👉 Fique de olho para garantir seu horário antes que acabe!"""
    message = bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=buttons)
    start(message)

def appointments_hours(call: CallbackQuery):
    delete_message(call.message)
    week_day = int(call.data.split("_")[2])

    buttons = InlineKeyboardMarkup()

    appoints = get_free_appointments()
    appoints_day: list[Appointment] = [appoint for appoint in appoints[week_day] if appoint.status == AppointmentStatus.FREE]

    if appoints_day:
        
        for appoint_hour in appoints_day:
            if appoint_hour.status == AppointmentStatus.FREE:
                text = f"{week_days[appoint_hour.hour.weekday()]} - {appoint_hour.hour.hour}H00"
                data = f"appointments_hour_{appoint_hour.id}"

                buttons.row(InlineKeyboardButton(text=text, callback_data=data))

        text = """✂️ Nesse dia temos os seguintes horários livres:"""
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=buttons)
        return
    
    return_menu(buttons)
    text = f"""🚫 Agenda atualizada!

Enquanto você pensava, alguém foi mais rápido 😅
Infelizmente, todos os horários para este dia já foram preenchidos.

👉 Mas calma: volte e escolha outro dia disponível para garantir seu corte ✂️"""
    message = bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=buttons)
   
def appointments_confirm(call: CallbackQuery):
    delete_message(call.message)
    buttons = InlineKeyboardMarkup()

    appoint_id = int(call.data.split("_")[2])
    appoint = get_appointment(appoint_id)

    if appoint and appoint.status == AppointmentStatus.FREE:
        # atualizar de FREE para RESERVED
        appoint.status = AppointmentStatus.RESERVED
        appoint.client_id = get_client(call.message.chat.id).id
        update_appointment(appoint) 

        appoint_hour = appoint.hour
        week_day = week_days[appoint.hour.weekday()]
        day = appoint.hour.day
        month = appoint.hour.month
        text = f"""✂️ Você selecionou o horário [{appoint_hour}:00 — {week_day}, {day}/{month}] para o seu corte.
        
👉 Deseja confirmar a solicitação de agendamento?"""
        
        buttons.add(InlineKeyboardButton("✅ Confirmar", callback_data=f"appointments_register_{appoint_id}"))
        buttons.add(InlineKeyboardButton("❌ Selecionar outro horário", callback_data=f"appointments_day_{appoint.hour.weekday()}"))
        
        bot.send_message(call.message.chat.id, text=text, reply_markup=buttons)
        return

    return_menu(buttons)
    text = f"""⚡ Esse horário acabou de ser preenchido!

Parece que outro cliente solicitou a última vaga de [{appoint.hour.hour}:00] antes de você.

👉 Por favor, selecione outro horário disponível nesse dia para não ficar sem seu corte 💈."""
    bot.send_message(call.message.chat.id, text=text, reply_markup=buttons)
    
def appointments_register(call: CallbackQuery):
    delete_message(call.message)

    buttons = InlineKeyboardMarkup()
    return_menu(buttons)
    appoint_id = int(call.data.split("_")[2])
    appoint = get_appointment(appoint_id)

    appoint.status = AppointmentStatus.REQUESTED
    update_appointment(appoint)
    text = f"Sua solicitação foi enviada com sucesso para o admin!"
    message = bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=buttons)
    time.sleep(5)
    start(message)

    # enviar mensagem para o administrador
    text = f"Eae admin!\nNova solicitação de agendamento para corte na área! id={appoint}"
    bot.send_message(chat_id=get_admin().chat_id, text=text)
    
def appointments_cancel(call: CallbackQuery):
    delete_message(call.message)

    appoint_id = call.data.split("_").pop()
    chat_id = call.message.chat.id
    message_id = call.message.id

    buttons = InlineKeyboardMarkup()
    appoint = get_appointment(appoint_id)

    if appoint:
        buttons.row(InlineKeyboardButton("❌ Voltar", callback_data=f"appointments_my"))
        buttons.row(InlineKeyboardButton("✅ Cancelar", callback_data=f"appointments_cancelConfirm_{appoint_id}"))

        text = f"""⚠️ Você realmente deseja cancelar seu agendamento de:
📅 {week_days[appoint.hour.weekday()]}, {appoint.hour.day}/{appoint.hour.month} — ⏰ {appoint.hour.hour}:00?

👉 Lembrando que o cancelamento só pode ser feito até o dia anterior ao corte."""
        
        bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=buttons)
        return
    
    return_menu(buttons)
    text = f"""⚠️ Ops! Tivemos uma falha ao acessar seu cadastro no sistema.

👉 Tente novamente em alguns instantes.
Se o problema continuar, entre em contato com a equipe da barbearia 💈."""
    bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons)

def appointments_cancelConfirm(call: CallbackQuery):
    delete_message(call.message)

    appoint_id = call.data.split("_").pop()
    chat_id = call.message.chat.id
    message_id = call.message.id

    appoint = get_appointment(appoint_id)

    if appoint:
        appoint.status = AppointmentStatus.FREE
        update_appointment(appoint)

        text = f"""✅ **Cancelamento efetuado com sucesso!**

Seu agendamento para 📅 **{week_days[appoint.hour.weekday()]}, {appoint.hour.day}/{appoint.hour.month} — ⏰ {appoint.hour.hour}:00** foi cancelado.

Esperamos ver você em breve para marcar um novo horário 💈."""
        bot.send_message(chat_id=chat_id, text=text)
        start(call.message)
        return
    
    buttons = InlineKeyboardMarkup()
    buttons.row(InlineKeyboardButton("🔄 Tentar Novamente", callback_data=f"appointments_my_{appoint_id}"))
    buttons.row(InlineKeyboardButton("📞 Falar com a Barbearia", callback_data=f""))
    return_menu(buttons)

    text = f"""⚠️ Ops! Tivemos uma falha ao acessar seu cadastro no sistema.

👉 Tente novamente em alguns instantes.
Se o problema continuar, entre em contato com a equipe da barbearia 💈."""
    
    bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons)

def appointment_callback_handler(call: CallbackQuery):
    print("ERROR no HANDLER")
    data = call.data.split("_")
    print(f"FOI PARA O HANDLER registrado {data[1]}")
    
    match data[1] :
        case "my":
            print("MY_APPOINTMENT")
            my_appointment(call)
            ... 
        case "week":
            print("FOI PARA SEMANA, PARA EXIBIR OS DIAS COM HORÁRIOS LIVRES")
            appointments_days(call)

        case "day":
            print("FOI PARA DIA, PARA EXIBIR OS HORÁRIOS DO DIA QUE ESTÃO LIVRES")
            appointments_hours(call)

        case "hour":
            print("FOI PARA HORA, PARA CONFIRMAR O HORÁRIO SELECIONADO")
            appointments_confirm(call)

        case "register":
            print("FOI PARA REGISTER, PARA REGISTRO DA HORA SELECIONADA")
            appointments_register(call)

        case "cancel":
            print("CONFRMAR CANCELAMENTO DO AGENDAMENTO!")
            appointments_cancel(call)

        case "cancelConfirm":
            print("CANCELAR AGENDAMENTO!")
            appointments_cancelConfirm(call)


bot.register_callback_query_handler(appointment_callback_handler, 
                                    lambda call: call.data and call.data.startswith("appoint")
                                    )
