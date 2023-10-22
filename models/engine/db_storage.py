#!/usr/bin/python3
"""This module defines a class to manage database storage"""
from models.base_model import Base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
import MySQLdb
from .classes import classes


class DBStorage:
    """
    This class manages storage of hbnb models in a MySQL database.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        The above function initializes a connection to a MySQL
        """
        connect = MySQLdb.connect(host="localhost", port=3306,
                                  user="hbnb_dev", passwd="hbnb_dev_pwd",
                                  charset="utf8")
        cursor = connect.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS hbnb_dev_db")
        connect.commit()
        cursor.close()
        connect.close()
        self.__engine = create_engine('mysql+mysqldb://'
                                      '{}:{}@{}:3306/{}'.format(
                                          getenv('HBNB_MYSQL_USER'), getenv(
                                              'HBNB_MYSQL_PWD'),
                                          getenv('HBNB_MYSQL_HOST'), getenv(
                                              'HBNB_MYSQL_DB')
                                      ), pool_pre_ping=True)
        if getenv("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        The function `all` retrieves all instances of a specified
        """
        my_dict = {}
        # Session = sessionmaker(bind=self.__engine)
        # self.__session = Session()
        if cls:
            my_query = self.__session.query(cls).all()
            for i in my_query:
                my_dict[str(cls.__name__) + "." + i.id] = i
            return my_dict
        for key, value in classes.items():
            my_query = self.__session.query(value).all()
            for i in my_query:
                my_dict[str(key) + "." + i.id] = i
        return my_dict

    def new(self, obj):
        """
        The function adds an object to a session.
        """
        self.__session.add(obj)

    def save(self):
        """
        The save function commits changes to the session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        The delete function deletes an object from the session.
        """
        if obj is None:
            return
        self.__session.delete(obj)

    def reload(self):
        """
        The `reload` function creates all the necessary tables
        in the database and initializes a new
        session.
        """
        from ..amenity import Amenity
        from ..city import City
        from ..place import Place
        from ..review import Review
        from ..state import State
        from ..user import User
        Base.metadata.create_all(self.__engine)
        my_session = scoped_session(sessionmaker(bind=self.__engine,
                                    expire_on_commit=False))
        self.__session = my_session()

    def close(self):
        """
        The close function removes the session
        """
        self.__session.close()
        self.reload()
