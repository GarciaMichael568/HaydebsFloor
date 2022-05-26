import os
import discord
from datetime import datetime
from pytz import timezone
from features.recentFeature import Recent
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
 #call time
now = datetime.now()
format = "%m/%d/%Y %I:%M:%S"
time1 = now.strftime(format) + "\n"
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
        nftCollection = Recent(message.content)
        nftCollection.message_to_underscore()
        nftCollection.get_totalListings()
        if (nftCollection.listedCount == -1):
            await message.channel.send("Couldn't find token: " + message.content)
            return
        nftCollection.get_recentlyListed()
        #check if dict is empty - todo
        nftCollection.format_results()
        nftCollection.format_output()
        await message.channel.send(time1 + nftCollection.output)


if __name__=="__main__":
    client.run(my_secret)