# This Python file uses the following encoding: utf-8
from aiogram import Dispatcher, Bot, executor, types
from db import Database
from datetime import datetime
import random


TOKEN = '################################'


bot = Bot(TOKEN)
dp = Dispatcher(bot)
db = Database('regestrationdb.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if(not db.user_exists(message.from_user.id)):
        print('start')
        db.adduser(message.from_user.id)
        await bot.send_message(message.from_user.id, text='Привет! Укажи свой класс (номер и букву слитно)\nstart - запуск бота\n/week - отправляет расписание на неделю\n/today - отправлет расписание на сегодня\n/calls - Расписание звонков первой смены; /calls2 - второй\n/tomorrow - отправляет расписание на завтра\n/class - выбрать/изменить свой класс\n/help - отправляет вседоступные команды\nБот предназначен для учащихся 5-11 классов!')
    else:
        await bot.send_message(message.from_user.id, text='Друг, ты уже зарегистрирован!')
    

@dp.message_handler(commands=['class'])
async def classs(message: types.Message):
    print('class')
    if db.user_exists(message.from_user.id) == True:
        db.set_signup(message.from_user.id, "setclass")
        await bot.send_message(message.from_user.id, text='Введите новый класс (например 8Д, 11А)')
    else:
        db.adduser(message.from_user.id)
        db.set_signup(message.from_user.id, "setclass")
        await bot.send_message(message.from_user.id, text='Введите новый класс (например 8Д, 11А)')
        

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
   await bot.send_message(message.from_user.id, text='Расписание на каждый день под рукой\n/start - запуск бота\n/week - отправляет расписание на неделю\n/today - отправлет расписание на сегодня\n/calls - Расписание звонков первой смены; /calls2 - второй\n/tomorrow - отправляет расписание на завтра\n/class - выбрать/изменить свой класс\n/help - отправляет вседоступные команды')

@dp.message_handler(commands=['today'])
async def today(message: types.Message):
    if db.user_exists(message.from_user.id) == True:
        print('today')
        if db.get_signup(message.from_user.id) == 'setclass':
            await bot.send_message(message.from_user.id, text='Укажи свой класс (/class)')
        else:
            now = datetime.now() 
            dw = datetime.isoweekday(now)
            if dw == 6 or dw == 7:
                await bot.send_message(message.from_user.id, text='Сегодня выходной! Хорошего отдыха!') 
            else:    
                try:
                    await bot.send_message(message.from_user.id, text='Расписание на сегодня:\n\n'+db.shedule(message.from_user.id, dw))
                except:
                    await bot.send_message(message.from_user.id, text='Ошибка. Скорее всего, вы указали несуществующий класс. Если вы указали существующий класс - пишите в тех. поддержку')
    else:
        db.adduser(message.from_user.id)
        db.set_signup(message.from_user.id, "setclass")
        await bot.send_message(message.from_user.id, text='Введите новый класс (например 8Д, 11А)')


@dp.message_handler(commands=['tomorrow'])
async def today(message: types.Message):
    if db.user_exists(message.from_user.id) == True:
        if db.get_signup(message.from_user.id) == '':
            await bot.send_message(message.from_user.id, text='Что-то странное. Попробуй указать класс снова')
        elif db.get_signup(message.from_user.id) == 'setclass':
            await bot.send_message(message.from_user.id, text='Укажи свой класс (/class)')
        else:
            print('tomorrow')
            now = datetime.now() 
            dw = datetime.isoweekday(now) + 1
            if dw == 8:
                dw = 1 
            if dw == 6 or dw == 7:
                await bot.send_message(message.from_user.id, text='Завтра выходной! Хорошего отдыха!')
            else:
                try:
                    await bot.send_message(message.from_user.id, text='Расписание на завтра:\n\n'+db.shedule(message.from_user.id, dw))
                except:
                    await bot.send_message(message.from_user.id, text='Ошибка. Скорее всего, вы указали несуществующий класс. Если вы указали существующий класс - пишите в тех. поддержку')
    else:
        db.adduser(message.from_user.id)
        db.set_signup(message.from_user.id, "setclass")
        await bot.send_message(message.from_user.id, text='Введите новый класс (например 8Д, 11А)')

@dp.message_handler(commands=['week'])
async def today(message: types.Message):
    if db.user_exists(message.from_user.id) == True:
        if db.get_signup(message.from_user.id) == '':
            await bot.send_message(message.from_user.id, text='Что-то странное. Попробуй указать класс снова')
        elif db.get_signup(message.from_user.id) == 'setclass':
            await bot.send_message(message.from_user.id, text='Укажи свой класс (/class)')
        else:
            print('week')
            try:
                await bot.send_message(message.from_user.id, text='Расписание на неделю:'+db.shedule(message.from_user.id, 0, week=True))
            except:
                await bot.send_message(message.from_user.id, text='Ошибка. Скорее всего, вы указали несуществующий класс. Если вы указали существующий класс - пишите в тех. поддержку')
    else:
        db.adduser(message.from_user.id)
        db.set_signup(message.from_user.id, "setclass")
        await bot.send_message(message.from_user.id, text='Введите новый класс (например 8Д, 11А)')

@dp.message_handler(commands=['calls'])
async def today(message: types.Message): 
    await bot.send_message(message.from_user.id, text='1 смена:\n1 урок | 8:30 - 9:10\n2 урок | 9:25 - 10:05\n3 урок | 10:25 - 11:05\n4 урок | 11:25 - 12:05\n5 урок | 12:20 - 13:00\n6 урок | 13:30 - 14:10\n7 урок | 14:20 - 15:00\n8 урок | 15:20 - 16:00')
@dp.message_handler(commands=['calls2'])
async def today(message: types.Message): 
    await bot.send_message(message.from_user.id, text='2 смена:\n1 урок | 13:30 - 14:10\n2 урок | 14:20 - 15:00\n3 урок | 15:20 - 16:00\n4 урок | 16:10 - 16:50\n5 урок | 17:00 - 17:40\n6 урок | 17:50 - 18:30')

@dp.message_handler(commands=['sendall'])
async def sendall(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == 1221912187:
            text = message.text[9:]
            us = db.get_users()
            if 'Расписание' in text and '!!!' in text:
                for row in us:
                    try:
                        print(db.get_signup(row[0]))
                        if db.get_signup(row[0]) == "('setclass',)":
                            await bot.send_message((row[0]), text='Чтобы получать рассылку, нужно указать класс!')
                        else:
                            if 'на завтра!!!' in text:
                                await bot.send_message((row[0]), 'Расписание на завтра:\n\n'+db.shedule(row[0], int(text[0])))    
                            else:
                                await bot.send_message((row[0]), 'Расписание на сегодня:\n\n'+db.shedule(row[0], int(text[0])))
                        db.set_active(row[0], 1)
                    except:
                        db.set_active(row[0], 0)
                await bot.send_message(message.from_user.id, "Успешная рассылка")
            
            elif 'Класс!!!' in text:
                us = db.get_users(1)
                for row in us:
                    try:
                        await bot.send_message((row[0]), 'Напоминаю, что рассылка расписания работает для пользователей, указавших класс. Укажите класс /class')
                        if int(row[0]) != 1:
                            db.set_active(row[0], 1)
                    except:
                        db.set_active(row[0], 0)
                await bot.send_message(message.from_user.id, "Успешная рассылка")

            elif '8Д ДЗ' in text:
                text = message.text[15:]
                us = db.get_users(t=2)
                for row in us:
                    try:
                        await bot.send_message((row[0]), 'ДЗ для 8Д на завтра:\n\n'+text)
                        if int(row[0]) != 1:
                            db.set_active(row[0], 1)
                    except:
                        db.set_active(row[0], 0)
                await bot.send_message(message.from_user.id, "Успешная рассылка")

            else:
                for row in us:
                    try:
                        await bot.send_message((row[0]), text)
                        if int(row[0]) != 1:
                            db.set_active(row[0], 1)
                    except:
                        db.set_active(row[0], 0)
                await bot.send_message(message.from_user.id, "Успешная рассылка")


@dp.message_handler(content_types=['text'])
async def bot_message(message):
    if message.chat.type == 'private':
        a = message.text+' '
        a = a.upper()
        print(a)
        try:
            if 2 <= len(message.text) <= 3  and (message.text[0]) in ['8','9','1', '5', '6', '7'] and (a[1] in ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'И'] or a[2] in ['А', 'Б', 'В', 'Г', 'Д']):
                db.set_class(message.from_user.id, message.text.upper())
                db.set_signup(message.from_user.id, 'done')
                await bot.send_message(message.from_user.id, text='Класс сохранен')   
            else:
                b = random.randint(1,100)
                if b > 98:
                    await bot.send_message(message.from_user.id, text='БИ ДЕ!')
                else:
                    if 'ПРИВЕТ' in a or 'ДАРОВА' in a or 'ХАЙ' in a:
                        await bot.send_message(message.from_user.id, text='Хааай. Чё как?')
                    elif 'НОРМ' in a or 'ХОРОШО' in a:
                        await bot.send_message(message.from_user.id, text='Ясно!')
                    elif 'КАК ДЕЛА' in a or 'А ТЫ?' in a or 'А У ТЕБЯ' in a:
                        await bot.send_message(message.from_user.id, text='Нормально в целом')
                    elif 'ТЕБЯ' in a and 'ЗОВУТ' in a:
                        await bot.send_message(message.from_user.id, text='Меня зовут Сюзамен. Приятно познакомиться')
                    elif 'ИДИ НАХУЙ' in a or 'ПОШЁЛ НАХУЙ' in a:
                        await bot.send_message(message.from_user.id, text='Ахахаха, сам иди, тухлич')
                    elif 'ХУЙ' in a or 'БЛЯ' in a or 'ПИЗД' in a or 'ДОЛБОЁ' in a or 'ПОРН' in a or 'ГЕЙ' in a or 'МУДАК' in a or 'МУДЕНЬ' in a:
                        await bot.send_message(message.from_user.id, text='Как некультурно :(')
                    elif 'ПОН' in a:
                        await bot.send_message(message.from_user.id, text='Есть моментик!')
                    elif 'АХА' in a or 'ХАХ' in a or 'ХИХ' in a or 'ИХИ' in a:
                        await bot.send_message(message.from_user.id, text=':)')
                    elif 'СПАСИБО' in a or 'СПС' in a:
                        a = random.randint(1,2)
                        if a == 1:
                            await bot.send_message(message.from_user.id, text='Да не за что :)')        
                        else:
                            await bot.send_message(message.from_user.id, text='Пожалуйста :)')    
                    elif 'ТЫ ДЕВОЧКА?' in a or 'ТЫ ДЕВУШКА' in a:
                        await bot.send_message(message.from_user.id, text='Так точно!')
                    elif 'ТЫ' in a and ('МАЛЬЧИК' in a or 'ДЕВОЧКА' in a or 'ПОЛА' in a):
                        await bot.send_message(message.from_user.id, text='Я Сюзаменн!')
                    elif 'ВЫГЛЯДИШЬ' in a:
                        await bot.send_message(message.from_user.id, text='На аватарке - я!')
                    elif 'ФОТО' in a:
                        await bot.send_message(message.from_user.id, text='Я есть на аватарке')
                    elif 'ДА' in a or 'НЕТ' in a:
                        await bot.send_message(message.from_user.id, text='Пон')
                    elif 'ЛОХ' in a:
                        await bot.send_message(message.from_user.id, text='Сам')
                    elif db.get_signup(message.from_user.id) == 'setclass':
                        await bot.send_message(message.from_user.id, text='Класс указан некорректно!')


        except:
            await bot.send_message(message.from_user.id, text='Хм....')  

            
        
                         

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
