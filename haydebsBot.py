import os
import requests
import discord
import json
import time
import datetime
import webbrowser
import operator
from dotenv import load_dotenv
load_dotenv()
#from requests.exceptions import ConnectionError
#get listing to adjust offset: most recent listings
#api-mainnet.magiceden.dev/v2/collections/:symbol/listings?offset=0&limit=20

#https://api-mainnet.magiceden.dev/v2/collections/{collection_looks_like_this}/stats
#get total listing subtract 20 = twenty most recent listings
#"listedCount" - 20

#https://magiceden.io/item-details/{tokenAddress}
#buy/image
my_secret = os.getenv('Bullish')
client = discord.Client()


#functions
def get_recentlyListed(listedCount, nft):
    url = requests.get(
        f"https://api-mainnet.magiceden.dev/v2/collections/{nft}/listings?offset={listedCount - 5}&limit=5"
    )
    print(url)
    data = json.loads(url.text)
    results = {}
    for token in data:
        results.update({token["tokenMint"]:token["price"]})
    sorted_d = dict( sorted(results.items(), key=operator.itemgetter(1)))
    return sorted_d


def get_totalListings(nft):
    try:
        url = requests.get(
            f"https://api-mainnet.magiceden.dev/v2/collections/{nft}/stats")
        data = json.loads(url.text)
        listedCount = data["listedCount"]
        return listedCount
    except:
        return -1


def format_results(results):
    dictList = list(results.values())
    big = list(results.keys())
    end = []
    for i in range(len(big)):
      end.append(dictList[i])
      end.append(big[i])
    newResults = [
        "https://magiceden.io/item-details/" +
        url if isinstance(url, str) else "Price: " + str(url)
        for url in end
    ]
    return newResults


def message_to_underscore(nft):
    finalmessage = nft[8:]
    finalmessage = finalmessage.replace(" ","_")
    return finalmessage

 
#main
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    #nftCollection = message_to_underscore(message.content)
    if message.author == client.user:
        return
    if message.content.startswith('!recent'):
        nftCollection = message_to_underscore(message.content).lower()
        #print("1. Successfully captured nft name.")
        listedCount = get_totalListings(nftCollection)
        if (listedCount == -1):
            await message.channel.send("Couldn't find token: " + message.content)
            return
        #print("2. Successfully captured total listings.")
        results = get_recentlyListed(listedCount, nftCollection)
        #print("3. Succesfully captured recently listed.")
        results = format_results(results)
        #print("4. Succesfully formatted list.")
        results = '\n'.join(str(e) for e in results)
        #print("5. Successfully changed list to string.")
        await message.channel.send(results)


if __name__=="__main__":
    client.run(my_secret)