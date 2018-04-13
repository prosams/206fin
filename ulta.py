import requests
import json
from bs4 import BeautifulSoup

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

def cacheRequest(url):
    if url in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[url]
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url)
        resptext = resp.text
        CACHE_DICTION[url] = resp.text
        fw = open(CACHE_FNAME,"w")
        fw.write(resptext)
        fw.close() # Close the open file
        return CACHE_DICTION[url]

# eyereq = cacheRequest("https://www.ulta.com/makeup-eyes?N=26yd&No=0&Nrpp=1000")
# # this is because max numbers of products on a page is 1000 but there are like
# # 1700 products total for eye stuff so u need to do it twice
# facereq = cacheRequest("https://www.ulta.com/makeup-face?N=26y3&No=0&Nrpp=1000")
# lipreq = cacheRequest("https://www.ulta.com/makeup-lips?N=26yq&No=0&Nrpp=1000")
# toolreq = cacheRequest("https://www.ulta.com/tools-brushes-makeup-brushes-tools?N=27hn&No=0&Nrpp=1000")

def uniqueUltaUrl(type): #can be eyes, face, lips, and tools
    base = "https://www.ulta.com/"
    if type == "eyes": # https://www.ulta.com/makeup-eyes?N=26yd&No=0&Nrpp=1000
        category = "makeup-eyes"
        end = "?N=26yd&No=0&Nrpp=1000"
    elif type == "face":
        category = "makeup-face"
        end = "?N=26y3&No=0&Nrpp=1000"
    elif type == "lips":
        category = "makeup-lips"
        end = "?N=26yq&No=0&Nrpp=1000"
    elif type == "tools":
        category = "tools-brushes-makeup-brushes-tools"
        end = "?N=27hn&No=0&Nrpp=1000"
    total = base + category + end
    return total

def getAllProdType(kind): #takes in eyes, lips, face, tools
    returnlist = []
    first_url = uniqueUltaUrl(kind)
    page = cacheRequest(first_url)
    soup = BeautifulSoup(page, 'html.parser')
    elements = soup.find_all(class_ = "productQvContainer")

    for x in elements:
        print("++++++++")
        roughDesc = x.find(class_="prod-desc")
        finDesc = roughDesc.text.strip() # basically product name

        titlerough = x.find(class_ = "prod-title")
        finTit = titlerough.text.strip() # product brand

        urlDetails = x.find('a', href = True)["href"] # this should be the indiv product url
        finalurl = "https://www.ulta.com" + urlDetails

        try:
            pricerough = x.find(class_ = "regPrice")
            finPrice = pricerough.text.strip()
            Sale = False
            # print("Not on Sale")
        except:
            pricerough = x.find(class_ = "pro-new-price")
            finPrice = pricerough.text.strip()
            Sale = True
            # print("On Sale")

        #-------------- specific page crawl starts here ----------------

        second = cacheRequest(finalurl)
        soup = BeautifulSoup(second, 'html.parser')

        proditem = soup.find(class_ = "product-item-no") #has size and itemnum
        prodnum = soup.find(id = "itemNumber")
        finalprodnum = prodnum.text.strip()

        itemsize = proditem.find(id = "itemSize")
        sizefinal = itemsize.text.strip()
        itemdim = proditem.find(id = "itemSizeUOM")
        dimfinal = itemdim.text.strip()
        sizeNdim = sizefinal + " " + dimfinal

        percentrecommend = soup.find(class_ = "pr-snapshot-consensus-value pr-rounded")
        finalpercentrec = percentrecommend.text.strip()

        numreviewclass = soup.find(class_ = "pr-snapshot-average-based-on-text")
        numreview = numreviewclass.find(class_ = "count")
        numreviewfinal = numreview.text.strip()

        starrate = soup.find(class_ = "pr-rating pr-rounded average")
        starfinal = starrate.text.strip()
        # print(finalprodnum)
        # print(finalpercentrec + " would recommend")
        # print(numreviewfinal + " reviews")
        # print(starfinal + " stars")
        ultimateTuple = (finDesc, finTit, finPrice, finalprodnum, sizeNdim, finalpercentrec, numreviewfinal, starfinal, Sale, finalurl)
        returnlist.append(ultimateTuple)
        # print(ultimateTuple)
    print(returnlist)
    return returnlist

eyelist = getAllProdType("eyes")
