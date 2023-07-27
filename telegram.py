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
    huobi = State()


async def show_main_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Binance', 'Huobi', 'Назад')
    await message.reply('Выберите биржу:', reply_markup=keyboard)


async def show_binance_button(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('BTC', 'ETH', 'BUSD', 'BNB', 'Назад')
    await message.reply('Выберите криптовалюту:', reply_markup=keyboard)


async def show_huobi_button(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('BTC', 'ETH', 'LTC', 'XRP', 'HT', 'TRX', 'Назад')
    await message.reply('Выберите криптовалюту:', reply_markup=keyboard)


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
        text = binance_get_p2p_scheme(asset2=f'{message.text}')
        await bot.send_message(message.chat.id, text)
    elif message.text == 'Назад':
        await state.finish()
        await show_main_menu(message)


@dp.message_handler(state=YourState.huobi)
async def huobi_state(message: types.Message, state: FSMContext):
    if message.text in ['BTC', 'ETH', 'LTC', 'XRP', 'HT', 'TRX']:
        text = huobi_get_p2p_scheme(coin2=f'{message.text}')
        await bot.send_message(message.chat.id, text)
    elif message.text == 'Назад':
        await state.finish()
        await show_main_menu(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
