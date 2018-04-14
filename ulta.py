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
		resp = requests.get(url)
		CACHE_DICTION[url] = resp.text
		dumped_json_cache = json.dumps(CACHE_DICTION, indent = 4)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
		return CACHE_DICTION[url]

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

	if kind == "eyes":
		category = "Eye"
	elif kind == "lips":
		category = "Lip"
	elif kind == "face":
		category = "Face"
	elif kind == "tools":
		category = "Tool"

	for x in elements:
		# print("++++++++")
		roughDesc = x.find(class_="prod-desc")
		finDesc = roughDesc.text.strip() # basically product name
		# print(finDesc)

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

		second = requests.get(finalurl)
		secondtext = second.text
		soup = BeautifulSoup(secondtext, 'html.parser')

		try:
			proditem = soup.find(class_ = "product-item-no") #has size and itemnum
			prodnum = soup.find(id = "itemNumber")
			finalprodnum = prodnum.text.strip()
		except:
			finalprodnum = None

		try:
			itemsize = proditem.find(id = "itemSize")
			# sizefinal = itemsize.text.strip()
			# itemdim = proditem.find(id = "itemSizeUOM")
			# dimfinal = itemdim.text.strip()
			sizeNdim = itemsize.text.strip()
		except:
			sizeNdim = None
		print(size)

		try:
			percentrecommend = soup.find(class_ = "pr-snapshot-consensus-value pr-rounded")
			percentrec = percentrecommend.text.strip()
			finalpercentrec = percentrec[:-1]
			# print(finalpercentrec)
		except:
			finalpercentrec = "No '% would recommend' available"
			# print(finalpercentrec)

		try:
			numrevclass = soup.find(id = "rws_cnts")
			numreview = numrevclass.text.strip()
			numreviewfinal = numreview[1:-1]
			# print(numreviewfinal)
		except:
			numreviewfinal = None
			# print("there are no reviews")

		try:
			starrate = soup.find(class_ = "pr-rating pr-rounded average")
			starfinal = starrate.text.strip()
		except:
			starfinal = None
			# print("there are no star ratings")
		# print(finalpercentrec + " would recommend")
		# print(numreviewfinal + " reviews")
		# print(starfinal + " stars")
		ultimateTuple = (finDesc, finTit, category, finPrice, finalprodnum, sizeNdim, finalpercentrec, numreviewfinal, starfinal, Sale, finalurl)
		returnlist.append(ultimateTuple)
		# print(ultimateTuple)
	# print(returnlist)
	return returnlist

eyelist = getAllProdType("eyes")
eyetup = eyelist
liplist = getAllProdType("lips")
liptup = liplist
facelist = getAllProdType("face")
facetup = facelist
toolist = getAllProdType("tools")
tooltup = toolist

allprodDict = {}
allprodDict["Eye"] = eyetup
allprodDict["Lip"] = liptup
allprodDict["Face"] = facetup
allprodDict["Tool"] = tooltup

megalist = eyetup + liptup + facetup + tooltup

fw = open("allprodlist.json","w")
fw.write(megalist)
fw.close() # Close the open file

print(allprodDict)

DBNAME = "ultadata.db"
def init_db(x):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
	statement = '''
            DROP TABLE IF EXISTS 'Products';
        '''
    cur.execute(statement)
    conn.commit()
    statement = '''
        CREATE TABLE 'Products' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL,
            'Brand' TEXT NOT NULL,
            'Cost' REAL NOT NULL,
            'ItemNum' TEXT NOT NULL,
            'ItemSizeOZ' REAL,
            'PercentRec' REAL,
            'Reviews' INTEGER,
            'StarRating' REAL,
            'Sale' TEXT NOT NULL,
            'Url' TEXT NOT NULL,
            );
        '''
	cur.execute(statement)
	conn.commit()

	statement = '''
            DROP TABLE IF EXISTS 'Categories';
        '''
	cur.execute(statement)
    conn.commit()

	conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        CREATE TABLE 'Categories' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Category' TEXT NOT NULL,
            'BrandsTotalNum' TEXT NOT NULL,
            'ProductsTotalNum' TEXT NOT NULL,
            );
        '''
	cur.execute(statement)
	conn.commit()
