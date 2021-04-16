import discord
from bs4 import BeautifulSoup
import requests
import asyncio

multicoreGB5 = {}
singlecoreGB5 = {}

TOKEN = 'DISCORDTOKEN'
page = requests.get("https://browser.geekbench.com/processor-benchmarks")
soup = BeautifulSoup(page.content, 'html.parser')

client = discord.Client()


def CPUs():
    CPUList = []
    for CPU in multicoreGB5:
        CPUList.append(CPU[0])
    return CPUList


def helpcom():
    return "```" \
           "Commands\n" \
           "|help = this thing here\n" \
           "|gbsingle *full CPU name*\n" \
           "|gbmulti *full CPU name*" \
           "```"


def Geekbenchmulticore(CPU):
    return f'```The {CPU} scores on average {multicoreGB5.get(CPU)} points in Geekbench 5 multicore```'


def Geekbenchsinglecore(CPU):
    return f'```The {CPU} scores on average {singlecoreGB5.get(CPU)} points in Geekbench 5 singlecore```'


async def GatherData(CPUs, results, data):
    for CPU, result in zip(CPUs, results[1:]):
        CPUmod = CPU.text.strip().replace(" ", "_").replace("Intel_Core_i3-", "").replace("Intel_Core_i5-",
                                                                                          "").replace(
            "Intel_Core_i7-", "").replace("Intel_Core_i9-", "").replace("AMD_Ryzen_3_", "").replace("AMD_Ryzen_5_",
                                                                                                    "").replace(
            "AMD_Ryzen_7_", "").replace("AMD_Ryzen_9_", "").replace("AMD_Ryzen_Threadripper_", "").replace(
            "Intel_Xeon_", "").replace("AMD_", "").replace("Intel_", "")

        data[CPUmod] = result.text.strip()


@client.event
async def on_message(message):
    if message.content.startswith("|help"):
        await message.channel.send(helpcom())

    elif message.content.startswith("|gbmulti"):
        await message.channel.send(Geekbenchmulticore(message.content.split()[1]))

    elif message.content.startswith("|gbsingle"):
        await message.channel.send(Geekbenchsinglecore(message.content.split()[1]))

    elif message.content.startswith("|cpus"):
        await message.channel.send(CPUs())


@client.event
async def on_ready():
    print("BenchBot 1.0")
    while True:
        multiresults = soup.find(id='multi-core').find_all(class_='score')
        singleresults = soup.find(id='single-core').find_all(class_='score')

        CPUs1 = soup.find(id='multi-core').find_all('a')
        CPUs2 = soup.find(id='single-core').find_all('a')

        await GatherData(CPUs1, multiresults, multicoreGB5)
        await GatherData(CPUs2, singleresults, singlecoreGB5)

        await asyncio.sleep(3600)


client.run(TOKEN)
