from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def init_browser():
   
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

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #Click the button ('full_image')
    full_image_elem=browser.find_by_id('full_image')
    full_image_elem.click()

    #Click the button ('more info')
    browser.is_element_present_by_text("more info", wait_time=0.5)
    more_info_elem=browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    #Getting the new html from current page
    html=browser.html
    current=BeautifulSoup(html,'html.parser')

    img_ref=current.find('figure', class_="lede").a['href']
    featured['img']=f"https://www.jpl.nasa.gov{img_ref}"
    
    return featured

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
    tableD={}
    url="https://space-facts.com/mars/"
    df = pd.read_html(url)[0] #table itself
    df.columns = ["Mars Facts", "value"]
    tt=df.to_html(index=False)
    tableD['facts']=df.to_html(index=False)

    return tableD

