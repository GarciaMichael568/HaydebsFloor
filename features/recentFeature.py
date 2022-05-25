import requests
import json
import operator
class Recent:
    
    def __init__(self,message):
        self.message = message
        self.nft = ""
        self.listedCount = 0
        self.sortedDict = {}
        self.result = ""
        self.output = ""
    
    #instance methods: in order of operation
    def message_to_underscore(self):
        finalmessage = self.message[8:]
        finalmessage = finalmessage.replace(" ","_")
        self.nft = finalmessage.lower()

    def get_totalListings(self):
        try:
            url = requests.get(f"https://api-mainnet.magiceden.dev/v2/collections/{self.nft}/stats")
            data = json.loads(url.text)
            listedC = data["listedCount"]
            self.listedCount = listedC
        except:
            self.listedCount = -1

    def get_recentlyListed(self):
        try:
            url = requests.get(
                f"https://api-mainnet.magiceden.dev/v2/collections/{self.nft}/listings?offset={self.listedCount - 5}&limit=5"
            )
            data = json.loads(url.text)
            results = {}
            for token in data:
                results.update({token["tokenMint"]:token["price"]})
            sorted_d = dict( sorted(results.items(), key=operator.itemgetter(1)))
            self.sortedDict = sorted_d
        except:
            self.sortedDict = {}

    def format_results(self):
        dictList = list(self.sortedDict.values())
        big = list(self.sortedDict.keys())
        end = []
        for i in range(len(big)):
            end.append(dictList[i])
            end.append(big[i])
        self.result = ["https://magiceden.io/item-details/" + url if isinstance(url, str) else "Price: " + str(url) for url in end]

    def format_output(self):
        self.output = '\n'.join(str(e) for e in self.result)
