import os
import pdfkit
import time
import random
import requests
from bs4 import BeautifulSoup


def fetch_links(
    url,
    link_selector,
    base_url,
    depth_limit=5,
    current_depth=1,
    visited=None):
    if not visited:
        visited = set()
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all(class_=link_selector)
    for link in links:
        href = link.get('href')
        if href and href.startswith('/docs'):
            full_url = base_url + href
            if full_url not in visited:
                print(full_url)
                visited.add(full_url)
                if current_depth < depth_limit:
                    time.sleep(random.randint(1, 3))
                    fetch_links_dfs(full_url, link_selector, base_url, depth_limit, current_depth + 1, visited)
    return visited


def download_documents_as_pdf(links, output_folder="./output", 
                              time_sleep=(1, 3), recure=0, failed_links=None, prefix="", output_name=""):
    """下载文档内容并保存为PDF"""
    if failed_links is None:
        failed_links = []
    if recure > 3:
        print("Recure limit reached")
        return failed_links
    if os.path.exists(output_folder) is False:
        os.makedirs(output_folder)
    for link in links:
        try:
            # 使用pdfkit转换HTML为PDF，需要先在系统中安装wkhtmltopdf
            if not output_name:
                output_name = '-'.join(link.replace(prefix, "").split("/"))
            pdfkit.from_url(link, os.path.join(output_folder, f"{output_name}.pdf"))
            print(f"Downloaded {link}")
            # 生成随机延迟，避免被服务器识别为爬虫
            sleep_time = random.randint(time_sleep[0], time_sleep[1])
            time.sleep(sleep_time)  # 添加适当的延迟
        except Exception as e:
            print(f"Error downloading document {link}: {e}")
            failed_links.append(link)
    if failed_links and recure < 3:
        print("Retrying failed downloads")
        return download_documents_as_pdf(failed_links, output_folder, time_sleep, recure + 1, failed_links)
    return failed_links


if __name__ == "__main__":
    links = fetch_links("https://python.langchain.com/docs/expression_language/")
    failed_link = download_documents_as_pdf(link_set)
    print(failed_link)
