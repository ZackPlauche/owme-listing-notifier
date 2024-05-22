import requests
import bs4

from owme.models import Apartment

__all__ = [
    'URLS',
    'BASE_URL',
    'Apartment',
    'get_listings',
    'get_all_listings',
    'get_available_listings',
    '_get_studio_cards',
    '_parse_studio_card',
    '_parse_listings',
]


BASE_URL = 'https://www.owme.pt'

URLS = {
    'available listings': 'https://www.owme.pt/estudios/disponveis',
    'all listings': 'https://www.owme.pt/estudios',
    'available soon': 'https://www.owme.pt/estudios/disponiveis-brevemente',
}


def get_listings(url: str) -> list[Apartment]:
    """Get listings from a given OWME url."""
    response = requests.get(url)
    return _parse_listings(response.text)


def get_all_listings() -> list[Apartment]:
    """Get all listings from the OWME website."""
    listings = []
    offset = 0
    base_url = URLS['all listings']
    url = base_url
    while True:
        html = requests.get(url).text
        current_listings = _parse_listings(html)
        listings += current_listings
        if 'list-pagination-next' in html:
            offset += len(current_listings)
            url = base_url + f'?offset={offset + 1}'
            continue
        break
    return listings


def get_available_listings() -> list[Apartment]:
    """Get new listings from the available listings page."""
    available_listings = get_listings(URLS['available listings'])
    available_soon_listings = get_listings(URLS['available soon'])
    return available_listings + available_soon_listings


def _get_studio_cards(html: str) -> list[bs4.element.Tag]:
    """Get studio cards from a given url."""
    soup = bs4.BeautifulSoup(html, 'html.parser')
    return soup.select('.list-grid > div')


def _parse_studio_card(studio_card: bs4.element.Tag) -> Apartment:
    """Parse a studio card to get the apartment details."""
    try:
        grid_title = studio_card.select_one('.grid-title').text.strip()
        price = studio_card.select_one('.product-price')
        if price:
            price = price.text.strip('\n').replace('€', '').replace('Sale Price:0.00 Original Price:', '')
        return Apartment(
            address=grid_title.split(' - ')[0],
            number=int(grid_title.split(' ')[-1]),
            url=BASE_URL + studio_card.select_one('a')['href'],
            price=price,
            available=studio_card.find('div', class_='sold-out') is None
        )
    except Exception as e:
        print(studio_card.prettify())
        raise e


def _parse_listings(html: str) -> list[Apartment]:
    """Parse listings from a given html."""
    return [_parse_studio_card(studio_card) for studio_card in _get_studio_cards(html)]
