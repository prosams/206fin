# 206fin
final project for si 206: scraping and crawling ulta
-------------------------
Data sources used: Everything came from https://www.ulta.com, more specifically, the primary Eye, Lip, Face, and Tools pages.

-------------------------
Q: How is the code structured?

A: My code uses four main functions to retrieve the data from online or the cache and to create a database out of it. The getAllProdType() function takes in the category of product and returns a list of tuples. Each tuple contains in depth product information for one product.

The JsonFileCreator() function creates the JSON file that is later used to create the database — basically, it stores the data received from the getAllProdType() function in a file outside of the main ulta.py file so that the information can be accessed apart from it.
  Apart from the last two functions that create the actual databases, I also have four plotly functions.
