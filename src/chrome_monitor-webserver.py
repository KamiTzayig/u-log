from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify the domains of your extensions here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ExtensionData(BaseModel):
    timestamp: str
    timezone: str
    windows: list

@app.post("/log")
async def log_extension_data(data: ExtensionData):

    # print("Received data:", data.model_dump())
    with open("browser-logs.txt", 'a', encoding="utf-8") as logBrowser:
        try:
            logBrowser.write(f"{data.model_dump()}\n")
            
        except Exception: 
            print("Error getting char")

    # Here you could save the data to a file or database
    return {"message": "Data received successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
