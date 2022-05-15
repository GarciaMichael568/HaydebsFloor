import os
import requests
import discord
import json
import time
import datetime
import webbrowser
#from requests.exceptions import ConnectionError
#get listing to adjust offset: most recent listings
#api-mainnet.magiceden.dev/v2/collections/:symbol/listings?offset=0&limit=20

#https://api-mainnet.magiceden.dev/v2/collections/{collection_looks_like_this}/stats
#get total listing subtract 20 = twenty most recent listings
#"listedCount" - 20

#https://magiceden.io/item-details/{tokenAddress}
#buy/image
my_secret = 'OTc1MjQ4OTU3OTI2MTU0MjUw.GpXccp.iwyA6pXkchhECpY2kA6G4XLx_59HG10rhQy8_0'
#my_secret = os.environ['Bullish']
client = discord.Client()


#functions
def get_recentlyListed(listedCount, nft):
    url = requests.get(
        f"https://api-mainnet.magiceden.dev/v2/collections/{nft}/listings?offset={listedCount-5}&limit=5"
    )
    print(url)
    data = json.loads(url.text)
    results = []
    for token in data:
        results.append(token["price"])
        results.append(token["tokenMint"])
    return results


def get_totalListings(nft):
    url =requests.get(f"https://apimainnet.magiceden.dev/v2/collections/{nft}/stats")
    data = json.loads(url.text)
    listedCount = data["listedCount"]
    return listedCount
    


def format_results(results):
    newResults = [
        "https://magiceden.io/item-details/" +
        url if isinstance(url, str) else "Price: " + str(url)
        for url in results
    ]
    return newResults


#main
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    nftCollection = "slowlanaslugs"
    if message.author == client.user:
        return
    if message.content.startswith('!recent'):
        print(message.content)
        listedCount = get_totalListings(nftCollection)
        print(listedCount)
        results = get_recentlyListed(listedCount, nftCollection)
        #print(results)
        results = format_results(results)
        results = '\n'.join(str(e) for e in results)
        await message.channel.send(results)
        #for nft in results:
        #await message.channel.send(nft)


client.run(my_secret)