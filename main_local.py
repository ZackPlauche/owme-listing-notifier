import schedule

import gmail
import owme
from owme.notifications import notify_about_new_apartments


times = []
for i in range(24):
    times.append(str(i).zfill(2) + ':00')
    times.append(str(i).zfill(2) + ':30')

exclude_list = [
    'Rua Alexandre Herculano 16A Studio 16',
    'Rua do Brasil 134 Studio 1',
    'Av Afonso Henriques 27 Studio 7',
    'Av Afonso Henriques 27 Studio 23',
    'Rua António Vasconcelos 15 Studio 18',
]


def requirements(listing: owme.Apartment):
    return (listing.price < 400 or 'Rua do Brasil' in listing.address) and not listing.name in exclude_list


if __name__ == '__main__':
    notify_about_new_apartments([gmail.EMAIL], message='New apartments finally found', filter_func=requirements)
    for time in times:
        schedule.every().day.at(time).do(notify_about_new_apartments, [gmail.EMAIL], message='New apartments finally found', filter_func=requirements)
    while True:
        schedule.run_pending()
