import discord
import json
import todo_list
import guess
import today_covid_cases
import react

with open('data_storage.json', 'r', encoding = 'utf-8') as data_storage:
    j_data = json.load(data_storage)

client = discord.Client()


@client.event
async def on_ready():
    # 開始運行，在終端機傳送訊息
    print(f'{client.user} is online')
    
@client.event
async def on_message(message): 
    # 機器人不會因為自己傳的訊息而重複觸發反應
    if message.author == client.user:
        return
  
    # 回覆使用者傳送的特定訊息
    if message.content.startswith('孤單寂寞覺得冷'):
        await message.channel.send(f'<@{message.author.id}>，我永遠與你同在~~')
    
    # todo list
    # 建立 todo 物件
    todo = todo_list.Todo(message.content)
    for command in todo.commands:
        if message.content.startswith(command):
            # 成功進來的 command 就是使用者開頭輸入的正確 todo list指令，但還不確定是其中的哪個指令，當然也不確定指令後面的語法又是否正確    
            # 這邊就交給 todo list.py 處理了，他會根據指令內容回傳正確訊息或是指令語法錯誤、輸入日期不合乎常理等等
            await message.channel.send(todo.command_work(command))
                      
    
    # 猜數字遊戲
    # 建立 guess 物件
    guess_object = guess.Game(message.content)  
    for command in guess_object.commands:
        if message.content.startswith(command):
            # 成功進來的 command 就是使用者開頭輸入的正確 guess 指令，但還不確定是其中的哪個指令，當然也不確定指令後面的語法又是否正確    
            # 這邊就交給 guess.py 處理了，他會根據指令內容回傳正確訊息或是指令語法錯誤、輸入數字不合乎常理等等      
            await message.channel.send(guess_object.command_work(command, message.author))
            break
    # # 抽圖片
    # # 建立 image 物件
    # image = react.Get_image(message.content)
    # for command in image.commands:
    #     if message.content.startswith(command):
    #         # 成功進來的 command 就是使用者開頭輸入的正確 抽 指令，但還不確定是其中的哪個指令，當然也不確定指令後面的語法又是否正確    
    #         # 這邊就交給 react.py 處理了，他會根據指令內容回傳正確訊息或是指令語法錯誤、
    #         await message.channel.send(image.command_work(command))

    if message.content.startswith('$covid_19'):
        await message.channel.send(f'今日新增 {today_covid_cases.get_covid_data()} 例確診')


# 開始執行    
client.run(j_data['TOKEN'])