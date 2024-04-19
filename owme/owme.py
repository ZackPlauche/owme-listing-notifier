import requests
import bs4

from decimal import Decimal
from pydantic import BaseModel

__all__ = [
    'PAGES', 
    'BASE_URL',
    'Apartment', 
    'get_listings',
    'get_new_listings', 
]


class Apartment(BaseModel):
    address: str
    number: int
    url: str
    price: Decimal | None = None

    def __str__(self) -> str:
        return f'{self.name} -  €{self.price}: {self.url}'
    
    @property
    def name(self) -> str:
        return f'{self.address} Studio {self.number}'


BASE_URL = 'https://www.owme.pt'

PAGES = {
    'available listings': 'https://www.owme.pt/estudios/disponveis',
    'all listings': 'https://www.owme.pt/estudios',
    'available soon': 'https://www.owme.pt/estudios/disponiveis-brevemente',
}


def get_listings(url: str) -> list[Apartment]:
    """Get listings from a given url."""
    listings = []
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    studio_cards = soup.select('.list-grid > div')
    for studio_card in studio_cards:
        grid_title = studio_card.select_one('.grid-title').text.strip()
        price = studio_card.select_one('.product-price')
        if price:
            price = price.text.strip('\n').strip('€')
        apartment = Apartment(
            address=grid_title.split(' - ')[0],
            number=int(grid_title.split(' ')[-1]),
            url=BASE_URL + studio_card.select_one('a')['href'],
            price=price,
        )
        listings.append(apartment)
    return listings


def get_new_listings() -> list[Apartment]:
    """Get new listings from the available listings page."""
    available_listings = get_listings(PAGES['available listings'])
    available_soon_listings = get_listings(PAGES['available soon'])
    return available_listings + available_soon_listings