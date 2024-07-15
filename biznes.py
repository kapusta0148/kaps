import telebot
from telebot import types
import requests

data = {}
ide = []
crypto = []
banka = []
otzov = ["Бот заебись", "10 баллов из 10", "всем советую", "Ок", "Кок"]
name1 = []
symma = 0
symma1 = 0
symma2 = 0
symma3 = 0
symma4 = 0
symma5 = 0
symma6 = 0
ton_price_rub = 0
not_price_rub = 0
eth_price_rub = 0
btc_price_rub = 0
trx_price_rub = 0
ltc_price_rub = 0

bot = telebot.TeleBot('7080942322:AAFDP0zVLBSes-fn5X1SMCIcb72WwRv53AU')


@bot.message_handler(commands=["restart"])
def restart(message):
    bot.send_message(-4256642266, f"Пользователь @{' '.join(name1)} отменил покупку.")
    bot.send_message(message.chat.id, f"Вы начали заново.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button2 = types.KeyboardButton("Выбрать криптовалюту")
    button3 = types.KeyboardButton("Price")
    button4 = types.KeyboardButton("Help")
    button5 = types.KeyboardButton("Отзывы")
    markup.add(button2, button3, button4, button5)
    bot.send_message(message.chat.id, f'👇👇👇', reply_markup=markup)
    global symma
    symma = symma * 0
    crypto.clear()
    ide.clear()
    banka.clear()
    name1.clear()
    bot.register_next_step_handler(message, vubor)


@bot.message_handler(commands=["start"])
def start(message):
    name = message.from_user.username
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button2 = types.KeyboardButton("Выбрать криптовалюту")
    button3 = types.KeyboardButton("Price")
    button4 = types.KeyboardButton("Help")
    button5 = types.KeyboardButton("Отзывы")
    markup.add(button2, button3, button4, button5)
    bot.send_message(message.chat.id, f'Здравствуйте, @{name}, этот бот поможет тебе купить '
                                      f'криптовалюту даже если тебе нет 18 лет. '
                                      f'Но прежде чем перейти к покупке важно знать некоторые правила:\n'
                                      f'1) Если вы хотите купить не целое количество валюты, то '
                                      f'писать количество нужно через точку. Пример: 0.1\n'
                                      f'2) Вам нужно иметь свой ID кошелька, чтобы его получить, создайте'
                                      f' криптокошелёк, создать его можно по этой ссылке --> https://t.me/wallet\n'
                                      f'3) Если на каком-то из этапов покупки вы захотите отменить покупку'
                                      f'просто пропишете эту команду --> /restart\n'
                                      f'4) Если у вас есть вопрос то задайте его мне https://t.me/kapusta0148\n',
                     reply_markup=markup)


def get_bybit_price(symbol):
    url = f"https://api.bybit.com/v2/public/tickers?symbol={symbol}USDT"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and data['ret_code'] == 0:
        return float(data['result'][0]['last_price'])
    else:
        print(f"Ошибка получения цены {symbol}: {data.get('ret_msg')}")
        return None


def get_usdt_rub_rate():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    data = response.json()
    return float(data['Valute']['USD']['Value'])


def update_prices():
    global ton_price_rub, not_price_rub, eth_price_rub, btc_price_rub, trx_price_rub, ltc_price_rub
    ton_price_usdt = get_bybit_price("TON")
    not_price_usdt = get_bybit_price("NOT")
    eth_price_usdt = get_bybit_price("ETH")
    btc_price_usdt = get_bybit_price("BTC")
    trx_price_usdt = get_bybit_price("TRX")
    ltc_price_usdt = get_bybit_price("LTC")
    usdt_rub = get_usdt_rub_rate()

    if all([ton_price_usdt, not_price_usdt, eth_price_usdt, btc_price_usdt, trx_price_usdt, ltc_price_usdt,  usdt_rub]):
        ton_price_rub = ton_price_usdt * usdt_rub
        not_price_rub = not_price_usdt * usdt_rub
        eth_price_rub = eth_price_usdt * usdt_rub
        btc_price_rub = btc_price_usdt * usdt_rub
        trx_price_rub = trx_price_usdt * usdt_rub
        ltc_price_rub = ltc_price_usdt * usdt_rub
    else:
        print("Ошибка получения цен. Глобальные переменные не обновлены.")


@bot.message_handler(content_types=["text"])
def vubor(message):
    name = message.from_user.username
    name1.append(name)
    if message.text == "Выбрать криптовалюту":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button10 = types.KeyboardButton("TON")
        button11 = types.KeyboardButton("ETH")
        button13 = types.KeyboardButton("BTC")
        button14 = types.KeyboardButton("TRX")
        button15 = types.KeyboardButton("NOT")
        button16 = types.KeyboardButton("LTC")
        markup.add(button10, button11, button13, button14, button15, button16)
        bot.send_message(message.chat.id, f"Выберите из списка подходящую валюту, которую вы бы хотели приобрести."
                                          f"👇👇", reply_markup=markup)
        bot.register_next_step_handler(message, handle_text)
    elif message.text == "Help":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button17 = types.KeyboardButton("назад")
        markup.add(button17)
        bot.send_message(message.chat.id, f"При возникновении тех. проблем или вопросов по эксплуатации бота, "
                                          f"напишите нашему тех. менеджеру: "
                                          f"https://t.me/kapusta0148", reply_markup=markup)
        bot.register_next_step_handler(message, back)
    elif message.text == "Price":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button17 = types.KeyboardButton("назад")
        markup.add(button17)
        update_prices()
        bot.send_message(message.chat.id,
                         f"💰 *Цены на Bybit в рублях:*\n\n"
                         f"TON: {ton_price_rub:.2f} RUB\n"
                         f"NOT: {not_price_rub:.2f} RUB\n"
                         f"ETH: {eth_price_rub:.2f} RUB\n"
                         f"BTC: {btc_price_rub:.2f} RUB\n"
                         f"TRX: {trx_price_rub:.2f} RUB\n"
                         f"LTC: {ltc_price_rub:.2f} RUB\n",
                         reply_markup=markup)
        bot.register_next_step_handler(message, back)
    elif message.text == "Отзывы":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button17 = types.KeyboardButton("Следующий отзыв")
        button18 = types.KeyboardButton("назад")
        markup.add(button17, button18)
        bot.send_message(message.chat.id, f"{' '.join(otzov[0:1])}", reply_markup=markup)
        del otzov[0:1]
        bot.register_next_step_handler(message, back)


def back(message):
    if message.text == "назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button2 = types.KeyboardButton("Выбрать криптовалюту")
        button3 = types.KeyboardButton("Price")
        button4 = types.KeyboardButton("Help")
        button5 = types.KeyboardButton("Отзывы")
        markup.add(button2, button3, button4, button5)
        bot.send_message(message.chat.id, f'Вы вернулись назад  ', reply_markup=markup)
    elif message.text == "Следующий отзыв":
        if len(otzov) == 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button17 = types.KeyboardButton("назад")
            markup.add(button17)
            bot.send_message(message.chat.id, "Отзывы закончились.", reply_markup=markup)
            bot.register_next_step_handler(message, back)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button17 = types.KeyboardButton("Следующий отзыв")
            button18 = types.KeyboardButton("назад")
            markup.add(button17, button18)
            bot.send_message(message.chat.id, f"{' '.join(otzov[0:1])}", reply_markup=markup)
            del otzov[0:1]
            bot.register_next_step_handler(message, back)


def handle_text(message):
    update_prices()
    if message.text == "TON":
        global symma
        symma = symma + ton_price_rub
        crypto.append("TON")
    elif message.text == "ETH":
        global symma1
        symma = symma1 + eth_price_rub
        crypto.append("ETH")
    elif message.text == "BTC":
        global symma3
        symma = symma3 + btc_price_rub
        crypto.append("BTC")
    elif message.text == "TRX":
        global symma4
        symma = symma4 + trx_price_rub
        crypto.append("TRX")
    elif message.text == "NOT":
        global symma5
        symma = symma5 + not_price_rub
        crypto.append("NOT")
    elif message.text == "LTC":
        global symma6
        symma = symma6 + ltc_price_rub
        crypto.append("LTC")
    bot.reply_to(message, "Следующим шагом пришлите нам название вашего банка, через который будет проводиться оплата🏦",
                 reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_bank)


def get_bank(message):
    if message.text == "/restart":
        bot.send_message(-4256642266, f"Пользователь @{' '.join(name1)} отменил покупку.")
        bot.send_message(message.chat.id, f"Вы начали заново.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button2 = types.KeyboardButton("Выбрать криптовалюту")
        button3 = types.KeyboardButton("Price")
        button4 = types.KeyboardButton("Help")
        button5 = types.KeyboardButton("Отзывы")
        markup.add(button2, button3, button4, button5)
        bot.send_message(message.chat.id, f'👇👇👇', reply_markup=markup)
        global symma
        symma = symma * 0
        crypto.clear()
        ide.clear()
        banka.clear()
        name1.clear()
        bot.register_next_step_handler(message, vubor)
    else:
        bank = message.text
        banka.append(bank)
        bot.send_message(message.chat.id, f"Сколько вы хотите купить {' '.join(crypto)} ?")
        bot.register_next_step_handler(message, get_id)


def get_id(message):
    if message.text == "/restart":
        bot.send_message(-4256642266, f"Пользователь @{' '.join(name1)} отменил покупку.")
        bot.send_message(message.chat.id, f"Вы начали заново.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button2 = types.KeyboardButton("Выбрать криптовалюту")
        button3 = types.KeyboardButton("Price")
        button4 = types.KeyboardButton("Help")
        button5 = types.KeyboardButton("Отзывы")
        markup.add(button2, button3, button4, button5)
        bot.send_message(message.chat.id, f'👇👇👇', reply_markup=markup)
        global symma
        symma = symma * 0
        crypto.clear()
        ide.clear()
        banka.clear()
        name1.clear()
        bot.register_next_step_handler(message, vubor)
    else:
        data[message.chat.id] = {"id": message.text}
        bot.send_message(message.chat.id, "Назовите id вашего кошелька.")
        bot.register_next_step_handler(message, get_info)


def get_info(message):
    if message.text == "/restart":
        bot.send_message(-4256642266, f"Пользователь @{' '.join(name1)} отменил покупку.")
        bot.send_message(message.chat.id, f"Вы начали заново.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button2 = types.KeyboardButton("Выбрать криптовалюту")
        button3 = types.KeyboardButton("Price")
        button4 = types.KeyboardButton("Help")
        button5 = types.KeyboardButton("Отзывы")
        markup.add(button2, button3, button4, button5)
        bot.send_message(message.chat.id, f'👇👇👇', reply_markup=markup)
        global symma
        symma = symma * 0
        crypto.clear()
        ide.clear()
        banka.clear()
        name1.clear()
        bot.register_next_step_handler(message, vubor)
    else:
        colvo = message.text
        data[message.chat.id]['colvo'] = colvo
        ide.append(colvo)
        rub = float(data[message.chat.id]['id'])
        bot.send_message(message.chat.id, f"Вы хотите купить: {data[message.chat.id]['id']} {' '.join(crypto)}\n"
                                          f"Это будет стоит: {(rub * symma) + (rub * symma) / 10} rub\n"
                                          f"ID вашего кошелшька: {colvo} \n"
                                          f"Имя вашего банка: {' '.join(banka)}\n"
                                          f"Если все данные верны нажмите продолжить если нет нажмите вернуться.\n")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button5 = types.KeyboardButton("продолжить")
        button6 = types.KeyboardButton("назад")
        markup.add(button5, button6)
        bot.send_message(message.chat.id, f'👇👇👇 ', reply_markup=markup)
        bot.register_next_step_handler(message, finaly)


def finaly(message):
    if message.text == "продолжить":
        rub = float(data[message.chat.id]['id'])
        bot.send_message(-4256642266, f"Количество: {data[message.chat.id]['id']} {' '.join(crypto)}\n"
                                      f"ID кошелька: {' '.join(ide)}\n"
                                      f"Имя банка: {' '.join(banka)}\n"
                                      f"Стоимость: {(rub * symma) + (rub * symma) / 10} rub\n"
                                      f"Имя: @{' '.join(name1)}\n")
        bot.send_message(message.chat.id, f"Отлично теперь вам нужно отправить {(rub * symma) + (rub * symma) / 10} RUB"
                                          f" на этот номер карты: 123456789 после того как вы отправили всю сумму"
                                          f"вам нужно прислать в этот бот фото квитанции именно квитанцию, скрин "
                                          f"перевода не подойдёт. Если вы хотите отменить покупку нажмите сюда --> "
                                          f"/restart",
                         reply_markup=telebot.types.ReplyKeyboardRemove())

    elif message.text == "назад":
        bot.reply_to(message, "Что вы хотите исправить?")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button7 = types.KeyboardButton(f"Количество {' '.join(crypto)}")
        button8 = types.KeyboardButton("ID вашего кошелька")
        button9 = types.KeyboardButton("Название вашего банка")
        button10 = types.KeyboardButton("Криптовалюту")
        markup.add(button7, button8, button9, button10)
        bot.send_message(message.chat.id, f'👇👇👇 ', reply_markup=markup)
        bot.register_next_step_handler(message, notfinaly)


def notfinaly(message):
    if message.text == f"Количество {' '.join(crypto)}":
        bot.send_message(message.chat.id, f'введите нужное количество')
        bot.register_next_step_handler(message, notfinaly2)
    elif message.text == "ID вашего кошелька":
        bot.send_message(message.chat.id, f'введите верный id кошелька')
        bot.register_next_step_handler(message, notfinaly3)
    elif message.text == "Название вашего банка":
        bot.send_message(message.chat.id, f'введите верное название вашего банка')
        bot.register_next_step_handler(message, notfinaly4)
    elif message.text == "Криптовалюту":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button10 = types.KeyboardButton("TON")
        button11 = types.KeyboardButton("ETH")
        button12 = types.KeyboardButton("GRAM")
        button13 = types.KeyboardButton("BTC")
        button14 = types.KeyboardButton("TRX")
        button15 = types.KeyboardButton("NOT")
        button16 = types.KeyboardButton("LTC")
        markup.add(button10, button11, button12, button13, button14, button15, button16)
        bot.send_message(message.chat.id, f"Пожайлуста выберите одну из этих валют👇👇", reply_markup=markup)
        global symma
        symma = symma * 0
        crypto.clear()
        bot.register_next_step_handler(message, notfinaly5)


def notfinaly2(message):
    data[message.chat.id] = {"id": message.text}
    rub = float(data[message.chat.id]['id'])
    bot.send_message(message.chat.id, f"Вы хотите купить: {data[message.chat.id]['id']} {' '.join(crypto)}\n"
                                      f"Это будет стоит: {(rub * symma) + (rub * symma) / 10} rub\n"
                                      f"ID вашего кошелшька: {' '.join(ide)} \n"
                                      f"Имя вашего банка: {' '.join(banka)}\n"
                                      f"Если все данные верны нажмите продолжить если нет нажмите вернуться.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button5 = types.KeyboardButton("продолжить")
    button6 = types.KeyboardButton("назад")
    markup.add(button5, button6)
    bot.send_message(message.chat.id, f'👇👇👇 ', reply_markup=markup)
    bot.register_next_step_handler(message, finaly)


def notfinaly3(message):
    colvo = message.text
    data[message.chat.id]['colvo'] = colvo
    ide.clear()
    ide.append(colvo)
    rub = float(data[message.chat.id]['id'])
    bot.send_message(message.chat.id, f"Вы хотите купить: {data[message.chat.id]['id']} {' '.join(crypto)}\n"
                                      f"Это будет стоит: {(rub * symma) + (rub * symma) / 10} rub\n"
                                      f"ID вашего кошелшька: {colvo} \n"
                                      f"Имя вашего банка: {' '.join(banka)}\n"
                                      f"Если все данные верны нажмите продолжить если нет нажмите вернуться.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button5 = types.KeyboardButton("продолжить")
    button6 = types.KeyboardButton("назад")
    markup.add(button5, button6)
    bot.send_message(message.chat.id, f'👇👇👇 ', reply_markup=markup)
    bot.register_next_step_handler(message, finaly)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo = message.photo[-1]
    file_id = photo.file_id
    bot.send_photo(-4256642266, f"{file_id}", f"@{' '.join(name1)}")
    bot.send_message(message.chat.id, "Отлично ожидайте, в течении 10 минут вам придёт ваша криптовалюта, а пока можете"
                                      " оставить свой отзыв написав его в этот бот.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button2 = types.KeyboardButton("Я хочу оставить отзыв")
    button3 = types.KeyboardButton("Я не хочу оставлять отзыв")
    markup.add(button2, button3)
    bot.send_message(message.chat.id, f'Для этого выберите 👇👇', reply_markup=markup)
    bot.register_next_step_handler(message, vuborot)


def notfinaly4(message):
    bank = message.text
    banka.clear()
    banka.append(bank)
    rub = float(data[message.chat.id]['id'])
    bot.send_message(message.chat.id, f"Вы хотите купить: {data[message.chat.id]['id']} {' '.join(crypto)}\n"
                                      f"Это будет стоит: {(rub * symma) + (rub * symma) / 10} rub\n"
                                      f"ID вашего кошелшька: {' '.join(ide)} \n"
                                      f"Имя вашего банка: {' '.join(banka)}\n"
                                      f"Если все данные верны нажмите продолжить если нет нажмите назад.\n")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button5 = types.KeyboardButton("продолжить")
    button6 = types.KeyboardButton("назад")
    markup.add(button5, button6)
    bot.send_message(message.chat.id, f'👇👇👇 ', reply_markup=markup)
    bot.register_next_step_handler(message, finaly)


def notfinaly5(message):
    if message.text == "TON":
        global symma
        symma = symma + ton_price_rub
        crypto.append("TON")
    elif message.text == "ETH":
        global symma1
        symma = symma1 + eth_price_rub
        crypto.append("ETH")
    elif message.text == "BTC":
        global symma3
        symma = symma3 + btc_price_rub
        crypto.append("BTC")
    elif message.text == "TRX":
        global symma4
        symma = symma4 + trx_price_rub
        crypto.append("TRX")
    elif message.text == "NOT":
        global symma5
        symma = symma5 + not_price_rub
        crypto.append("NOT")
    elif message.text == "LTC":
        global symma6
        symma = symma6 + ltc_price_rub
        crypto.append("LTC")
    rub = float(data[message.chat.id]['id'])
    bot.send_message(message.chat.id, f"Вы хотите купить: {data[message.chat.id]['id']} {' '.join(crypto)}\n"
                                      f"Это будет стоит: {(rub * symma) + (rub * symma) / 10} rub\n"
                                      f"ID вашего кошелшька: {' '.join(ide)} \n"
                                      f"Имя вашего банка: {' '.join(banka)}\n"
                                      f"Если все данные верны нажмите продолжить если нет нажмите вернуться.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button5 = types.KeyboardButton("продолжить")
    button6 = types.KeyboardButton("назад")
    markup.add(button5, button6)
    bot.send_message(message.chat.id, f'👇👇👇 ', reply_markup=markup)
    bot.register_next_step_handler(message, finaly)


def vuborot(message):
    if message.text == 'Я хочу оставить отзыв':
        bot.send_message(message.chat.id, "Напишите ваш отзыв.")
        bot.register_next_step_handler(message, vuborot1)
    elif message.text == "Я не хочу оставлять отзыв":
        bot.send_message(message.chat.id, f'Очень жаль(')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button2 = types.KeyboardButton("Выбрать криптовалюту")
        button3 = types.KeyboardButton("Price")
        button4 = types.KeyboardButton("Help")
        button5 = types.KeyboardButton("Отзывы")
        markup.add(button2, button3, button4, button5)
        bot.send_message(message.chat.id, f'👇👇👇', reply_markup=markup)
        global symma
        symma = symma * 0
        crypto.clear()
        ide.clear()
        banka.clear()
        name1.clear()
        bot.register_next_step_handler(message, vubor)


def vuborot1(message):
    indt = message.text
    bot.send_message(-4256642266, indt)
    bot.send_message(message.chat.id, f'Спасибо за отзыв!')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button2 = types.KeyboardButton("Выбрать криптовалюту")
    button3 = types.KeyboardButton("Price")
    button4 = types.KeyboardButton("Help")
    button5 = types.KeyboardButton("Отзывы")
    markup.add(button2, button3, button4, button5)
    bot.send_message(message.chat.id, f'👇👇👇', reply_markup=markup)
    global symma
    symma = symma * 0
    crypto.clear()
    ide.clear()
    banka.clear()
    name1.clear()
    bot.register_next_step_handler(message, vubor)


bot.infinity_polling()
