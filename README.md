# TelegramPixivInfoBot
```
Return Pixiv Illustration to Telegram Group

Supported function:

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
6./ugoira ugoiraID
| Return the gif document of given ugoira.





Requests
--------
TelegramBotApi : https://pypi.org/project/TelegramBotAPI/
pixivpy : https://pypi.org/project/PixivPy/
zipfile : 
imageio : https://pypi.org/project/imageio/
```
