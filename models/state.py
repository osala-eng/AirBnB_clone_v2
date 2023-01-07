#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
from models.stringtemplates import HBNB_TYPE_STORAGE, DB


class State(BaseModel, Base):
    """
    State class
    Relationship between Class state to city
    """
    __tablename__ = 'states'

    if (getenv(HBNB_TYPE_STORAGE) == DB):
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        name = ''

        @property
        def cities(self):
            '''Return a list of city instances in filestorage'''
            from models import storage

            list_cities = []
            for city in storage.all:
                list_cities.append(city)

            return list_cities
