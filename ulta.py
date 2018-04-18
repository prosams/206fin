import requests
import plotly.plotly as py
import plotly.graph_objs as go
import json
from bs4 import BeautifulSoup
import sqlite3
import random

class IdidntKnowINeededAClass:
	def __init__(self, name):
		self.name = name

CACHE_FNAME = 'cache.json'
try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

def cacheRequest(url): # this is called in other functions
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

def uniqueUltaUrl(type, numresult = "500"): #can be eyes, face, lips, and tools — this is called in other funcs
	base = "https://www.ulta.com/"
	if type == "eyes": # https://www.ulta.com/makeup-eyes?N=26yd&No=0&Nrpp=1000
		category = "makeup-eyes"
		end = "?N=26yd&No=0&Nrpp={}".format(numresult)
	elif type == "face":
		category = "makeup-face"
		end = "?N=26y3&No=0&Nrpp={}".format(numresult)
	elif type == "lips":
		category = "makeup-lips"
		end = "?N=26yq&No=0&Nrpp={}".format(numresult)
	elif type == "tools":
		category = "tools-brushes-makeup-brushes-tools"
		end = "?N=27hn&No=0&Nrpp={}".format(numresult)
	total = base + category + end
	return total

# print(uniqueUltaUrl("eyes", "48"))

def getAllProdType(kind, numresult = "500"): #takes in eyes, lips, face, tools — also called in other funcs
	returnlist = []
	first_url = uniqueUltaUrl(kind, numresult)
	page = cacheRequest(first_url)
	soup = BeautifulSoup(page, 'html.parser')
	elements = soup.find_all(class_ = "productQvContainer")

	if kind == "eyes": #gets the numbers that will differentiate the categories
		category = "1"
	elif kind == "lips":
		category = "2"
	elif kind == "face":
		category = "3"
	elif kind == "tools":
		category = "4"

	for x in elements:
		roughDesc = x.find(class_="prod-desc")
		finDesc = roughDesc.text.strip() # ******** basically product name

		print(finDesc) # THIS PRINT IS ON PURPOSE so you can see what category you're on!!

		titlerough = x.find(class_ = "prod-title")
		finTit = titlerough.text.strip() # ********* product brand
		urlDetails = x.find('a', href = True)["href"] # *******this should be the indiv product url
		finalurl = "https://www.ulta.com" + urlDetails

		try:
			pricerough = x.find(class_ = "regPrice")
			strippedprice = pricerough.text.strip()
			if len(strippedprice) > 7:
				splitprice = strippedprice.split("-")
				moreexpensive = splitprice[-1]
				finPrice = moreexpensive[2:]
			else:
				finPrice = strippedprice[1:]
			Sale = "No"
		except:
			pricerough = x.find(class_ = "pro-new-price")
			strippedprice = pricerough.text.strip()
			if len(strippedprice) > 7:
				splitprice = strippedprice.split("-")
				moreexpensive = splitprice[-1]
				finPrice = moreexpensive[2:]
			else:
				finPrice = strippedprice[1:]
			Sale = "Yes"

		#---------------------- specific page crawl starts here --------------------------
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
			sizeNdim = itemsize.text.strip()
		except:
			sizeNdim = None

		try:
			percentrecommend = soup.find(class_ = "pr-snapshot-consensus-value pr-rounded")
			percentrec = percentrecommend.text.strip()
			finalpercentrec = percentrec[:-1]
		except:
			finalpercentrec = None

		try:
			numrevclass = soup.find(id = "rws_cnts")
			numreview = numrevclass.text.strip()
			numreviewfinal = numreview[1:-1]
		except:
			numreviewfinal = None

		try:
			starrate = soup.find(class_ = "pr-rating pr-rounded average")
			starfinal = starrate.text.strip()
		except:
			starfinal = None

		ultimateTuple = (finDesc, finTit, category, finPrice, finalprodnum, sizeNdim, finalpercentrec, numreviewfinal, starfinal, Sale, finalurl)
		returnlist.append(ultimateTuple)
		# print(ultimateTuple)
	# print(returnlist)
	return returnlist

 # ************ THIS CODE HERE IS TO CREATE THE JSON FILE THAT WILL BE USED FOR PRODUCTS TABLE *******
def JsonFileCreator(): # this is the func that calls the cache func and uses the other func
	eyelist = getAllProdType("eyes")
	eyetup = eyelist
	liplist = getAllProdType("lips", "1000") # changes the url so that the site displays 1000 products (lol)
	liptup = liplist
	facelist = getAllProdType("face")
	facetup = facelist
	toolist = getAllProdType("tools", "1000")
	tooltup = toolist
	allprodDict = {}
	allprodDict["1"] = eyetup
	allprodDict["2"] = liptup
	allprodDict["3"] = facetup
	allprodDict["4"] = tooltup
	megalist = eyetup + liptup + facetup + tooltup
	dumped = json.dumps(megalist)
	fw = open("allprodlist.json","w")
	fw.write(dumped)
	fw.close() # Close the open file
 # ******************* code for json file ends here **********************

DBNAME = "ultadata.db"
def init_db(x): # this function creates the database - initializes the (empty) tables!
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

def fillthings(): # this function fills the database with info using the json file we made earlier
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

	eyebrandlist = []
	eyeprodlist = []
	toolbrandlist = []
	toolprodlist = []
	facebrandlist = []
	faceprodlist = []
	lipbrandlist = []
	lipprodlist = []
	for x in loaded:
		if x[2] == "1":
			eyeprodlist.append(x[0])
			if x[1] not in eyebrandlist and not None:
				eyebrandlist.append(x[1])
		elif x[2] == "2":
			lipprodlist.append(x[0])
			if x[1] not in lipbrandlist and not None:
				lipbrandlist.append(x[1])
		elif x[2] == "3":
			faceprodlist.append(x[0])
			if x[1] not in facebrandlist and not None:
				facebrandlist.append(x[1])
		elif x[2] == "4":
			toolprodlist.append(x[0])
			if x[1] not in toolbrandlist and not None:
				toolbrandlist.append(x[1])

	eyetup = ("Eye", len(eyebrandlist), len(eyeprodlist))
	liptup = ("Lip", len(lipbrandlist), len(lipprodlist))
	facetup = ("Face", len(facebrandlist), len(faceprodlist))
	tooltup = ("Tool", len(toolbrandlist), len(toolprodlist))
	categorytuple = (eyetup, liptup, facetup, tooltup)
	for tup in categorytuple:
		insert = (None, tup[0], tup[1], tup[2])
		statement = 'INSERT INTO "Categories" '
		statement += 'VALUES (?, ?, ?, ?)'
		cur.execute(statement, insert)
		conn.commit()

def avbrand(): # this function sorts by the average star rating of a brand
	print("Please be patient.. I'm doing things, this may take a few seconds..")

	try:
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
		WHERE StarRating IS NOT NULL
		GROUP BY Brand
		ORDER BY AVG(StarRating) ASC
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
					title = 'Brand Name',
					range = len(plotlytuplist)
				),
					yaxis = dict(
					title = 'Average Star Rating (Out of 5 Stars)',
					range = [0, 5]
				),
					height = 1000,
					width = 2000
			)
		fig = go.Figure(data=data, layout=layout)
		py.plot(fig, filename = 'avrating')
		print("Plotly should be opening a graph in a new window on your browser!")
	except:
		return("Plotly seems to be throwing a tantrum... Wait a little bit, try a different command, and come back to this in a minute or so. ")

def costPerOz(): # this function calculates the cost per ounce of a product
	print("Please be patient.. I'm doing things, this may take a few seconds..")

	try:
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
		ORDER BY CAST(Cost AS DECIMAL)/CAST(ItemSizeOz AS DECIMAL) ASC LIMIT 100
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
					title = "Product Cost Per Ounce",
					xaxis = dict(
					title = 'Product Name',
					range = len(plotlytuplist)
				),
					yaxis = dict(
					title = 'Cost in USD',
					range = [0, 20]),
					height = 800,
					width = 2000)

		fig = go.Figure(data=data, layout=layout)
		py.plot(fig, filename = 'ultacostperounce')
		print("Plotly should be opening a graph in a new window on your browser!")
	except:
		return("Plotly seems to be throwing a tantrum... Wait a little bit, try a different command, and come back to this in a minute or so. ")

def numberPeopleRecommend():  # this is the percent of people who would recommend times the number of reviews
	print("Please be patient.. I'm doing things, this may take a few seconds..") # (to find number of people who would recommend)

	try:
		DB_NAME = 'ultadata.db'
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
		ORDER BY (CAST(PercentRec AS DECIMAL)/100)*Reviews
		DESC LIMIT 100
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
					title = "Number of People Who Would Recommend (% Recommend * Number of Reviews)",
					xaxis = dict(
					title = 'Product Name',
					range = len(plotlytuplist)
				),
					yaxis = dict(
					title = 'Number of People Who Would Recommend',
					range = [0, 12000]),
					height = 800,
					width = 1500)

		fig = go.Figure(data=data, layout=layout)
		py.plot(fig, filename = 'ulta-bar')
		print("Plotly should be opening a graph in a new window on your browser!")
	except:
		return("Plotly seems to be throwing a tantrum... Wait a little bit, try a different command, and come back to this in a minute or so. ")


def costNStarCorrelation(): # this function plots the product price against the star rating to see if there is a correlation between the two
	print("Please be patient.. I'm doing things, this may take a few seconds..")
	try:
		DB_NAME = 'ultadata.db'
		try:
			conn = sqlite3.connect(DB_NAME)
			cur = conn.cursor()
		except Error as e:
			print(e)
		query = "SELECT * FROM 'products'"
		cur.execute(query)

		basic_statement = '''
		SELECT starrating, Cost, Name
		FROM Products
		JOIN Categories
		ON Categories.Id = Products.Category
		WHERE starrating IS NOT NULL
		ORDER BY Products.starrating DESC
		'''
		cur.execute(basic_statement)
		plotlytuplist = []
		for row in cur:
			try:
				pair = (row[0], round(float(row[1]), 1), row[2]) #this rounds like in project 3
				plotlytuplist.append(pair)
			except:
				continue
		# print(plotlytuplist)

		trace1 = go.Scatter(
				type='scatter',
				y =[x[0] for x in plotlytuplist],
				x =[x[1] for x in plotlytuplist],
				mode = 'markers',
				name = 'markers',
				text = [x[2] for x in plotlytuplist] # this names each individual point
				)
		data = [trace1]

		layout = go.Layout(
					title = "Correlation Between Cost of Product + Star Rating",
					xaxis = dict(
					title = 'Cost of Product',
					range = len(plotlytuplist)
				),
					yaxis = dict(
					title = 'Star Rating out of Five Stars',
					range = [0, 5.5]
				),
					height = 1000,
					width = 1000
			)

		fig = go.Figure(data=data, layout=layout)
		py.plot(fig, filename = 'star-cost-correlation')
		print("Plotly should be opening a graph in a new window on your browser!")
	except:
		return("Plotly seems to be throwing a tantrum... Wait a little bit, try a different command, and come back to this in a minute or so. ")

def simpleinteractive():
	userstring = input("Type either [brand], [generalprod], or _______")
	conn = sqlite3.connect("ultadata.db")
	cur = conn.cursor()
	returnlist = []

	if "brand" in userstring:
		print("Printing the brand names and their average star rating.")
		basic_statement = '''
		SELECT Brand, AVG(StarRating)
		FROM Products
		JOIN Categories
		ON Categories.Id = Products.Category
		WHERE StarRating IS NOT NULL
		GROUP BY Brand
		ORDER BY AVG(StarRating) DESC
		'''
		cur.execute(basic_statement)
		conn.commit()

		for row in cur:
			indiv = (row[0], round(float(row[1]), 2))
			returnlist.append(list(indiv))
		for x in returnlist:
			final = '{0:25} {1:15}'.format(*x)
			print(final)
		print("If you would like to see a Plotly visualization of this data, type [avbrand]")

	if "generalprod" in userstring:
		limitnum = "LIMIT 100"
		splitinput = userstring.split()
		if len(splitinput) > 1:
			limitnum = splitinput[-1]
		print("Printing the top 100 most highly rated products")

		basic_statement = '''
		SELECT Name, Brand, StarRating, Cost, Categories.Category
		FROM Products
		JOIN Categories
		ON Categories.Id = Products.Category
		GROUP BY Brand
		ORDER BY StarRating
		DESC {}
		'''.format(limitnum)
		cur.execute(basic_statement)
		conn.commit()

		for row in cur:
			indiv = [row[0], row[1], row[2], str(row[3]), row[4]]
			if len(indiv[0]) > 25:
				indiv[0] = indiv[0][:24] + '...'
			indiv[3] = "   $" + indiv[3]
			returnlist.append(indiv)
		for x in returnlist:
			final = '{0:30} {1:23} {2:10} {3:14} {4:10}'.format(*x)
			print(final)

	if "price" in userstring:
		limitnum = "LIMIT 100"
		splitinput = userstring.split()
		if len(splitinput) > 1:
			limitnum = splitinput[-1]

# avbrand()
# costPerOz()
# costNStarCorrelation()
# numberPeopleRecommend()

def activeFunc():
	userInput = input("Enter a command (or 'help' for some more options): ")

	while userInput != "exit":
		print(" + + + + + ")

		if userInput == "help":
			print("products\n	Type if you would like to see simple product information from Ulta. [You will be prompted for more.]")
			print("avbrand\n	Opens up a plotly graph on your webbrowser.\n	Displays the average star rating of all brands.")
			print("ozcost\n	Opens up a plotly graph on your webbrowser.\n	Displays the cost per ounce of a product.")
			print("starcost\n	Opens up a plotly graph on your webbrowser.\n	Displays a scatter plot comparing the cost of a product and its star rating.")
			print("numrec\n	Opens up a plotly graph on your webbrowser.\n	Displays the number of people that would recommend a product\n	by multiplying the percentage of people who would recommend a product by the # of reviews.")
			print("exit\n	Exits the program")
			print("help\n	Lists available commands (these instructions)")

		elif userInput == 'exit':
			break

		elif "avbrand" in userInput:
			print("Calculating the average star rating of all brands..")
			avbrand()
		elif "ozcost" in userInput:
			print("Calculating the cost per ounce of product...")
			costPerOz()
		elif "starcost" in userInput:
			print("Comparing the price of a product to its star rating...")
			costNStarCorrelation()
		elif "numrec" in userInput:
			print("Calculating the number of people who woudl recommend products...")
			numberPeopleRecommend()

		else:
			print("Command not recognized: " + userInput)
			print("Make sure you've typed your command in the proper format.")

		print(" + + + + + ")
		secondInput = input("Enter a command (or 'help' for some more options): ")
		userInput = secondInput

if __name__ == "__main__":
	activeFunc()
	# JsonFileCreator()
	# init_db(DBNAME)
	# fillthings()

	print("Exiting the program... come back soon!")
