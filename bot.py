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
        ["Сурогаи склад роҳ  🚚", "Сурогаи склад авиа✈️", "Нархнома 💲"],
        ["Молҳои манъшуда ❌", "Контакт 👤"],
        ["Тафтиши трек-код 🔍", "Дарси ройгон!"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text('Хуш омадед ба Telegram боти  Сомон Сугд Карго. Ман ба шумо дар ёфтани суроғаҳои анбор, санҷидани трек код ва бо нархҳо шинос шудан кӯмак мекунам', reply_markup=reply_markup)

# Функция для обработки сообщений с кнопок
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == "Сурогаи склад роҳ  🚚":
        response = "1) AL-KH \n2)13711652794\n3) 广州市荔湾区环市西路黑山三街20号宇宙鞋城E区113-119档8 Al-Kh /Шахр/Ном ва номери телефон"
        await update.message.reply_text(response)
        await update.message.reply_photo("https://raw.githubusercontent.com/uskhurshed/cargo/master/photo_2024-10-08_19-49-26.jpg")

    if text == "Сурогаи склад авиа✈️":
        response = "Avia / Ном ВА номери шумо \n19068507113\n浙江省 金华市 义乌市\n桥东二区34栋8号 1 avia Al-Kh / Шахр Ном ВА немери шумо"
        await update.message.reply_text(response)
        await update.message.reply_photo("https://raw.githubusercontent.com/uskhurshed/cargo/master/photo_5406973989118667037_y.jpg")


    elif text == "Нархнома 💲":
        response = "РОҲ\n> Аз 1кг то 40кг  - 3$ \n> Аз 40кг зиёд  - 2,8$\n> Аз 100кг зиёд алохида нарх дода мешавад\n> Аз 1куб 300$\n\nАВИА\n\nСрок доставки: 7-13 дней 🚀\n• 10$\кг\n• До 31.12.2024 — всего 9$\кг 🎉"
        await update.message.reply_text(response)
        await update.message.reply_photo("https://raw.githubusercontent.com/uskhurshed/cargo/master/Нарх2.png")

    elif text == "Молҳои манъшуда ❌":
        response = "ЗАПРЕЩЕННЫЕ ТОВАРЫ\nНЕЛЬЗЯ 🚫 ЗАКАЗАТЬ ИЗ КИТАЯ , ДАННЫЙ МОМЕНТ ПРОВЕРКА ИДЕТ ТЩАТЕЛЬНО ‼️\nЗапрещенные товары \n🚫 Лекарственное средство (порошок, таблетки, жидкие лекарства)\n🚫 Все виды жидких веществ (парфюм, ароматизаторы и тд)\n🚫 Все виды холодного оружия (ножи, электрошокеры , биты и т.д)\n 🚫 Не принимаем электронные сигареты, кальяны и т.д\n🚫 ТОВАРЫ С ПРИЗНАКАМИ 18+ \n🚫 Смартфон ( телефоны ) и ноутбук\n\nЗапрещенные вещи для перевозки в АВИАции, пожалуйста, соблюдайте правила.\nЗапрещенные вещи 🚫\nХолодное оружие 🗡️\nХимические вещества 🧪\nБаллон с дихлофосом (газ) 🧴\nВещи 18+ 🔞\nЛюбые опасные предметы ⚠️\nС аккумуляторами 🔋\nВсе эти вещи запрещены ❌"
        await update.message.reply_text(response)

    elif text == "Контакт 👤":
        response = "Контакт : www.instagram.com/somon_sugd_cargo \n Телефон +992990050500 Whatsapp, Telegram "
        await update.message.reply_text(response)

    elif text == "Тафтиши трек-код 🔍":
        response = "Трек-коди худро ворид намоед:"
        await update.message.reply_text(response)

    elif text == "Дарси ройгон!":
        response = " Дарсхои ройгонро аз инчо дастрас кунед: https://t.me/somon_sugd_cargo/31"
        await update.message.reply_text(response)

    else:
        # Если текст не совпадает ни с одной из команд кнопок, считаем его трек-кодом
        await check_track_code(update, context)


# Функция для проверки трек-кода
# Функция для проверки трек-кода
async def check_track_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    track_code = update.message.text
    logger.info(f"Получен трек-код: {track_code}")

    # Выполняем поиск трек-кода
    result = data[data['code'] == track_code]
    logger.info(f"Результат поиска: {result}")

    if not result.empty:
        status_china = result['china'].values[0]
        status_khujand = result['khujand'].values[0]
        arrival_date = result['arrival_date'].values[0]  # Извлекаем дату прибытия на склад

        if status_khujand:
            response = f"Бори Шумо бо трек-коди {track_code} ба Хучанд омадааст, мунтазири занг шавед."
        elif status_china:
            response = (f"Бори Шумо бо трек-коди {track_code} ба склади Хитой санаи {arrival_date} кабул шудааст ва рузхои наздик ба Хучанд омада мерасад.")
        else:
            response = f"Бори Шумо бо трек-коди {track_code} холо ба склади Хитой кабул нашуааст."
    else:
        response = f"Бори Шумо бо трек-коди {track_code} холо ба склади Хитой кабул нашуааст."

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

    # Регистрируем обработчик сообщений с кнопок и трек-кодов
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main() 
