from pyrogram import Client, filters

import youtube_dl
from youtube_search import YoutubeSearch
import requests

import os
import time

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------

@Client.on_message(filters.command("s") & ~filters.channel & ~filters.edited)
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('🌸 𝐅𝐢𝐧𝐝𝐢𝐧𝐠 𝐘𝐨𝐮𝐫 𝐒𝐨𝐧𝐠 🎸••••')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            performer = f"[Movie_ott]" 
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('**𝐈 𝐚𝐦 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝 𝐫𝐞𝐬𝐮𝐥𝐭 𝐢𝐧 𝐲𝐨𝐮𝐫 𝐫𝐞𝐪𝐮𝐞𝐬𝐭💔. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐫𝐲 𝐚𝐧𝐨𝐭𝐡𝐞𝐫 𝐬𝐨𝐧𝐠 𝐨𝐫 𝐮𝐬𝐞 𝐜𝐨𝐫𝐫𝐞𝐜𝐭 𝐬𝐩𝐞𝐥𝐥𝐢𝐧𝐠💞!**')
            return
    except Exception as e:
        m.edit(
            "**𝐄𝐧𝐭𝐞𝐫 𝐒𝐨𝐧𝐠 𝐍𝐚𝐦𝐞 𝐰𝐢𝐭𝐡 𝐂𝐨𝐦𝐦𝐚𝐧𝐝💞**❗\nFor 𝐄𝐱𝐚𝐦𝐩𝐥𝐞: /s Alone Marshmellow"
        )
        print(str(e))
        return
    m.edit("🔼🎵•••")
    m.edit("⏫•🎵••")
    m.edit("🔽••🎵•")
    m.edit("⏬•••🎵")
    m.edit("ℙ𝕝𝕖𝕒𝕤𝕖 𝕨𝕒𝕚𝕥 𝕚𝕥 𝕞𝕒𝕪 𝕥𝕒𝕜𝕖 𝕤𝕠𝕞𝕖 𝕥𝕚𝕞𝕖.")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'{msg.from_user.mention}\n🎹 <b> 𝑻𝒊𝒕𝒍𝒆:</b> <a href="{link}">{title}</a>\n🎙️ <b>𝑫𝒖𝒓𝒂𝒕𝒊𝒐𝒏:</b> <code>{duration}</code>\n🎵 <b>𝑽𝒊𝒆𝒘𝒔:</b> <code>{views}</code>\n🔼𝑼𝒑𝒍𝒐𝒂𝒅𝒆𝒅 𝒃𝒚: <a href=https://t.me/meenu_filter_bot> 𝑵𝒂𝒕𝒂𝒍𝒊𝒂 𝑫𝒚𝒆𝒓 🌸 </a>  '
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
        message.delete()
    except Exception as e:
        m.edit('**𝐀𝐧 𝐄𝐫𝐫𝐨𝐫 𝐎𝐜𝐜𝐮𝐫𝐞𝐝 ❌ \n𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧 𝐥𝐚𝐭𝐞𝐫 🙂**')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
