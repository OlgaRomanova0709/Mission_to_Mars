from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_news():
    browser = init_browser()
    news = {}

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    var=soup.select_one('.image_and_description_container')
    var_last_article=var.select_one('.list_text')
    news['title']=var_last_article.select_one('.content_title').text
    news['p']=var_last_article.select_one('.article_teaser_body').text

    return news

def scrape_featured():
    browser = init_browser()
    featured = {}

    url = 'https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA19913'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    img_ref=soup.find('figure', class_="lede").a['href']
    featured['img']=f"https://www.jpl.nasa.gov{img_ref}"
    return featured

def scrape_weather():
    browser = init_browser()
    weather_news = {}

    url="https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    weather=soup.find_all('div',class_="js-tweet-text-container")[0]
    weather_news['inf']=weather.find('p').text
    return weather_news

def scrape_hemi():
    browser = init_browser()

    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    hemispheres=soup.find_all('div',class_="item") 
    
    hemi_list=[]
    for hemi in hemispheres:
        hemi_dict={}
        hemi_dict['title']=hemi.div.a.h3.text
        h=hemi.a['href']
        hemi_url=f"https://astrogeology.usgs.gov/{h}"
        browser.visit(hemi_url)
        html = browser.html
        soup= BeautifulSoup(html,'html.parser')
        a=soup.find('div', class_='downloads').ul.li.a['href']
        hemi_dict['img_url']=a
        hemi_list.append(hemi_dict)

    return hemi_list

def scrape_table():
    browser = init_browser()
    url="https://space-facts.com/mars/"
    browser.visit(url)
    html = browser.html

    soup = BeautifulSoup(html, "html.parser")
    one=soup.find_all("div", class_="textwidget")[3].table.tbody
    table_inf=one.find_all('tr')
    table_mars=[]
    for i in table_inf:
        dict_mars={}
        dict_mars['title']=i.find_all('td')[0].text
        dict_mars['value']=i.find_all('td')[1].text
        table_mars.append(dict_mars)


    return table_mars

