## class PopCat(session=None)
main class that interacts with the api

params

`session`(optional) aiohttp.ClientSession
session to be used to request

methods

## async def color(color)
get info on a hex color

params

`color` str
color string
must be a hex string like "696969"

raises

InvalidColor: the color was invalid
