from fastapi import FastAPI
from pywebio.platform.fastapi import asgi_app
#TODO - change to tool
from checkprj import checkprj

app = FastAPI()

@app.get("/",)
async def read_root():
	pass

#TODO - change to tool
subapp = asgi_app(checkprj)

app.mount("/tool", subapp)