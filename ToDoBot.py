import  asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, state
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

BOT_TOKEN = '8843466514:AAHJ8LG7chY7BsHX9-8qw6c9SkgYowppsLY'
class AddTask(StatesGroup):
    WaitingForTask = State()
    WaitingForDelete = State()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
tasks = []
button1= KeyboardButton(text='Add task')
button2= KeyboardButton(text='Task list')
button3= KeyboardButton(text='Delete task')
keyboard = ReplyKeyboardMarkup(
    keyboard= [
        [button1],
        [button2],
        [button3]
    ],
    resize_keyboard=True
)
@dp.message(AddTask.WaitingForTask)
async def save_task(message: Message, state: FSMContext):
    tasks.append(message.text)
    await message.answer(f'Task added: {message.text}')
    await state.clear()
@dp.message(AddTask.WaitingForDelete)
async def delete_task(message: Message, state: FSMContext):
    index = int(message.text) - 1
    deleted = tasks.pop(index)
    await message.answer(f'Task deleted {deleted}')
    await state.clear()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Hello, its ToDo Bot 😄')
    await message.answer('👇', reply_markup=keyboard)
@dp.message(Command('add'))
async def addtask(message: Message):
    text = message.text
    if text.startswith('/add'):
        parts = text.split()
        task = ' '.join(parts[1:])
        tasks.append(task)
        await message.answer(f'Task added: {task}')

@dp.message(Command('list'))
async def tasklist(message: Message):
    text = message.text
    result = 'Task list:\n'
    if text == '/list':
        for index, task in enumerate(tasks):
            result += f'{index + 1}. {task}\n'
        await message.answer(result)

@dp.message()
async def buttons(message: Message, state: FSMContext):
    text = message.text
    if text == 'Task list':
        result = 'Task list:\n'
        for index, task in enumerate(tasks):
            result += f'{index + 1}. {task}\n'
        await message.answer(result)
    elif text == 'Add task':
        await state.set_state(AddTask.WaitingForTask)
        await message.answer('Write your task')
    if text == 'Delete task':
        await state.set_state(AddTask.WaitingForDelete)
        await message.answer('Write task you want to delete')



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
