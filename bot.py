import logging
import pandas as pd
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ContextTypes

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка данных из CSV
data = pd.read_csv('data.csv')

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Адреси склад 📍", callback_data='address'), InlineKeyboardButton("Нархнома 💲", callback_data='prices')],
        [InlineKeyboardButton("Молҷои манъшуда ❌", callback_data='prohibited'), InlineKeyboardButton("Контакт 👤", callback_data='contact')],
        [InlineKeyboardButton("Тафтиши трек-код 🔍", callback_data='track_code')],
        [InlineKeyboardButton("Обуна шудан 👤", callback_data='subscribe')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Меню:', reply_markup=reply_markup)

# Функция для обработки нажатий на кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'address':
        await query.edit_message_text(text="Адреси склад: ...")
    elif data == 'prices':
        await query.edit_message_text(text="Нархнома: ...")
    elif data == 'prohibited':
        await query.edit_message_text(text="Молҷои манъшуда: ...")
    elif data == 'contact':
        await query.edit_message_text(text="Контакт: ...")
    elif data == 'track_code':
        await query.edit_message_text(text="Введите трек-код:")
    elif data == 'subscribe':
        await query.edit_message_text(text="Обунаро ба дастгирӣ гирифтед!")

async def check_track_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    track_code = update.message.text
    result = data[data['трек-код'] == int(track_code)]

    if not result.empty:
        status_china = result['Хитой'].values[0]
        status_khujand = result['Хучанд'].values[0]
        response = f"Трек-код: {track_code}\nХитой: {status_china}\nХучанд: {status_khujand}"
    else:
        response = "Трек-код не найден."

    await update.message.reply_text(response)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Напишите /start для начала общения со мной.')

def main():
    # Вставьте сюда токен, который вы получили от @BotFather
    TOKEN = '7463604205:AAFX7fk2JTk3UHrZQp0NBl9w9KOfebVBXd0'

    # Создаем объект Application и передаем ему токен вашего бота.
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Регистрируем обработчик нажатий на кнопки
    application.add_handler(CallbackQueryHandler(button))

    # Регистрируем обработчик сообщений
    application.add_handler(MessageHandler(Filters.text & ~Filters.command, check_track_code))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
