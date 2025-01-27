import asyncio 
from pyrogram import Client, filters, enums
from config import LOG_CHANNEL, API_ID, API_HASH, NEW_REQ_MODE
from plugins.database import db
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

LOG_TEXT = """<b>#NewUser
    
ID - <code>{}</code>

Nᴀᴍᴇ - {}

Bot @RequestAccepterXBot 🦋</b>
"""

@Client.on_message(filters.command('start'))
async def start_message(c,m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id, m.from_user.first_name)
        await c.send_message(LOG_CHANNEL, LOG_TEXT.format(m.from_user.id, m.from_user.mention))
    await m.reply_photo(f"https://envs.sh/fgl.jpg",
        caption=f"<b>ʜᴇʟʟᴏ {m.from_user.mention} 👋\n\n• ɪ ᴀᴍ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ᴀᴄᴄᴇᴘᴛᴏʀ ʙᴏᴛ.\n• ɪ ᴄᴀɴ ᴀᴄᴄᴇᴘᴛ ᴀʟʟ ᴏʟᴅ ᴘᴇɴᴅɪɴɢ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ.\n\n• ғᴏʀ ᴀʟʟ ᴘᴇɴᴅɪɴɢ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ᴜsᴇ - /accept</b>",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton('🇮🇳 𝐔𝐩𝐝𝐚𝐭𝐞 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 🇮🇳', url='https://t.me/synaxnetwork')
            ],[
                InlineKeyboardButton("𝐒𝐮𝐩𝐩𝐨𝐫𝐭 ☘️", url='https://t.me/synaxchatgroup'),
                InlineKeyboardButton("𝐁𝐨𝐭𝐬 🍁", url='https://t.me/synaxbots')
            ]]
        )
    )

@Client.on_message(filters.command('accept') & filters.private)
async def accept(client, message):
    show = await message.reply("**Please Wait.....**")
    user_data = await db.get_session(message.from_user.id)
    if user_data is None:
        await show.edit("**ғᴏʀ ᴀᴄᴄᴇᴘᴛ ᴘᴇɴᴅɪɴɢ ʀᴇǫᴜᴇsᴛ ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ /login ғɪʀsᴛ.**")
        return
    try:
        acc = Client("joinrequest", session_string=user_data, api_hash=API_HASH, api_id=API_ID)
        await acc.connect()
    except:
        return await show.edit("**Your Login Session Expired. So /logout First Then Login Again By - /login**")
    show = await show.edit("**Now Forward A Message From Your Channel Or Group With Forward Tag\n\nMake Sure Your Logged In Account Is Admin In That Channel Or Group With Full Rights.**")
    vj = await client.listen(message.chat.id)
    if vj.forward_from_chat and not vj.forward_from_chat.type in [enums.ChatType.PRIVATE, enums.ChatType.BOT]:
        chat_id = vj.forward_from_chat.id
        try:
            info = await acc.get_chat(chat_id)
        except:
            await show.edit("**Error - Make Sure Your Logged In Account Is Admin In This Channel Or Group With Rights.**")
    else:
        return await message.reply("**Message Not Forwarded From Channel Or Group.**")
    await vj.delete()
    msg = await show.edit("**Accepting all join requests... Please wait until it's completed.**")
    try:
        while True:
            await acc.approve_all_chat_join_requests(chat_id)
            await asyncio.sleep(1)
            join_requests = [request async for request in acc.get_chat_join_requests(chat_id)]
            if not join_requests:
                break
        await msg.edit("**Successfully accepted all join requests.**")
    except Exception as e:
        await msg.edit(f"**An error occurred:** {str(e)}")
        
@Client.on_chat_join_request(filters.group | filters.channel)
async def approve_new(client, m):
    if NEW_REQ_MODE == False:
        return 
    try:
        if not await db.is_user_exist(m.from_user.id):
            await db.add_user(m.from_user.id, m.from_user.first_name)
            await client.send_message(LOG_CHANNEL, LOG_TEXT.format(m.from_user.id, m.from_user.mention))
        await client.approve_chat_join_request(m.chat.id, m.from_user.id)
        try:
            await client.send_message(m.from_user.id, "**Hello {}!\nWelcome To {}\n\n__Powered By : @SynaxBots __**".format(m.from_user.mention, m.chat.title))
        except:
            pass
    except Exception as e:
        print(str(e))
        pass
