import discord
import asyncio

from gb5scraper import multicoreGB5
from gb5scraper import singlecoreGB5
import gb5scraper

# Opens the file containing the token and reads the first line
TOKEN = open("TOKEN.txt", "r").readline()

client = discord.Client()


# Compares two CPUs

def Faster(dictionary, CPU1, CPU2):
    if int(dictionary.get(CPU1)) > int(dictionary.get(CPU2)):
        return f'The {CPU1} is ~{round(100 - (int(dictionary.get(CPU2)) / int(dictionary.get(CPU1))) * 100, 2)}% faster'
    elif int(dictionary.get(CPU2)) > int(dictionary.get(CPU1)):
        return f'The {CPU2} is ~{round(100 - (int(dictionary.get(CPU1)) / int(dictionary.get(CPU2))) * 100, 2)}% faster'


def CompareCPU(dictionary, CPU1, CPU2):
    return f'```{CPU1} --> {dictionary.get(CPU1)} points\n' \
           f'{CPU2} --> {dictionary.get(CPU2)} points\n' \
           f'---------------------------------\n' \
           f'{Faster(dictionary, CPU1, CPU2)}```'


# Help command


def helpcom():
    return "```" \
           "Commands\n" \
           "|help = this thing here\n" \
           "|gbsingle *CPU* = single core Geekbench 5\n" \
           "|gbmulti *CPU* = multi core Geekbench 5\n" \
           "|gbcomparesingle *CPU1* *CPU2* = compares two CPUs in single core Geekbench 5\n" \
           "|gbcomparemulti *CPU1* *CPU2* = compares two CPUs in multi core Geekbench 5" \
           "```"


def Geekbenchmulticore(CPU):
    return f'```The {CPU} scores on average {multicoreGB5.get(CPU)} points in Geekbench 5 multicore```'


def Geekbenchsinglecore(CPU):
    return f'```The {CPU} scores on average {singlecoreGB5.get(CPU)} points in Geekbench 5 singlecore```'


@client.event
async def on_message(message):
    if message.content.startswith("|help"):
        await message.channel.send(helpcom())

    elif message.content.startswith("|gbcomparesingle"):
        try:
            await message.channel.send(CompareCPU(singlecoreGB5, message.content.split()[1].capitalize(),
                                                  message.content.split()[2].capitalize()))

        except IndexError:
            await message.channel.send("```Please try again with valid CPUs```")

    elif message.content.startswith("|gbcomparemulti"):
        try:
            await message.channel.send(
                CompareCPU(multicoreGB5, message.content.split()[1].capitalize(),
                           message.content.split()[2].capitalize()))

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
    print("BenchBot 1.1")
    asyncio.create_task(gb5scraper.main())
    print("Ready")


client.run(TOKEN)
