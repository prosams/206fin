# 206fin
final project for si 206: scraping and crawling ulta
-------------------------
Data sources used: Everything came from https://www.ulta.com, more specifically, the primary Eye, Lip, Face, and Tools pages.
-------------------------
Q: How is the code structured?
A: My code uses four main functions to retrieve the data from online or the cache and to create a database out of it. The getAllProdType() function takes in the category of product and returns a list of tuples. Each tuple contains in depth product information for one product.

The JsonFileCreator() function creates the JSON file (named allprodlist.json) that is later used to create the database — basically, it stores the data received from the getAllProdType() function in a file outside of the main ulta.py file so that the information can be accessed apart from it.
Apart from the last two functions that create the actual databases, I also have four plotly functions.
-------------------------
The general way to run this program would be to open up the ulta.py file in terminal and run it. Typing help displays all the commands that can be made. <products> allows the user to choose from one of two in-terminal data visualizations by using <generalprod> and <brand>, including general information about a specified number of products and the average star rating of all brands. <generalprod> and <brand> can only be used once <products> has been inputted.

<avbrand>, <ozcost>, <starcost> and <numrec> all open up plotly displays on the web browser.

If you would like to recreate the database from scratch (strongly advised against because it takes over an hour to do so due to the sheer number of requests that must be made), you must first comment out the activeFunc() function then uncomment JsonFileCreator(), init_db(DBNAME), and fillthings().
-------------------------
General info about the files within this repository:

 - ulta.py is the MAIN FILE. Run this to get the finished project.
 - test.py is the TEST FILE. Run this to get the tests.
 - ultadata.db is the DATABASE file. If you delete this file, it will take a really long time to remake it.
 - allprodlist.json is a file that is used to make the database file.
 - cache.json — this file is not up to date because Github would not let me push my full cache to the server because it's so large (almost 800 mb!)
