import owme
from owme import Apartment


def test_get_listings_on_all_listings_page():
    listings = owme.get_listings(owme.PAGES['all listings'])
    assert len(listings) > 0
    assert all(isinstance(listing, Apartment) for listing in listings)


def test_get_listings_on_available_listings_page():
    listings = owme.get_listings()
    if listings:
        assert all(isinstance(listing, Apartment) for listing in listings)
    else:
        pass