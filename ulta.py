import requests
import json
from bs4 import BeautifulSoup
import sqlite3

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
		end = "?N=26yd&No=0&Nrpp=500"
	elif type == "face":
		category = "makeup-face"
		end = "?N=26y3&No=0&Nrpp=500"
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
		print(finDesc)

		titlerough = x.find(class_ = "prod-title")
		finTit = titlerough.text.strip() # product brand

		urlDetails = x.find('a', href = True)["href"] # this should be the indiv product url
		finalurl = "https://www.ulta.com" + urlDetails

		try:
			pricerough = x.find(class_ = "regPrice")
			finPrice = pricerough.text.strip()
			Sale = "No"
			# print("Not on Sale")
		except:
			pricerough = x.find(class_ = "pro-new-price")
			finPrice = pricerough.text.strip()
			Sale = "Yes"
			# print("On Sale")

		#-------------- specific page crawl starts here ----------------

		# second = requests.get(finalurl)
		# secondtext = second.text
		secondtext = cacheRequest(finalurl)
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
		# print(sizeNdim)

		try:
			percentrecommend = soup.find(class_ = "pr-snapshot-consensus-value pr-rounded")
			percentrec = percentrecommend.text.strip()
			finalpercentrec = percentrec[:-1]
			# print(finalpercentrec)
		except:
			finalpercentrec = None
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
dumped = json.dumps(megalist)
fw = open("allprodlist.json","w")
fw.write(dumped)
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
	statement1 = '''
		CREATE TABLE 'Products' (
			'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
			'Name' TEXT NOT NULL,
			'Brand' TEXT NOT NULL,
			'Category' TEXT NOT NULL,
			'Cost' REAL NOT NULL,
			'ItemNum' TEXT,
			'ItemSizeOZ' REAL,
			'PercentRec' REAL,
			'Reviews' INTEGER,
			'StarRating' REAL,
			'Sale' TEXT NOT NULL,
			'Url' TEXT NOT NULL
			);
		'''
	cur.execute(statement1)
	conn.commit()

	statement2 = '''
			DROP TABLE IF EXISTS 'Categories';
		'''
	cur.execute(statement2)
	conn.commit()
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	statement3 = '''
		CREATE TABLE 'Categories' (
			'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
			'Category' TEXT NOT NULL,
			'BrandsTotalNum' TEXT NOT NULL,
			'ProductsTotalNum' TEXT NOT NULL
			);
		'''
	cur.execute(statement3)
	conn.commit()

def fillthings():
	conn = sqlite3.connect("ultadata.db")
	cur = conn.cursor()

	myfile = open("allprodlist.json", 'r')
	data = myfile.read()
	loaded = json.loads(data) # this should be a list of lists

	for x in loaded:
		insertion = (None, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10])
		statement = 'INSERT INTO "Products"'
		statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
		cur.execute(statement, insertion)
		# at the end of this hopefully the products table has been filled
		conn.commit()

init_db(DBNAME)
fillthings()
