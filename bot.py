import requests
import re
import discord
from datetime import datetime as date 

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def cleanhtml(raw):
  cleantext = re.sub(CLEANR, ',', raw)
  cleantext = cleantext.split(",")
  cleantext = [x for x in cleantext if x]
  return cleantext


client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$table'):
        day = date.today().strftime('%A')
        weekend = False
        if day != "Saturday":
            if day != "Sunday":
                pass
            else:
                weekend = True
        else:
            weekend = True
        
        if weekend != True:
            r = requests.get('http://baka-rozvrh.bubileg.cz/rozvrh-content.php?section=marvdf')
            r = r.text.split("<tr>")
            rr = []

            for tr in r:
                if tr.startswith("<td class=\"class\">2IT</td>"):
                    tr = cleanhtml(tr)
                    tr.pop(len(tr)-1)
                    tr.pop(0)
                    rr.append(tr)
                else:
                    pass
            twoIt = rr[0]
            embedVar = discord.Embed(title="Rozvrh 2.IT", description="Dnes je: {}".format(date.today().strftime('%y.%m.%d')), color=0xF43701)
            count = 0
            count2 = 0
            while count != len(twoIt) / 3:
                embedVar.add_field(name="{}. {}".format(count+1, twoIt[count2]), value="Učitel: {}\nUčebna: {}".format(twoIt[count2+1], twoIt[count2+2]), inline=True)
                count+=1
                count2+=3

            await message.channel.send(embed=embedVar)
        else:
            await message.channel.send("O víkendech se zobrazuje pouze starý rozvrh, vrať se v pondělí.")

client.run("token")