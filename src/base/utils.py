# coding=utf-8
"""
utils.py

@Author:    Jason Nwakaeze
@Date:      January 02, 2019
@Time:      3:42 PM

This module contains a number of utility functions useful throughout our application.
No references are made to specific models or resources. As a result, they are useful with or
without the application context.
"""
from datetime import date, datetime
from math import ceil

import json
from marshmallow import ValidationError, EXCLUDE
from sqlalchemy.orm import DeclarativeMeta
from flask import jsonify


class CustomJSONEncoder(json.JSONEncoder):
    """ JSON encoder that supports date formats """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return datetime.combine(obj, datetime.min.time()).isoformat()

        # Handle SQLAlchemy model instances
        if isinstance(obj.__class__, DeclarativeMeta):
            # Convert SQLAlchemy model to dictionary
            return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

        # Handle bytes
        if isinstance(obj, bytes):
            return obj.decode("utf-8")

        # Default handler
        return json.JSONEncoder.default(self, obj)


def marshal(data, schema):
    """
    Prepares the response object with the specified schema.

    :param data: The data object to be serialized.
    :param schema: The schema class that should be used to serialize the response.
    :return: A JSON-serializable dictionary or a Flask response object.
    """
    resp_ = None

    # Handle list of SQLAlchemy model instances
    if isinstance(data, list):
        try:
            resp_ = schema(many=True).dump(data)
        except ValidationError as e:
            print("Errors", e)

    # Handle single SQLAlchemy model instance
    elif hasattr(data, '__table__'):
        try:
            resp_ = schema().dump(data)
        except ValidationError as e:
            print("Errors", e)

    # Handle dict objects
    elif isinstance(data, dict):
        try:
            resp_ = schema().dump(data, many=False)
        except ValidationError as e:
            print("Errors", e)

    # For unsupported types, raise an exception
    else:
        raise TypeError("Unsupported data type for marshalling.")

    return jsonify(resp_)


def convert_dict(data, indent=None, to_json=False):
    json_str = json.dumps(data, indent=indent, cls=CustomJSONEncoder)
    if to_json:
        # json_str = json_str.rstrip("'").lstrip("'")
        json_str = json.loads(json_str)
    return json_str


def clean_kwargs(ignored_keys, data):
    """
    Removes the ignored_keys from the data sent

    ignored_keys: keys to remove from the data (list or tuple)
    data: data to be cleaned (dict)

    returns: cleaned data
    """

    for key in ignored_keys:
        data.pop(key, None)

    return data


def roundUp(n, d=2):
    d = int('1' + ('0' * d))
    return ceil(n * d) / d


def populate_obj(obj, data):
    """
    Populates an object with the data passed to it

    param obj: Object to be populated
    param data: The data to populate it with (dict)

    returns: obj populated with data


    """
    for name, value in data.items():
        if hasattr(obj, name):
            # print(name, value)
            if isinstance(value, float):
                value = roundUp(value)
            setattr(obj, name, value)

    return obj
