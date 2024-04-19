import os
import random

from dotenv import load_dotenv

import gmail
from owme.notifications import notify_about_new_apartments

load_dotenv(override=True)

LUIZA_EMAIL = os.getenv('LUIZA_EMAIL')

flowers = '🌻💐🌹'
pet_names = ['baby', 'snuggems', 'sexy mama', 'snugglebear', 'boss lady']
quality_words = ['good', 'great', 'awesome', 'epic', 'fantastic', 'spectacular']

LUIZA_MESSAGE = f"""\
Hey {random.choice(pet_names)}! 🙂 Hope you're having a {random.choice(quality_words)} day today {random.choice(flowers)}

Here are some new apartments on the OWME website that you might like in your price range:
"""


if __name__ == '__main__':
    notify_about_new_apartments([gmail.EMAIL, LUIZA_EMAIL], LUIZA_MESSAGE, lambda listing: listing.price <= 400)