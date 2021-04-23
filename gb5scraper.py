from bs4 import BeautifulSoup
import requests
import asyncio
import datetime


multicoreGB5 = {}
singlecoreGB5 = {}


'''
This function removes unnecessary parts from the CPU names and capitalizes them to make it easier for the user to input
the correct processor
'''


async def GatherData(CPUs, results, data):
    for CPU, result in zip(CPUs, results[1:]):
        CPUmod = CPU.text.strip().replace(" ", "_").replace("Intel_Core_i3-", "").replace("Intel_Core_i5-",
                                                                                          "").replace(
            "Intel_Core_i7-", "").replace("Intel_Core_i9-", "").replace("AMD_Ryzen_3_", "").replace("AMD_Ryzen_5_",
                                                                                                    "").replace(
            "AMD_Ryzen_7_", "").replace("AMD_Ryzen_9_", "").replace("AMD_Ryzen_Threadripper_", "").replace(
            "Intel_Xeon_", "").replace("AMD_", "").replace("Intel_", "").capitalize()

        data[CPUmod] = result.text.strip()

# HTML parser


async def main():
    while True:
        page = requests.get("https://browser.geekbench.com/processor-benchmarks")
        soup = BeautifulSoup(page.content, 'html.parser')

        multiresults = soup.find(id='multi-core').find_all(class_='score')
        singleresults = soup.find(id='single-core').find_all(class_='score')

        CPUs1 = soup.find(id='multi-core').find_all('a')
        CPUs2 = soup.find(id='single-core').find_all('a')

        await GatherData(CPUs1, multiresults, multicoreGB5)
        await GatherData(CPUs2, singleresults, singlecoreGB5)
        print(f'Geekbench, updated {datetime.datetime.now().strftime("%B %d, %Y --- %X %Z")}', end='')

        await asyncio.sleep(3600*24)
