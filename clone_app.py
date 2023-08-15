import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_file(url, folder_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_name = url.split("/")[-1]
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {file_name}")
    else:
        print(f"Failed to download: {url}")

def download_image(url, folder_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_name = url.split("/")[-1]
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded image: {file_name}")
    else:
        print(f"Failed to download image: {url}")

def clone_page(url, output_folder):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Download HTML content
        html_file_path = os.path.join(output_folder, 'index.html')
        with open(html_file_path, 'wb') as html_file:
            html_file.write(response.content)
        print("Downloaded HTML")

        # Download CSS and JS files
        for link in soup.find_all(['link', 'script']):
            if link.has_attr('href') or link.has_attr('src'):
                if link.has_attr('href'):
                    file_url = urljoin(url, link['href'])
                else:
                    file_url = urljoin(url, link['src'])

                file_folder = os.path.dirname(os.path.relpath(file_url, url))
                file_folder_path = os.path.join(output_folder, file_folder)
                os.makedirs(file_folder_path, exist_ok=True)

                download_file(file_url, file_folder_path)

        # Download images
        for img in soup.find_all('img'):
            if img.has_attr('src'):
                img_url = urljoin(url, img['src'])
                img_folder = os.path.dirname(os.path.relpath(img_url, url))
                img_folder_path = os.path.join(output_folder, img_folder)
                os.makedirs(img_folder_path, exist_ok=True)

                download_image(img_url, img_folder_path)
    else:
        print(f"Failed to clone page: {url}")

if __name__ == "__main__":
    page_url = "https://tunis-nextjs.vercel.app/home-rtl"  # Replace with the URL of the page you want to clone
    output_folder = "gaju_tunis"     # Replace with the desired output folder name

    clone_page(page_url, output_folder)
