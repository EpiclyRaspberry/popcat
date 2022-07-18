# popcat
an asynchronous api wrapper for https://popcat.xyz/api
### installation
#### pip
`pip install git+https://github.com/EpiclyRaspberry/popcat`
~~coming on pypi soon ™~~
#### pydroid
1. You need to download the source by:
> Desktop mode
- Set this window to desktop mode
- Press `Code`(green button) then `Download ZIP`
- Extract the downloaded zip to somewhere
> [Termux](https://termux.com/)
- do `git clone https://github.com/EpiclyRaspberry/popcat` on any directory except `$HOME`
> [Pocket Git](http://pocketgit.com/)(Paid)
- Share this page's link then select Pocket Git
- Press HTTP
- Press the save icon on top left
- Find the Repo, Press on it, Then Press Clone
2. Now Open Terminal on PyDroid
3. 
## basic usage
```python
import asyncio
from popcat import PopCat

async def  main():
    async with PopCat() as cat:
        color=await cat.color("ff8844")
        print (color.name,color.rgb,color.hex,sep=" - ")
asyncio.run(main())
```
## endpoints covered
```
/color
/lyrics
/screenshot
/showerthoughts
/chatbot
/subreddit
/quote
/joke
/fact
/lulcat
/mock
/welcomecard - unstable function
/sadcat
/oogway
/communism
/car
```
