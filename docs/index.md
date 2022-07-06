# Welcome to PopCat docs

PopCat is an asynchronous api wrapper for [popcat.xyz](https://popcat.xyz/api)

## Basic usage
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

