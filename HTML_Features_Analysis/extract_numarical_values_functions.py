import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib.request
import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By

# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager


# Extract error links function
def extract_links(total_links, url):
    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        base_url = soup.find('base')['href'] if soup.find('base') else url

        # Find the website domain
        dom_list = re.findall('^(?:https?://)?((?:[^/?#]+\.)?([^/?#]+))', base_url)
        website_domain = dom_list[0][1]

        # Extract all links from the HTML content
        links = [a['href'] for a in soup.find_all('a') if 'href' in a.attrs]

        # print (links,base_url)

        # Categorize links as internal or external
        internal_links = []
        external_links = []
        error_hyperlinks = []

        for link in links:
            parsed_link = urlparse(link)
            if not bool(parsed_link.netloc):  # Relative URL
                internal_links.append(website_domain + parsed_link.path)
            elif parsed_link.netloc == url:  # Internal link
                internal_links.append(link)
            else:  # External link
                external_links.append(link)

        # Check the status of each link using requests
        for link in links:
            try:
                response = requests.head(link, timeout=5)  # Set a timeout of 5 seconds
                if response.status_code != 200:
                    error_hyperlinks.append(link)
            except (requests.exceptions.RequestException, requests.exceptions.Timeout):
                error_hyperlinks.append(link)

        Internal_Links_Ratio = len(internal_links) / total_links if total_links > 0 else 0
        External_Links_Ratio = len(external_links) / total_links if total_links > 0 else 0
        External_to_Internal_Ratio = len(external_links) / len(internal_links) if len(internal_links) > 0 else 0
        error_hyperlinks_ratio = len(error_hyperlinks) / total_links if total_links > 0 else 0

        print("Internal Links Ratio:", Internal_Links_Ratio)
        print("External Links Ratio:", External_Links_Ratio)
        print("External to Internal Ratio:", External_to_Internal_Ratio)
        print("Error Hyperlinks Ratio:", error_hyperlinks_ratio)

        return Internal_Links_Ratio, External_Links_Ratio, External_to_Internal_Ratio, error_hyperlinks_ratio

    except Exception as e:
        print(f"Error processing file {url}: {e}")
        return 0,0,0,0


# extract other numarical values form URL
def extract_numarical_values(url): 
    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read()
        
        if html_content is None:
            # Handle the case where the HTML content is not retrieved successfully
            # Return default values or handle the error accordingly
            print(f"Error occurred while retrieving HTML content for URL: {url}")
            return 0, 0, 0, 0, 0, 0, 0, 0 

        soup = BeautifulSoup(html_content, 'html.parser')

        # find all anchor tags and extract href attributes
        a_tags = soup.find_all('a')
        a_list = []
        for a in a_tags:
            href = a.get("href")
            if href:
                a_list.append(href)
        
        # find all Link tags and extract href attributes
        link_tags = soup.find_all('link', href=lambda href: href and href.endswith('.css'))
        css_list = [link.get('href') for link in link_tags]
        
        # find all img tags and extract src attributes
        img_tags = soup.find_all("img")
        img_list = []
        for img in img_tags:
            src = img.get("src")
            if src:
                img_list.append(src)

        # find all script tags and extract src attributes
        # Find all <script> tags with 'src' attributes
        script_tags = soup.find_all("script", src=True)
        script_list = [script['src'] for script in script_tags]

        # find all form tags and extract action attributes
        form_tags = soup.find_all("form")
        form_list = []
        for form in form_tags:
            action = form.get("action")
            if action:
                form_list.append(action)

        # # Extract null hyperlinks
        null_hyperlinks = ['#', 'javascript:void(0);', '#content']
        null_hyperlinks_total = len([link for link in a_list if link in null_hyperlinks])
        null_hyperlinks_a = len([link for link in soup.find_all('a') if link.get('href') and link.get('href') in null_hyperlinks])   


        # #total links 
        total_links = len(a_list) + len(css_list) + len(img_list) + len(script_list) + len(form_list)

        # calculate ratios
        a_tag_ratio = len(a_list) / total_links if total_links > 0 else 0
        css_ratio = len(css_list) / total_links if total_links > 0 else 0
        img_ratio = len(img_list) / total_links if total_links > 0 else 0
        script_ratio = len(script_list) / total_links if total_links > 0 else 0
        null_ratio = null_hyperlinks_total / total_links if total_links > 0 else 0
        a_tag_null_ratio = null_hyperlinks_a / len(a_list) if total_links > 0 else 0
        form_count = len(form_list)

        print("Script Ratio:", script_ratio)
        print("CSS Ratio:", css_ratio)
        print("Image Ratio:", img_ratio)
        print("A Tag Ratio:", a_tag_ratio)
        print("A Tag Null Ratio:", a_tag_null_ratio)
        print("Null Ratio:", null_ratio)
        print("Form Count:", form_count)
        print("Total Links:", total_links)

        return [script_ratio, css_ratio, img_ratio, a_tag_ratio, a_tag_null_ratio, null_ratio, form_count, total_links]

    except Exception as e:
        print(f"Error processing file {html_content}: {e}")
        return 0, 0, 0, 0, 0, 0, 0, 0
