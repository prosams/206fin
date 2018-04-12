import requests
import json
from bs4 import BeautifulSoup
#
# CACHE_FNAME = 'cache.json'
# try:
# 	cache_file = open(CACHE_FNAME, 'r')
# 	cache_contents = cache_file.read()
# 	CACHE_DICTION = json.loads(cache_contents)
# 	cache_file.close()
# except:
# 	CACHE_DICTION = {}
#
def basicEyeCache(url):
	if url in CACHE_DICTION:
		print("Getting cached data...")
		return CACHE_DICTION[url]
	else:
		eyereq = requests.get(eyeurl)
		CACHE_DICTION[eyeurl] = eyereq.text
		dumped_json_cache = json.dumps(CACHE_DICTION, indent = 4)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
		return CACHE_DICTION[eyeurl]

newfile = "newfile.html"

eyeurl = "https://www.sephora.com/shop/eye-makeup?pageSize=300"
eyereq = requests.get(eyeurl)
eyetext = eyereq.text
# print(eyetext)
# CACHE_DICTION[eyeurl] = eyereq.text

# dumped_json_cache = json.dumps(eyetext, indent = 4)
# fw = open(newfile,"w")
# fw.write(dumped_json_cache)
# fw.close() # Close the open file
# print(dumped_json_cache)



# f = open(newfile)
# html = f.read()
# html = eyetext.read()
soup = BeautifulSoup(eyetext, 'html.parser')
# print(soup.prettify())
# pls = soup.find_all("div", class_ = "css-s1k656")
# comp = soup.find_all("div", attrs = {"data-comp":"ProductGrid"})
# prods = soup.find_all(class_ = "css-196wge2")
# print(prods)

spans = soup.find_all("span")
print(len(spans))
lines = [span.get_text() for span in spans]
for x in lines:
    print(x)
# print(soup.find_all('div', class_='\"css-115paux\"'))

# new = soup.find_all("onelinknotx")
# itemnames = soup.find_all("span", attrs = {"data-at":"sku_item_name"})
# itemnames = soup.find(class_ = "css-1r6no3d OneLinkNoTx")
# spans = soup.find_all('span', {'class' : 'css-1r6no3d OneLinkNoTx'})
# spans = soup.find_all(class_ = "css-cw20ea")

# itemnames = soup.find("div", class_ = "css-115paux")
# print(itemnames)
