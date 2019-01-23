# -*- coding: utf-8 -*-

from Naked.toolshed.shell import execute_js, muterun_js
import discord
import twitch
import sched
import time
import sys
import os
import wikia
from random import randint

TOKEN = str(open("token","r").readline())
TOKEN = str(TOKEN.replace("\r",''))
TOKEN = str(TOKEN.replace("\n",''))
client = discord.Client()

with open("twitchCred") as f:
    content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

client2 = twitch.TwitchClient(content[0],content[1])

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('?hello'):
        msg= "You're a special kind of child aren't you?"
        await client.send_message(message.channel, msg)

    if message.content.startswith('!stream'):
        ans = turnNameintoID(str(message.content).split('!stream ')[1])
        if "Offline" in ans:
            msg = "{0.author.mention} No stream live".format(message)
            await client.send_message(message.channel, msg)
        elif "Unknown" in ans:
            msg = "{0.author.mention} Unknown username, please check it".format(message)
            await client.send_message(message.channel, msg)
        else:
            msg = "{0.author.mention} Stream Online here: " + str(ans)
            msg = msg.format(message)
            await client.send_message(message.channel, msg)
    
    if message.content.startswith('?stream'):
        streamerList = ['StreamerOne', 'StreamerTwo', 'StreamerThree']
        for streamer in streamerList:
            ans = turnNameintoID(str(streamer))
            if "Offline" in ans:
                msg = "{0.author.mention} The stream of " + str(streamer) + " is offline"
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                msg = "{0.author.mention} The stream of " + str(streamer) + " is live there: " + str(ans)
                msg = msg.format(message)
                await client.send_message(message.channel, msg)


    if message.content.startswith('!avatar'):
        for user in message.mentions:
            await client.send_message(message.author, embed=avatar(user))

    if message.content.startswith('?avatar') and ' ' in message.content:
        for user in message.mentions:
            await client.send_message(message.channel, embed=avatar(user))

    if message.content.startswith('?anime'):
        await client.send_message(message.channel, "On it")
        msg = ''
        try:
            types = message.content.split(', ')[1]
            if "tv" in types.lower() or "movie" in types.lower() or  "ova" in types.lower() or "special" in types.lower() or "ona" in types.lower():
                await client.send_message(message.channel, "Type " + types + " detected, query in progress")
            else:
                message.content = message.content.split(', ')[0] + ", tv"
                await client.send_message(message.channel, "No type have been detected, types are TV, movie, specia, ona or ova, assuming TV")
        except:
            message.content = message.content + ", tv"
            await client.send_message(message.channel, "No anime type have been given, TV is assumed")
        response = muterun_js('final.js ' + message.content.split('?anime ')[1])
        if response.exitcode==0:
            lista = str(response.stdout).split(" | ")
            del lista[-1]
            for anime in lista:
                test = str(anime).split(" $ ")
                anime_url = '<' +str(test[1]) + '>'
                msg += 'Here is your query: ' + test[0][2:]  + " " + anime_url + '\n'.format(message)
            if msg == '':
                await client.send_message(message.channel, "Nothing was found or returned")
            else:
                await client.send_message(message.channel, msg)
        else:
            msg = "Sorry, there is a problem: " + str(response.stderr) + " Go tell someone"
            await client.send_message(message.channel, msg)
    
    if message.content.startswith('?season'):
        await client.send_message(message.channel, "On it")
        listMessage = season(message.content, message)
        for msg in listMessage:
            await client.send_message(message.author, msg)
        await client.send_message(message.channel, "Result sent by DM")

    if message.content.startswith('?random'):
        msgList = random(message)
        for msg in msgList:
            try:
                await client.send_message(message.channel, msg)
            except:
                'pass'

    if message.content.startswith('?kancolle '):
        page = wikia.page("Kancolle", message.content.split('?kancolle ')[1])
        await client.send_message(message.channel, "Query result: " + page.title + ': ' + page.url + ''.format(message))

    if message.content.startswith('?aaci'):
        await client.send_message(message.channel, "Here is the AACI table: http://i.imgur.com/nkpYAwB.png")

    if message.content.startswith('?lb'):
        await client.send_message(message.channel, "Here is the land base table: https://i.imgur.com/pmuBMki.png")

    if message.content.startswith('?dev'):
        await client.send_message(message.channel, "Here is the development table: https://i.imgur.com/ZehPS8X.png")

    if message.content.startswith('?fit'):
        await client.send_message(message.channel, "Here is the fit table: https://i.imgur.com/gsRpH70.png")

    if message.content.startswith('?range'):
        await client.send_message(message.channel, "Here is the range table: https://i.imgur.com/JubBLwo.png")

    if message.content.startswith('!help'):
        msg = 'There is no help for people like you {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

def season(request, message):
    msg = 'Here is your query : '
    i = 0
    messageList = []
    response = muterun_js('season.js ' + request.split('?season ')[1])
    if response.exitcode==0:
        lista = str(response.stdout).split(" | ")
        del lista[-1]
        for anime in lista:
            name, url = str(anime).split(" $ ")
            anime_url = '<' + str(url) + '>'
            msg +=  name[2:] + " " + anime_url + '\n'.format(message)
            if i == 13:
                messageList.append(msg)
                i = 0
                msg = ''
            i = i + 1
        return messageList
    else:
        return "Sorry, there was a problem: " + str(response.stderr) + " Go tell someone"

def random(message):
    l=0
    msgList = []
    for l in range(3):
        ids, idl = generateId()
        msg = fetchRandom(ids, idl, message, 0)
        if msg != '':
            msgList.append(msg)
    return msgList

def fetchRandom(ids, idl, message, ntry):
    msg = ''
    query = "https://myanimelist.net/anime/" + str(ids)
    idl = ','+str(ids)+','
    response = muterun_js('random.js ' + query)
    if response.exitcode == 0:
        name, url = str(response.stdout).split(" $ ")
        anime_url = '<' + str(url[:-4]) + '>'
        msg = 'Here is your query: ' + name[2:] + " " + anime_url + ''.format(message)
        if(len(msg) > 2000):
            with open('idban', 'a') as f:
                f.write(idl)
            if(ntry < 2):
                ids, idl = generateId()
                fetchRandom(ids, idl, message, ntry+1)
        else:
            return msg
    else:
        return "Sorry, there was a problem: " + str(response.stderr) + " Go tell someone"

def generateId():
    ids = randint(0,35800)
    idl = ','+str(ids)+','
    if idl in open('idban').read():
        while(idl in open('idban').read()):
            print('Id banned')
            ids = randint(0,35800)
            idl = ','+str(ids)+','
    return ids, idl


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def checkUsersLive(userId):
    global client2
    get_stream_by_user = client2.streams.get_stream_by_user(userId, "live")
    acc = str(get_stream_by_user)
    if "live" in acc:
        before, after = acc.split("'url': '")
        url, useless = after.split("', 'views'")
        return url
    else:
        return "Offline"

def turnNameintoID(name):
    global client2
    users = client2.users.translate_usernames_to_ids([name])
    for user in users:
        idUser = user.id
    try:
        return checkUsersLive(idUser)
    except:
        return "Unknown"

def avatar(user):
    pfp = user.avatar_url
    embed = discord.Embed(title="User request", description='{}, self Profile picture'.format(user.mention), color=0xecce8b)
    embed.set_image(url=(pfp))
    return embed

client.run(TOKEN)
