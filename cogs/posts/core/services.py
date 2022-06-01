# Service Objects and Domain Logic
import discord
from typing import List 
import datetime 
from .models import Post
import servus
import config 

async def save_post(session:servus.ClientSession, post:Post):
    # make post request.
    resp = await servus.post(
        session=session,
        url= config.PERSIST_POST_ENDPOINT,
        data= post.to_json()
    )
    
    # status_flag resp.response.status == 200
    # json_flag resp.json == {"message":"Success"}
    status_flag, json_flag = True, True 
    return all([status_flag, json_flag])
    