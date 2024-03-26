from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

import os
from datetime import datetime
from tzlocal import get_localzone
import sys
import json

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_desktop_path():
    # For Windows
    if os.name == 'nt':
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    # For MacOS
    elif os.name == 'posix':
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    # Adjust as needed for other operating systems
    else:
        raise NotImplementedError("This script only supports Windows and MacOS.")
    return desktop

def log(filename, data):
    # Specify the path to the 'output' directory on the Desktop
    output_dir = os.path.join(get_desktop_path(), 'u-log/output'+datetime.today().strftime('%Y%m%d'))
    
    # Ensure the 'output' directory exists
    ensure_dir_exists(output_dir)
    
    # Specify the path to the file within the 'output' directory
    file_path = os.path.join(output_dir, filename)
    
    # Get the current timestamp in the local timezone
    timestamp = datetime.now(tz=get_localzone())
    data["timestamp"] = timestamp.isoformat()
    
        # Serialize data to a JSON string if it's a dictionary
    if isinstance(data, dict):
        data_str = json.dumps(data, ensure_ascii=False)
    else:
        data_str = str(data)
    
    # Safely open the file for appending and write the data
    with open(file_path, 'a', encoding="utf-8") as log:
        log.write(f"{data_str}\n")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify the domains of your extensions here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ExtensionData(BaseModel):
    windows: list

@app.post("/log")
async def log_extension_data(data: ExtensionData):

    try:
        log("chrome_extension_logs.txt", data.model_dump())        
    except Exception: 
        print("Error getting char")

    # Here you could save the data to a file or database
    return {"message": "Data received successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=2226)



