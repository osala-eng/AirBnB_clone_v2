#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.stringtemplates import HBNB_TYPE_STORAGE, DB
from os import getenv
from sqlalchemy import String, Column, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    if getenv(HBNB_TYPE_STORAGE) == DB:
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review', backref='place',
                               cascade='all, delete, delete-orphan')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False,
                                 back_populates='place_amenities')

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self) -> list:
            '''Return list of reviews'''
            from models import storage
            from models.review import Review

            list_reviews = []
            for review in storage.all(Review).values():
                if review.place_id == self.id:
                    list_reviews.append(review)
            return list_reviews

        @property
        def amenities(self) -> list:
            '''Get amenity list'''
            from models import storage
            from models.amenity import Amenity

            list_amenities = []
            for amnty in storage.all(Amenity).values():
                if amnty.id in self.amenity_ids:
                    list_amenities.append(amnty)
            return list_amenities

        @amenities.setter
        def amenities(self, amenity=None) -> None:
            '''Set amenity list'''

            if amenity:
                self.amenity_ids.append(amenity.id)
