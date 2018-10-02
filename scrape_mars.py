# coding: utf-8
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

# def init_browser():
#     # @NOTE: Replace the path with your actual path to the chromedriver
#     executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
#     browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    ## SCRAPE MARS NEWS

    # Visit Mars news website
    mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(mars_news_url)

    # Parse HTML with Beautiful Soup
    mars_news_html = browser.html
    news_soup = bs(mars_news_html, 'html.parser')

    # Find the first article
    article = news_soup.find('li', class_='slide')

    # Extract the title and parargraph information from the first article
    news_title = article.find('div', class_='content_title').find('a').text
    news_p = article.find('div', class_='article_teaser_body').text

    ## SCRAPE JPL FEATURED IMAGE

    # Visit JPL website
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    # Parse HTML with Beautiful Soup
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    # Extract the url from the featured image
    featured_image = jpl_soup.find('div', class_='carousel_container').find('article')['style'].split("url('")

    # Append the extracted url to the main url to acquire the complete url to the image
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image[-1][:-3]

    ## SCRAPE MARS WEATHER (TWITTER)

    # Visit Mars Weather's twitter page
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # Parse HTML with Beautiful Soup
    weather_html = browser.html
    weather_soup = bs(weather_html, 'html.parser')

    # Extract the text from the first tweet
    mars_weather = weather_soup.find('li', class_='js-stream-item').find('p', class_='tweet-text').text

    ## SCRAPE MARS FACTS

    # Visit website containing Mars facts
    facts_url = 'http://space-facts.com/mars/'
    browser.visit(facts_url)

    # Create a list of all the tables on the Mars facts webpage
    tables = pd.read_html(facts_url)

    # Create a df from the first table
    df = tables[0]

    # Set the column names of the df
    df.columns = ['Attribute', 'Measurement']

    # Change the index
    df = df.set_index('Attribute')

    # Convert the df to html
    html_table = df.to_html()

    # Remove the newlines in the html code
    html_table = html_table.replace('\n', '')

    ## SCRAPE MARS HEMISPHERES

    # Visit the website with info regarding Mars hemispheres
    hemi_homepage_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_homepage_url)

    # Create an HTML object for the homepage and parse HTML with Beautiful Soup
    hemi_homepage_html = browser.html 
    hemi_homepage_soup = bs(hemi_homepage_html, 'html.parser')

    # Create a list to store dictionaries with title and link info for each image
    hemisphere_image_urls = []

    # Find all images on the homepage
    products = hemi_homepage_soup.find_all('div', class_='item')

    # Loop through each image
    for product in products:
        # Create a dictionary for the current image
        current_hemisphere_image = {}

        # Extract the title of the image and add this to the dictionary
        current_hemisphere_image['title'] = product.find('div', class_='description').find('a', class_='product-item').find('h3').text
        
        # Extract the link to get the high res image
        href = product.find('div', class_='description').find('a', class_='product-item')['href']
        
        # Visit the link containing the high res image
        url_to_visit = 'https://astrogeology.usgs.gov/' + href
        browser.visit(url_to_visit)
        
        # Create an HTML object for the visited link and parse HTML with Beautiful Soup
        html = browser.html
        soup = bs(html, 'html.parser')
        
        # Extract the link for the high res image and add this to the dictionary
        image_url = soup.find('div', class_='downloads').find('li').find('a')['href']
        current_hemisphere_image['img_url'] = image_url

        # Append the current dictionary to the current_hemisphere_image list
        hemisphere_image_urls.append(current_hemisphere_image)
        
        # Return to homepage
        browser.visit(hemi_homepage_url)

    # Create dictionary of compiled scraped data
    scraped_mars = {'news': {'news_title': news_title, 'news_p': news_p},
                   'featured_image_url': featured_image_url,
                    'weather': mars_weather,
                    'facts_table': html_table,
                    'hemispheres': hemisphere_image_urls
                   }

    return scraped_mars

