import time
import json

# todo list 資料儲存
send_todo_list = ''

# 取得很長的 $todo help 指令的文字檔
with open('data_storage.json', 'r', encoding = 'utf-8') as data_storage:
    j_data = json.load(data_storage)

class Todo():
    def __init__(self, message) -> None:
        self.commands = ['$todo help', '$todo add', '$todo delete', '$todo list', '$todo clear']
        self.help_informations = j_data['todo_help_string']
        self.message = message
        self.delete_num = 0
    
    # 將日期變成絕對時間，方便比大小
    def get_real_time(self, date):
        time_string = date + ' 23:59:59'
        struct_time = time.strptime(time_string, "%Y/%m/%d %H:%M:%S")
        time_stamp = int(time.mktime(struct_time)) 
        return time_stamp
    
    # 將絕對時間變成正常日期格式，方便輸出
    def back_normal_timeformat(self, real_time):
        struct_time = time.localtime(real_time)
        time_string = time.strftime("%Y/%m/%d %H:%M:%S", struct_time)
        time_string = time_string.replace(' 23:59:59', '')
        return time_string
    
    # 處理日期排序問題    
    def date_sort(self):
        global send_todo_list
        
        # 儲存舊的 todo_list
        old_todo_list = []
        # 儲存絕對時間，方便排序
        time_save = []
        print(send_todo_list)
        # 將目前的 todo_list 變為 list 格式，方便資料處理
        present_todo_list = send_todo_list.split('\n', send_todo_list.count('\n')-1)
        
        # 取得 send_todo_list 的日期並進行排序
        for thing in present_todo_list:  
            time_save.append(self.get_real_time(thing[thing.find('/')-4: thing.find(':')]))
            # 例外處理，因為最後一個 \n 不會被 split 給當作分隔，反而被當作 todo的任務 ，所以要手動消去
            if thing == present_todo_list[-1]:
                thing = thing.replace('\n', '')
            old_todo_list.append(thing)
        time_save = list(set(time_save))
        time_save.sort()
        # 將 send_todo_list 清除，並傳入排序後的資料 
        send_todo_list = ''
        for real_time in time_save:
            for thing in old_todo_list:
                # 照時間排序並寫入正確的順序
                if thing[thing.find('/')-4: thing.find(':')] == self.back_normal_timeformat(real_time):
                    send_todo_list += f'{thing}\n'
    
    # 加入新事項                
    def add(self):
        global send_todo_list
        
        # 先找出截止日期(可以進來這裡代表初步的語法格式沒錯)
        deadline = self.message[self.message.find('add')+4:self.message.find('/')+6]
        
        # 檢查日期是否超出常理
        month = int(deadline[deadline.find('/')+1: deadline.find('/')+3])
        day = int(deadline[deadline.find('/')+4: ])
        thirtyone_months = [1, 3, 5, 7, 8, 10, 12]
        thirty_months = [4, 6, 9, 11]
        if month < 1 or month > 12 or month % 1 != 0:
            return '**日期錯誤**'
        elif month == 2 and day > 29:
            return '**日期錯誤**'
        elif month in thirtyone_months and day > 31:
            return '**日期錯誤**'
        elif month in thirty_months and day > 30:
            return '**日期錯誤**'
        elif month % 1 != 0:
            return '**日期錯誤**'
        
        # 時光不能倒流QQ
        if self.get_real_time(deadline) < time.time():
            return '**主人，請把握當下，時光不能倒流喔~**'
        
        task = self.message[self.message.find('/')+7: ]
        
        # 寫入
        send_todo_list += f'{deadline}: {task}\n'
               
        # 照時間排序
        self.date_sort()
                        
        return '**成功添加!**'
    
    # 展示 todo_list
    def show_list(self):
        global send_todo_list
        
        # 建立要回傳的訊息
        show_list = ''
        
        # 將 todo 編號後再回傳
        for num, thing in enumerate(send_todo_list.split('\n', send_todo_list.count('\n')-1)):
            # 例外處理，因為最後一個 \n 不會被 split 給當作分隔，反而被當作 todo的任務 ，所以要手動消去
            if thing == send_todo_list.split('\n', send_todo_list.count('\n')-1)[-1]:
                thing = thing.replace('\n', '')
            show_list += f'{num+1}. {thing}\n'
                      
        return show_list
    
    # 刪除事項
    def delete_todo(self):
        global send_todo_list
        
        for num, thing in enumerate(send_todo_list.split('\n', send_todo_list.count('\n')-1)):
            # 例外處理，因為最後一個 \n 不會被 split 給當作分隔，反而被當作 todo的任務 ，所以要手動消去
            if thing == send_todo_list.split('\n', send_todo_list.count('\n')-1)[-1]:
                thing = thing.replace('\n', '')
            
            if  self.delete_num == str(num+1):
                send_todo_list = send_todo_list.replace(f'{thing}\n', '')
                return '**刪除成功**'
        # 若使用者輸入奇怪的數字
        return '**刪除失敗**'
               
    # 尋找指令是哪個並執行對應命令(todo_list中的 main function)
    def command_work(self, command):
        global send_todo_list
        
        # 查找是哪個指令
        self.command_site = self.commands.index(command)
        
        # $todo help
        if self.command_site == 0:
            if len(self.message) != 10:
                return '**語法錯誤!**'
            return self.help_informations
        
        # $todo add
        elif self.command_site == 1:
            if self.message.count('/') != 2 or\
            self.message[self.message.find('add')+3] != ' ' or\
            self.message[self.message.find('/')+6] != ' ':
                return '**語法錯誤!**'
            return self.add()
        
        # $todo delete   
        elif self.command_site == 2:
            if send_todo_list == '':
                return '**還未添加事項喔~**'
            self.delete_num = self.message[self.message.find('delete')+7: ]
            return self.delete_todo()
        
        # $todo list
        elif self.command_site == 3:
            if send_todo_list == '':
                return '**還未添加事項喔~**'
            return self.show_list()
        
        # $todo clear
        elif self.command_site == 4:
            if send_todo_list == '':
                return '**還未添加事項喔~**'
            send_todo_list = ''
            return '**成功清除所有事項!**'