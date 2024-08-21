"""
odm.py

@Author: Jason Nwakaeze
@Date: December 18, 2018

The base class for application services. All services that inherit from the parent class will carry basic functionality that can be
overridden. Functionality for each service class include:
    - create: Create a new object
    - create_many: Create multiple objects at once
    - update: Update an existing object
    - update_many: Update multiple objects at once
    - get: Retrieve an object by ID
    - get_by_ids: get an array of objects by a list of ids
    - query: Retrieve a collection of objects by query
    - delete: Delete an object by ID
    - delete_by_ids: Delete a collection of objects by query via ids

"""

from datetime import datetime
from ..base import utils
from sqlalchemy.exc import SQLAlchemyError


class ServiceFactory(object):
    """
    Service factory generator. This class will produce other service classes required by any application that uses it.
    """

    @classmethod
    def create_service(cls, klass, db_session):
        """ Create and generate a service class using the model class provided """

        class BaseService:
            model_class = klass
            db = db_session

            @classmethod
            def get(cls, obj_id):
                """ Get a single object from the database by primary key """

                if isinstance(obj_id, cls.model_class):
                    return obj_id

                try:
                    obj = cls.model_class.query.get(obj_id)
                    if not obj:
                        raise ValueError(f"No object found with ID {obj_id}")
                    return obj
                except SQLAlchemyError as e:
                    print(e)
                    raise

            @classmethod
            def find_one(cls, **params):
                """ Find a single object that matches the criteria within the parameters """

                try:
                    obj = cls.model_class.query.filter_by(**params).first()
                    if not obj:
                        print("Could not find any object that matches this criteria")
                    return obj
                except SQLAlchemyError as e:
                    print(e)
                    raise

            @classmethod
            def create(cls, ignored_args=None, **kwargs):
                """ Base create method """

                if not ignored_args:
                    ignored_args = ["id", "date_created", "last_updated"]

                try:
                    data = {k: v for k, v in kwargs.items() if k not in ignored_args}
                    obj = cls.model_class(**data)
                    cls.db.session.add(obj)
                    cls.db.session.commit()
                    return obj
                except SQLAlchemyError as e:
                    cls.db.session.rollback()
                    print(e)
                    raise

            @classmethod
            def update(cls, obj_id, ignored_args=None, **kwargs):
                """ Update an existing record by primary key """

                if not ignored_args:
                    ignored_args = ["id", "date_created", "last_updated"]

                obj = cls.get(obj_id)

                try:
                    for key, value in kwargs.items():
                        if key not in ignored_args:
                            setattr(obj, key, value)
                    if "last_updated" in ignored_args:
                        obj.last_updated = datetime.utcnow()
                    cls.db.session.commit()
                    return obj
                except SQLAlchemyError as e:
                    cls.db.session.rollback()
                    print(e)
                    raise

            @classmethod
            def delete(cls, obj_id):
                """ Delete an object by primary key """

                obj = cls.get(obj_id)

                try:
                    cls.db.session.delete(obj)
                    cls.db.session.commit()
                    return obj
                except SQLAlchemyError as e:
                    cls.db.session.rollback()
                    print(e)
                    raise

        return BaseService
