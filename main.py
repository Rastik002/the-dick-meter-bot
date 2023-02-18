from datetime import datetime
from random import randint
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from config import *
from database import *

bot = Bot(token)
dp = Dispatcher(bot)
connect()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	a = await bot.get_me()
	addgroup = InlineKeyboardMarkup()
	addgroup.add(
	    InlineKeyboardButton(text="Добавить бота в группу", url=f'http://t.me/{a.username}?startgroup=Lichka')
	)
	await message.answer("Привет! я линейка — бот для чатов (групп)\n\nСмысл бота: бот работает только в чатах. Раз в 24 часа игрок может прописать команду /dick, где в ответ получит от бота рандомное число.\nРандом работает от -5 см до +10 см.\n\nЕсли у тебя есть вопросы — пиши команду: /help", reply_markup=addgroup)

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
	await message.answer('Команды бота:\n/dick — Вырастить/уменьшить член\n/top_dick — Топ 10 членов чата\n/global_top - Глобальный топ 10 игроков\n\nКонтакты:\nАдмин — @Rastik002')

@dp.message_handler(commands=['dick'])
async def dick(message: types.Message):
	if message.chat.type != "supergroup":
		a = await bot.get_me()
		addgroup = InlineKeyboardMarkup()
		addgroup.add(
		    InlineKeyboardButton(text="Добавить бота в группу", url=f'http://t.me/{a.username}?startgroup=Lichka')
		)
		return await message.answer('Я работаю только в чатах (группах)', reply_markup=addgroup)
	chat_id = message.chat.shifted_id  
	if not message.from_user.username:
		await message.answer("Для пользования ботом установите username в настройках телеграма.")
	if not Users.select().where(Users.chat_id == chat_id).where(Users.user_id == message.from_user.id).exists():
		Users.create(user_id=message.from_user.id, username=message.from_user.username, chat_id=chat_id)
	userInfo = Users.select().where(Users.chat_id == chat_id).where(Users.user_id == message.from_user.id)[0]
	a = randint(-5, 10)
	da = datetime.now()
	end_date = datetime.now() + time
	if str(da) > userInfo.end_date or userInfo.end_date == '':
		if a < 0:
			b = abs(a)
			Users.update(dick=userInfo.dick-int(b), end_date=end_date).where(Users.user_id == message.from_user.id).where(Users.chat_id == chat_id).execute()
			await message.answer(f'Твой писюн уменьшился на {b} см\nТеперь он равен {userInfo.dick-int(b)} см')
		else:
			Users.update(dick=userInfo.dick+int(a), end_date=end_date).where(Users.user_id == message.from_user.id).where(Users.chat_id == chat_id).execute()
			await message.answer(f'Твой писюн увеличился на {a} см\nТеперь он равен {userInfo.dick+int(a)} см')
	else:
		await message.answer(f'Ты уже играл\nСейчас он равен {userInfo.dick} см.\nСледующая попытка завтра!')

@dp.message_handler(commands=['top_dick'])
async def top(message: types.Message):
	if message.chat.type == "private":
		a = await bot.get_me()
		addgroup = InlineKeyboardMarkup()
		addgroup.add(
		    InlineKeyboardButton(text="Добавить бота в группу", url=f'http://t.me/{a.username}?startgroup=Lichka')
		)
		return await message.answer('Я работаю только в чатах (группах)', reply_markup=addgroup)
	try:
		chat_id = message.chat.shifted_id
		top_worker=''
		num = 0
		userInfo = Users.select().where(Users.chat_id == chat_id).order_by(Users.dick.desc()).limit(10)
		for top in userInfo:
			num = num+1
			top_worker += f'<b>{num}. @{top.username}</b> — <b>{top.dick}</b> см\n\n'
		await message.answer(f'{top_worker}\n', parse_mode='html')
	except:
		await message.answer('В базе нет игроков.')

@dp.message_handler(commands=['global_top'])
async def globaltop(message: types.Message):
	if message.chat.type == "supergroup":
		return await message.answer('Данная команда доступна только в личке с ботом❗️')
	try:
		top_worker=''
		num = 0
		userInfo = Users.select(Users.username).distinct().limit(10)
		for top in userInfo:
			dickInfo = Users.select().where(Users.username == top.username).where(Users.dick)
			for kek in dickInfo:
				num = num+1
			top_worker += f'<b>{num}. @{top.username}</b> — <b></b>{kek.dick} см\n\n'
		await message.answer(f'{top_worker}\n', parse_mode='html')
	except:
		await message.answer('В базе нет игроков.')

if __name__ == '__main__':
	executor.start_polling(dispatcher=dp, skip_updates=True)