import telebot, requests
from django.shortcuts import render
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from .models import Tasks, CompletedTasks
from company.models import Staff, Team, Company, TaskType, Admins
from django.conf import settings
from django.http import HttpResponse

# Create your views here.

bot = telebot.TeleBot(settings.TOKEN)


def web_hook_view(request):
    if request.method == 'POST':
        json_string = request.body.decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return HttpResponse(status=200)
    return HttpResponse('OK')


@bot.message_handler(commands = ['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    if Staff.objects.filter(tg_id=user_id).exists():
        user = Staff.objects.all()
        text = 'Salom, {}'.format(user.name)
        bot.send_message(user_id, text)
    else:
        Staff.objects.create(tg_id=user_id, name=first_name, username=username)
        text = "Siz yangi a'zosiz. Bazaga qo'shildiz"
        bot.send_message(user_id, text)


