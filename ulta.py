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

def cacheRequest(type):
    unique_ident = uniqueUltaUrl(type)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(unique_ident)
        resptext = resp.text
        CACHE_DICTION[unique_ident] = resp.text
        fw = open(CACHE_FNAME,"w")
        fw.write(resptext)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

# eyeurl = "https://www.ulta.com/makeup-eyes?N=26yd&No=0&Nrpp=1000"
# eyereq = requests.get(eyeurl)
# eyetext = eyereq.text

newfile = "htmlulta.json"
# fw = open(newfile,"w")
# fw.write(eyetext)
# fw.close() # Close the open file

f = open(newfile)
html = f.read()
soup = BeautifulSoup(html, 'html.parser')
prod = soup.find_all(class_="prod-desc")
elements = soup.find_all(class_ = "productQvContainer")
for x in elements:
    roughDesc = x.find(class_="prod-desc")
    finDesc = roughDesc.text.strip()
    titlerough = x.find(class_ = "prod-title")
    finTit = titlerough.text.strip()
    print("++++++++")
    print(finTit)
    print(finDesc)

    urlDetails = x.find('a', href = True)["href"]


# for x in prod:
#     prodDescrption = x.text.strip()
    # print(prodDescrption)

# count = 0
# for x in prod:
#     count +=1
# print(count)
# print(prod)