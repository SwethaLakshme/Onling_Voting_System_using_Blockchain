import hashlib
import json


class Block():
    def __init__(self,tstamp,name,voterid,party,prevhash=''):
        
        self.tstamp=tstamp
        self.name=name
        self.voterid=voterid
        self.party=party
        self.prevhash=prevhash
        self.hash=self.calcHash()

    def calcHash(self):
        block_string=json.dumps({"tstamp":self.tstamp,"name":self.name,"voterid":self.voterid,"party":self.party,"prevhash":self.prevhash},sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def __str__(self):
        
        string="tstamp: "+str(self.tstamp)+"\n"
        string+="name: "+str(self.name)+"\n"
        string+="voterid"+str(self.voterid)+"\n"
        string+="party"+str(self.party)+"\n"
        string+="prevhash: "+str(self.prevhash)+"\n"
        string+="hash: "+str(self.hash)+"\n"
        return string
##    def printHashes(self):
##        print("prevhash",self.prevhash)
##        print("hash",self.hash)

##bblock=Block(1,"01/02/2019",100)
##bblock.printHashes()

class BlockChain():
    def __init__(self):
        self.chain=[self.generateGenesisBlock(),]
    def generateGenesisBlock(self):
        return Block("01/01/2019","gensis name","gensis reason","Gensis Block")
    def getLastBlock(self):
        return self.chain[-1]
    def addBlock(self,newBlock):
        newBlock.prevhash=self.getLastBlock().hash
        newBlock.hash=newBlock.calcHash()
        self.chain.append(newBlock)

# osa=BlockChain()
# li=[]
# li2=[]
# li.append("1")
# li.append("20/05/2017")
# li.append("saran")
# li.append("fever")
# li.append("something cold")
# li.append("2")
# li.append("20/05/2017")
# li.append("gopal")
# li.append("fever")
# li.append("something cold")
# print(li)
# for i in range(len(li)/4):
#     li2.append(li[i])
# print(li2)
# osa.addBlock(Block(li[0],li[1],li[2],li[3],li[4]))
# print(type(osa.chain))
# for b in osa.chain:
#     print(b.nonce)
#     print(b.tstamp)
#     print(b.name)
#     print(b.reason)
#     print(b.detail)
#     print(b.prevhash)
#     print(b.hash)
