import os
import time
import string
import random
import asyncio
import aiofiles
import datetime
import shutil, psutil
from utils_bot import *
from Adarsh import StartTime
from Adarsh.utils.broadcast_helper import send_msg
from Adarsh.utils.database import Database
from Adarsh.bot import StreamBot
from Adarsh.vars import Var
from pyrogram import filters, Client
from pyrogram.types import Message
db = Database(Var.DATABASE_URL, Var.name)
Broadcast_IDs = {}


@StreamBot.on_message(filters.command('ping'))
async def ping(b, m):
    start_t = time.time()
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await m.reply_text(f"<b>📊 ᴘɪɴɢ ɪs - {time_taken_s:.3f} ᴍs</b>")
    

@StreamBot.on_message(filters.command("stats") & filters.private  & filters.user(list(Var.OWNER_ID)))
async def stats(bot, update):
    currentTime = readable_time((time.time() - StartTime))
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    aks_users = await db.total_users_count()
    aksstats = (
        'ʙᴏᴛ sᴛᴀᴛᴜs\n'
        f'ʙᴏᴛ ᴜᴘᴛɪᴍᴇ - {currentTime}\n'
        f'ᴛᴏᴛᴀʟ ᴅɪsᴋ sᴘᴀᴄᴇ - {total}\n'
        f'ᴜsᴇᴅ - {used}\n'
        f'ꜰʀᴇᴇ - {free}\n'
        f'ᴄᴘᴜ - {cpuUsage}%\n'
        f'ʀᴀᴍ - {memory}%\n'
        f'ᴅɪsᴋ- {disk}\n\n'
        'ᴅᴀᴛᴀ ᴜsᴀɢᴇ\n'
        f'ᴜᴘʟᴏᴀᴅ - {sent}\n'
        f'ᴅᴏᴡɴ - {recv}\n'
        f'ᴛᴏᴛᴀʟ ᴜsᴇʀs - {aks_users}'
    )
    await update.reply_text(aksstats)


        
@StreamBot.on_message(filters.command("broadcast") & filters.private  & filters.user(list(Var.OWNER_ID)))
async def broadcast_(c, m):
    user_id=m.from_user.id
    out = await m.reply_text(
            text=f"Broadcast initiated! You will be notified with log file when all the users are notified."
    )
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not Broadcast_IDs.get(broadcast_id):
            break
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    Broadcast_IDs[broadcast_id] = dict(
        total=total_users,
        current=done,
        failed=failed,
        success=success
    )
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(
                user_id=int(user['id']),
                message=broadcast_msg
            )
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if Broadcast_IDs.get(broadcast_id) is None:
                break
            else:
                Broadcast_IDs[broadcast_id].update(
                    dict(
                        current=done,
                        failed=failed,
                        success=success
                    )
                )
    if Broadcast_IDs.get(broadcast_id):
        Broadcast_IDs.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()
    if failed == 0:
        await m.reply_text(
            text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    else:
        await m.reply_document(
            document='broadcast.txt',
            caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    os.remove('broadcast.txt')




