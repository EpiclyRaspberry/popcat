# asyncat
an asynchronous api wrapper for https://popcat.xyz/api

## basic usage
```python
import asyncio
from asyncat import PopCat

async def  main():
    async with PopCat() as cat:
        color=await cat.color("ff8844")
        print (color.name,color.rgb,color.hex,sep=" - ")
asyncio.run(main())
```
