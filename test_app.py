import owme
from owme import Apartment
import whatsapp


def test_get_listings_on_all_listings_page():
    listings = owme.get_listings(owme.PAGES['all listings'])
    assert len(listings) > 0
    assert all(isinstance(listing, Apartment) for listing in listings)
    assert all(listing.price is None for listing in listings)

def test_get_listings_on_available_listings_page():
    listings = owme.get_listings(owme.PAGES['available listings'])
    if listings:
        assert all(isinstance(listing, Apartment) for listing in listings)
    else:
        pass


sample_message = """\
Hello! 

I hope you're having a good day today :)\
"""


def test_send_whatsapp_message():
    whatsapp.send_message('+351 911 193 242', sample_message)
