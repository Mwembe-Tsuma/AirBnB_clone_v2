#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, ForeignKey
from models.base_model import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
import os
from models.city import City


class State(BaseModel, Base):
    """
     State class
     The State class represents a state
    """

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        cities = relationship('City', backref='state', cascade="all, delete")
        pass
    else:
        @property
        def cities(self):
            """
            The function "cities" returns a list of cities associated
            with a specific state.
            """
            from models import storage
            city_list = []
            for city in list(storage.all(City).values()):
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
