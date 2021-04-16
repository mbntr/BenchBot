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


def Faster(dictionary, CPU1, CPU2):
    if int(dictionary.get(CPU1)) > int(dictionary.get(CPU2)):
        return f'The {CPU1} is ~{round(100 - (int(dictionary.get(CPU2)) / int(dictionary.get(CPU1)))*100, 2)}% faster'
    elif int(dictionary.get(CPU2)) > int(dictionary.get(CPU1)):
        return f'The {CPU2} is ~{round(100 - (int(dictionary.get(CPU1)) / int(dictionary.get(CPU2)))*100, 2)}% faster'


def helpcom():
    return "```" \
           "Commands\n" \
           "|help = this thing here\n" \
           "|gbsingle *CPU* = single core Geekbench 5\n" \
           "|gbmulti *CPU* = multi core Geekbench 5\n" \
           "|gbcomparesingle *CPU1* *CPU2* = compares two CPUs in single core Geekbench 5\n" \
           "|gbcomparemulti *CPU1* *CPU2* = compares two CPUs in multi core Geekbench 5"\
           "```"


def Geekbenchmulticore(CPU):
    return f'```The {CPU} scores on average {multicoreGB5.get(CPU)} points in Geekbench 5 multicore```'


def Geekbenchsinglecore(CPU):
    return f'```The {CPU} scores on average {singlecoreGB5.get(CPU)} points in Geekbench 5 singlecore```'


def CompareCPU(dictionary, CPU1, CPU2):
    return f'```{CPU1} --> {dictionary.get(CPU1)} points\n' \
           f'{CPU2} --> {dictionary.get(CPU2)} points\n' \
           f'---------------------------------\n' \
           f'{Faster(dictionary, CPU1, CPU2)}```'


async def GatherData(CPUs, results, data):
    for CPU, result in zip(CPUs, results[1:]):
        CPUmod = CPU.text.strip().replace(" ", "_").replace("Intel_Core_i3-", "").replace("Intel_Core_i5-",
                                                                                          "").replace(
            "Intel_Core_i7-", "").replace("Intel_Core_i9-", "").replace("AMD_Ryzen_3_", "").replace("AMD_Ryzen_5_",
                                                                                                    "").replace(
            "AMD_Ryzen_7_", "").replace("AMD_Ryzen_9_", "").replace("AMD_Ryzen_Threadripper_", "").replace(
            "Intel_Xeon_", "").replace("AMD_", "").replace("Intel_", "").capitalize()

        data[CPUmod] = result.text.strip()


@client.event
async def on_message(message):
    if message.content.startswith("|help"):
        await message.channel.send(helpcom())

    elif message.content.startswith("|gbcomparesingle"):
        try:
            await message.channel.send(CompareCPU(singlecoreGB5, message.content.split()[1].capitalize(), message.content.split()[2].capitalize()))

        except IndexError:
            await message.channel.send("```Please try again with valid CPUs```")

    elif message.content.startswith("|gbcomparemulti"):
        try:
            await message.channel.send(
                CompareCPU(multicoreGB5, message.content.split()[1].capitalize(), message.content.split()[2].capitalize()))

        except IndexError:
            await message.channel.send("```Please try again with valid CPUs```")

    elif message.content.startswith("|gbmulti"):
        try:
            await message.channel.send(Geekbenchmulticore(message.content.split()[1].capitalize()))

        except IndexError or TypeError:
            await message.channel.send("```Please try again with a valid CPU```")

    elif message.content.startswith("|gbsingle"):
        try:
            await message.channel.send(Geekbenchsinglecore(message.content.split()[1].capitalize()))

        except IndexError or TypeError:
            await message.channel.send("```Please try again with a valid CPU```")


@client.event
async def on_ready():
    print("BenchBot 1.1\nReady")
    while True:
        multiresults = soup.find(id='multi-core').find_all(class_='score')
        singleresults = soup.find(id='single-core').find_all(class_='score')

        CPUs1 = soup.find(id='multi-core').find_all('a')
        CPUs2 = soup.find(id='single-core').find_all('a')

        await GatherData(CPUs1, multiresults, multicoreGB5)
        await GatherData(CPUs2, singleresults, singlecoreGB5)

        await asyncio.sleep(3600)


client.run(TOKEN)
