import telebot
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from .models import Tasks, CompletedTasks
from company.models import Staff, Team, Company, TaskType, Admins, Unknown
from .const import btn, STEPS, task_btn
from .helpers import main_menu, company_menu, hide_menu, team_menu, task_menu, task_menu_name
from .helpers import navigation, task_marketing_menu, task_design_menu, task_media_menu
from .helpers import marketing_mention_menu, confirm_menu
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
    'mention': '',
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
    global is_mention
    global saved
    finish_more = False
    finish_link = False
    finish_deadline = False
    is_mention = False
    first_name = message.from_user.first_name
    username = message.from_user.username
    user_id = message.from_user.id
    get = Staff.objects.get(telegram_id=user_id)
    if is_admin(message, user_id):
        get.step = 0
        text = f'Salom, *{first_name}*,\n*ABUTECH* topshiriq botiga xush kelibsiz!\n\n_Bot test rejimida ishlayapti!_'
        bot.send_message(user_id, text, parse_mode='Markdown', reply_markup=main_menu())
        get.step = 1
        get.save()


@bot.message_handler(regexp=btn['statistics'])
def show_stats(message):
    task_count = Tasks.objects.all().count()
    completed_task_count = CompletedTasks.objects.all().count()
    uncompleted_task_count = Tasks.objects.all().filter(is_completed=False).count()
    media_task_count = Tasks.objects.all().filter(team='Media', is_completed=True).count()
    marketing_task_count = Tasks.objects.all().filter(team='Marketing', is_completed=True).count()
    design_task_count = Tasks.objects.all().filter(team='Dizayn', is_completed=True).count()

    companies = Company.objects.values_list('name', flat=True)
    teams = Team.objects.values_list('name', flat=True)

    msg = 'Umumiy vazifalar soni: {}\n\n'.format(task_count)
    msg += '*Bajarildi:* {}\n'.format(completed_task_count)
    msg += '*Bajarilmagan:* {}\n\n'.format(uncompleted_task_count)
    msg += 'Jamoalar bo\'yicha\n'
    for i in teams:
        msg += f"*{i}:* {Tasks.objects.all().filter(team=i).count()}\n"

    bot.send_message(user_id, msg, parse_mode='Markdown')

    comp_msg = "Kompaniyalar bo'yicha\n\n"
    for i in companies:
        comp_msg += f"*{i}:* {Tasks.objects.all().filter(company=i).count()}\n"
    bot.send_message(user_id, comp_msg, parse_mode='Markdown')
    return main(message)


@bot.message_handler(regexp=btn['clean'])
def clean(message):
    if is_admin(message, user_id):
        get.step = 0
        for i in data:
            i = ''
        return main(message)


@bot.message_handler(func=lambda message: get.step == 1 or get.step == 11)
def company(message):
    # Faqat admin VA VAZIFA BERISH yuborilganda
    if is_admin(message, user_id):
        if message.text == btn['order_task']:
            global task_data
            text = "Kompaniyani tanlang"
            bot.send_message(user_id, text, reply_markup=company_menu())
            get.step = 2
        elif message.text == btn['send_tasks'] or get.step == 11:
            text = 'Topshiriq ID raqamini kiriting'
            bot.send_message(user_id, text, reply_markup=navigation_menu[1])
            get.step = 12


# ==========================SEND TASK=======================
@bot.message_handler(func=lambda message: get.step == 12, content_types='text')
def check_task_id(message):
    if is_admin(message, user_id):
        global id
        id = message.text
        find_id = Tasks.objects.filter(task_id=id).exists()
        if find_id:
            find_id = Tasks.objects.get(task_id=id)
            id_msg = "*TOPSHIRIQ ID: {} | Vaqt: {}*\n\n".format(id, find_id.created_at)
            id_msg += "*Kompaniya:* {}\n".format(find_id.company)
            id_msg += "*Jamoa:* {}\n".format(find_id.team)
            id_msg += "*Vazifa turi:* {}\n".format(find_id.task_type)
            id_msg += "*Yubordi:* {}\n".format(find_id.from_admin)

            text = 'Topshiriq topildi.\n\n*Iltimos uni to\'gri ekanini tekshiring*'

            bot.send_message(user_id, id_msg, parse_mode='Markdown', reply_markup=confirm_menu())
            bot.send_message(user_id, text, parse_mode='Markdown', reply_markup=confirm_menu())
            get.step = 13
        else:
            text = "Topshiriq topilmadi.\n_ID raqam xato. Bazadan tekshirib ko'ring_"
            bot.send_message(user_id, text, parse_mode='Markdown', reply_markup=hide_menu())
            get.step = 11
            return company(message)


# Completed task uchun migrate qilish
# TRY qo'yilishi mumkin if xatolik == True)
@bot.message_handler(func=lambda message: get.step == 13, regexp=btn['confirm'])
def complete_task(message):
    find_task = Tasks.objects.get(task_id=id)
    find_task.is_completed = True
    now = datetime.now().strftime("%d.%m.%Y, %H:%M")
    CompletedTasks.objects.create(completed_id=find_task.task_id, team=find_task.team,
                                              company=find_task.company, time=now)
    text = "Vazifa topshirildi"
    bot.send_message(user_id, text)
    return main(message)


# ==========================ORDER TASK=======================
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
            text = "Batafsil ma'lumot.\n\n*Diqqat:* _Audio yoki matnli xabar yoki ikkisini ham yuborishingiz mumkin_"
            finish_more = True
            get.step = 5
            # ============AUDIO yoki TEXT tekshirish==========
            bot.send_message(user_id, text, parse_mode='Markdown', reply_markup=hide_menu())
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
        data['more_voice'] = message.message_id  # Message ID forward uchun
        text = 'Ovozli izoh saqlandi. *Ortga qayting*'
        bot.send_message(user_id, text, parse_mode='Markdown', reply_markup=navigation_menu[0])
        # bot.forward_message(settings.CHANNEL, message.chat.id, message.message_id)


@bot.message_handler(func=lambda message: get.step == 5, content_types=['text'])
def get_more_text(message):
    if message.text == btn['back']:
        return task(message)
    if finish_more and message.text != btn['back']:
        data['more_text'] = message.text  # Message text saqladim, forward qilganda qo'shiladi
        text = 'Matnli izoh saqlandi. *Ortga qayting*'
        bot.send_message(user_id, text, parse_mode='Markdown', reply_markup=navigation_menu[0])

    elif finish_link and message.text != btn['back']:
        data['url'] = message.text  # URL saqlandi
        text = 'Link saqlandi. *Ortga qayting*'
        bot.send_message(user_id, text, parse_mode='Markdown', reply_markup=navigation_menu[0])

    elif finish_deadline == True and message.text != btn['back']:
        data['deadline'] = message.text
        text = 'Dedlayn saqlandi. *Ortga qayting*'
        bot.send_message(user_id, text, parse_mode='Markdown', reply_markup=navigation_menu[0])
    get.step = 3


@bot.message_handler(func=lambda message: get.step == 6, regexp=btn['next'])
def task_type(message):
    name = Team.objects.values_list('name', flat=True)
    # 0.Marketing, 1.Media, 2.Dizayn
    if data['team'] == name[0]:  # Marketing

        text = 'Vazifa turini tanlang.\n\n*Jamoa:* {}'.format(name[0])
        bot.send_message(user_id, text, parse_mode='Markdown', reply_markup=task_marketing_menu())
        get.step = 7
        is_mention = True
    if data['team'] == name[1]:  # Media
        get.step = 8
        text = 'Vazifa turini tanlang.\n\n*Jamoa:* {}'.format(name[1])
        bot.send_message(user_id, text, parse_mode='Markdown', reply_markup=task_media_menu())
    if data['team'] == name[2]:  # Dizayn
        get.step = 8
        text = 'Vazifa turini tanlang.\n\n*Jamoa:* {}'.format(name[2])
        bot.send_message(user_id, text, parse_mode='Markdown', reply_markup=task_design_menu())


#         Faqat marketingda mention qilish
@bot.message_handler(func=lambda message: get.step == 7, content_types=['text'])
def marketing_mention(message):
    data['task_type'] = message.text
    text = 'Kimga vazifa beramiz?\n\n*Diqqat*: Ushbu xodimga vazifa haqida xabar boradi!'
    bot.send_message(user_id, text, parse_mode='Markdown', reply_markup=marketing_mention_menu())
    get.step = 8


@bot.message_handler(func=lambda message: get.step == 8, content_types=['text'])
def confirm_task(message):
    get.step = 9
    if data['team'] == 'Marketing':
        data['mention'] = message.text
    else:
        data['task_type'] = message.text

    saved = '*Topshiriq ID:* {}\n\n'.format(data['id'])
    saved += '*Kompaniya:* {}\n'.format(data['company'])
    saved += '*Jamoa:* {}\n'.format(data['team'])
    saved += '*Dedlayn:* {}\n'.format(data['deadline'])
    saved += '*Vazifa turi:* {}\n'.format(data['task_type'])
    saved += '*Link:* {}\n'.format(data['url'])
    saved += '*Batafsil matn:* {}\n'.format(data['more_text'])
    if data['team'] == 'Marketing':
        saved += '*Kimga:* {}\n'.format(data['mention'])

    bot.send_message(user_id, saved, parse_mode='Markdown', reply_markup=confirm_menu())

    if data['more_voice'] is not " ":
        try:
            voice_msg = data['more_voice']
            bot.forward_message(user_id, user_id, data['more_voice'])
        except:
            pass
    else:
        pass

    text = "Saqlangan ma'lumotni tasdiqlang"
    bot.send_message(user_id, text, reply_markup=confirm_menu())


# Barchasi bazaga kiritiladi. Birma bir tartib joylashtirish
@bot.message_handler(func=lambda message: get.step == 9, regexp=btn['confirm'])
def save_data(message):
    send_mention = False

    user = Staff.objects.get(telegram_id=user_id)
    admin = user.first_name
    number = Tasks.objects.values_list('task_id', flat=True).last()
    task_id = number + 1
    # ======BAZAGA YANGI OBJECT CREATE======
    try:
        time = datetime.now().strftime("%d.%m.%Y, %H:%M")
        Tasks.objects.create(task_id=task_id, created_at=time, company=data['company'], team=data['team'], mention=data['mention'], task_type=data['task_type'], deadline=data['deadline'], link=data['url'], more=data['more_text'], from_admin=admin)
    except:
        print('ERROR')
        pass

    text = 'Ma\'lumotlar saqlandi!'
    bot.send_message(user_id, text, reply_markup=hide_menu())

    # ========KANALGA FORWARD QILISH======
    saved = ''
    saved = "*TOPSHIRIQ ID:* {} | *Vaqt:* {}\n\n".format(task_id, datetime.now().strftime("%d.%m.%Y, %H:%M"))
    saved +=  "*Kompaniya:* {}\n".format(data['company'])
    saved += "*Jamoa:* {}\n".format(data['team'])
    saved += "*Vazifa turi:* {}\n".format(data['task_type'])
    saved += "*Link:* {}\n".format(data['url'])
    saved += "*Batafsil:* {}\n".format(data['more_text'])
    saved += "*Dedlayn:* {}\n\n".format(data['deadline'])
    saved += "*Yubordi:* {} | @{}".format(message.chat.first_name, message.chat.username)
    if data['team'] == "Marketing":
        saved += "\n*Kim uchun:* {}".format(data['mention'])
        mention = Staff.objects.get(first_name=data['mention'])
        mention_id = mention.telegram_id
        print(mention_id)
        send_mention = True
    hash_name = data['company'].replace(" ", "")
    hash_name = hash_name.replace("'", "").capitalize()
    saved += "\n\n#{}\n#{}".format(hash_name, data['team'])
    bot.send_message(settings.CHANNEL, saved, parse_mode='Markdown', disable_web_page_preview=True,
                     disable_notification=False)
    if send_mention:
        bot.send_message(mention_id, saved, parse_mode='Markdown', disable_web_page_preview=True,
                         disable_notification=False)
    if data['more_voice'] is not " ":
        try:
            msg = data['more_voice']
            bot.forward_message(settings.CHANNEL, user_id, msg)
        except:
            pass




def failed(message):
    text = "Telegram ID bazasidan topilmadi. Ro'yhatdan o'tish uchun iltimos adminga (@abutechadmin) murojaat qiling!\n\nAbutech: @shoxruxmirzoo"
    bot.send_message(message.from_user.id, text, reply_markup=hide_menu())
    if not Unknown.objects.filter(telegram_id=user_id).exists():
        Unknown.objects.create(first_name=first_name, username=username, telegram_id=user_id).save()
    else:
        pass
