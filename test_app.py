import owme
from owme import Apartment


def test_get_listings():
    listings = owme.get_listings(owme.PAGES['all listings'])
    assert len(listings) > 0
    assert all(isinstance(listing, Apartment) for listing in listings)