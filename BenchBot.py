import discord
import asyncio

from gb5scraper import multicoreGB5
from gb5scraper import singlecoreGB5
import gb5scraper
import platform
import subprocess

# Opens the file containing the token and reads the first line
TOKEN = open("TOKEN.txt", "r").readline()

client = discord.Client()
OS = platform.system()


def BotInfo():
    return "```BenchBot 1.2, developed by Monabuntur, April 2021\n" \
           "Github: https://github.com/monabuntur/BenchBot```"


def BotSpecs():
    if OS == 'Linux':
        return f'```OS: {OS} {platform.release()}\n' \
               'CPU: %s' \
               f'Total RAM installed: {subprocess.check_output("echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE) / (1073741824)))", shell=True).strip().decode()}' % (str(subprocess.check_output("cat /proc/cpuinfo | grep 'model name' | uniq", shell=True).strip().decode())[13:])

    elif OS == 'Windows':
        return f'```OS: {OS} {platform.release()}, Build {platform.version()}\n' \
               f"CPU: {str(subprocess.check_output('wmic cpu get name /format:list').strip().decode()[5:])}\n" \
               f"Total RAM installed: {round(float(subprocess.check_output('wmic OS get TotalVisibleMemorySize /Value').strip().decode()[23:]) / 1048576, 1)} GB\n```"

    elif OS == "Darwin":
        return "```Too cool for macOS```"

    else:
        return "```Unsupported action, this likely means that the bot is running on an OS that is neither Windows nor " \
               "Linux``` "


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
           "|gbcomparemulti *CPU1* *CPU2* = compares two CPUs in multi core Geekbench 5\n" \
           "|bpecs = Specs of the system the bot is running on\n" \
           "|botinfo = pretty self explanatory" \
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

    elif message.content.startswith("|bpecs"):
        await message.channel.send(BotSpecs())

    elif message.content.startswith("|botinfo"):
        await message.channel.send(BotInfo())


@client.event
async def on_ready():
    print("BenchBot 1.2")
    asyncio.create_task(gb5scraper.main())


client.run(TOKEN)
