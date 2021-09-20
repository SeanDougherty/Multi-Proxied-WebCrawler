# VRBO Proxied WebCrawler
A Proxy based Web Crawler built using BeautifulSoup, Selenium, and fake_useragent to crawl VRBO webpages and pull pricing information. The program pulls from a list of publicly available proxies listed by www.sslproxies.org to continually cycle through connections thus avoiding VRBOs DoS mitigation protections. This program is not intended for any malicious uses and is purely educational. There is no guarantee of continued functionality as VRBO may have altered the structure of their webpage. Proxied WebCrawler is highly dependent on the HTML format of VRBO's webpage remaining static and will cease to function if certain DOM nodes, tags, flags, or values have changed.

## Compiling

To begin crawling web pages, run webcrawler.py via Python3
```bash
	$ python3 webcrawler.py
```

This will begin to crawl vrbo for web pages and save any valid pages it finds (it does this by checking to see if a price is listed in the page’s meta-data)

When you want to analyze the collected html pages, run stats.py via Python3
```bash
	$ python3 stats.py
```

This will print the Average price and Variance to the command line and will populate a matplotlib graph of the distribution

## Results:

Average price: $279.42
Variance: 43566.2476

## Improvements:

This script can be improved in a number of ways.

First, the beginnings of a method have been written to allow this program to perform an initial crawl of vrbo that collects only valid page ids. Currently, only 1 in ~15 page ids are valid which drastically reduces the rate at which valid pages are saved.

Second, there are no checks to see if a page has already been crawled/checked. Using some simple checking one would be able to prevent this.

Third, the range of valid values for page id are unknown. Currently, only ids between 20,000 and 200,000 are being tested.

