# # # spike file for 206 final project
# #
import requests
import json
from bs4 import BeautifulSoup
import sqlite3
import plotly.plotly as py
import plotly.graph_objs as go
# #
# # # eyelist = getAllProdType("eyes")
# # # eyetup = eyelist
# # # liplist = getAllProdType("lips")
# # # liptup = liplist
# # # facelist = getAllProdType("face")
# # # facetup = facelist
# # # toolist = getAllProdType("tools")
# # # tooltup = toolist
# # #
# # # allprodDict = {}
# # # allprodDict["Eye"] = eyetup
# # # allprodDict["Lip"] = liptup
# # # allprodDict["Face"] = facetup
# # # allprodDict["Tool"] = tooltup
# # # megalist = eyetup + liptup + facetup + tooltup
# # # dumped = json.dumps(megalist)
# # # fw = open("allprodlist.json","w")
# # # fw.write(dumped)
# # # fw.close() # Close the open file
# # #
# # # print(allprodDict)
# #
# # # DBNAME = "ultadata.db"
# # # def init_db(x):
# # # 	conn = sqlite3.connect(DBNAME)
# # # 	cur = conn.cursor()
# # # 	statement = '''
# # # 			DROP TABLE IF EXISTS 'Products';
# # # 		'''
# # # 	cur.execute(statement)
# # # 	conn.commit()
# # # 	statement1 = '''
# # # 		CREATE TABLE 'Products' (
# # # 			'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
# # # 			'Name' TEXT NOT NULL,
# # # 			'Brand' TEXT NOT NULL,
# # # 			'Category' TEXT NOT NULL,
# # # 			'Cost' REAL NOT NULL,
# # # 			'ItemNum' TEXT,
# # # 			'ItemSizeOZ' REAL,
# # # 			'PercentRec' REAL,
# # # 			'Reviews' INTEGER,
# # # 			'StarRating' REAL,
# # # 			'Sale' TEXT NOT NULL,
# # # 			'Url' TEXT NOT NULL
# # # 			);
# # # 		'''
# # # 	cur.execute(statement1)
# # # 	conn.commit()
# # #
# # # 	statement2 = '''
# # # 			DROP TABLE IF EXISTS 'Categories';
# # # 		'''
# # # 	cur.execute(statement2)
# # # 	conn.commit()
# # #
# # # 	conn = sqlite3.connect(DBNAME)
# # # 	cur = conn.cursor()
# # # 	statement3 = '''
# # # 		CREATE TABLE 'Categories' (
# # # 			'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
# # # 			'Category' TEXT NOT NULL,
# # # 			'BrandsTotalNum' TEXT NOT NULL,
# # # 			'ProductsTotalNum' TEXT NOT NULL
# # # 			);
# # # 		'''
# # # 	cur.execute(statement3)
# # # 	conn.commit()
# # #
# # # # init_db(DBNAME)
# # #
# # # def fillthings():
# # # 	conn = sqlite3.connect("ultadata.db")
# # # 	cur = conn.cursor()
# # #
# # # 	myfile = open("allprodlist.json", 'r')
# # # 	data = myfile.read()
# # # 	loaded = json.loads(data) # this should be a list of lists
# # #
# # # 	for x in loaded:
# # # 		insertion = (None, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10])
# # # 		statement = 'INSERT INTO "Products"'
# # # 		statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
# # # 		cur.execute(statement, insertion)
# # # 		# at the end of this hopefully the products table has been filled
# # # 		conn.commit()
# # #
# # # 	eyebrandlist = []
# # # 	eyeprodlist = []
# # # 	toolbrandlist = []
# # # 	toolprodlist = []
# # # 	facebrandlist = []
# # # 	faceprodlist = []
# # # 	lipbrandlist = []
# # # 	lipprodlist = []
# # #
# # # 	for x in loaded:
# # # 		if x[2] == "Eye":
# # # 			eyeprodlist.append(x[0])
# # # 			if x[1] not in eyebrandlist and not None:
# # # 				eyebrandlist.append(x[1])
# # # 		elif x[2] == "Tool":
# # # 			toolprodlist.append(x[0])
# # # 			if x[1] not in toolbrandlist and not None:
# # # 				toolbrandlist.append(x[1])
# # # 		elif x[2] == "Face":
# # # 			faceprodlist.append(x[0])
# # # 			if x[1] not in facebrandlist and not None:
# # # 				facebrandlist.append(x[1])
# # # 		elif x[2] == "Lip":
# # # 			lipprodlist.append(x[0])
# # # 			if x[1] not in lipbrandlist and not None:
# # # 				lipbrandlist.append(x[1])
# # #
# # # 	eyetup = ("Eye", len(eyebrandlist), len(eyeprodlist))
# # # 	liptup = ("Lip", len(lipbrandlist), len(lipprodlist))
# # # 	facetup = ("Face", len(facebrandlist), len(faceprodlist))
# # # 	tooltup = ("Tool", len(toolbrandlist), len(toolprodlist))
# # # 	categorytuple = (eyetup, liptup, facetup, tooltup)
# # #
# # # 	for tup in categorytuple:
# # # 		insert = (None, tup[0], tup[1], tup[2])
# # # 		statement = 'INSERT INTO "Categories" '
# # # 		statement += 'VALUES (?, ?, ?, ?)'
# # # 		cur.execute(statement, insert)
# # # 		conn.commit()
# # #
# # # 	print("ok it made it here!!")
# #
# #
# # def costNStarCorrelation():
# # 	DB_NAME = 'ultadata.db'
# # 	try:
# # 		conn = sqlite3.connect(DB_NAME)
# # 		cur = conn.cursor()
# # 	except Error as e:
# # 		print(e)
# # 	query = "SELECT * FROM 'products'"
# # 	cur.execute(query)
# #
# # 	basic_statement = '''
# # 	SELECT starrating, Cost, Name
# # 	FROM Products
# # 	JOIN Categories
# # 	ON Categories.Id = Products.Category
# # 	WHERE starrating IS NOT NULL
# # 	ORDER BY Products.starrating DESC
# # 	'''
# # 	cur.execute(basic_statement)
# # 	plotlytuplist = []
# # 	for row in cur:
# # 		try:
# # 			pair = (row[0], round(float(row[1]), 1), row[2]) #this rounds like in project 3
# # 			plotlytuplist.append(pair)
# # 		except:
# # 			continue
# # 	print(plotlytuplist)
# #
# # 	trace1 = go.Scatter(
# # 			type='scatter',
# # 			y =[x[0] for x in plotlytuplist],
# # 			x =[x[1] for x in plotlytuplist],
# # 			mode = 'markers',
# # 			name = 'markers',
# # 			text = [x[2] for x in plotlytuplist] # this names each individual point
# # 			)
# # 	data = [trace1]
# #
# # 	layout = go.Layout(
# # 				title = "Correlation Between Cost of Product + Star Rating",
# # 				xaxis = dict(
# # 				title = 'Cost of Product',
# # 				range = len(plotlytuplist)
# # 			),
# # 				yaxis = dict(
# # 				title = 'Star Rating out of Five Stars',
# # 				range = [0, 5.5]
# # 			),
# # 				height = 1000,
# # 				width = 1000
# # 		)
# #
# # 	fig = go.Figure(data=data, layout=layout)
# # 	py.plot(fig, filename = 'star-cost-correlation')
# #
# #
# #
# # def avbrand(): # this function sorts by the average star rating of a brand
# # 	DB_NAME = 'ultadata.db'
# # 	try:
# # 		conn = sqlite3.connect(DB_NAME)
# # 		cur = conn.cursor()
# # 	except Error as e:
# # 		print(e)
# #
# # 	basic_statement = '''
# # 	SELECT Brand, AVG(StarRating)
# # 	FROM Products
# # 	JOIN Categories
# # 	ON Categories.Id = Products.Category
# # 	GROUP BY Brand
# # 	ORDER BY AVG(StarRating) DESC
# # 	'''
# # 	cur.execute(basic_statement)
# # 	plotlytuplist = []
# # 	for row in cur:
# # 		try:
# # 			pair = (row[0], round(float(row[1]), 1)) #this rounds like in project 3
# # 			plotlytuplist.append(pair)
# # 		except:
# # 			continue
# # 	# print(plotlytuplist)
# #
# # 	trace1 = go.Bar(
# # 		x=[x[0] for x in plotlytuplist],
# # 		y=[x[1] for x in plotlytuplist]
# # 		)
# # 	data = [trace1]
# #
# # 	layout = go.Layout(
# # 				title = "Average Star Rating for Brands Overall",
# # 				xaxis = dict(
# # 				range = len(plotlytuplist)
# # 			),
# # 				yaxis = dict(
# # 				range = [0, 5]
# # 			),
# # 				height=500,
# # 				width=1000
# # 		)
# #
# # 	fig = go.Figure(data=data, layout=layout)
# # 	py.plot(fig, filename = 'ulta-bar')
# #
# # def costPerOz(): #this is exactly  what the function says i t is lol
# # 	DB_NAME = 'ultadata.db'
# # 	try:
# # 		conn = sqlite3.connect(DB_NAME)
# # 		cur = conn.cursor()
# # 	except Error as e:
# # 		print(e)
# #
# # 	basic_statement = '''
# # 	SELECT Name, CAST(Cost AS DECIMAL)/CAST(ItemSizeOz AS DECIMAL)
# # 	FROM Products
# # 	JOIN Categories
# # 	ON Categories.Id = Products.Category
# # 	WHERE CAST(Cost AS DECIMAL)/CAST(ItemSizeOz AS DECIMAL) IS NOT NULL
# # 	ORDER BY CAST(Cost AS DECIMAL)/CAST(ItemSizeOz AS DECIMAL) DESC
# # 	'''
# # 	cur.execute(basic_statement)
# #
# # 	plotlytuplist = []
# # 	for row in cur:
# # 		try:
# # 			pair = (row[0], round(float(row[1]), 1)) #this rounds like in project 3
# # 			plotlytuplist.append(pair)
# # 		except:
# # 			continue
# # 	# print(plotlytuplist)
# #
# # 	trace1 = go.Bar(
# # 		x=[x[0] for x in plotlytuplist],
# # 		y=[x[1] for x in plotlytuplist]
# # 		)
# # 	data = [trace1]
# #
# # 	layout = go.Layout(
# # 				title = "Product Cost Per Ounce",
# # 				xaxis = dict(
# # 				range = len(plotlytuplist)
# # 			),
# # 				yaxis = dict(
# # 				range = [0, 5000]),
# # 				height=600,
# # 				width=1000)
# #
# # 	fig = go.Figure(data=data, layout=layout)
# # 	py.plot(fig, filename = 'ulta-bar')
# #
# # def numberPeopleRecommend():  # this is the percent of people who would recommend times the number of reviews
# # 	DB_NAME = 'ultadata.db'   # (to find number of people who would recommend)
# # 	try:
# # 		conn = sqlite3.connect(DB_NAME)
# # 		cur = conn.cursor()
# # 	except Error as e:
# # 		print(e)
# #
# # 	basic_statement = '''
# # 	SELECT Name, (CAST(PercentRec AS DECIMAL)/100)*Reviews
# # 	FROM Products
# # 	JOIN Categories
# # 	ON Categories.Id = Products.Category
# # 	WHERE (CAST(PercentRec AS DECIMAL)/100)*Reviews IS NOT NULL
# # 	ORDER BY (CAST(PercentRec AS DECIMAL)/100)*Reviews DESC
# # 	LIMIT 50
# # 	'''
# #
# # 	cur.execute(basic_statement)
# # 	plotlytuplist = []
# # 	for row in cur:
# # 		try:
# # 			pair = (row[0], round(float(row[1]), 2)) #this rounds like in project 3
# # 			plotlytuplist.append(pair)
# # 		except:
# # 			continue
# # 	# print(plotlytuplist)
# # 	trace1 = go.Bar(
# # 		x=[x[0] for x in plotlytuplist],
# # 		y=[x[1] for x in plotlytuplist]
# # 		)
# # 	data = [trace1]
# #
# # 	layout = go.Layout(
# # 				title = "Number of People Who Would Recommend",
# # 				xaxis = dict(
# # 				range = len(plotlytuplist)
# # 			),
# # 				yaxis = dict(
# # 				range = [0, 12000]),
# # 				height=700,
# # 				width=1000)
# #
# # 	fig = go.Figure(data=data, layout=layout)
# # 	py.plot(fig, filename = 'ulta-bar')
# #
# #
# # # avbrand()
# # # costPerOz()
# # # process_command()
# # # numberPeopleRecommend()
# #
# # # eyereq = cacheRequest("https://www.ulta.com/makeup-eyes?N=26yd&No=0&Nrpp=1000")
# # # # this is because max numbers of products on a page is 1000 but there are like
# # # # 1700 products total for eye stuff so u need to do it twice
# # # facereq = cacheRequest("https://www.ulta.com/makeup-face?N=26y3&No=0&Nrpp=1000")
# # # lipreq = cacheRequest("https://www.ulta.com/makeup-lips?N=26yq&No=0&Nrpp=1000")
# # # toolreq = cacheRequest("https://www.ulta.com/tools-brushes-makeup-brushes-tools?N=27hn&No=0&Nrpp=1000")
# #
# # # eyeurl = "https://www.ulta.com/makeup-eyes?N=26yd&No=0&Nrpp=1000"
# # # eyereq = requests.get(eyeurl)
# # # eyetext = eyereq.text
# #
# # newfile = "htmlulta.json"
# # # fw = open(newfile,"w")
# # # fw.write(eyetext)
# # # fw.close() # Close the open file
# # #
# # # f = open(newfile)
# # # html = f.read()
# # # soup = BeautifulSoup(html, 'html.parser')
# # # elements = soup.find_all(class_ = "productQvContainer")
# # # for x in elements:
# # #     print("++++++++")
# # #     roughDesc = x.find(class_="prod-desc")
# # #     finDesc = roughDesc.text.strip()
# # #
# # #     titlerough = x.find(class_ = "prod-title")
# # #     finTit = titlerough.text.strip()
# # #
# # #     urlDetails = x.find('a', href = True)["href"]
# # #     finalurl = "https://www.ulta.com" + urlDetails
# # #
# # #     print(finTit)
# # #     print(finDesc)
# # #     print(finalurl)
# # #     try:
# # #         pricerough = x.find(class_ = "regPrice")
# # #         finPrice = pricerough.text.strip()
# # #         Sale = False
# # #         print("Not on Sale")
# # #     except:
# # #         pricerough = x.find(class_ = "pro-new-price")
# # #         finPrice = pricerough.text.strip()
# # #         Sale = True
# # #         print("On Sale")
# # #     print(finPrice)
# # #     #------- specific page crawl starts here
# # #     second = requests.get(finalurl)
# # #     secondtext = second.text
# # #     soup = BeautifulSoup(secondtext, 'html.parser')
# # #
# # #     proditem = soup.find(class_ = "product-item-no") #has size and itemnum
# # #     prodnum = soup.find(id = "itemNumber")
# # #     finalprodnum = prodnum.text.strip()
# # #
# # #     itemsize = proditem.find(id = "itemSize")
# # #     sizefinal = itemsize.text.strip()
# # #     itemdim = proditem.find(id = "itemSizeUOM")
# # #     dimfinal = itemdim.text.strip()
# # #     sizeNdim = sizefinal + " " + dimfinal
# #
# # 	# percentrecommend = soup.find(class_ = "pr-snapshot-consensus-value pr-rounded")
# # 	# finalpercentrec = percentrecommend.text.strip()
# # 	#
# # 	# numreviewclass = soup.find(class_ = "pr-snapshot-average-based-on-text")
# # 	# numreview = numreviewclass.find(class_ = "count")
# # 	# numreviewfinal = numreview.text.strip()
# # 	#
# # 	# starrate = soup.find(class_ = "pr-rating pr-rounded average")
# # 	# starfinal = starrate.text.strip()
# #
# # 	# print(finalprodnum)
# # 	# print(finalpercentrec + " would recommend")
# # 	# print(numreviewfinal + " reviews")
# # 	# print(starfinal + " stars")
#
# import requests
# import plotly.plotly as py
# import plotly.graph_objs as go
# import json
# from bs4 import BeautifulSoup
# import sqlite3
# import random
#
# class UltaProd:
# 	def __init__(self, name, brand, cat, cost, retailnum, sizeoz = "No size available.", percent = "No percent recommend available.", reviews = "No reviews available.", star = "No star rating available.", sale = "No sale status available.", url = "No url available."):
# 		self.name = name
# 		self.brand = brand
# 		self.cat = cat
# 		self.cost = cost
# 		self.retailnum = retailnum
# 		self.sizeoz = sizeoz
# 		self.percent = percent
# 		self.reviews = reviews
# 		self.star = star
# 		self.sale = sale
# 		self.url = url
# 	def __str__(self):
# 		returnstuff = "+++ Product Name: {} —— {} +++\nPrice: {}        Size in ounces: {} \nStar Rating: {}        Reviews: {}\nURL: {}".format(self.name, self.brand, self.cost, self.sizeoz, self.star, self.reviews, self.url)
# 		return returnstuff
#
# CACHE_FNAME = 'cache.json'
# try:
# 	cache_file = open(CACHE_FNAME, 'r')
# 	cache_contents = cache_file.read()
# 	cache_file.close()
# 	CACHE_DICTION = json.loads(cache_contents)
# except:
# 	CACHE_DICTION = {}
#
# def cacheRequest(url):
# 	if url in CACHE_DICTION:
# 		print("Getting cached data...")
# 		return CACHE_DICTION[url]
# 	else:
# 		print("Making a request for new data...")
# 		resp = requests.get(url)
# 		CACHE_DICTION[url] = resp.text
# 		dumped_json_cache = json.dumps(CACHE_DICTION, indent = 4)
# 		fw = open(CACHE_FNAME,"w")
# 		fw.write(dumped_json_cache)
# 		fw.close() # Close the open file
# 		return CACHE_DICTION[url]
#
# def uniqueUltaUrl(type): #can be eyes, face, lips, and tools
# 	base = "https://www.ulta.com/"
# 	if type == "eyes": # https://www.ulta.com/makeup-eyes?N=26yd&No=0&Nrpp=1000
# 		category = "makeup-eyes"
# 		end = "?N=26yd&No=0&Nrpp=500"
# 	elif type == "face":
# 		category = "makeup-face"
# 		end = "?N=26y3&No=0&Nrpp=500"
# 	elif type == "lips":
# 		category = "makeup-lips"
# 		end = "?N=26yq&No=0&Nrpp=1000"
# 	elif type == "tools":
# 		category = "tools-brushes-makeup-brushes-tools"
# 		end = "?N=27hn&No=0&Nrpp=1000"
# 	total = base + category + end
# 	return total
#
# def getAllProdType(kind): #takes in eyes, lips, face, tools
# 	returnlist = []
# 	first_url = uniqueUltaUrl(kind)
# 	page = cacheRequest(first_url)
# 	soup = BeautifulSoup(page, 'html.parser')
# 	elements = soup.find_all(class_ = "productQvContainer")
#
# 	if kind == "eyes": #gets the numbers that will differentiate the categories
# 		category = "1"
# 	elif kind == "lips":
# 		category = "2"
# 	elif kind == "face":
# 		category = "3"
# 	elif kind == "tools":
# 		category = "4"
#
# 	for x in elements:
# 		roughDesc = x.find(class_="prod-desc")
# 		finDesc = roughDesc.text.strip() # ******** basically product name
#
# 		# print(finDesc) # THIS PRINT IS ON PURPOSE so you can see what category you're on!!
#
# 		titlerough = x.find(class_ = "prod-title")
# 		finTit = titlerough.text.strip() # ********* product brand
# 		urlDetails = x.find('a', href = True)["href"] # *******this should be the indiv product url
# 		finalurl = "https://www.ulta.com" + urlDetails
#
# 		try:
# 			pricerough = x.find(class_ = "regPrice")
# 			strippedprice = pricerough.text.strip()
# 			if len(strippedprice) > 7:
# 				splitprice = strippedprice.split("-")
# 				moreexpensive = splitprice[-1]
# 				finPrice = moreexpensive[2:]
# 			else:
# 				finPrice = strippedprice[1:]
# 			Sale = "No"
# 		except:
# 			pricerough = x.find(class_ = "pro-new-price")
# 			strippedprice = pricerough.text.strip()
# 			if len(strippedprice) > 7:
# 				splitprice = strippedprice.split("-")
# 				moreexpensive = splitprice[-1]
# 				finPrice = moreexpensive[2:]
# 			else:
# 				finPrice = strippedprice[1:]
# 			Sale = "Yes"
#
# 		#---------------------- specific page crawl starts here --------------------------
# 		secondtext = cacheRequest(finalurl)
# 		soup = BeautifulSoup(secondtext, 'html.parser')
#
# 		try:
# 			proditem = soup.find(class_ = "product-item-no") #has size and itemnum
# 			prodnum = soup.find(id = "itemNumber")
# 			finalprodnum = prodnum.text.strip()
# 		except:
# 			finalprodnum = None
#
# 		try:
# 			itemsize = proditem.find(id = "itemSize")
# 			sizeNdim = itemsize.text.strip()
# 		except:
# 			sizeNdim = None
#
# 		try:
# 			percentrecommend = soup.find(class_ = "pr-snapshot-consensus-value pr-rounded")
# 			percentrec = percentrecommend.text.strip()
# 			finalpercentrec = percentrec[:-1]
# 		except:
# 			finalpercentrec = None
#
# 		try:
# 			numrevclass = soup.find(id = "rws_cnts")
# 			numreview = numrevclass.text.strip()
# 			numreviewfinal = numreview[1:-1]
# 		except:
# 			numreviewfinal = None
#
# 		try:
# 			starrate = soup.find(class_ = "pr-rating pr-rounded average")
# 			starfinal = starrate.text.strip()
# 		except:
# 			starfinal = None
#
# 		# ultimateTuple = (finDesc, finTit, category, finPrice, finalprodnum, sizeNdim, finalpercentrec, numreviewfinal, starfinal, Sale, finalurl)
# 		finalprod = UltaProd(finDesc, finTit, category, finPrice, finalprodnum, sizeNdim, finalpercentrec, numreviewfinal, starfinal, Sale, finalurl)
# 		returnlist.append(finalprod)
# 		print(finalprod)
# 	print(returnlist)
# 	return returnlist
#
#  # ************ THIS CODE HERE IS TO CREATE THE JSON FILE THAT WILL BE USED FOR PRODUCTS TABLE *******
# def JsonFileCreator():
# 	eyelist = getAllProdType("eyes")
# 	eyetup = eyelist
# 	liplist = getAllProdType("lips")
# 	liptup = liplist
# 	facelist = getAllProdType("face")
# 	facetup = facelist
# 	toolist = getAllProdType("tools")
# 	tooltup = toolist
# 	allprodDict = {}
# 	allprodDict["1"] = eyetup
# 	allprodDict["2"] = liptup
# 	allprodDict["3"] = facetup
# 	allprodDict["4"] = tooltup
# 	megalist = eyetup + liptup + facetup + tooltup
# 	dumped = json.dumps(megalist)
# 	fw = open("allprodlist.json","w")
# 	fw.write(dumped)
# 	fw.close() # Close the open file
#  # ******************* code for json file ends here **********************
#
# DBNAME = "ultadata.db"
# def init_db(x):
# 	conn = sqlite3.connect(DBNAME)
# 	cur = conn.cursor()
# 	statement = '''
# 			DROP TABLE IF EXISTS 'Products';
# 		'''
# 	cur.execute(statement)
# 	conn.commit()
# 	statement1 = '''
# 		CREATE TABLE 'Products' (
# 			'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
# 			'Name' TEXT NOT NULL,
# 			'Brand' TEXT NOT NULL,
# 			'Category' TEXT NOT NULL,
# 			'Cost' REAL NOT NULL,
# 			'ItemNum' TEXT,
# 			'ItemSizeOZ' REAL,
# 			'PercentRec' REAL,
# 			'Reviews' INTEGER,
# 			'StarRating' REAL,
# 			'Sale' TEXT NOT NULL,
# 			'Url' TEXT NOT NULL
# 			);
# 		'''
# 	cur.execute(statement1)
# 	conn.commit()
#
# 	statement2 = '''
# 			DROP TABLE IF EXISTS 'Categories';
# 		'''
# 	cur.execute(statement2)
# 	conn.commit()
# 	conn = sqlite3.connect(DBNAME)
# 	cur = conn.cursor()
# 	statement3 = '''
# 		CREATE TABLE 'Categories' (
# 			'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
# 			'Category' TEXT NOT NULL,
# 			'BrandsTotalNum' TEXT NOT NULL,
# 			'ProductsTotalNum' TEXT NOT NULL
# 			);
# 		'''
# 	cur.execute(statement3)
# 	conn.commit()
#
# def fillthings():
# 	conn = sqlite3.connect("ultadata.db")
# 	cur = conn.cursor()
# 	myfile = open("allprodlist.json", 'r')
# 	data = myfile.read()
# 	loaded = json.loads(data) # this should be a list of lists
#
# 	for x in loaded:
# 		insertion = (None, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10])
# 		statement = 'INSERT INTO "Products"'
# 		statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
# 		cur.execute(statement, insertion)
# 		# at the end of this hopefully the products table has been filled
# 		conn.commit()
#
# 	eyebrandlist = []
# 	eyeprodlist = []
# 	toolbrandlist = []
# 	toolprodlist = []
# 	facebrandlist = []
# 	faceprodlist = []
# 	lipbrandlist = []
# 	lipprodlist = []
# 	for x in loaded:
# 		if x[2] == "1":
# 			eyeprodlist.append(x[0])
# 			if x[1] not in eyebrandlist and not None:
# 				eyebrandlist.append(x[1])
# 		elif x[2] == "2":
# 			lipprodlist.append(x[0])
# 			if x[1] not in lipbrandlist and not None:
# 				lipbrandlist.append(x[1])
# 		elif x[2] == "3":
# 			faceprodlist.append(x[0])
# 			if x[1] not in facebrandlist and not None:
# 				facebrandlist.append(x[1])
# 		elif x[2] == "4":
# 			toolprodlist.append(x[0])
# 			if x[1] not in toolbrandlist and not None:
# 				toolbrandlist.append(x[1])
#
# 	eyetup = ("Eye", len(eyebrandlist), len(eyeprodlist))
# 	liptup = ("Lip", len(lipbrandlist), len(lipprodlist))
# 	facetup = ("Face", len(facebrandlist), len(faceprodlist))
# 	tooltup = ("Tool", len(toolbrandlist), len(toolprodlist))
# 	categorytuple = (eyetup, liptup, facetup, tooltup)
# 	for tup in categorytuple:
# 		insert = (None, tup[0], tup[1], tup[2])
# 		statement = 'INSERT INTO "Categories" '
# 		statement += 'VALUES (?, ?, ?, ?)'
# 		cur.execute(statement, insert)
# 		conn.commit()
#
# def starRatingFunc():
# 	DB_NAME = 'ultadata.db'
# 	try:
# 		conn = sqlite3.connect(DB_NAME)
# 		cur = conn.cursor()
# 	except Error as e:
# 		print(e)
#
# 	basic_statement = '''
# 	SELECT Name, starrating
# 	FROM Products
# 	JOIN Categories
# 	ON Categories.Id = Products.Category
# 	ORDER BY Products.starrating DESC
# 	'''
# 	strulta = str(basic_statement)
# 	cur.execute(strulta)
# 	plotlytuplist = []
# 	for row in cur:
# 		try:
# 			pair = (row[0], round(float(row[1]), 1)) #this rounds like in project 3
# 			plotlytuplist.append(pair)
# 		except:
# 			continue
# 	# print(plotlytuplist)
#
# 	trace1 = go.Bar(
# 			type='scatter',
# 			x=[x[0] for x in plotlytuplist],
# 			y=[x[1] for x in plotlytuplist],
# 			)
# 	data = [trace1]
#
# 	layout = go.Layout(
# 				title = "Products ordered by star rating",
# 				xaxis = dict(
# 				title = 'Name of Product',
# 				range=len(plotlytuplist)
# 			),
# 				yaxis = dict(
# 				title = 'Star Rating',
# 				range = [0, 5]
# 			),
# 				height = 1000,
# 				width = 2000
# 		)
# 	fig = go.Figure(data=data, layout=layout)
# 	py.plot(fig, filename = 'ultastarrating')
#
# def avbrand(): # this function sorts by the average star rating of a brand
# 	DB_NAME = 'ultadata.db'
# 	try:
# 		conn = sqlite3.connect(DB_NAME)
# 		cur = conn.cursor()
# 	except Error as e:
# 		print(e)
#
# 	basic_statement = '''
# 	SELECT Brand, AVG(StarRating)
# 	FROM Products
# 	JOIN Categories
# 	ON Categories.Id = Products.Category
# 	GROUP BY Brand
# 	ORDER BY AVG(StarRating) DESC
# 	'''
# 	cur.execute(basic_statement)
# 	plotlytuplist = []
# 	for row in cur:
# 		try:
# 			pair = (row[0], round(float(row[1]), 1)) #this rounds like in project 3
# 			plotlytuplist.append(pair)
# 		except:
# 			continue
# 	# print(plotlytuplist)
#
# 	trace1 = go.Bar(
# 		x=[x[0] for x in plotlytuplist],
# 		y=[x[1] for x in plotlytuplist]
# 		)
# 	data = [trace1]
#
# 	layout = go.Layout(
# 				title = "Average Star Rating for Brands Overall",
# 				xaxis = dict(
# 				title = 'Brand Name',
# 				range = len(plotlytuplist)
# 			),
# 				yaxis = dict(
# 				title = 'Average Star Rating (Out of 5 Stars)',
# 				range = [0, 5]
# 			),
# 				height = 1000,
# 				width = 2000
# 		)
# 	fig = go.Figure(data=data, layout=layout)
# 	py.plot(fig, filename = 'avrating')
#
# def costPerOz():
# 	DB_NAME = 'ultadata.db'
# 	try:
# 		conn = sqlite3.connect(DB_NAME)
# 		cur = conn.cursor()
# 	except Error as e:
# 		print(e)
#
# 	basic_statement = '''
# 	SELECT Name, CAST(Cost AS DECIMAL)/CAST(ItemSizeOz AS DECIMAL)
# 	FROM Products
# 	JOIN Categories
# 	ON Categories.Id = Products.Category
# 	WHERE CAST(Cost AS DECIMAL)/CAST(ItemSizeOz AS DECIMAL) IS NOT NULL
# 	ORDER BY CAST(Cost AS DECIMAL)/CAST(ItemSizeOz AS DECIMAL) DESC
# 	'''
# 	cur.execute(basic_statement)
#
# 	plotlytuplist = []
# 	for row in cur:
# 		try:
# 			pair = (row[0], round(float(row[1]), 1)) #this rounds like in project 3
# 			plotlytuplist.append(pair)
# 		except:
# 			continue
# 	# print(plotlytuplist)
#
# 	trace1 = go.Bar(
# 		x=[x[0] for x in plotlytuplist],
# 		y=[x[1] for x in plotlytuplist]
# 		)
# 	data = [trace1]
#
# 	layout = go.Layout(
# 				title = "Product Cost Per Ounce",
# 				xaxis = dict(
# 				title = 'Product Name',
# 				range = len(plotlytuplist)
# 			),
# 				yaxis = dict(
# 				title = 'Cost in USD',
# 				range = [0, 10000]),
# 				height = 1000,
# 				width = 2000)
#
# 	fig = go.Figure(data=data, layout=layout)
# 	py.plot(fig, filename = 'ultacostperounce')
#
# def numberPeopleRecommend():  # this is the percent of people who would recommend times the number of reviews
# 	DB_NAME = 'ultadata.db'   # (to find number of people who would recommend)
# 	try:
# 		conn = sqlite3.connect(DB_NAME)
# 		cur = conn.cursor()
# 	except Error as e:
# 		print(e)
#
# 	basic_statement = '''
# 	SELECT Name, (CAST(PercentRec AS DECIMAL)/100)*Reviews
# 	FROM Products
# 	JOIN Categories
# 	ON Categories.Id = Products.Category
# 	WHERE (CAST(PercentRec AS DECIMAL)/100)*Reviews IS NOT NULL
# 	ORDER BY (CAST(PercentRec AS DECIMAL)/100)*Reviews
# 	ASC LIMIT 100
# 	'''
# 	cur.execute(basic_statement)
# 	plotlytuplist = []
# 	for row in cur:
# 		try:
# 			pair = (row[0], round(float(row[1]), 2)) #this rounds like in project 3
# 			plotlytuplist.append(pair)
# 		except:
# 			continue
# 	# print(plotlytuplist)
# 	trace1 = go.Bar(
# 		x=[x[0] for x in plotlytuplist],
# 		y=[x[1] for x in plotlytuplist]
# 		)
# 	data = [trace1]
#
# 	layout = go.Layout(
# 				title = "Number of People Who Would Recommend (% Recommend * Number of Reviews)",
# 				xaxis = dict(
# 				title = 'Product Name',
# 				range = len(plotlytuplist)
# 			),
# 				yaxis = dict(
# 				title = 'Number of People Who Would Recommend',
# 				range = [0, 50]),
# 				height = 800,
# 				width = 1500)
#
# 	fig = go.Figure(data=data, layout=layout)
# 	py.plot(fig, filename = 'ulta-bar')
#
# def costNStarCorrelation():
# 	DB_NAME = 'ultadata.db'
# 	try:
# 		conn = sqlite3.connect(DB_NAME)
# 		cur = conn.cursor()
# 	except Error as e:
# 		print(e)
# 	query = "SELECT * FROM 'products'"
# 	cur.execute(query)
#
# 	basic_statement = '''
# 	SELECT starrating, Cost, Name
# 	FROM Products
# 	JOIN Categories
# 	ON Categories.Id = Products.Category
# 	WHERE starrating IS NOT NULL
# 	ORDER BY Products.starrating DESC
# 	'''
# 	cur.execute(basic_statement)
# 	plotlytuplist = []
# 	for row in cur:
# 		try:
# 			pair = (row[0], round(float(row[1]), 1), row[2]) #this rounds like in project 3
# 			plotlytuplist.append(pair)
# 		except:
# 			continue
# 	print(plotlytuplist)
#
# 	trace1 = go.Scatter(
# 			type='scatter',
# 			y =[x[0] for x in plotlytuplist],
# 			x =[x[1] for x in plotlytuplist],
# 			mode = 'markers',
# 			name = 'markers',
# 			text = [x[2] for x in plotlytuplist] # this names each individual point
# 			)
# 	data = [trace1]
#
# 	layout = go.Layout(
# 				title = "Correlation Between Cost of Product + Star Rating",
# 				xaxis = dict(
# 				title = 'Cost of Product',
# 				range = len(plotlytuplist)
# 			),
# 				yaxis = dict(
# 				title = 'Star Rating out of Five Stars',
# 				range = [0, 5.5]
# 			),
# 				height = 1000,
# 				width = 1000
# 		)
#
# 	fig = go.Figure(data=data, layout=layout)
# 	py.plot(fig, filename = 'star-cost-correlation')
#
# getAllProdType("eyes")
# # JsonFileCreator()
# # init_db(DBNAME)
# # fillthings()
# # starRatingFunc() # ask about this func it ugly
# # avbrand()
# # costPerOz()
# # costNStarCorrelation()
# # numberPeopleRecommend()

conn = sqlite3.connect("ultadata.db")
cur = conn.cursor()
returnlist = []

# basic_statement = '''
# SELECT Name, Brand, StarRating, Cost, Categories.Category
# FROM Products
# JOIN Categories
# ON Categories.Id = Products.Category
# GROUP BY Brand
# ORDER BY StarRating
# DESC {}
# '''.format(limitnum)
# cur.execute(basic_statement)
# conn.commit()
#
# for row in cur:
#     indiv = [row[0], row[1], row[2], str(row[3]), row[4]]
#     if len(indiv[0]) > 25:
#         indiv[0] = indiv[0][:24] + '...'
#     indiv[3] = "   $" + indiv[3]
#     returnlist.append(indiv)
# for x in returnlist:
#     final = '{0:30} {1:23} {2:10} {3:14} {4:10}'.format(*x)
#     print(final)
returnlist = []
limitnum = "LIMIT 100"
basic_statement = '''
SELECT Name, Brand, StarRating, Cost, Categories.Category
FROM Products
JOIN Categories
ON Categories.Id = Products.Category
GROUP BY Brand
ORDER BY Cost
ASC {}
'''.format(limitnum)
cur.execute(basic_statement)
conn.commit()

for row in cur:
    indiv = [row[0], row[1], row[2], str(row[3]), row[4]]
    for x in indiv:
        if x == None:
            x = "N/A"
    if len(indiv[0]) > 25:
        indiv[0] = indiv[0][:24] + '...'
    indiv[3] = "   $" + indiv[3]
    print(indiv)
    returnlist.append(indiv)

print(returnlist)
for x in returnlist:
    final = '{0:30} {1:23} {2:10} {3:14} {4:10}'.format(*x)
    print(final)
