from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from exchanges import binance_get_p2p_scheme, huobi_get_p2p_scheme

bot = Bot(token='6387405385:AAGuXiv3YixYDhEia8b1ejSGMpejso-tuS4')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class YourState(StatesGroup):
    binance = State()
    binance_limit = State()
    binance_bank = State()
    huobi = State()
    huobi_limit = State()
    huobi_bank = State()


async def show_main_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Binance', 'Huobi', 'Назад')
    await bot.send_message(message.chat.id, 'Выберите биржу:', reply_markup=keyboard)


async def give_bank_binance(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Monobank', 'PrivatBank', 'Sportbank', 'ABank', 'Назад')
    await bot.send_message(message.chat.id, 'Выберите банк:', reply_markup=keyboard)


async def give_limit_binance(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('10000', '20000', '5000', 'Назад')
    await bot.send_message(message.chat.id, 'Выберите или напишите лимит:', reply_markup=keyboard)



async def show_binance_button(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('BTC', 'ETH', 'BUSD', 'BNB', 'Назад')
    await bot.send_message(message.chat.id, 'Выберите криптовалюту:', reply_markup=keyboard)


async def give_bank_huobi(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Monobank', 'PrivatBank', 'Sportbank', 'ABank', 'Назад')
    await bot.send_message(message.chat.id, 'Выберите банк:', reply_markup=keyboard)


async def give_limit_huobi(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('10000', '20000', '5000', 'Назад')
    await bot.send_message(message.chat.id, 'Выберите или напишите лимит:', reply_markup=keyboard)


async def show_huobi_button(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('BTC', 'ETH', 'LTC', 'XRP', 'HT', 'TRX', 'Назад')
    await bot.send_message(message.chat.id, 'Выберите криптовалюту:', reply_markup=keyboard)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await show_main_menu(message)


@dp.message_handler()
async def process_all_messages(message: types.Message):
    if message.text in ['Binance', 'Huobi', 'Назад']:
        if message.text == 'Binance':
            await YourState.binance.set()
            await show_binance_button(message)
        elif message.text == 'Huobi':
            await YourState.huobi.set()
            await show_huobi_button(message)
        else:
            await show_main_menu(message)


@dp.message_handler(state=YourState.binance)
async def binance_state(message: types.Message, state: FSMContext):
    if message.text in ['BTC', 'ETH', 'BUSD', 'BNB']:
        await state.update_data(coin=message.text)
        await give_bank_binance(message)
        await YourState.binance_bank.set()
    elif message.text == 'Назад':
        await state.finish()
        await show_main_menu(message)


@dp.message_handler(state=YourState.binance_bank)
async def binance_bank(message: types.Message, state: FSMContext):
    if message.text in ['Monobank', 'PrivatBank', 'Sportbank', 'ABank']:
        await state.update_data(bank=message.text)
        await give_limit_binance(message)
        await YourState.binance_limit.set()
    elif message.text == 'Назад':
        await state.finish()
        await show_main_menu(message)


@dp.message_handler(state=YourState.binance_limit)
async def binance_limit(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await show_main_menu(message)
    try:
        limit = int(message.text)
        state_data = await state.get_data()
        coin = state_data.get('coin')
        bank = state_data.get('bank')
        text = binance_get_p2p_scheme(asset2=coin, bank=[bank], limit=limit)
        await bot.send_message(message.chat.id, text)
        await YourState.binance.set()
        await show_binance_button(message)
    except:
        await bot.send_message(message.chat.id, 'Назад')


@dp.message_handler(state=YourState.huobi)
async def huobi_state(message: types.Message, state: FSMContext):
    if message.text in ['BTC', 'ETH', 'LTC', 'XRP', 'HT', 'TRX']:
        await state.update_data(coin=message.text)
        await give_bank_huobi(message)
        await YourState.huobi_bank.set()
    elif message.text == 'Назад':
        await state.finish()
        await show_main_menu(message)


@dp.message_handler(state=YourState.huobi_bank)
async def huobi_bank(message: types.Message, state: FSMContext):
    if message.text in ['Monobank', 'PrivatBank', 'Sportbank', 'ABank']:
        await state.update_data(bank=message.text)
        await give_limit_huobi(message)
        await YourState.huobi_limit.set()
    elif message.text == 'Назад':
        await state.finish()
        await show_main_menu(message)


@dp.message_handler(state=YourState.huobi_limit)
async def huobi_limit(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await show_main_menu(message)
    try:
        limit = int(message.text)
        state_data = await state.get_data()
        coin = state_data.get('coin')
        bank = state_data.get('bank')
        text = huobi_get_p2p_scheme(coin2=coin, bank=bank, limit=limit)
        await bot.send_message(message.chat.id, text)
        await YourState.huobi.set()
        await show_huobi_button(message)
    except:
        await bot.send_message(message.chat.id, 'Назад')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
