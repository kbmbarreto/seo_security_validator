import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import requests


async def get_hreflang_urls(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    hreflang_urls = []

    for link in soup.find_all('link', rel='alternate'):
        hreflang_url = link.get('href')
        hreflang_code = link.get('hreflang')
        if hreflang_url and hreflang_code:
            hreflang_urls.append((hreflang_url, hreflang_code))

    return hreflang_urls


async def check_noindex(page, url: str):
    await page.goto(url)
    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')

    meta_tag = soup.find('meta', attrs={'name': 'robots'})
    if meta_tag and 'noindex' in meta_tag.get('content', '').lower():
        return True
    return False


async def validate_hreflang(url: str, page):
    hreflang_urls = await get_hreflang_urls(url)
    problematic_urls = []

    for hreflang_url, hreflang_code in hreflang_urls:
        try:
            print(f"Verificando {hreflang_code} -> {hreflang_url}")
            has_noindex = await check_noindex(page, hreflang_url)

            if has_noindex:
                problematic_urls.append((hreflang_url, hreflang_code))
                print(f"❌ Problema encontrado! {hreflang_url} possui 'noindex'")
            else:
                print(f"✅ {hreflang_url} está indexável.")

        except Exception as e:
            print(f"Erro ao acessar {hreflang_url}: {e}")

    return problematic_urls


async def main():
    urls = [
        "https://teleferico.apps.etc.br",
        "https://teleferico.apps.etc.br/estaciones-de-teleferico/estacion-oasis/",
        "https://teleferico.apps.etc.br/choose-your-ticket/?zona_origen=OASIS&wmc-currency=CLP"
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        all_problematic_urls = []

        for url in urls:
            print(f"\n🔍 Testando URL principal: {url}")
            problematic_urls = await validate_hreflang(url, page)
            all_problematic_urls.extend(problematic_urls)

        await browser.close()

        if all_problematic_urls:
            print("\n🚩 URLs com problemas de 'noindex':")
            for url, code in all_problematic_urls:
                print(f"- {code}: {url}")
        else:
            print("\n🎉 Todas as URLs estão indexáveis!")


if __name__ == "__main__":
    asyncio.run(main())