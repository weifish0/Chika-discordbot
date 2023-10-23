import discord
from discord.ext import commands
import os
import random
from load_save import load,save 


jdata=load('data_storage.json')
class Get_image():
    def  __init__(self,msg):
      self.commans=["抽","超級抽抽抽","超級抽"]
      self.msg=msg
    # 自己file的圖，都要是.jpg   
    def 抽(self): 
            # await ctx.send("載入中... (請稍候)") 
            # your file name"01"
            imagelist=os.listdir(r'資料夾名')
            pic = discord.File(' 本地資料夾路徑'+imagelist[random.randint(0,len(imagelist)-1)]) + ".jpg"
            return pic
            # await ctx.send("完成!")
    # 網站上的圖*指定keyword  
    def 超級抽抽抽(self):     
        img_url=get_want_url(self.msg)
        jdata["WantimageURL"]=img_url
        save('data_storage.json',jdata)
        img_urls=jdata["WantimageURL"]
        n=random.randint(0,len(img_urls)-1)
        url=img_urls[n]
        return url+".jpg"
    # 網站上的圖
    def 超級抽(self, ctx): 
        img_url=get_img_url()
        jdata["imageURL"]=img_url
        save('data_storage.json',jdata)
        img_urls=jdata["imageURL"]
        n=random.randint(0,len(img_urls)-1)
        url=img_urls[n]
        return url+".jpg"
        
        
        
        
        
    
        
    
    


            
            
        