import logging
import pandas as pd
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка данных из CSV с указанием кодировки и разделителя
try:
    data = pd.read_csv('data.csv', encoding='latin1', delimiter=';')
    logger.info("Данные успешно загружены из data.csv")
except Exception as e:
    logger.error(f"Ошибка при загрузке данных из data.csv: {e}")

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["Адреси склад 📍", "Нархнома 💲"],
        ["Молҷои манъшуда ❌", "Контакт 👤"],
        ["Тафтиши трек-код 🔍"],
        ["Обуна шудан 👤"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text('Меню:', reply_markup=reply_markup)

# Функция для обработки сообщений с кнопок
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == "Адреси склад 📍":
        response = "1) НОМ ВА НОМЕРИ ШУМО \n2)15857907645\n3) 浙江省义乌市江东街道梅湖新村14栋3单元201室 sugd/ \n4)шахр/ном ва номери дастии шумо"
    elif text == "Нархнома 💲":
        response = "Нархнома:\n\n1кг - 2,5$\n\n1куб - 280$\n\nАз 500грам кам 20с"
    elif text == "Молҷои манъшуда ❌":
        response = "КАРГОИ МО ХАМИН ГУНА ЧИЗОРА ҚАБУЛ НАМЕКУНАД!\n\n1. Дорувори (парашок таблетка дорухои обаки).\n\n2. Ҳамаи намуди чизе ки обаки хастанд (Духи ва ғайра).\n\n3. Ҳамаи намуди силоҳи сард (корча, электрошокер ба монанди инхо, бита ва ғайра) умуман манъ аст.\n\n4. Электронный сигарет, калян ба монанди хамин чизо кабул намекунем.\n\nАгар ягон чизи шишагин дошта бошед пешаки бо админ маслихат кунед."
    elif text == "Контакт 👤":
        response = "Контакт : www.instagram.com/somon_sugd_cargo"
    elif text == "Тафтиши трек-код 🔍":
        response = "Введите трек-код:"
    elif text == "Обуна шудан 👤":
        response = "Обунаро ба дастгирӣ гирифтед!"
    else:
        response = "Неизвестная команда."

    await update.message.reply_text(response)

# Функция для проверки трек-кода
async def check_track_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    track_code = update.message.text
    logger.info(f"Получен трек-код: {track_code}")
    result = data[data['code'] == int(track_code)]
    logger.info(f"Результат поиска: {result}")

    if not result.empty:
        status_china = result['china'].values[0]
        status_khujand = result['khujand'].values[0]
        response = f"Трек-код: {track_code}\n"

        if status_khujand:
            response += "Ваш заказ по трек-коду прибыл в Худжанд, ожидайте звонка от оператора."
        elif status_china:
            response += "Ваш заказ по трек-коду прибыл в Китай и будет отправлен в Худжанд в ближайшие дни."
        else:
            response += "Ваш товар еще не пришел на склад."
    else:
        response = "Ваш трек-код не найден."

    logger.info(f"Ответ: {response}")
    await update.message.reply_text(response)

# Функция для команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Напишите /start для начала общения со мной.')

# Главная функция
def main():
    # Вставьте сюда токен, который вы получили от @BotFather
    TOKEN = '7463604205:AAFX7fk2JTk3UHrZQp0NBl9w9KOfebVBXd0'

    # Создаем объект Application и передаем ему токен вашего бота.
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Регистрируем обработчик сообщений с кнопок
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    # Регистрируем обработчик сообщений для трек-кодов
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(r'^\d+$'), check_track_code))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
