import owme
from owme import Apartment


def test_get_listings():
    listings = owme.get_listings(owme.URLS['all listings'])
    assert len(listings) > 0
    assert all(isinstance(listing, Apartment) for listing in listings)

def test_get_available_listings():
    listings = owme.get_available_listings()
    assert all(listing.available for listing in listings)