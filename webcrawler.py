from urllib.request import Request, urlopen
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import re
import os
from subprocess import Popen, PIPE
from statistics import variance, mean
from selenium import webdriver
import time


def main():
    proxies = getProxies()                          #return a list of proxies 
    ct = 0                                          #iterator for how many pages have been attempted
    proxy_ct = 0                                    #iterator for choosing a new proxy
    found_pages = 0                                 #counter for number of valid webpages crawled
    while (found_pages < 200):                      #keep crawling until 200 webpages have been found
        new_proxy = False                           #by default, we aren't using a new proxy
        this_proxy_idx = proxy_ct % (len(proxies)-1)#if you iterate through all proxies, start back at the beginning of the proxy list
        if (ct % 4) == 0:                           #every fourth request, switch to a new proxy
            proxy_ct += 1                           
            new_proxy = True                        #When a new proxy is used, we need to grab a new cookie
        result = getRoomPage(getPageNumbers(1)[0], proxies[this_proxy_idx], new_proxy)    #create request
        if (result):                                #result is True when a valid page has been found
            found_pages += 1
        time.sleep(0.15)                            #wait to simulate user interation, this is set very low because the curl request typically takes ~15 seconds to complete
        ct += 1                                     #increment each time we try to get a new room page

def getProxies():                                   #returns a list of valid proxies in the format ["ip:port","ip:port"...]
    proxies=[]
    ua = UserAgent()
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    for row in proxies_table.tbody.find_all('tr'):
        proxies.append(row.find_all('td')[0].string + ":" +  row.find_all('td')[1].string)
    
    return proxies 


def getPageNumbers(pageCount):                      #returns a list of random page id's between 20k and 200k. the list is of length pageCount. 
    page_nos=[]
    for i in range(pageCount):
        page_nos.append(random.randint(20000,200000))
    
    return page_nos

#def getPageNumbersNew(pageCount):                   #currently incomplete method for crawling for valid page ids by analyzing vrbo's browse pages, can safely ignore.
#    page_nos=[]
#    options = webdriver.ChromeOptions()
#    options.add_argument("--headless")
#    options.add_argument("--no-sandbox")
#    options.add_argument("--disabled-dev-shm-usage")
#    browser = webdriver.Chrome(executable_path="./chromedriver", options=options)
#    currentPage = 2
#    while (len(page_nos) < pageCount):
#        browser.get('https://www.vrbo.com/search/keywords:united-states/page:' + str(currentPage))
#        browser.execute_script
#        soup = BeautifulSoup(browser.page_source, 'html.parser')
#        crawled_soup = soup.find_all(href=re.compile("pet"))
#        print("found " + str(len(crawled_soup)) + " hits")
#        for hit in crawled_soup:
#            href = hit.get("href")
#            end_of_id = href.find('?')
#            page_nos.append(href[1:end_of_id])
#        currentPage += 1
#        time.sleep(5)
    

def getRoomPage(page_no, proxy_addr, new_proxy):    #attempts to request a page from vrbo with a given page id (aka page_no) and using a given proxy address (aka proxy_addr). Returns True if a valid page is found, returns False otherwise
    print("proxy_address: " + proxy_addr)
    print("page_no: " + str(page_no))
    if (new_proxy):
        with open("vrbo/vrbo_" +str(page_no)+".html","wb") as output_file, open("errorFile.txt", "wb") as error_file:
            p = Popen([
                "curl",
                "-p", proxy_addr,
                "-c", "cookiefile.txt",
                "-b", "cookiefile.txt",
                "-L",
                "-m", "15",
                "-H", "Accept: application/json, text/javascript, */*; q=0.01\\",
                "-H", "Accept-Encoding:",
                "-H", "Connection: keep-alive\\",
                "-H", "X-Requested-With: XMLHttpRequest",
                "--user-agent", "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
                "https://www.vrbo.com/"+str(page_no)
                ],
                stdout=PIPE, #send output to pipe
                #stdout=output_file,
                stderr=error_file)
            print("pulling html...")
            response = p.communicate()[0] #dump response into a variable
            print("crawling...")
            soup = BeautifulSoup(response, 'html.parser')
            crawled_soup = soup.find("meta",{"property":"og:price:amount"})
            print("done crawling!")
            if (crawled_soup):
                price = crawled_soup.get("content")
                print("HEY PRICE IS " + str(price) + ". WE DID IT ! \n\n")
                output_file.write(response)
                return True
    else:
        with open("vrbo/vrbo_" +str(page_no)+".html","wb") as output_file, open("errorFile.txt", "wb") as error_file:
            p = Popen([
                "curl",
                "-p", proxy_addr,
                "-b", "cookiefile.txt",
                "-L",
                "-m", "15",
                "-H", "Accept: application/json, text/javascript, */*; q=0.01\\",
                "-H", "Accept-Encoding:",
                "-H", "Connection: keep-alive\\",
                "-H", "X-Requested-With: XMLHttpRequest",
                "--user-agent", "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
                "https://www.vrbo.com/"+str(page_no)
                ],
                stdout=PIPE,
                stderr=error_file)
            print("pulling html...")
            response = p.communicate()[0] #dump response into a variable
            print("crawling...")
            soup = BeautifulSoup(response, 'html.parser')
            crawled_soup = soup.find("meta",{"property":"og:price:amount"})
            print("done crawling!")
            if (crawled_soup):
                price = crawled_soup.get("content")
                print("HEY PRICE IS " + str(price) + ". WE DID IT ! \n\n")
                output_file.write(response)
                return True

    os.remove("vrbo/vrbo_"+str(page_no)+".html")
    return False


if __name__ == "__main__":
    main()


