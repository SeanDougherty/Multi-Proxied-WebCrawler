import matplotlib.pyplot as plt
from statistics import variance, mean
from bs4 import BeautifulSoup
from subprocess import Popen, PIPE
import os
import re

def main():
    path = 'vrbo/'
    prices = []
    for filename in os.listdir(path):
        try:
            with open(path+filename, "rb") as input_file:
                soup = BeautifulSoup(input_file, 'html.parser')
                price = int(soup.find("meta",{"property":"og:price:amount"}).get("content"))
                prices.append(price)
        except:
            print("we lost a page, are you currently crawling?")

    print("average price is: " + str(mean(prices)))
    print("variance is: " + str(variance(prices)))
    plt.hist(prices, color = 'blue', edgecolor = 'black', bins = 50)
    plt.show()
    
if __name__ == "__main__":
    main()
