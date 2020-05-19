import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from .models import Tasks, CompletedTasks
from company.models import Staff, Team, Company, TaskType, Admins
from django.db.models import F
from .const import btn, STEPS, task_btn

from django.conf import settings


def hide_menu():
    return ReplyKeyboardRemove()


def navigation():
    button1 = ReplyKeyboardMarkup(True, True, row_width=2)
    button2 = ReplyKeyboardMarkup(True, True, row_width=2)
    back = [KeyboardButton(btn['back'])]
    clean = [KeyboardButton(btn['clean'])]
    button1.add(*back)
    button2.add(*clean)
    return [button1, button2]


def main_menu():
    buttons = ReplyKeyboardMarkup(True, True, row_width=2)
    key = [KeyboardButton(btn['order_task']),
           KeyboardButton(btn['send_tasks']),
           KeyboardButton(btn['statistics'])]
    buttons.add(*key)
    return buttons


def company_menu():
    buttons = ReplyKeyboardMarkup(True, True, row_width=3)
    name = Company.objects.values_list('name', flat=True)
    key = [KeyboardButton(text=text) for text in name]
    clean = KeyboardButton(btn['clean'])
    buttons.add(*key)
    buttons.add(clean)
    return buttons


def team_menu():
    buttons = ReplyKeyboardMarkup(True, True, row_width=3)
    name = Team.objects.values_list('name', flat=True)
    key = [KeyboardButton(text=text) for text in name]
    clean = KeyboardButton(btn['clean'])
    buttons.add(*key)
    buttons.add(clean)
    return buttons


def task_menu():
    buttons = ReplyKeyboardMarkup(True, True, row_width=3)
    name = task_btn
    key = [KeyboardButton(text=name[text]) for text in name]
    clean_next = [KeyboardButton(btn['next']),
                  KeyboardButton(btn['clean'])]
    buttons.add(*clean_next)
    buttons.add(*key)
    return buttons

def task_design_menu():
    buttons = ReplyKeyboardMarkup(True, True, row_width=3)
    name = TaskType.objects.all().filter(teamname__name='Dizayn')
    key = [KeyboardButton(text=str(text)) for text in name]
    clean = KeyboardButton(btn['clean'])
    buttons.add(*key)
    buttons.add(clean)
    return buttons


def task_media_menu():
    buttons = ReplyKeyboardMarkup(True, True, row_width=3)
    name = TaskType.objects.all().filter(teamname__name='Media')
    key = [KeyboardButton(text=str(text)) for text in name]
    clean = KeyboardButton(btn['clean'])
    buttons.add(*key)
    buttons.add(clean)
    return buttons


def task_marketing_menu():
    buttons = ReplyKeyboardMarkup(True, True, row_width=3)
    name = TaskType.objects.all().filter(teamname__name='Marketing')
    key = [KeyboardButton(text=str(text)) for text in name]
    clean = KeyboardButton(btn['clean'])
    buttons.add(*key)
    buttons.add(clean)
    return buttons


def marketing_mention_menu():
    buttons = ReplyKeyboardMarkup(True, True, row_width=3)
    name = Staff.objects.all().filter(team__name='Marketing')
    key = [KeyboardButton(text=str(text)) for text in name]
    clean = KeyboardButton(btn['clean'])
    buttons.add(*key)
    buttons.add(clean)
    return buttons


def confirm_menu():
    buttons = ReplyKeyboardMarkup(True, True, row_width=3)
    clean = KeyboardButton(btn['clean'])
    key = KeyboardButton(btn['confirm'])
    buttons.add(key, clean)

    return buttons


def task_menu_name():
    name = task_btn
    key = []
    for i in name:
        key.append(name[i])
    return key
