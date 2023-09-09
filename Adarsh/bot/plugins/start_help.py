from Adarsh.bot import StreamBot
from Adarsh.vars import Var
import logging
logger = logging.getLogger(__name__)
from Adarsh.bot.plugins.stream import MY_PASS
from Adarsh.utils.human_readable import humanbytes
from Adarsh.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant
from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.name)
from pyrogram.types import ReplyKeyboardMarkup

                      
@StreamBot.on_message(filters.command('start') & filters.private)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started !!"
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        await m.reply_text(
            text= "<b>ɪ ᴀᴍ ᴀ ᴀᴅᴠᴀɴᴄᴇ ᴛᴇʟᴇɢʀᴀᴍ ꜰɪʟᴇ/ᴠɪᴅᴇᴏ ᴛᴏ ᴘᴇʀᴍᴀɴᴇɴᴛ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ. ɪ ᴄᴀɴ ɢᴇɴᴇʀᴀᴛᴇ ᴅɪʀᴇᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ & ᴅɪʀᴇᴄᴛ ᴏɴʟɪɴᴇ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋ.\n\nᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴀɴʏ ᴠɪᴅᴇᴏ/ꜰɪʟᴇ & sᴇᴇ ᴍʏ ᴘᴏᴡᴇʀ...</b>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('📝 ᴜᴘᴅᴀᴛᴇs', url='https://telegram.me/KK_BOTS'),
                    InlineKeyboardButton('🧙🏻‍♀️ sᴜᴘᴘᴏʀᴛ', url='https://telegram.me/movie_a1')
                ],
                [
                    InlineKeyboardButton('❓ ʜᴇʟᴘ ❓', callback_data="help")
                ]
            ])
        )
    else:

        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, ids=int(usr_cmd))

        file_size = None
        if get_msg.video:
            file_size = f"{humanbytes(get_msg.video.file_size)}"
        elif get_msg.document:
            file_size = f"{humanbytes(get_msg.document.file_size)}"
        elif get_msg.audio:
            file_size = f"{humanbytes(get_msg.audio.file_size)}"

        file_name = None
        if get_msg.video:
            file_name = f"{get_msg.video.file_name}"
        elif get_msg.document:
            file_name = f"{get_msg.document.file_name}"
        elif get_msg.audio:
            file_name = f"{get_msg.audio.file_name}"

        stream_link = "https://{}/{}".format(Var.FQDN, get_msg.id) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}".format(Var.FQDN,
                                     Var.PORT,
                                     get_msg.id)

        msg_text = "**ᴛᴏᴜʀ ʟɪɴᴋ ɪs ɢᴇɴᴇʀᴀᴛᴇᴅ...⚡\n\n📧 ғɪʟᴇ ɴᴀᴍᴇ :-\n{}\n {}\n\n💌 ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ :- {}\n\n♻️ ᴛʜɪs ʟɪɴᴋ ɪs ᴘᴇʀᴍᴀɴᴇɴᴛ ᴀɴᴅ ᴡᴏɴ'ᴛ ɢᴇᴛ ᴇxᴘɪʀᴇᴅ ♻️\n\n<b>❖</b>**"
        await m.reply_text(            
            text=msg_text.format(file_name, file_size, stream_link),
            
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⚡ ᴅᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ ⚡", url=stream_link)]])
        )


@StreamBot.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    if data == "help":
        await query.message.edit_text(
            text = "<b>sᴇɴᴅ ᴍᴇ ᴀɴʏ ғɪʟᴇ/ᴠɪᴅᴇᴏ ᴛʜᴇɴ ɪ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴘᴇʀᴍᴀɴᴇɴᴛ sʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ ᴏғ ɪᴛ\n\nᴛʜɪs ʟɪɴᴋ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴏʀ ᴛᴏ sᴛʀᴇᴀᴍ ᴜsɪɴɢ ᴇxᴛᴇʀɴᴀʟ ᴠɪᴅᴇᴏ ᴘʟᴀʏᴇʀs ᴛʜʀᴏᴜɢʜ ᴍʏ sᴇʀᴠᴇʀs\n\nғᴏʀ sᴛʀᴇᴀᴍɪɴɢ ᴊᴜsᴛ ᴄᴏᴘʏ ᴛʜᴇ ʟɪɴᴋ ᴀɴᴅ ᴘᴀsᴛᴇ ɪᴛ ɪɴ ʏᴏᴜʀ ᴠɪᴅᴇᴏ ᴘʟᴀʏᴇʀ ᴛᴏ sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ.\n\nᴛʜɪs ʙᴏᴛ ɪs ᴀʟsᴏ sᴜᴘᴘᴏʀᴛ ɪɴ ᴄʜᴀɴɴᴇʟ. ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴀs ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ʀᴇᴀʟ ᴛɪᴍᴇ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ ғᴏʀ ᴇᴠᴇʀʏ ғɪʟᴇs/ᴠɪᴅᴇᴏs</b>",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("ʙᴀᴄᴋ", callback_data = "aksstart")
                    ]
                ]
            )
        )
    elif query.data == "aksstart":
        buttons = [[
                    InlineKeyboardButton('📝 ᴜᴘᴅᴀᴛᴇs', url='https://telegram.me/KK_BOTS'),
                    InlineKeyboardButton('🧙🏻‍♀️ sᴜᴘᴘᴏʀᴛ', url='https://telegram.me/movie_a1')
                ],
                [
                    InlineKeyboardButton('❓ ʜᴇʟᴘ ❓', callback_data="help")
                ]
              ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text= "<b>ɪ ᴀᴍ ᴀ ᴀᴅᴠᴀɴᴄᴇ ᴛᴇʟᴇɢʀᴀᴍ ꜰɪʟᴇ/ᴠɪᴅᴇᴏ ᴛᴏ ᴘᴇʀᴍᴀɴᴇɴᴛ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ. ɪ ᴄᴀɴ ɢᴇɴᴇʀᴀᴛᴇ ᴅɪʀᴇᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ & ᴅɪʀᴇᴄᴛ ᴏɴʟɪɴᴇ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋ.\n\nᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴀɴʏ ᴠɪᴅᴇᴏ/ꜰɪʟᴇ & sᴇᴇ ᴍʏ ᴘᴏᴡᴇʀ...</b>",
            reply_markup=reply_markup    
        )



