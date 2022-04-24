from fastapi import Depends, FastAPI,File, UploadFile
from fastapi.responses import FileResponse,RedirectResponse

from app.db import create_db_and_tables
from app.models import UserDB
from app.users import auth_backend, current_active_user, fastapi_users

import os

def check_create_userdir(user):
    root_directory = os.path.dirname(__file__)
    filespath = os.path.join(root_directory, "files")
    userpath = os.path.join(filespath, user)
    
    if not os.path.exists(filespath):
        os.mkdir(filespath)
    if not os.path.exists(userpath):
        os.mkdir(userpath)
    
    return userpath

def get_filename(path):
    filename_list=[]
    for root,dirs,files in os.walk(path):
        filename_list.extend(files)
    return filename_list

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])


@app.get("/authenticated-route")
async def authenticated_route(user: UserDB = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

@app.post("/file_upload")
async def file_upload(file: UploadFile = File(...),user: UserDB = Depends(current_active_user)):
    userpath = check_create_userdir(user.email)
    filepath = os.path.join(userpath, file.filename)
    try:
        res = await file.read()
        with open(filepath, "wb") as f:
            f.write(res)
        return {"message": "success",  'filename': file.filename}
    except Exception as e:
        return {"message": str(e),  'filename': file.filename}

@app.get("/file_download/{filename}")
async def file_download(filename:str,user: UserDB = Depends(current_active_user)):
    userpath = check_create_userdir(user.email)
    filepath = os.path.join(userpath, filename)
    return FileResponse(filepath)

@app.get("/list")
async def get_all_files(user: UserDB = Depends(current_active_user)):
    """
    :return: filename list
    """
    userpath = check_create_userdir(user.email)
    return get_filename(userpath)


@app.delete("/file_delete/{filename}")
async def file_delete(filename:str,user: UserDB = Depends(current_active_user)):
    userpath = check_create_userdir(user.email)
    filepath = os.path.join(userpath, filename)
    os.remove(filepath)
    return None

@app.get("/")
async def default():
    """
    redirect to docs
    """
    return RedirectResponse("/docs")

@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    
