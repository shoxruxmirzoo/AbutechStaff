import telebot, requests
from django.shortcuts import render
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from .models import Tasks, CompletedTasks
from company.models import Staff, Team, Company, TaskType, Admins
from django.conf import settings
from django.db.models import F
from django.http import HttpResponse
from django.db import IntegrityError

# Create your views here.

bot = telebot.TeleBot(settings.TOKEN)


def web_hook_view(request):
    if request.method == 'POST':
        json_string = request.body.decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return HttpResponse(status=200)
    return HttpResponse('OK')


@bot.message_handler(commands=['start'])
def start_msg(message):
    global user_id
    global username
    global first_name
    global is_member
    is_member = False
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    # company_list = Company.objects.values_list
    if Staff.objects.filter(telegram_id=user_id, team__name__isnull=False, company__name__isnull=False).exists():
        is_member = True
        if Admins.objects.filter(name__isnull=False).exists():
            text = 'Salom Admin'
        else:
            text = "Salom, {}\n\nLavozim - hodim".format(first_name)
        company = Company.objects.values_list('name', flat=True)
        reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = [KeyboardButton(text=text) for text in company]
        reply_markup.add(*buttons)
        bot.send_message(user_id, text, reply_markup=reply_markup)
    else:
        is_member = False
        Staff.objects.create(name=first_name, telegram_id=user_id, username=username)
        text = "Sizni kompaniya ishchilar ro'yxatidan topa olmadim"
        bot.send_message(user_id, text)


@bot.message_handler(content_types='text')
def text_msg(message):
    text = "Qaless"
    team = Team.objects.values_list('name', flat=True)
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [KeyboardButton(text=text) for text in team]
    reply_markup.add(*buttons)
    bot.send_message(user_id, text, reply_markup=reply_markup)
