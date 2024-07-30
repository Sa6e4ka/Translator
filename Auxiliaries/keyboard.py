from aiogram.utils.keyboard import InlineKeyboardBuilder


def button(text : list):
    KB = InlineKeyboardBuilder()
    for i in text:
        KB.button(text=i, callback_data=i)
    KB.adjust(1,)
    return KB.as_markup()


'''
Клавиатура главного меню
'''
StartKB = InlineKeyboardBuilder()
buttons_list = ["Save words", "Learn words", "Delete words"]

for i in buttons_list:
    StartKB.button(text=i, callback_data=i)
StartKB.adjust(1,)