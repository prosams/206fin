# spike file for 206 final project

import requests
import json
from bs4 import BeautifulSoup
import sqlite3
import plotly.plotly as py
import plotly.graph_objs as go

# eyelist = getAllProdType("eyes")
# eyetup = eyelist
# liplist = getAllProdType("lips")
# liptup = liplist
# facelist = getAllProdType("face")
# facetup = facelist
# toolist = getAllProdType("tools")
# tooltup = toolist
#
# allprodDict = {}
# allprodDict["Eye"] = eyetup
# allprodDict["Lip"] = liptup
# allprodDict["Face"] = facetup
# allprodDict["Tool"] = tooltup
# megalist = eyetup + liptup + facetup + tooltup
# dumped = json.dumps(megalist)
# fw = open("allprodlist.json","w")
# fw.write(dumped)
# fw.close() # Close the open file
#
# print(allprodDict)

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
#
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
# # init_db(DBNAME)
#
# def fillthings():
# 	conn = sqlite3.connect("ultadata.db")
# 	cur = conn.cursor()
#
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
#
# 	for x in loaded:
# 		if x[2] == "Eye":
# 			eyeprodlist.append(x[0])
# 			if x[1] not in eyebrandlist and not None:
# 				eyebrandlist.append(x[1])
# 		elif x[2] == "Tool":
# 			toolprodlist.append(x[0])
# 			if x[1] not in toolbrandlist and not None:
# 				toolbrandlist.append(x[1])
# 		elif x[2] == "Face":
# 			faceprodlist.append(x[0])
# 			if x[1] not in facebrandlist and not None:
# 				facebrandlist.append(x[1])
# 		elif x[2] == "Lip":
# 			lipprodlist.append(x[0])
# 			if x[1] not in lipbrandlist and not None:
# 				lipbrandlist.append(x[1])
#
# 	eyetup = ("Eye", len(eyebrandlist), len(eyeprodlist))
# 	liptup = ("Lip", len(lipbrandlist), len(lipprodlist))
# 	facetup = ("Face", len(facebrandlist), len(faceprodlist))
# 	tooltup = ("Tool", len(toolbrandlist), len(toolprodlist))
# 	categorytuple = (eyetup, liptup, facetup, tooltup)
#
# 	for tup in categorytuple:
# 		insert = (None, tup[0], tup[1], tup[2])
# 		statement = 'INSERT INTO "Categories" '
# 		statement += 'VALUES (?, ?, ?, ?)'
# 		cur.execute(statement, insert)
# 		conn.commit()
#
# 	print("ok it made it here!!")


def process_command():
	DB_NAME = 'ultadata.db'
	try:
		conn = sqlite3.connect(DB_NAME)
		cur = conn.cursor()
	except Error as e:
		print(e)
	query = "SELECT * FROM 'products'"
	cur.execute(query)

	basic_statement = '''
	SELECT Name, starrating
	FROM Products
	JOIN Categories
	ON Categories.Id = Products.Category
	ORDER BY Products.starrating DESC
	'''
	strulta = str(basic_statement)
	cur.execute(strulta)
	plotlytuplist = []
	for row in cur:
		try:
			pair = (row[0], round(float(row[1]), 1)) #this rounds like in project 3
			plotlytuplist.append(pair)
		except:
			continue
	print(plotlytuplist)

	trace1 = go.Scatter(
			type='scatter',
			x=[x[0] for x in plotlytuplist],
			y=[x[1] for x in plotlytuplist],
			marker=dict(
			color=['rgb({},{},{})'.format(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)) for x in plotlytuplist],
			size=10
			),
				line=dict(
				color=['rgb({},{},{})'.format(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)) for x in plotlytuplist],
				width = 4
				),
				mode='markers+lines'
			)
	data = [trace1]

	layout = go.Layout(
				title="testgraph",
				xaxis = dict(
				range=len(plotlytuplist)
			),
				yaxis = dict(
				range=[0, 5]
			),
				height=500,
				width=1000
		)

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename = 'ulta-line')

def avbrand(): # this function sorts by the average star rating of a brand
	DB_NAME = 'ultadata.db'
	try:
		conn = sqlite3.connect(DB_NAME)
		cur = conn.cursor()
	except Error as e:
		print(e)

	basic_statement = '''
	SELECT Brand, AVG(StarRating)
	FROM Products
	JOIN Categories
	ON Categories.Id = Products.Category
	GROUP BY Brand
	ORDER BY AVG(StarRating) DESC
	'''
	cur.execute(basic_statement)
	plotlytuplist = []
	for row in cur:
		try:
			pair = (row[0], round(float(row[1]), 1)) #this rounds like in project 3
			plotlytuplist.append(pair)
		except:
			continue
	# print(plotlytuplist)

	trace1 = go.Bar(
		x=[x[0] for x in plotlytuplist],
		y=[x[1] for x in plotlytuplist]
		)
	data = [trace1]

	layout = go.Layout(
				title = "Average Star Rating for Brands Overall",
				xaxis = dict(
				range = len(plotlytuplist)
			),
				yaxis = dict(
				range = [0, 5]
			),
				height=500,
				width=1000
		)

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename = 'ulta-bar')

def costPerOz(): #this is exactly  what the function says i t is lol
	DB_NAME = 'ultadata.db'
	try:
		conn = sqlite3.connect(DB_NAME)
		cur = conn.cursor()
	except Error as e:
		print(e)

	basic_statement = '''
	SELECT Name, CAST(Cost AS DECIMAL)/CAST(ItemSizeOz AS DECIMAL)
	FROM Products
	JOIN Categories
	ON Categories.Id = Products.Category
	WHERE CAST(Cost AS DECIMAL)/CAST(ItemSizeOz AS DECIMAL) IS NOT NULL
	ORDER BY CAST(Cost AS DECIMAL)/CAST(ItemSizeOz AS DECIMAL) DESC
	'''
	cur.execute(basic_statement)

	plotlytuplist = []
	for row in cur:
		try:
			pair = (row[0], round(float(row[1]), 1)) #this rounds like in project 3
			plotlytuplist.append(pair)
		except:
			continue
	# print(plotlytuplist)

	trace1 = go.Bar(
		x=[x[0] for x in plotlytuplist],
		y=[x[1] for x in plotlytuplist]
		)
	data = [trace1]

	layout = go.Layout(
				title = "Product Cost Per Ounce",
				xaxis = dict(
				range = len(plotlytuplist)
			),
				yaxis = dict(
				range = [0, 5000]),
				height=600,
				width=1000)

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename = 'ulta-bar')

def numberPeopleRecommend():  # this is the percent of people who would recommend times the number of reviews
	DB_NAME = 'ultadata.db'   # (to find number of people who would recommend)
	try:
		conn = sqlite3.connect(DB_NAME)
		cur = conn.cursor()
	except Error as e:
		print(e)

	basic_statement = '''
	SELECT Name, (CAST(PercentRec AS DECIMAL)/100)*Reviews
	FROM Products
	JOIN Categories
	ON Categories.Id = Products.Category
	WHERE (CAST(PercentRec AS DECIMAL)/100)*Reviews IS NOT NULL
	ORDER BY (CAST(PercentRec AS DECIMAL)/100)*Reviews DESC
	'''

	cur.execute(basic_statement)
	plotlytuplist = []
	for row in cur:
		try:
			pair = (row[0], round(float(row[1]), 2)) #this rounds like in project 3
			plotlytuplist.append(pair)
		except:
			continue
	# print(plotlytuplist)
	trace1 = go.Bar(
		x=[x[0] for x in plotlytuplist],
		y=[x[1] for x in plotlytuplist]
		)
	data = [trace1]

	layout = go.Layout(
				title = "Number of People Who Would Recommend",
				xaxis = dict(
				range = len(plotlytuplist)
			),
				yaxis = dict(
				range = [0, 5000]),
				height=600,
				width=1000)

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename = 'ulta-bar')





# avbrand()
# costPerOz()
# process_command()
numberPeopleRecommend()

# eyereq = cacheRequest("https://www.ulta.com/makeup-eyes?N=26yd&No=0&Nrpp=1000")
# # this is because max numbers of products on a page is 1000 but there are like
# # 1700 products total for eye stuff so u need to do it twice
# facereq = cacheRequest("https://www.ulta.com/makeup-face?N=26y3&No=0&Nrpp=1000")
# lipreq = cacheRequest("https://www.ulta.com/makeup-lips?N=26yq&No=0&Nrpp=1000")
# toolreq = cacheRequest("https://www.ulta.com/tools-brushes-makeup-brushes-tools?N=27hn&No=0&Nrpp=1000")

# eyeurl = "https://www.ulta.com/makeup-eyes?N=26yd&No=0&Nrpp=1000"
# eyereq = requests.get(eyeurl)
# eyetext = eyereq.text

newfile = "htmlulta.json"
# fw = open(newfile,"w")
# fw.write(eyetext)
# fw.close() # Close the open file
#
# f = open(newfile)
# html = f.read()
# soup = BeautifulSoup(html, 'html.parser')
# elements = soup.find_all(class_ = "productQvContainer")
# for x in elements:
#     print("++++++++")
#     roughDesc = x.find(class_="prod-desc")
#     finDesc = roughDesc.text.strip()
#
#     titlerough = x.find(class_ = "prod-title")
#     finTit = titlerough.text.strip()
#
#     urlDetails = x.find('a', href = True)["href"]
#     finalurl = "https://www.ulta.com" + urlDetails
#
#     print(finTit)
#     print(finDesc)
#     print(finalurl)
#     try:
#         pricerough = x.find(class_ = "regPrice")
#         finPrice = pricerough.text.strip()
#         Sale = False
#         print("Not on Sale")
#     except:
#         pricerough = x.find(class_ = "pro-new-price")
#         finPrice = pricerough.text.strip()
#         Sale = True
#         print("On Sale")
#     print(finPrice)
#     #------- specific page crawl starts here
#     second = requests.get(finalurl)
#     secondtext = second.text
#     soup = BeautifulSoup(secondtext, 'html.parser')
#
#     proditem = soup.find(class_ = "product-item-no") #has size and itemnum
#     prodnum = soup.find(id = "itemNumber")
#     finalprodnum = prodnum.text.strip()
#
#     itemsize = proditem.find(id = "itemSize")
#     sizefinal = itemsize.text.strip()
#     itemdim = proditem.find(id = "itemSizeUOM")
#     dimfinal = itemdim.text.strip()
#     sizeNdim = sizefinal + " " + dimfinal

	# percentrecommend = soup.find(class_ = "pr-snapshot-consensus-value pr-rounded")
	# finalpercentrec = percentrecommend.text.strip()
	#
	# numreviewclass = soup.find(class_ = "pr-snapshot-average-based-on-text")
	# numreview = numreviewclass.find(class_ = "count")
	# numreviewfinal = numreview.text.strip()
	#
	# starrate = soup.find(class_ = "pr-rating pr-rounded average")
	# starfinal = starrate.text.strip()

	# print(finalprodnum)
	# print(finalpercentrec + " would recommend")
	# print(numreviewfinal + " reviews")
	# print(starfinal + " stars")
