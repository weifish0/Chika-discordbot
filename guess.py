from ast import Global
import random
import datetime
import json

key = ''
guess_time = 0
send_win_list=""

# 取得很長的 $guess help 指令的文字檔
with open('data_storage.json', 'r', encoding = 'utf-8') as data_storage:
    j_data = json.load(data_storage)

class Game():
    def __init__(self, message)->None:
        self.commands = ['$guess help', '$guess start', '$guess exit', '$guess scoreboard', '$guess ']
        self.message = message
        self.help_informations = j_data['guess_help_string']

    def win_store(self):
        global send_win_list
        
        # 儲存新的 win_list
        old_win_list = []
        # 儲存絕對時間，方便排序
        times_save = []
        # 將目前的 todo_list 變為 list 格式，方便資料處理
        present_win_list = send_win_list.split('\n', send_win_list.count('\n')-1)
        
        # 取得 send_todo_list 的日期並進行排序
        for thing in present_win_list:  
            times_save.append(thing[thing.find('/')-4: thing.find(':')])
            # 例外處理，因為最後一個 \n 不會被 split 給當作分隔，反而被當作 todo的任務 ，所以要手動消去
            if thing == present_win_list[-1]:
                thing = thing.replace('\n', '')
            old_win_list.append(thing)
        times_save = list(set(times_save))
        times_save.sort()
        # 將 send_todo_list 清除，並傳入排序後的資料 
        send_win_list = ''
        for guess_time in times_save:
            for thing in old_win_list:
                # 照時間排序並寫入正確的順序
                if thing[thing.find('/')-4: thing.find(':')] == guess_time:
                    send_win_list += f'{thing}\n'
    def author_check(self,author):
      global send_win_list
      global guess_time
      author_check_bool = False
      if len(send_win_list)==0 or send_win_list.find(str(author))==-1:
        return True
      else:
        send_author_list = send_win_list.split("/n")
        send_win_list = ""
        for author_check in send_author_list:
          if str(author) in author_check:
            if int(author_check[0:author_check.find(':')])>guess_time:
              author_check_bool = True
          send_win_list = send_win_list+author_check+"\n"
        return author_check_bool     
              
    # 尋找指令是哪個並執行對應命令(game中的 main function)
    def command_work(self, command, author):
        global key
        global guess_time
        global send_win_list
        
        self.command_site = self.commands.index(command)

        
        # $guess help
        if self.command_site == 0:
            if len(self.message) != 11:
                return '**格式有誤，請參考 $guess help 格式!**'
            return self.help_informations
        
        # $guess start
        elif self.command_site == 1:
            # 重置上局的 正確答案、猜的次數、選數字的列表
            key = ''
            guess_time = 0
            
            if len(self.message) != 12:
                return '**格式有誤，請參考 $guess help 格式!**'
            # 隨機選出一個正確答案
            for num in random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9'], 4):
                key += num
            print(key)
            return '**遊戲開始!** ,eg:`$guess 1235`'
        
        # $guess exit
        elif self.command_site == 2:
            if len(self.message) != 11:
                return '**格式有誤，請參考 $guess help 格式!**'
            return '**退出成功**'
        
        # $guess scoreboard
        elif self.command_site == 3:
            if len(self.message) != 17:
                return '**格式有誤，請參考 $guess help 格式!**'
             # 建立要回傳的訊息
            show_list = ''
        
        # 將 todo 編號後再回傳
            for num, thing in enumerate(send_win_list.split('\n', send_win_list.count('\n')-1)):
            # 例外處理，因為最後一個 \n 不會被 split 給當作分隔，反而被當作 todo的任務 ，所以要手動消去
                if thing == send_win_list.split('\n', send_win_list.count('\n')-1)[-1]:
                    thing = thing.replace('\n', '')
                guess_time=thing[0: thing.find(':')]
                person=thing[ thing.find(':')+1:]
                show_list += f'{num+1}. 猜{guess_time}次 {person} \n'
                      
            return show_list      
        
        elif self.command_site == 4:
            if len(self.message) != 11 and not(self.message.isdigit()):
                return '**格式有誤，請參考 $guess help 格式!**'

            guess = []
            guess_number = self.message[7:]
            A,B = 0,0
            for key_site in range(4):
                temporary_key = guess_number[0:1]
                guess_number = guess_number[1:] 
                guess.append(temporary_key)
               
              
                if temporary_key == key[key_site: key_site + 1]:
                    A += 1
            B={x for x in self.message if x in key}
            B=len(B)-A
            guess_time += 1    
            if A == 4:
              if self.author_check(author):
                send_win_list+=f"{guess_time}:{author}\n"
                self.win_store()
              return (f'恭喜答對,答案是{key},你用了{guess_time}次機會')
                    
            else:
                print(str(author))
                return(f'{A}A{B}B')   
    
         