import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin


def find_relative_protocol_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # Procurar todos os elementos que podem ter URLs problemáticas
        tags_with_src = soup.find_all(['img', 'script', 'iframe', 'source'])
        tags_with_href = soup.find_all(['link', 'a'])

        # Expressão regular para identificar links relativos ao protocolo
        relative_protocol_pattern = re.compile(r'^//')

        problematic_links = []

        for tag in tags_with_src:
            url_value = tag.get('src')
            if url_value and relative_protocol_pattern.match(url_value):
                problematic_links.append(urljoin(url, url_value))

        for tag in tags_with_href:
            url_value = tag.get('href')
            if url_value and relative_protocol_pattern.match(url_value):
                problematic_links.append(urljoin(url, url_value))

        if problematic_links:
            print(f"\nURLs problemáticas encontradas em {url}:")
            for link in problematic_links:
                print(link)
        else:
            print(f"\nNenhum link problemático encontrado em {url}.")

    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")


if __name__ == "__main__":
    site_url = "https://teleferico.apps.etc.br"
    find_relative_protocol_links(site_url)
