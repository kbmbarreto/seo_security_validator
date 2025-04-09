import requests
from bs4 import BeautifulSoup
import re

def find_nofollow_directives(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # Verificar se existe uma meta tag 'robots' com 'nofollow'
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        if meta_robots and 'nofollow' in meta_robots.get('content', '').lower():
            print(f"\nAtenção: A meta tag 'robots' contém 'nofollow' em {url}.")

        # Verificar links individuais com rel='nofollow'
        nofollow_links = soup.find_all('a', attrs={'rel': 'nofollow'})
        if nofollow_links:
            print(f"\nLinks encontrados com 'rel=nofollow' em {url}:")
            for link in nofollow_links:
                print(link.get('href'))

        # Verificar cabeçalhos HTTP para 'X-Robots-Tag'
        x_robots_tag = response.headers.get('X-Robots-Tag')
        if x_robots_tag and 'nofollow' in x_robots_tag.lower():
            print(f"\nAtenção: Cabeçalho HTTP 'X-Robots-Tag' contém 'nofollow' em {url}.")

    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")


if __name__ == "__main__":
    site_url = "https://teleferico.apps.etc.br/"
    find_nofollow_directives(site_url)
