import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
import os
import json
from tqdm import tqdm
from rich.console import Console
from rich.table import Table
from rich.prompt import IntPrompt, Confirm
from rich.prompt import InvalidResponse

console = Console()

CATEGORIES_URL = 'https://www.olx.ua/uk/'
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/125.0.6422.112 Safari/537.36'
    )
}

async def fetch_text(session, url):
    async with session.get(url, headers=HEADERS) as resp:
        resp.raise_for_status()
        return await resp.text()

async def fetch_categories(json_path='olx_categories.json'):
    async with aiohttp.ClientSession() as session:
        text = await fetch_text(session, CATEGORIES_URL)
    soup = BeautifulSoup(text, 'html.parser')
    div = soup.find('div', {'data-testid': 'home-categories-menu-row'})
    categories = []
    if div:
        for link in div.find_all('a'):
            title = link.find('p', class_='css-1h1uzh8')
            title = title.get_text(strip=True) if title else 'N/A'
            href = link.get('href', 'N/A')
            img = link.find('img')
            img_src = img.get('src') or (img.get('srcset','').split()[0] if img and img.get('srcset') else 'N/A')
            categories.append({
                'category_id': link.get('data-testid', 'N/A'),
                'title': title,
                'href': href,
                'image_src': img_src
            })
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
    return categories

async def load_categories(json_path='olx_categories.json'):
    if not os.path.exists(json_path):
        return await fetch_categories(json_path)
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

async def fetch_ads_from_page(session, url):
    text = await fetch_text(session, url)
    soup = BeautifulSoup(text, 'html.parser')
    ads = []
    for block in soup.find_all('div', {'data-testid': 'l-card'}):
        title_elem = block.find('h4', class_='css-1g61gc2')
        if title_elem:
            title = title_elem.get_text(strip=True)
            link_tag = title_elem.find_parent('a')
        else:
            title = 'N/A'
            link_tag = block.find('a', class_='css-1tqlkj0')
        href = link_tag.get('href') if link_tag else 'N/A'
        url_full = href if href.startswith('http') else f"https://www.olx.ua{href}"
        price = block.find('p', {'data-testid': 'ad-price'})
        price = price.get_text(strip=True) if price else 'N/A'
        loc = block.find('p', {'data-testid': 'location-date'})
        loc = loc.get_text(strip=True) if loc else 'N/A'
        img = block.find('img')
        img_src = 'not_found'
        if img:
            src = img.get('src') or (img.get('srcset','').split()[0] if img.get('srcset') else None)
            if src:
                img_src = src if src.startswith('http') else f"https://www.olx.ua{src}"
        ads.append({
            'title': title,
            'url': url_full,
            'price': price,
            'location': loc,
            'image': img_src
        })
    return ads

async def fetch_ad_details(session, ad):
    text = await fetch_text(session, ad['url'])
    soup = BeautifulSoup(text, 'html.parser')
    desc = soup.find('div', {'data-testid': 'ad_description'})
    ad['description'] = desc.get_text(separator=' ', strip=True) if desc else 'N/A'
    params = {}
    seller_type = 'N/A'
    container = soup.find('div', {'data-testid': 'ad-parameters-container'})
    if container:
        for p in container.find_all('p'):
            txt = p.get_text(strip=True)
            if ':' not in txt:
                seller_type = txt
            else:
                k, v = txt.split(':',1)
                params[k.strip()] = v.strip()
    ad['seller_type'] = seller_type
    ad['parameters'] = json.dumps(params, ensure_ascii=False)
    imgs = [img.get('src') for img in soup.find_all('img', {'data-testid': 'ad-photo'}) if img.get('src')]
    ad['gallery'] = ';'.join(imgs)
    footer = soup.find('div', {'data-cy': 'ad-footer-bar-section'})
    if footer:
        id_span = footer.find('span', class_='css-w85dhy')
        views_span = footer.find('span', {'data-testid': 'page-view-counter'})
        ad['id'] = id_span.get_text(strip=True).replace('ID:','').strip() if id_span else ''
        ad['views'] = views_span.get_text(strip=True).replace('Views:','').strip() if views_span else ''
    seller_card = soup.find('div', {'data-testid': 'seller_card'})
    if seller_card:
        trader = seller_card.find('p', {'data-testid': 'trader-title'})
        ad['trader_title'] = trader.get_text(strip=True) if trader else 'N/A'
        name = seller_card.find('h4', {'data-testid': 'user-profile-user-name'})
        ad['seller_name'] = name.get_text(strip=True) if name else 'N/A'
        score_elem = seller_card.select_one('div[data-testid="score-widget"] p')
        ad['seller_rating'] = score_elem.get_text(strip=True) if score_elem else 'N/A'
        reviews = seller_card.find('p', class_='css-1rgx7in')
        ad['seller_reviews'] = reviews.get_text(strip=True) if reviews else 'N/A'
        badge = seller_card.find('div', {'data-testid': 'delivery-badge'})
        ad['deliveries'] = badge.get_text(separator=' ', strip=True) if badge else 'N/A'
        member = seller_card.find('p', {'data-testid': 'member-since'})
        ad['member_since'] = member.get_text(strip=True) if member else 'N/A'
        last_seen = seller_card.find('p', {'data-testid': 'lastSeenBox'})
        ad['last_seen'] = last_seen.get_text(strip=True) if last_seen else 'N/A'
    return ad

async def save_to_csv(path, ads_async_iter, deep=False):
    base = ['title','url','price','location','image']
    extra = ['description','seller_type','parameters','gallery','id','views',
             'seller_name','seller_rating','seller_reviews','deliveries'] if deep else []
    fieldnames = base + extra
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        async for ad in ads_async_iter:
            row = {k: ad.get(k, '') for k in fieldnames}
            writer.writerow(row)

async def main():
    cats = await load_categories()
    table = Table(title="OLX Categories", show_lines=True)
    table.add_column("No.", justify="right", style="cyan", no_wrap=True)
    table.add_column("Category", style="magenta")
    for i, c in enumerate(cats, 1):
        table.add_row(str(i), c['title'])
    console.print(table)

    while True:
        try:
            idx = IntPrompt.ask(f"Select category number [1-{len(cats)}]")
            if 1 <= idx <= len(cats):
                idx -= 1
                break
            else:
                raise InvalidResponse("Number out of range.")
        except InvalidResponse as e:
            console.print(f"[red]Error:[/red] {e}")

    sel = cats[idx]
    total = IntPrompt.ask("How many ads to collect? Default", default=50)
    deep = Confirm.ask("Detailed parsing?", default=False)
    os.makedirs('output', exist_ok=True)
    name = sel['title'].replace('/','_')
    csv_file = os.path.join('output', f"{name}.csv")
    bar = tqdm(total=total, desc='Parsing ads')

    seen_urls = set()

    async with aiohttp.ClientSession() as session:
        done = 0
        page = 1

        async def gen_ads():
            nonlocal done, page
            while done < total:
                base_url = sel['href'] if sel['href'].startswith('http') else f"https://www.olx.ua{sel['href']}"
                url = base_url if page == 1 else f"{base_url}{('&' if '?' in base_url else '?')}page={page}"
                ads = await fetch_ads_from_page(session, url)
                if not ads:
                    break
                for ad in ads:
                    ad_url = ad['url']
                    if ad_url in seen_urls:
                        continue
                    seen_urls.add(ad_url)
                    if deep:
                        try:
                            await fetch_ad_details(session, ad)
                        except Exception as e:
                            console.print(f"[red]Error parsing {ad_url}: {e}[/red]")
                            continue
                    yield ad
                    done += 1
                    bar.update(1)
                    if done >= total:
                        bar.close()
                        return
                page += 1

        await save_to_csv(csv_file, gen_ads(), deep)

    bar.close()
    console.print(f"\n✅ [green]Saved {min(done,total)} ads to file[/green]: [bold]{csv_file}[/bold]")

if __name__ == '__main__':
    asyncio.run(main())