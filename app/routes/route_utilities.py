from flask import abort, make_response, request
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))

    #execute the query statement and retrieve the models
    query = db.select(cls).where(cls.id == model_id) #select records with an id = model_id
    book = db.session.scalar(query) #retrieve only one record model_id
    # We could also write the line above as:
    # model = db.session.execute(query).scalars()

    if not book:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return book