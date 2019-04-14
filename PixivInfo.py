# -*- coding: utf-8 -*-
"""
@author: HateNoSaiShi
"""

import telebot
import numpy as np
from pixivpy3 import AppPixivAPI
from telebot.types import InputMediaPhoto
import time
import requests


bot = telebot.AsyncTeleBot('Your Token here')

white_list = []
black_list = []
#===============================================================================

def PixivDownloadOrigin(pixiv_id, api):
    if api.user_id == 0:
        api.login("username", "passWord")
    json_result = api.illust_detail(pixiv_id, req_auth = True)
    if ('error' in json_result.keys()):
        local_url = -1
        title = -1
        tag = -1
        file = -1
        artist = - 1
    else:
        if json_result['illust']['page_count'] == 1:
            url = json_result['illust']['meta_single_page']['original_image_url']
        else:
            url = json_result['illust']['meta_pages'][0]['image_urls']['original']
        title = json_result['illust']['title']
        tag = json_result['illust']['tags']
        artist = json_result['illust']['user']['name']
        tag = [i['name'] for i in tag]
        
        name = url.split('/')[-1]
        local_url = '/root/'+name

        try:
            file = open(local_url, 'rb') 
        except:
            api.download(url)
            file = open(local_url, 'rb') 
    return file,title,tag,artist

#===============================

def PixivDownload(pixiv_id, api):
    if api.user_id == 0:
        api.login("username", "passWord")
    json_result = api.illust_detail(pixiv_id, req_auth = True)
    if ('error' in json_result.keys()):
        local_url = -1
        title = -1
        tag = -1
    else:
        '''if json_result['illust']['page_count'] == 1:
            url = json_result['illust']['meta_single_page']['original_image_url']
        else:
            url = json_result['illust']['meta_pages'][0]['image_urls']['original']'''
        url = json_result['illust']['image_urls']['large']
        title = json_result['illust']['title']
        tag = json_result['illust']['tags']

        tag = [i['name'] for i in tag]
        
        name = url.split('/')[-1]

        local_url = '/root/'+name

        try:
            file = open(local_url, 'rb') 
        except:
            api.download(url)
            file = open(local_url, 'rb') 
    return file,title,tag

#===============================

def PixivRanking(freq, num, api):
    if api.user_id == 0:
        api.login("username", "passWord")
    json_result = api.illust_ranking(freq, req_auth = True)
    work_list = json_result['illusts']
    if num > 10:
        num = 10
    random = []
    while (len(random) < num):
        temp_random = int(np.random.rand(1)* (len(work_list) - 1))
        if temp_random not in random:
            random.append(temp_random)
    select_work = [work_list[i] for i in random]
    work_id = [i['id'] for i in select_work]
    return work_id
 
#===============================

def PixivRelated(origin_id, num, api):
    if api.user_id == 0:
        api.login("username", "passWord")
    json_result = api.illust_related(origin_id, req_auth = True)
    if ('error' in json_result.keys()):
        id_list = []
    else:
        num = min(10, num)
        work_list = json_result['illusts']
        id_list = [i['id'] for i in work_list[:num]]
    return id_list

#===============================

def MessageIdTest(message_id):
    url = 'https://t.me/DailyTouhouDoujinPic/' + str(message_id)
    html = requests.get(url)
    text = html.text
    bool_result = False
    if ('title' in text and 'tags' in text):
        bool_result = True
    return bool_result
    
    
    
    
#===============================================================================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(1)
    text = """中文说明：
1./id illustID
|返回illustID对应的pixiv插画
2./touhou
|随机从东方同人插画频道forward一张插画
3./ranking type number
|返回number张type对应的榜单的插画。
|将type替换为(day，week，month，day_male，day_female),分别对应（日榜，周榜，月榜，男性向日榜，女性向日榜）。
|number小于等于5每张图独立推送，number大于5以album形式推送，最大值为10。
|number的缺省值为6。
4./related illustID number
|返回illustID对应图片的相关图片。
|number小于等于5每张图独立推送，number大于5以album形式推送，最大值为10。
|number的缺省值为5（注意，和/ranking不同）。
5./file illustID
|以文件形式返回对应的pixiv插画
☆源代码：请私聊获取
☆本bot不记录使用者任何群聊信息。


Instructions for use:
1./id illustID
| Return ONE picture with input illust_id
2./touhou
| Forward one illustration randomly from Touhou Doujin Pics Recommendation channel.
3./ranking type number
| Return multiple pictures form ranking
| Replace type with keyword (day, week, month, day_male or day_female) to fetch pictures from (daily, weekly, monthly, daily for male members or daily for female members) ranking.
| Each picture is displayed seperately for number no larger than FIVE while a single album is showed for number greater than FIVE.
| The default value for number is SIX while maximum value is TEN.
4./related illustID number
| Return related pictures of illustID not including itself.
| Each picture is displayed seperately for number no larger than FIVE while a single album is showed for number greater than FIVE.
| The default value for number is FIVE(WARNING:different from /ranking) while maximum value is TEN.
5./file illustID
| Return the piciture as a file.
☆Source Code：Please contact the owner
☆This bot never records any group chat history information.

推广： https://t.me/DailyTouhouDoujinPic
promotion : https://t.me/DailyTouhouDoujinPic
    """
    bot.reply_to(message, text)
    print(2)
    '''bot.reply_to(message, """使用方法：
    /id p站图片id 
    /ranking 频率(day,week,month) 数量(缺省为6，5以上不给出图片id)
    /related 图片id 数量(缺省为5) """)'''

#=============================== 
    
@bot.message_handler(commands=['id'])
def send_picture(message):
    bool_ban = False
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        if int(message.from_user.id) in black_list:
            bool_ban = True



    else:
        if int(message.chat.id) in black_list:
            bool_ban = True

 
    
    if bool_ban:
        bot.reply_to(message, '你/频道/群组 被BAN了, 请私聊bot确认是否为个人被ban')
        return 0
    
    pixiv_id = -1
    try:
        pixiv_id = message.text.split(' ')[1]
        try:
            int(pixiv_id)
            api = AppPixivAPI()
            api.login("username", "passWord")
            file,title,tags,artist = PixivDownloadOrigin(pixiv_id, api)
            if file == -1:
                bot.send_message(message.chat.id, '该图片不存在|Picture does not exist')
            else:
                caption = 'title : ' + title + '\n' + 'url : pixiv.net/i/' + pixiv_id + '\n' + 'tags : ' 
                for tag in tags:
                    if len(caption) + len(tag) < 193:
                        caption = caption + tag + '   '
                bot.send_photo(message.chat.id,file, caption)
        except:
            bot.send_message(message.chat.id, '満身創痍|使用范例： /id 43369925')
    except:
        bot.send_message(message.chat.id, '満身創痍|使用范例： /id 43369925')

#==============================        
        
@bot.message_handler(commands = ['ranking'])
def send_top(message):
    bool_ban = False
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        if int(message.from_user.id) in black_list:
            bool_ban = True

    else:
        if int(message.chat.id) in black_list:
            bool_ban = True

    
    if bool_ban:
        bot.reply_to(message, '你/频道/群组 被BAN了, 请私聊bot确认是否为个人被ban')
        return 0
    
    
    support_freq = ['day', 'week', 'month', 'day_male', 'day_female']
    try:
        split_list = message.text.split(' ')
        if len(split_list) > 3 or len(split_list) < 2:
            bot.send_message(message.chat.id, '満身創痍|使用范例： /ranking day 6')
            return -1
        elif len(split_list) == 3:
            frequence = split_list[1]
            num = split_list[2]
        elif len(split_list) == 2:
            frequence = split_list[1]
            num = 6
        num = int(num)

        if frequence not in support_freq:
            bot.send_message(message.chat.id, '不支持的关键词，请输入day,week,month,day_male或day_female')
        else:
            api = AppPixivAPI()
            api.login("username", "passWord")
            pixiv_id = PixivRanking(frequence, num, api)
            if num < 6:
                for i in pixiv_id:
                    file,title,tags = PixivDownload(i, api)
                    caption = 'url : pixiv.net/i/' + str(i) + '\n' + 'title : ' + title + '\n' + 'tags : '
                    for tag in tags:
                        if len(caption) + len(tag) < 193:
                            caption = caption + tag + '    '
                    bot.send_photo(message.chat.id, file, caption)
            else:
                file_list = []
                for i in pixiv_id:
                    temp_file,temp1,temp2 = PixivDownload(i, api)
                    file_list.append(InputMediaPhoto(temp_file))
                bot.send_media_group(message.chat.id,file_list)
    except:
        bot.send_message(message.chat.id, '満身創痍|使用范例： /ranking day 6')
    
#=============================
 
@bot.message_handler(commands = ['related'])
def send_related(message):
    bool_ban = False
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        if int(message.from_user.id) in black_list:
            bool_ban = True
    else:
        if int(message.chat.id) in black_list:
            bool_ban = True
    
    if bool_ban:
        bot.reply_to(message, '你/频道/群组 被BAN了, 请私聊bot确认是否为个人被ban')
        return 0
    
    try:
        split_list = message.text.split(' ')
        if len(split_list) > 3 or len(split_list) < 2:
            bot.send_message(message.chat.id, '満身創痍|使用范例： /related 43369925 5')
            return -1
        elif len(split_list) == 3:
            origin_id = split_list[1]
            num = split_list[2]
        elif len(split_list) == 2:
            origin_id = split_list[1]
            num = 5
        int(origin_id)
        num = int(num)

        if num <= 0:
            bot.send_message(message.chat.id, '満身創痍|使用范例： /related 43369925 5')
        else:
            api = AppPixivAPI()
            api.login("username", "passWord")
            id_list = PixivRelated(origin_id, num, api)
            if id_list == []:
                bot.send_message(message.chat.id, '该图片不存在或没有相关图片|Picture does not exist or has no related illustrations')
            elif len(id_list) < 6:
                for i in id_list:
                    file,title,tags = PixivDownload(i, api)
                    caption = 'url : pixiv.net/i/' + str(i) + '\n' + 'title : ' + title + '\n' + 'tags : '
                    for tag in tags:
                        if len(caption) + len(tag) < 193:
                            caption = caption + tag + '    '
                    bot.send_photo(message.chat.id, file, caption)
            else:
                file_list = []
                for i in id_list:
                    temp_file,temp1,temp2 = PixivDownload(i, api)
                    file_list.append(InputMediaPhoto(temp_file))
                bot.send_media_group(message.chat.id,file_list)
                
    except:
        bot.send_message(message.chat.id, '満身創痍|使用范例： /related 43369925 5')

#=============================

@bot.channel_post_handler(commands=['id'])
def send_picture_to_channel(message):  
    bool_ban = False
    if int(message.chat.id) in black_list:
        bool_ban = True
    if bool_ban:
        bot.reply_to(message, '你/频道/群组 被BAN了, 请私聊bot确认是否为个人被ban')
        return 0
    
    pixiv_id = -1
    try:
        pixiv_id = message.text.split(' ')[1]
        try:
            int(pixiv_id)
            api = AppPixivAPI()
            api.login("username", "passWord")
            file,title,tags,artist = PixivDownloadOrigin(pixiv_id, api)
  
            if file == -1:
                bot.send_message(message.chat.id, '该图片不存在|Picture does not exist')
            else:
                caption = 'title : ' + title + '\n' + 'artist : ' + artist + '\n' + 'url : pixiv.net/i/' + pixiv_id + '\n' +'tags : '  
                for tag in tags:
                    if len(caption) + len(tag) < 193:
                        caption = caption + '#' + tag + '  '
                bot.send_photo(message.chat.id,file, caption)
        except:
            bot.send_message(message.chat.id, '満身創痍|使用范例： /id 43369925')
    except:
        bot.send_message(message.chat.id, '満身創痍|使用范例： /id 43369925')

#=============================

@bot.message_handler(commands=['file'])
def send_file(message):
    bool_ban = False
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        #print(dir(message.from_user))
        if int(message.from_user.id) in black_list:
            bool_ban = True

    else:
        if int(message.chat.id) in black_list:
            bool_ban = True

    
    if bool_ban:
        bot.reply_to(message, '你/频道/群组 被BAN了, 请私聊bot确认是否为个人被ban')
        return 0
      
    pixiv_id = -1
    try:
        pixiv_id = message.text.split(' ')[1]
        try:
            int(pixiv_id)
            api = AppPixivAPI()
            api.login("username", "passWord")
            file,title,tags,artist = PixivDownloadOrigin(pixiv_id, api)
 
            if file == -1:
                bot.send_message(message.chat.id, '该图片不存在|Picture does not exist')
            else:
                bot.send_document(message.chat.id,file)
        except:
            bot.send_message(message.chat.id, '満身創痍|使用范例： /file 43369925')
    except:
        bot.send_message(message.chat.id, '満身創痍|使用范例： /file 43369925')

#=============================
@bot.message_handler(commands=['touhou'])
def forward_from_my_channel(message):
    
    MAX_ID = 2453
    
    while True:
        temp_id = int(np.random.rand(1)[0] * MAX_ID)
        if MessageIdTest(temp_id):
            _id_ = temp_id
            break
        else:
            temp_id += 1
            if MessageIdTest(temp_id):
                _id_ = temp_id
                break
    bot.forward_message(message.chat.id, -1001164118362, _id_)
    
        
#=============================

def polling():
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            bot.stop_polling()
            time.sleep(30)
     

#=============================



    
#===============================================================================
    
if __name__ == '__main__':
    '''try:
        bot.polling(none_stop=True)
    except:
        time.sleep(10)'''
    polling()

    
