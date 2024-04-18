import os
from typing import Callable

from dotenv import load_dotenv

import owme
import gmail

load_dotenv(override=True)


LUIZA_EMAIL = os.getenv('LUIZA_EMAIL')
LUIZA_MESSAGE = """\
Hey baby! 🙂 Hope you're having a good day today 🙂

Here are some new apartments on the OWME website that you might like.
"""


def notify_about_new_apartments(email: str, filter_func: Callable | None = None):
    """Notify a user about new apartments on the OWME website.

    filter_func example:
    lambda listing: listing.price < 500
    """

    print('Checking for new apartments...')
    new_listings = owme.get_listings(owme.PAGES['available listings'])
    if filter_func:
        new_listings = [listing for listing in new_listings if filter_func(listing)]
    if new_listings:
        message = LUIZA_MESSAGE + '\n'.join(str(listing) for listing in new_listings)
        gmail.send_email(email, subject='New Apartments on OWME 💌', body=message)


if __name__ == '__main__':
    notify_about_new_apartments(LUIZA_EMAIL)
