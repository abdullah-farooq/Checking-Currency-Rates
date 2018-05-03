import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import time

def connection(targetUrl):
    #getting infomation from xml
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    req = urllib.request.Request(url=targetUrl, headers=headers)  
    response = urllib.request.urlopen(req)
    tree = ET.fromstring(response.read())
    
    return tree   #root of the element tree, root.tag = 'Rates'

#define structure of data storage
class Rate(object):
    def __init__(self, symbol=None, bid=None, ask=None, high=None, low=None, direction=None, last=None, target=None):
        self.symbol = symbol
        self.bid = bid
        self.ask = ask
        self.high = high
        self.low = low
        self.direction = direction
        self.last = last
        self.target = target


#define function initialData, initialize the rate element in the array
#the symbol of the rate element root[i].attrib['Symbol']
#for all children:
#   tag:    root[i][j].tag
#   value:  root[i][j].text

def initialData(root, rateList, num):
    for i in range(0, num):
        rateList.append(Rate(root[i].attrib['Symbol'], root[i][0].text, root[i][1].text, root[i][2].text, root[i][3].text, root[i][4].text, root[i][5].text))
    return

def printList(rateList, num):
    print('Symbol'.rjust(14),'Bid'.rjust(14),'Last'.rjust(14),'      Target')
    print('---------------------------------------------------------')
    for i in range(0, num):
        print(rateList[i].symbol.rjust(14), rateList[i].bid.rjust(14), rateList[i].last.rjust(14), '       ', rateList[i].target)
    return

def setTarget(rateList, num):
    flag = False
    symbol_input = input("Enter the symbol that you want to keep track of:")
    i=0
    for i in range(0, num):
        if rateList[i].symbol == symbol_input:
            target_input = input("Enter the target rate:")
            rateList[i].target = target_input
            flag = True
            break
    if flag == False:
        print(symbol_input, ' is not in the list.')
    else:
        print('The target rate of',symbol_input,'has set to',target_input)
        print("")
    return (i,float(target_input))

def isTargetReached(index_and_target,rateList):

    Bid=float(rateList[index_and_target[0]].bid)
    flag=False
    print('The current rate is ', Bid)
    if(Bid==index_and_target[1]):
        print("Target Achieved")
        print("System will exit shortly......")
        flag=True
    elif(index_and_target[1]<Bid):
        print("Entered Target rate is lesser than the Current rate")
        print("Waiting for Bid to reach Target......")
    elif(index_and_target[1]>Bid):
        print("Entered Target rate is greater than the Current rate")
        print("Waiting for Bid to reach Target......")
    return flag

def main():
    #schedule.clear()
    flag=False

    targetUrl = 'http://rates.fxcm.com/RatesXML'

    rateList = []   #list of Rate object
    
    root = connection(targetUrl)    #root of the element tree
    num = len(root.getchildren())   #number of children of the root
    
    initialData(root, rateList, num)
    printList(rateList, num)

    #index_and_target is a tuple that contains index of currency as well as target rate
    #index_and_target[0]=index -----index_and_target[1]=target
    index_and_target=setTarget(rateList, num)

    while(flag==False):
        root = connection(targetUrl)
        rateList=[]
        initialData(root, rateList, num)
        flag=isTargetReached(index_and_target,rateList)
        print("")
        time.sleep(10)
    
if __name__ == "__main__":
    main()
