# imports
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser

# set up chromedriver to browse
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    mars_dict = {}
    browser = init_browser()

    # extract html for news
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "lxml")
    
    # get the title and paragraph that went with it, then print
    news_title = soup.find_all("div", class_="content_title")[1].text
    news_p = soup.find_all("div", class_="article_teaser_body")[0].text


    # extract html for the image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "lxml")

    # find the image source and form url
    image = soup.find_all("div", class_="img")[0].img["src"]
    featured_image_url = f'https://www.jpl.nasa.gov{image}'


    # extract the mars fact
    url = "https://space-facts.com/mars/"
    table = pd.read_html(url)
    mars_fact_html = table[0].to_html()


    # extract hemisphere data
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "lxml")

    # loop through the links and add the url for image under "Sample"
    hemisphere_image_urls = []

    image_titles = soup.find_all("h3")

    for image_title in image_titles:
        img_dict = {}
        title = image_title.text.strip()
        browser.click_link_by_partial_text(title)
        img_dict["title"] = title
        img_dict["img_url"] = browser.find_by_text("Sample")["href"]
        hemisphere_image_urls.append(img_dict)
        browser.visit(url)


    # store to mars_dict
    mars_dict["news_title"] = news_title
    mars_dict["news_p"] = news_p
    mars_dict["featured_image_url"] = featured_image_url
    mars_dict["mars_fact_table_html"] = mars_fact_html
    mars_dict["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()
    
    return mars_dict