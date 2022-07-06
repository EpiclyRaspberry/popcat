# popcat
an asynchronous api wrapper for https://popcat.xyz/api
### installation
`pip install git+https://github.com/EpiclyRaspberry/popcat`
~~coming on pypi soon ™~~
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
```
