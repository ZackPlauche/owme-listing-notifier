import logging
from datetime import datetime
from typing import Callable
from pathlib import Path

import gmail
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import Session, sessionmaker

import owme
from owme.notifier.dbmodels import Apartment, Base, Notification


class OWMENotifier:

    def __init__(self, db_uri: str):
        try:
            global gmail
            self.gmail = gmail.Client.from_env()
        except:
            feedback = 'OWMENotifier requires GMAIL_USERNAME and GMAIL_PASSWORD environment variables to be set.'
            raise Exception(feedback)
        engine = create_engine(db_uri)
        self.Session = sessionmaker(bind=engine)
        if engine.name == 'sqlite' and not Path(engine.url.database).exists():
            Base.metadata.create_all(engine)
            self.update_all_listings()

    def update_all_listings(self):
        """Update the database with all of owme's listings."""
        all_listings = owme.get_all_listings()
        with self.Session() as session:
            existing_apts = session.query(Apartment).all()
            existing_apt_urls = [apt.url for apt in existing_apts]
            new_listings = [Apartment(**listing.model_dump()) for listing in all_listings if listing.url not in existing_apt_urls]
            if new_listings:
                session.add_all(new_listings)
                logging.info(f'Added {len(new_listings)} new listings to the database.')
            session.commit()

    @staticmethod
    def _get_available_listings(session: Session) -> list[Apartment]:
        """Get and update the avialable listings from the OWME website"""
        available_apartments = []
        available_listings = owme.get_available_listings()
        # Check the database to see if the listings in the database has changed
        if available_listings:
            available_listing_urls = [apt.url for apt in available_listings]
            existing_apts = session.query(Apartment).filter(
                Apartment.url.in_(available_listing_urls),
                or_(Apartment.available == True)
            ).all()
            for apt in existing_apts:
                before_apt_available = apt.available
                apt.available = apt.url in available_listing_urls
                if before_apt_available != apt.available:
                    apt.last_availability_change = datetime.now()
                if apt.available:
                    available_apartments.append(apt)
            session.commit()
        return available_apartments

    def notify_about_new_apartments(self, 
                                    email: str | list[str], 
                                    subject: str = 'New Apartments on OWME 💌', 
                                    body: str = 'New apartments found!', 
                                    filter_func: Callable | None = None,
                                    no_send: bool = False,
                                    ):
        """Notify a user about new apartments on the OWME website."""
        emails = [email] if isinstance(email, str) else email
        with self.Session() as session:
            # Get available listings that match the preferences of the users
            apartments = self._get_available_listings(session)
            if filter_func:
                apartments: list[Apartment] = [listing for listing in apartments if filter_func(listing)]
            oldest_change = min(apt.last_availability_change for apt in apartments)
            for email in emails:
                new_apartments = []
                # Get the notifications that have been sent since the latest currently available jobs last availability change
                notifications = session.query(Notification).filter(
                    Notification.email == email,
                    and_(Notification.sent_at >= oldest_change)
                ).all()
                if notifications:
                    for apt in apartments:
                        if not any(apt in notification.apartments for notification in notifications):
                            new_apartments.append(apt)
                else:
                    new_apartments = apartments
                if new_apartments:
                    print(f'{len(new_apartments)} new apartments found for {email}.')
                    notification = Notification(email=email, subject=subject, body=body, apartments=new_apartments)
                    session.add(notification)
                    message = body + '\n' + '\n'.join(f'- {apt}' for apt in new_apartments)
                    if not no_send:
                        self.gmail.send_email(email, subject=subject, body=message)
                else:
                    print('No new apartments found.')
            session.commit()
