import random
import os
import owme

from dotenv import load_dotenv

load_dotenv(override=True)


emails = [
    # os.getenv('LUIZA_EMAIL'),
    os.getenv('ZACK_EMAIL'),
]

flowers = '🌻💐🌹'
pet_names = ['baby', 'snuggems', 'sexy mama', 'snugglebear', 'boss lady']
quality_words = ['good', 'great', 'awesome', 'epic', 'fantastic', 'spectacular']

with open('message.txt', 'r', encoding='utf-8') as file:
    message = file.read()

body = message.format(
    name=random.choice(pet_names),
    quality=random.choice(quality_words),
    emoji=random.choice(flowers),
)

notifier = owme.Notifier('sqlite:///owme.db')
notifier.update_all_listings()
available_listings = owme.get_available_listings()
s = notifier.Session()
l = notifier._get_available_listings(s, available_listings)
print(l)


# if __name__ == '__main__':
#     notifier.notify_about_new_apartments(emails, body=body, filter_func=lambda apt: apt.price < 400)
