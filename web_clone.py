import requests
import os
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


def download_file(url, folder_path, file_path):
    response = requests.get(url)
    if file_path[0] == "/":
        file_path = file_path[1:]
    print(file_path)
    os.makedirs(folder_path, exist_ok=True)
    directory_path = os.path.dirname(os.path.join(folder_path, file_path))
    os.makedirs(directory_path, exist_ok=True)
    if not os.path.exists(os.path.join(folder_path, file_path)):
        with open(os.path.join(folder_path, file_path), 'wb+') as file:
            file.write(response.content)


def clone_website(url, output_folder):
    # Create output folder if it doesn't exist
    print(output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Send a GET request to the base URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the <img> tags and download the associated images
    img_tags = soup.find_all('img')
    for img in img_tags:
        img_url = urljoin(url, img['src'])
        img_file_path = urlparse(img_url).path
        download_file(img_url, output_folder, img_file_path)

    # Find all the <link> tags with rel="stylesheet" and download the CSS files
    css_tags = soup.find_all('link', rel='stylesheet')
    for css in css_tags:
        css_url = urljoin(url, css['href'])
        css_file_path = urlparse(css_url).path
        download_file(css_url, output_folder, css_file_path)

    # Find all the <script> tags and download the associated JavaScript files
    script_tags = soup.find_all('script')
    for script in script_tags:
        if 'src' in script.attrs:
            script_url = urljoin(url, script['src'])
            script_file_path = urlparse(script_url).path
            download_file(script_url, output_folder, script_file_path)


    # Download the HTML file itself
    filename = os.path.join(output_folder, 'index.html')
    with open(filename, 'wb') as file:
        file.write(response.content)


def download_html_pages(url, output_folder):
    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <a> tags with 'href' attribute
    links = soup.find_all('a', href=True)

    for link in links:

        href = link['href']
        # Join the relative URL with the base URL
        absolute_url = urljoin(url, href)
        clone_website(absolute_url, output_folder,)
        # Parse the absolute URL to get the file name
        filename = urlparse(absolute_url).path

        if filename[0] == "/":
            filename = filename[1:]

        # Download the HTML page
        try:
            response = requests.get(absolute_url)
            if response.status_code == 200:
                directory_path = os.path.dirname(os.path.join(output_folder, filename))
                os.makedirs(directory_path, exist_ok=True)
                if not os.path.exists(os.path.join(folder_path, file_path)):
                    with open(output_folder +'/' + filename, 'wb') as file:
                        file.write(response.content)
                    print(f"Downloaded: {absolute_url}")
            else:
                print(f"Failed to download: {absolute_url} [Status Code: {response.status_code}]")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download: {absolute_url} [Error: {e}]")



# Example usage
website_url = 'https://admin.pixelstrap.com/enzo/template/index.html'
output_folder_path = './web'

download_html_pages(website_url, output_folder_path)
