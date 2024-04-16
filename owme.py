from pydantic import BaseModel
import requests
import bs4


class Apartment(BaseModel):
    address: str
    number: int
    url: str
    price: int | None = None

    def __str__(self) -> str:
        return f'{self.address} Studio {self.number} - {self.price}: {self.url}'


BASE_URL = 'https://www.owme.pt'

PAGES = {
    'available listings': 'https://www.owme.pt/estudios/disponveis',
    'all listings': 'https://www.owme.pt/estudios',
}


def get_listings(url: str) -> list[Apartment]:
    """Get listings from a given url."""
    listings = []
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    studio_cards = soup.select('.list-grid > div')
    for studio_card in studio_cards:
        grid_title = studio_card.select_one('.grid-title').text.strip()
        apartment = Apartment(
            address=grid_title.split(' - ')[0],
            number=int(grid_title.split(' ')[-1]),
            url=BASE_URL + studio_card.select_one('a')['href']
        )
        listings.append(apartment)
    return listings
