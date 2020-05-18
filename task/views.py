import telebot
from django.shortcuts import render
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from .models import Tasks, CompletedTasks
from company.models import Staff, Team, Company, TaskType, Admins, Unknown
from .const import btn, STEPS, task_btn
from .helpers import main_menu, company_menu, hide_menu, team_menu, task_menu, task_menu_name
from .helpers import navigation, task_marketing_menu, task_design_menu, task_media_menu
from django.conf import settings
from django.db.models import F
from django.http import HttpResponse

bot = telebot.TeleBot(settings.TOKEN)

staff = Staff.objects.values_list('telegram_id', flat=True)
company_name = Company.objects.values_list('name', flat=True)
team_name = Team.objects.values_list('name', flat=True)
# MENU NAVIGATION
navigation_menu = navigation()

# Some buttons
back = btn['back']
# DATA CONFIG
data = {
    'company': '',
    'team': '',
    'url': '',
    'more_voice': '',
    'more_text': '',
    'deadline': '',
    'task_type': '',
    'from_admin': '',
    'id': '',
}


def web_hook_view(request):
    if request.method == 'POST':
        json_string = request.body.decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return HttpResponse(status=200)
    return HttpResponse('OK')


def is_admin(message, user_id):
    if user_id in staff:
        return True
    else:
        return failed(message)


@bot.message_handler(commands=['start'])
def main(message):
    global first_name
    global username
    global user_id
    global get
    global get_task
    global finish_more
    global finish_link
    global finish_deadline
    finish_more = False
    finish_link = False
    finish_deadline = False
    first_name = message.from_user.first_name
    username = message.from_user.username
    user_id = message.from_user.id
    get = Staff.objects.get(telegram_id=user_id)
    if is_admin(message, user_id):
        get.step = 0
        text = f'Salom, {first_name}'
        bot.send_message(user_id, text, reply_markup=main_menu())
        get.step = 1
        get.save()


@bot.message_handler(regexp=btn['clean'])
def clean(message):
    if is_admin(message, user_id):
        get.step = 0
        for i in data:
            i = ''
        return main(message)


@bot.message_handler(func=lambda message: get.step == 1)
def company(message):
    # Faqat admin VA VAZIFA BERISH yuborilganda
    if is_admin(message, user_id) and message.text == btn['order_task']:
        global task_data
        text = "Kompaniyani tanlang"
        bot.send_message(user_id, text, reply_markup=company_menu())
        get.step = 2


@bot.message_handler(func=lambda message: get.step == 2)
def team(message):
    if is_admin(message, user_id) and message.text in company_name:
        data['company'] = message.text
        text = "Jamoani tanlang"
        bot.send_message(user_id, text, reply_markup=team_menu())
        get.step = 3


@bot.message_handler(func=lambda message: get.step == 3)
def task(message):
    print('tASK')
    if is_admin(message, user_id) and message.text in team_name or message.text == btn['back']:
        text = "Vazifalarni belgilang"
        bot.send_message(user_id, text, reply_markup=task_menu())
        global finish_more
        global finish_link
        global finish_deadline
        finish_more = False
        finish_link = False
        finish_deadline = False
        get.step = 4
        if message.text in team_name:
            data['team'] = message.text


@bot.message_handler(func=lambda message: get.step == 4)
def more(message):
    if is_admin(message, user_id):
        global finish_more
        global finish_link
        global finish_deadline
        # finish_deadline, finish_link, finish_more = False
        if message.text == task_btn['more']:
            text = "Batafsil ma'lumot.\n\nAudio yoki matnli xabar yuboring"
            finish_more = True
            get.step = 5
            # ============AUDIO yoki TEXT tekshirish==========
            bot.send_message(user_id, text, reply_markup=hide_menu())
        elif message.text == task_btn['url']:
            text = 'Linkni kiriting'
            finish_link = True
            get.step = 5
            bot.send_message(user_id, text, reply_markup=hide_menu())
        elif message.text == task_btn['deadline']:
            text = 'Dedlaynni kiriting'
            finish_deadline = True
            bot.send_message(user_id, text, reply_markup=hide_menu())
            get.step = 5
        elif message.text == btn['next']:
            get.step = 6
            return task_type(message)


# MORE uchun voices


@bot.message_handler(func=lambda message: get.step == 5, content_types=['voice'])
def get_more_voice(message):
    if finish_more:
        data['more_voice'] = message.message_id   # Message ID forward uchun
        text = 'Ovozli izoh saqlandi. Ortga qayting'
        bot.send_message(user_id, text, reply_markup=navigation_menu[0])
        # bot.forward_message(settings.CHANNEL, message.chat.id, message.message_id)


@bot.message_handler(func=lambda message: get.step == 5, content_types=['text'])
def get_more_text(message):
    if message.text == btn['back']:
        return task(message)
    if finish_more and message.text != btn['back']:
        data['more_text'] = message.text    #Message text saqladim, forward qilganda qo'shiladi
        text = 'Matnli izoh saqlandi. Ortga qayting'
        bot.send_message(user_id, text, reply_markup=navigation_menu[0])

    elif finish_link and message.text != btn['back']:
        data['url'] = message.text  # URL saqlandi
        text = 'Link saqlandi. Ortga qayting'
        bot.send_message(user_id, text, reply_markup=navigation_menu[0])

    elif finish_deadline == True and message.text != btn['back']:
        data['deadline'] = message.text
        text = 'Dedlayn saqlandi. Ortga qayting'
        bot.send_message(user_id, text, reply_markup=navigation_menu[0])
    get.step = 3


@bot.message_handler(func=lambda message: get.step == 6, regexp=btn['next'])
def task_type(message):
    name = Team.objects.values_list('name', flat=True)
    if data['team'] == name[0]: #Marketing
        text = 'Vazifa turini tanlang.\n\nJamoa: {}'.format(name[0])
        bot.send_message(user_id, text, reply_markup=task_marketing_menu())
    if data['team'] == name[1]: #Media
        text = 'Vazifa turini tanlang.\n\nJamoa: {}'.format(name[1])
        bot.send_message(user_id, text, reply_markup=task_media_menu())
    if data['team'] == name[2]: #Dizayn
        text = 'Vazifa turini tanlang.\n\nJamoa: {}'.format(name[2])
        bot.send_message(user_id, text, reply_markup=task_design_menu())




def failed(message):
    text = "Telegram ID bazasidan topilmadi. Ro'yhatdan o'tish uchun iltimos adminga (@abutechadmin) murojaat qiling!\n\nAbutech: @shoxruxmirzoo"
    bot.send_message(message.from_user.id, text, reply_markup=hide_menu())
    if not Unknown.objects.filter(telegram_id=user_id).exists():
        Unknown.objects.create(first_name=first_name, username=username, telegram_id=user_id).save()
    else:
        pass
