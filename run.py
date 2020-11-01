from six.moves import urllib
from bs4 import BeautifulSoup
import validators


#Initial and final date in range to be extracted
INITIAL_DATE = 1953
FINAL_DATE   = 2019


filepath = "export_data,csv"

#Open File 
f = open(filepath, "w")

coins = [["AUD","AUD","AUD","AUD","CAD","CAD","EUR","EUR","EUR","EUR","EUR"
        ,"EUR","EUR","GBP","GBP","GBP","GBP","GBP","GBP","NZD","NZD","NZD","NZD","USD"
        ,"USD","USD"],
        ["CAD","CHF","JPY","NZD","CZF","JPY","AUD","CAD","CHF","GBP","JPY","NZD"
         ,"USD","AUD","CAD","CHF","JPY","NZD","USD","CAD","CHF","JPY","USD","CAD"
         ,"CHF","JPY"]]


#Total urls to extract data from
URLCOUNT     = (FINAL_DATE - INITIAL_DATE) * 26

parsedcount = 0 #Succesfully parsed


#For every coin combination
for i in range(26):
    coin_1 = coins[0][i] # First  Coin 
    coin_2 = coins[1][i] # Second Coin

    coin = str(coin_1) + "/" + str(coin_2)
    
    
    #For every date in range
    for date in range(INITIAL_DATE,FINAL_DATE):
        
        #Building url
        lft_coin = "https://fxtop.com/en/historical-exchange-rates.php?A=1&C1="
        mid_coin = "&C2="
        lft_date = "&TR=1&DD1=01&MM1=01&YYYY1="
        mid_date = "&B=1&P=&I=1&DD2=31&MM2=12&YYYY2="
        rgt_date = "&btnOK=Go%21"

        
        #Constructed link
       # link =lft_coin + coin_1 + mid_coin + coin_2 + lft_date + str(date) + mid_date + str(date) + rgt_date
        link  = "https://www.yellowpages.com/search?search_terms=Electricians&geo_location_terms=CO&s=name"
        
        #Check valid url to avoid unwanted exit
        if validators.url(link):
            
            #Requesting url
            source = urllib.request.urlopen(link).read()
            soup = BeautifulSoup(source,'lxml')#Passing  source html to soup

            #Central table has 1 attr , border = 1
            table = soup.find('table', {"border" : "1"})

            #If there are data to be exported
            if table:

                parsedcount += 1 # increasing parsed count
               
                #Passing rows to csv
                for row in table.findAll("tr"):
                    cells = row.findAll("td")

                    #Building row for csv
                    tabledate = cells[0].find(text=True)
                    val  = cells[1].find(text=True)
                    perc = cells[2].find(text=True)
                    
                    #Line to be written onto csv file 
                    line = (str(tabledate) + ',' + str(val) + ',' + str(perc) + ',' + str(coin)+ "\n")

                    f.write(line)   # Write to csv

                # Output : Verified Date / Coins
                print("Extracted Data from : " + str(date) + " " + coin) 

            else:
                print ("ERROR:No table exists on :" + "Parsed " + str(date) + " " + coin) 

                

        #ERROR: Invalid url!      
        else:

            print ("ERROR:Invalid url for " + "Parsed " + str(date) + " " + coin) 

# Output : Succesfully extracted url count
print("Succesfully Extracted : " + str(parsedcount) + "/" + str(URLCOUNT) + "Urls")

f.close()

num_rows = len(open(filepath).readlines(  ))

# Output : Csv file length
print("Written " + str(num_rows) )

