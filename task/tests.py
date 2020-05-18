from django.test import TestCase

# Create your tests here.
import telebot
from django.shortcuts import render
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from .models import Tasks, CompletedTasks
from company.models import Staff, Team, Company, TaskType, Admins
from .const import btn
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


class Controller:
    def __init__(self, telegram_id=None, first_name=None, username=None, text=None):
        self.telegram_id = telegram_id
        self.first_name = first_name
        self.username = username
        self.text = text

    def start(self):
        user = Staff.objects.filter(telegram_id=self.telegram_id)
        if user:
            print(self.username)
            user.step = 0
            # user.save()
            msg = 'Salom'
            bot.send_message(self.telegram_id, msg, reply_markup=self.main_menu())
        else:
            bot.send_message(self.telegram_id, 'Kimsanee')

    def main_menu(self):
        buttons = ReplyKeyboardMarkup(True, True, row_width=2)
        order_task = KeyboardButton(btn['order_task'])
        send_task = KeyboardButton(btn['send_tasks'])
        statistics = KeyboardButton(btn['statistics'])
        buttons.add(order_task, send_task)
        buttons.add(statistics)
        return buttons

    def company(self):
        get = Staff.objects.get(telegram_id=self.telegram_id)
        get.step = 1
        get.save()
        msg = 'Kompaniyani tanlang'
        bot.send_message(self.telegram_id, msg, reply_markup=self.company_menu())

    def company_menu(self):
        buttons = ReplyKeyboardMarkup(True, True, row_width=3)
        company_name = Company.objects.values_list('name', flat=True)
        key = [KeyboardButton(text=text) for text in company_name]
        navigate = KeyboardButton(btn['back'])
        buttons.add(*key)
        buttons.add(navigate)
        return buttons

    def team(self):
        get = Staff.objects.get(telegram_id=self.telegram_id)
        get.step = 2
        get.save()
        task = Tasks.objects.get(from_admin__telegram_id=self.telegram_id)
        # result = saver(task)
        # task.link = result
        task.save()
        msg = "Jamoani tanlang"
        # msg += str(result)
        bot.send_message(self.telegram_id, msg, reply_markup=self.team_menu())

    def team_menu(self):
        buttons = ReplyKeyboardMarkup(True, True, row_width=3)
        team_name = Team.objects.values_list('name', flat=True)
        key = [KeyboardButton(text=text) for text in team_name]
        navigate = KeyboardButton(btn['back'])
        buttons.add(*key)
        buttons.add(navigate)
        return buttons

    def task(self):
        get = Staff.objects.get(telegram_id=self.telegram_id)
        get.step = 3
        get.save()
        task = Tasks.objects.get(company__name=self)
        msg = 'Jamoani tanlang'
        bot.send_message(self.telegram_id, msg, reply_markup=self.team_menu())

    # def task_menu(self):
    #     buttons = ReplyKeyboardMarkup(True, True, row_width=3)
    #     task_name = Tasks.objects.values_list('name', flat=True)
    #     key = [KeyboardButton(text=text) for text in team_name]
    #     navigate = KeyboardButton(btn['back'])
    #     buttons.add(*key)

    def back_step(self):  # ORTGA QAYTISH UCHUN
        get = Staff.objects.get(telegram_id=self.telegram_id)
        if get.step == 1:
            get.step = 0
            get.save()
            self.start()
        elif get.step == 2:
            get.step = 1
            get.save()
            self.company()

    # def typing_event(self):
    #     bot.send_chat_action(self.telegram_id, 'typing')


def saver(msg):
    print(msg)
    if msg:
        return msg


@bot.message_handler(commands=['start'])
def start(message):
    print(message.chat.id)
    Controller(telegram_id=message.from_user.id, first_name=message.from_user.first_name,
               username=message.from_user.username).start()


@bot.message_handler(content_types='text')
def send_message(message):
    tg_id = message.from_user.id
    print('Messageee')
    get = Staff.objects.get(telegram_id=tg_id)
    company_name = Company.objects.values_list('name', flat=True)

    if message.text == btn['order_task']:
        Controller(telegram_id=tg_id).company()

    elif message.text in company_name and get.step == 1:
        saver(message.text)
        Controller(telegram_id=tg_id).team()

    elif message.text == btn['back']:
        Controller(telegram_id=tg_id).back_step()


# @bot.message_handler(commands=['start'])
# def start_msg(message):
#     global user_id
#     global username
#     global first_name
#     global is_member
#     is_member = False
#     user_id = message.from_user.id
#     username = message.from_user.username
#     first_name = message.from_user.first_name
#     # company_list = Company.objects.values_list
#     if Staff.objects.filter(telegram_id=user_id, team__name__isnull=False, company__name__isnull=False).exists():
#         is_member = True
#         if Admins.objects.filter(name__isnull=False).exists():
#             text = 'Salom Admin'
#         else:
#             text = "Salom, {}\n\nLavozim - hodim".format(first_name)
#         company = Company.objects.values_list('name', flat=True)
#         reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#         buttons = [KeyboardButton(text=text) for text in company]
#         reply_markup.add(*buttons)
#         bot.send_message(user_id, text, reply_markup=reply_markup)
#     else:
#         is_member = False
#         Staff.objects.create(name=first_name, telegram_id=user_id, username=username)
#         text = "Sizni kompaniya ishchilar ro'yxatidan topa olmadim"
#         bot.send_message(user_id, text)
#
#
# @bot.message_handler(content_types='text')
# def text_msg(message):
#     text = "Qaless"
#     team = Team.objects.values_list('name', flat=True)
#     reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     buttons = [KeyboardButton(text=text) for text in team]
#     reply_markup.add(*buttons)
#     bot.send_message(user_id, text, reply_markup=reply_markup)
import telebot
from django.shortcuts import render
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from .models import Tasks, CompletedTasks
from company.models import Staff, Team, Company, TaskType, Admins
from .const import btn
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


class Controller:
    def __init__(self, telegram_id=None, first_name=None, username=None, text=None):
        self.telegram_id = telegram_id
        self.first_name = first_name
        self.username = username
        self.text = text

    def start(self):
        user = Staff.objects.filter(telegram_id=self.telegram_id)
        if user:
            print(self.username)
            user.step = 0
            # user.save()
            msg = 'Salom'
            bot.send_message(self.telegram_id, msg, reply_markup=self.main_menu())
        else:
            bot.send_message(self.telegram_id, 'Kimsanee')

    def main_menu(self):
        buttons = ReplyKeyboardMarkup(True, True, row_width=2)
        order_task = KeyboardButton(btn['order_task'])
        send_task = KeyboardButton(btn['send_tasks'])
        statistics = KeyboardButton(btn['statistics'])
        buttons.add(order_task, send_task)
        buttons.add(statistics)
        return buttons

    def company(self):
        get = Staff.objects.get(telegram_id=self.telegram_id)
        get.step = 1
        get.save()
        msg = 'Kompaniyani tanlang'
        bot.send_message(self.telegram_id, msg, reply_markup=self.company_menu())

    def company_menu(self):
        buttons = ReplyKeyboardMarkup(True, True, row_width=3)
        company_name = Company.objects.values_list('name', flat=True)
        key = [KeyboardButton(text=text) for text in company_name]
        navigate = KeyboardButton(btn['back'])
        buttons.add(*key)
        buttons.add(navigate)
        return buttons

    def team(self):
        get = Staff.objects.get(telegram_id=self.telegram_id)
        get.step = 2
        get.save()
        task = Tasks.objects.get(from_admin__telegram_id=self.telegram_id)
        result = self.text
        # task.link = result
        # task.save()
        msg = "Jamoani tanlang"
        msg += str(result)
        print(result)
        bot.send_message(self.telegram_id, msg, reply_markup=self.team_menu())

    def team_menu(self):
        buttons = ReplyKeyboardMarkup(True, True, row_width=3)
        team_name = Team.objects.values_list('name', flat=True)
        key = [KeyboardButton(text=text) for text in team_name]
        navigate = KeyboardButton(btn['back'])
        buttons.add(*key)
        buttons.add(navigate)
        return buttons

    def task(self):
        get = Staff.objects.get(telegram_id=self.telegram_id)
        get.step = 3
        get.save()
        task = Tasks.objects.get(company__name=self)
        msg = 'Jamoani tanlang'
        bot.send_message(self.telegram_id, msg, reply_markup=self.team_menu())

    def back_step(self):  # ORTGA QAYTISH UCHUN
        get = Staff.objects.get(telegram_id=self.telegram_id)
        if get.step == 1:
            get.step = 0
            get.save()
            self.start()
        elif get.step == 2:
            get.step = 1
            get.save()
            self.company()

    # def typing_event(self):
    #     bot.send_chat_action(self.telegram_id, 'typing')


#
# def saver(msg):
#     print(msg)
#     if msg:
#         return msg


@bot.message_handler(commands=['start'])
def start(message):
    print(message.chat.id)
    Controller(telegram_id=message.from_user.id, first_name=message.from_user.first_name,
               username=message.from_user.username).start()


@bot.message_handler(content_types='text')
def send_message(message):
    tg_id = message.from_user.id
    print('Messageee')
    get = Staff.objects.get(telegram_id=tg_id)
    company_name = Company.objects.values_list('name', flat=True)

    if message.text == btn['order_task']:
        Controller(telegram_id=tg_id).company()

    elif message.text in company_name and get.step == 1:
        saver(message.text)
        Controller(telegram_id=tg_id).team()

    elif message.text == btn['back']:
        Controller(telegram_id=tg_id).back_step()

# @bot.message_handler(commands=['start'])
# def start_msg(message):
#     global user_id
#     global username
#     global first_name
#     global is_member
#     is_member = False
#     user_id = message.from_user.id
#     username = message.from_user.username
#     first_name = message.from_user.first_name
#     # company_list = Company.objects.values_list
#     if Staff.objects.filter(telegram_id=user_id, team__name__isnull=False, company__name__isnull=False).exists():
#         is_member = True
#         if Admins.objects.filter(name__isnull=False).exists():
#             text = 'Salom Admin'
#         else:
#             text = "Salom, {}\n\nLavozim - hodim".format(first_name)
#         company = Company.objects.values_list('name', flat=True)
#         reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#         buttons = [KeyboardButton(text=text) for text in company]
#         reply_markup.add(*buttons)
#         bot.send_message(user_id, text, reply_markup=reply_markup)
#     else:
#         is_member = False
#         Staff.objects.create(name=first_name, telegram_id=user_id, username=username)
#         text = "Sizni kompaniya ishchilar ro'yxatidan topa olmadim"
#         bot.send_message(user_id, text)
#
#
# @bot.message_handler(content_types='text')
# def text_msg(message):
#     text = "Qaless"
#     team = Team.objects.values_list('name', flat=True)
#     reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     buttons = [KeyboardButton(text=text) for text in team]
#     reply_markup.add(*buttons)
#     bot.send_message(user_id, text, reply_markup=reply_markup)
