import youtube_dl
import discord
import json
import asyncio
from bs4 import BeautifulSoup
from urllib import parse, request

intents = discord.Intents.default()
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('login')
    print(client.user.id)
    print('------------------------')
    game = discord.Game("/제임스도움말")
    await client.change_presence(status=discord.Status.online, activity=game)
    js = {
        "playlist": []
    }
    with open("list.json", "w", encoding="utf-8") as list_file:
        json.dump(js, list_file, ensure_ascii=False, indent="\t")

    while True:
        try:
            with open("list.json", "r", encoding="utf-8") as list_file:
                js = json.load(list_file)
            list = js["playlist"]
            for vc in client.voice_clients:
                if vc.guild.id == list[0][2]:
                    voice = vc
            if voice.is_playing() or voice.is_paused():
                pass
            else:
                if len(list) == 0:
                    pass
                else:
                    file = open("볼륨.txt", "r")
                    volume = file.read()
                    file.close()

                    list.remove(list[0])
                    js["playlist"] = list
                    with open("list.json", "w", encoding="utf-8") as list_file:
                        json.dump(js, list_file, ensure_ascii=False, indent="\t")
                    try:
                        voice.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("file/" + list[0][0].split("=")[1] + ".mp3"), volume=float(volume) * 0.01))
                        voice.play()
                    except:
                        pass
        except:
            pass
        await asyncio.sleep(1)


@client.event
async def on_reaction_add(reaction, user):
    try:
        if reaction.message.embeds[0].title in ["재생", "스킵", "목록", "일시정지", "다시시작"] and user.id != 745829394387566652:
            if str(reaction.emoji) == "⏸":
                for vc in client.voice_clients:
                    if vc.guild == reaction.message.guild:
                        voice = vc
                try:
                    voice.pause()
                    embed = discord.Embed(title="일시정지", description="음악을 일시정지합니다.", color=0xa453d1)
                    embed.set_footer(
                        icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                        text="팀베이비(https://discord.gg/NXUEE4f)")
                    msg = await reaction.message.channel.send(embed=embed)
                    await reaction.message.delete()
                    await msg.add_reaction("⏸")
                    await msg.add_reaction("▶")
                    await msg.add_reaction("⏩")
                    await msg.add_reaction("❌")
                except:
                    pass

            if str(reaction.emoji) == "▶":
                for vc in client.voice_clients:
                    if vc.guild == reaction.message.guild:
                        voice = vc
                try:
                    voice.resume()
                    embed = discord.Embed(title="다시시작", description="음악을 다시 재생합니다.", color=0xa453d1)
                    embed.set_footer(
                        icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                        text="팀베이비(https://discord.gg/NXUEE4f)")
                    msg = await reaction.message.channel.send(embed=embed)
                    await reaction.message.delete()
                    await msg.add_reaction("⏸")
                    await msg.add_reaction("▶")
                    await msg.add_reaction("⏩")
                    await msg.add_reaction("❌")
                except:
                    pass

            if str(reaction.emoji) == "⏩":
                with open("list.json", "r", encoding="utf-8") as list_file:
                    js = json.load(list_file)
                for vc in client.voice_clients:
                    if vc.guild == reaction.message.guild:
                        voice = vc
                try:
                    if len(js["playlist"]) <= 1:
                        embed = discord.Embed(title="스킵", description="다음 음악이 없습니다.", color=0xa453d1)
                        voice.stop()
                    else:
                        embed = discord.Embed(title="스킵", description="다음 음악으로 넘어갑니다.\n다음 : `" + js["playlist"][1][1] + "`", color=0xa453d1)
                        voice.stop()
                    embed.set_footer(
                        icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                        text="팀베이비(https://discord.gg/NXUEE4f)")
                    msg = await reaction.message.channel.send(embed=embed)
                    await reaction.message.delete()
                    await msg.add_reaction("⏸")
                    await msg.add_reaction("▶")
                    await msg.add_reaction("⏩")
                    await msg.add_reaction("❌")
                except:
                    pass

            if str(reaction.emoji) == "❌":
                for vc in client.voice_clients:
                    if vc.guild == reaction.message.guild:
                        voice = vc
                try:
                    await voice.disconnect()
                    embed = discord.Embed(title="퇴장", description="퇴장합니다.", color=0xa453d1)
                    embed.set_footer(
                        icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                        text="팀베이비(https://discord.gg/NXUEE4f)")
                    await reaction.message.channel.send(embed=embed)
                except:
                    pass

    except:
        pass


@client.event
async def on_message(message):
    if message.content.startswith("/제임스도움말"):
        des1 = ("나. DJ **제임스 M. 베이비**...\n음악.. 들을거야?\n\n\u200b")

        des2 = ("음악재생 : `/음악` `노래제목`\n"
                "일시정지 : `/일시정지`\n"
                "다시시작 : `/다시시작`\n"
                "다음노래 : `/스킵`\n"
                "입장하기 : `/입장`\n"
                "퇴장하기 : `/퇴장`\n"
                "음악목록 : `/목록`\n"
                "목록삭제 : `/정리`\n"
                "볼륨조절 : `/볼륨` `1~100`\n\u200b")

        me = ("제작자 : <@441153729740275737>"
              "\n유튜브 : [섹시베이비](https://www.youtube.com/channel/UCv1unZDLpiO6c_7cBte7ZrA) 봇 초대 : [초대링크](https://discordapp.com/oauth2/authorize?client_id=543319948840140811&scope=bot)\n\u200b")

        embed = discord.Embed(color=0xa453d1)
        embed.add_field(name="소개", value=des1)
        embed.add_field(name="사용법", value=des2, inline=False)
        embed.add_field(name="출처", value=me, inline=False)
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.set_footer(icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png", text="팀베이비(https://discord.gg/t7xqqMK)")
        await message.channel.send(embed=embed)

    if message.content.startswith("/일시정지"):
        for vc in client.voice_clients:
            if vc.guild == message.guild:
                voice = vc
        try:
            voice.pause()
            embed = discord.Embed(title="일시정지", description="음악을 일시정지합니다.", color=0xa453d1)
            embed.set_footer(
                icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                text="팀베이비(https://discord.gg/NXUEE4f)")
            msg = await message.channel.send(embed=embed)
            await msg.add_reaction("⏸")
            await msg.add_reaction("▶")
            await msg.add_reaction("⏩")
            await msg.add_reaction("❌")
        except:
            pass

    if message.content.startswith("/스킵"):
        with open("list.json", "r", encoding="utf-8") as list_file:
            js = json.load(list_file)
        for vc in client.voice_clients:
            if vc.guild == message.guild:
                voice = vc
        try:
            if len(js["playlist"]) <= 1:
                embed = discord.Embed(title="스킵", description="다음 음악이 없습니다.", color=0xa453d1)
                voice.stop()
            else:
                embed = discord.Embed(title="스킵", description="다음 음악으로 넘어갑니다.\n다음 : `" + js["playlist"][1][1] + "`", color=0xa453d1)
                voice.stop()

            embed.set_footer(
                icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                text="팀베이비(https://discord.gg/NXUEE4f)")
            msg = await message.channel.send(embed=embed)
            await msg.add_reaction("⏸")
            await msg.add_reaction("▶")
            await msg.add_reaction("⏩")
            await msg.add_reaction("❌")
        except:
            pass

    if message.content.startswith("/다시시작"):
        for vc in client.voice_clients:
            if vc.guild == message.guild:
                voice = vc
        try:
            voice.resume()
            embed = discord.Embed(title="다시시작", description="음악을 다시 재생합니다.", color=0xa453d1)
            embed.set_footer(
                icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                text="팀베이비(https://discord.gg/NXUEE4f)")
            msg = await message.channel.send(embed=embed)
            await msg.add_reaction("⏸")
            await msg.add_reaction("▶")
            await msg.add_reaction("⏩")
            await msg.add_reaction("❌")
        except:
            pass
    if message.content.startswith("/퇴장"):
        for vc in client.voice_clients:
            if vc.guild == message.guild:
                voice = vc
        try:
            await voice.disconnect()
            embed = discord.Embed(title="퇴장", description="퇴장합니다.", color=0xa453d1)
            embed.set_footer(
                icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                text="팀베이비(https://discord.gg/NXUEE4f)")
            await message.channel.send(embed=embed)
        except:
            pass

    if message.content.startswith("/입장"):
        voice = ""
        for vc in client.voice_clients:
            if vc.guild == message.guild:
                voice = vc
        try:
            if voice:
                await voice.move_to(message.author.voice.channel)
            else:
                await message.author.voice.channel.connect()

            embed = discord.Embed(title="입장", description="입장합니다.", color=0xa453d1)
            embed.set_footer(
                icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                text="팀베이비(https://discord.gg/NXUEE4f)")
            await message.channel.send(embed=embed)

        except:
            embed = discord.Embed(title="오류", description="보이스채널에 들어가주세요.", color=0xa453d1)
            embed.set_footer(
                icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                text="팀베이비(https://discord.gg/NXUEE4f)")
            await message.channel.send(embed=embed)
            return

    if message.content.startswith("/목록"):
        with open("list.json", "r", encoding="utf-8") as list_file:
            js = json.load(list_file)
        list = js["playlist"]
        next = []
        for i in range(1, len(list)):
            next.append(str(i) + ". `" + list[i][1] + "`")
        try:
            embed = discord.Embed(title="목록", color=0xa453d1)
            embed.add_field(name="플레이중", value="`" + list[0][1] + "`\n\u200b", inline=False)
            embed.add_field(name="다음곡", value="\n".join(next), inline=False)
            embed.set_footer(
                icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                text="팀베이비(https://discord.gg/NXUEE4f)")
            msg = await message.channel.send(embed=embed)
            await msg.add_reaction("⏸")
            await msg.add_reaction("▶")
            await msg.add_reaction("⏩")
            await msg.add_reaction("❌")
        except:
            embed = discord.Embed(title="목록", color=0xa453d1)
            embed.add_field(name="플레이중", value="`" + list[0][1] + "`\n\u200b", inline=False)
            embed.set_footer(
                icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                text="팀베이비(https://discord.gg/NXUEE4f)")
            msg = await message.channel.send(embed=embed)
            await msg.add_reaction("⏸")
            await msg.add_reaction("▶")
            await msg.add_reaction("⏩")
            await msg.add_reaction("❌")

    if message.content.startswith("/볼륨"):
        volume1 = int(message.content.split(" ")[1])
        if volume1 < 1 or volume1 > 100:
            embed = discord.Embed(title="오류", description="1~100 사이로 입력해주세요.", color=0xa453d1)
            embed.set_footer(
                icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                text="팀베이비(https://discord.gg/NXUEE4f)")
            await message.channel.send(embed=embed)
            return
        file = open("볼륨.txt", "r")
        volume = file.read()
        file.close()
        file = open("볼륨.txt", "w")
        file.write(str(volume1))
        file.close()
        try:
            for vc in client.voice_clients:
                if vc.guild == message.guild:
                    voice = vc

            voice.source.volume = float(volume1) * 0.01
        except:
            pass
        embed = discord.Embed(title="볼륨", description="소리를 조절합니다. `" + str(volume) + "` -> `" + str(volume1) + "`", color=0xa453d1)
        embed.set_footer(
            icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
            text="팀베이비(https://discord.gg/NXUEE4f)")
        await message.channel.send(embed=embed)

    if message.content.startswith("/정리"):
        with open("list.json", "r", encoding="utf-8") as list_file:
            js = json.load(list_file)
        try:
            js = {
                "playlist": [js["playlist"][0]]
            }
            with open("list.json", "w", encoding="utf-8") as list_file:
                json.dump(js, list_file, ensure_ascii=False, indent="\t")
            embed = discord.Embed(title="정리", description="목록을 모두 지웠습니다.", color=0xa453d1)
            embed.set_footer(
                icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                text="팀베이비(https://discord.gg/NXUEE4f)")
            await message.channel.send(embed=embed)
            return
        except:
            pass

    if message.content.startswith("/음악"):
        try:
            summon_channel = message.author.voice.channel
        except:
            embed = discord.Embed(title="오류", description="보이스채널에 들어가주세요.", color=0xa453d1)
            embed.set_footer(
                icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                text="팀베이비(https://discord.gg/NXUEE4f)")
            await message.channel.send(embed=embed)
            return

        if "http" in message.content:
            url = message.content.split(" ")[1]
            ydl_opts = {
                'outtmpl': "file/" + url.split("=")[1] + '.mp3',
                'format': 'bestaudio/best',
                'no_warnings': True,
                'noplaylist': True,
                'nocheckcertificate': True,
                'ratelimit': '20K'
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            ydl = youtube_dl.YoutubeDL(ydl_opts)
            a = ydl.extract_info(url, download=False)
            title = a["title"]


        else:
            textToSearch = message.content[4:]
            query = parse.quote(textToSearch)
            url = "https://www.youtube.com/results?search_query=" + query
            response = request.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            vid = str(soup)[str(soup).find('Renderer":{"videoId":"')+22:str(soup).find('","thumbnail":{')]

            url = 'https://www.youtube.com/watch?v=' + vid

            ydl_opts = {
                'outtmpl': "file/" + url.split("=")[1] + '.mp3',
                'format': 'bestaudio/best',
                'no_warnings': True,
                'noplaylist': True,
                'nocheckcertificate': True
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            ydl = youtube_dl.YoutubeDL(ydl_opts)
            a = ydl.extract_info(url, download=False)
            title = a["title"]

        voice = ""
        cl = message.guild.get_member(745829394387566652)

        for vc in client.voice_clients:
            if vc.guild == message.guild:
                voice = vc

        if not voice:
            try:
                if cl.voice.channel:
                    voice = await summon_channel.connect()
                    await voice.disconnect()
                    voice = await summon_channel.connect()
            except:
                voice = await summon_channel.connect()

        with open("list.json", "r", encoding="utf-8") as list_file:
            js = json.load(list_file)
        list = js["playlist"]
        list.append([url, a["title"], message.guild.id])
        js["playlist"] = list
        with open("list.json", "w", encoding="utf-8") as list_file:
            json.dump(js, list_file, ensure_ascii=False, indent="\t")

        file = open("볼륨.txt", "r")
        volume = file.read()
        file.close()

        if len(list) >= 2:
            embed = discord.Embed(title="재생", description="`" + title + "`를 플레이리스트에 추가합니다.", color=0xa453d1)
            embed.set_footer(icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png", text="팀베이비(https://discord.gg/t7xqqMK)")
            msg = await message.channel.send(embed=embed)
            await msg.add_reaction("⏸")
            await msg.add_reaction("▶")
            await msg.add_reaction("⏩")
            await msg.add_reaction("❌")
            return
        else:
            voice.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("file/" + url.split("=")[1] + '.mp3'), volume=float(volume) * 0.01))
            embed = discord.Embed(title="재생", description="`" + title + "`를 재생합니다.", color=0xa453d1)
            embed.set_footer(icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png", text="팀베이비(https://discord.gg/t7xqqMK)")
            msg = await message.channel.send(embed=embed)
            await msg.add_reaction("⏸")
            await msg.add_reaction("▶")
            await msg.add_reaction("⏩")
            await msg.add_reaction("❌")
            return


client.run("토큰")





