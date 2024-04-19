from typing import Callable

import gmail
from . import owme


DEFAULT_MESSAGE = """\
Hey 
"""


def notify_about_new_apartments(
        email: str | list[str], 
        message: str = DEFAULT_MESSAGE, 
        filter_func: Callable | None = None,
        ):
    """Notify a user about new apartments on the OWME website.

    message: Message before the list of apartments

    filter_func example:
    lambda listing: listing.price < 500

    SIDE EFFECT: Show time
    """

    print('Checking for new apartments...')
    new_listings = owme.get_new_listings()
    if filter_func:
        new_listings = [listing for listing in new_listings if filter_func(listing)]
    if new_listings:
        print('New apartments found!')
        if isinstance(email, str):
            email = [email]
        message = message + '\n'.join(f'- ' + str(listing) for listing in new_listings)
        gmail.send_email(email, subject=f'New Apartments on OWME 💌', body=message)
    else:
        print('No new apartments found.')
