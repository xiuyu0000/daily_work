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


def download_documents_as_pdf(links):
    """下载文档内容并保存为PDF"""
    for link in links:
        try:
            # 使用pdfkit转换HTML为PDF，需要先在系统中安装wkhtmltopdf
            output_name = '-'.join(link.replace("https://python.langchain.com/docs/", "").split("/"))
            pdfkit.from_url(link, f"./output/{output_name}.pdf")
            print(f"Downloaded {link}")
            # 生成随机延迟，避免被服务器识别为爬虫
            sleep_time = random.randint(1, 3)
            time.sleep(sleep_time)  # 添加适当的延迟
        except Exception as e:
            print(f"Error downloading document {link}: {e}")


if __name__ == "__main__":
    links = fetch_links("https://python.langchain.com/docs/expression_language/")
    download_documents_as_pdf(link_set)
