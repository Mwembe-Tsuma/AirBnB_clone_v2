#!/usr/bin/python3
"""Define Engine for DBStorage."""
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """A class that handles database storage operations."""

    __engine = None
    __session = None

    def __init__(self):
        """Initializes the database engine and binds it to a new
        Session object.

        The database engine is created with the provided environment variables
        for the user, password, host, and database name.
        The Session object is then created and assigned to self.__session.
        """

        db_user = environ.get("HBNB_MYSQL_USER")
        db_password = environ.get("HBNB_MYSQL_PWD")
        db_host = environ.get("HBNB_MYSQL_HOST")  # (here = localhost)
        db_name = environ.get("HBNB_MYSQL_DB")
        hbnb_env = environ.get("HBNB_ENV")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                db_user, db_password, db_host, db_name
            ),
            echo=True,
            pool_pre_ping=True,
        )

        if hbnb_env == "test":
            Base.metadata.drop_all(self.__engine)

        Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def all(self, cls=None):

        """Returns a dictionary of models currently in storage"""
        objects = {}

        if cls is not None:
            query = self.__session.query(cls)
            for obj in query.all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            for cls in Base.__subclasses__():
                query = self.__session.query(cls)
                for obj in query.all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj

        return objects

    def new(self, obj):
        """add the object to the current database session (self.__session)."""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database (feature of SQLAlchemy)
        (WARNING: all classes who inherit from Base must be imported
        before calling Base.metadata.create_all(engine))"""
        """create the current database session (self.__session) from the engine
        (self.__engine) by using a sessionmaker
        - the option expire_on_commit must be set to False ;
        and scoped_session - to make sure your Session is thread-safe"""

        from models.state import State
        from models.city import City
        from models.place import Place
        from models.amenity import Amenity
        from models.review import Review
        from models.user import User

        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False,
        )
        Session = scoped_session(Session)
        self.__session = Session()

    def close(self):
        """Call remove() on private session or close() on Session."""
        self.__session.close()
