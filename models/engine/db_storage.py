#!/usr/bin/python3
"""This module defines a class to manage database storage"""
import os
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.city import City
from models.state import State

user = os.getenv('HBNB_MYSQL_USER')
pwd = os.getenv('HBNB_MYSQL_PWD')
host = os.getenv('HBNB_MYSQL_HOST')
db = os.getenv('HBNB_MYSQL_DB')
env = os.getenv('HBNB_ENV')


class DBStorage:
    """class to manages storage of hbnb models in SQL db"""
    __classes = [State, City, User, Place, Review, Amenity]
    __engine = None
    __session = None

    def __init__(self):
        """Initializes SQL database storage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
    if env == "test":
        Base.MetaData.drop_all()

    def all(self, cls=None):
        """Returns a dict of models in storage"""
        m_dict = {}
        if cls in self.__classes:
            resl = DBStorage.__session.query(cls)
            for row in resl:
                key = "{}.{}".format(row.__class__.__name__, row.id)
                m_dict[key] = row
        elif cls is None:
            for cl in self.__classes:
                resl = DBStorage.__session.query(cl)
                for row in resl:
                    key = "{}.{}".format(row.__class__.__name__, row.id)
                    m_dict[key] = row
        return m_dict

    def new(self, obj):
        """Adds new object to storage"""
        DBStorage.__session.add(obj)

    def save(self):
        """Commits the session changes"""
        DBStorage.__session.commit()

    def delete(self, obj=None):
        """Removes an object from the db"""
        DBStorage.__session.delete(obj)

    def reload(self):
        """Loads storage db"""

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        DBStorage.__session = Session()

    def close(self):
        """Close"""
        DBStorage.__session.close()
