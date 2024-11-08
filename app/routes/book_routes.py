from flask import Blueprint, abort, make_response, request
from app.models.book import Book
from app.routes.route_utilities import validate_model
from ..db import db

bp = Blueprint("bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()

    try:
        new_book = Book.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_book)
    db.session.commit()

    return new_book.to_dict(), 201

@bp.get("")
def get_all_books():
    query = db.select(Book)
    
    title_param = request.args.get("title")
    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    sorting_param = request.args.get("sort", "asc").lower()  # Default to ascending if not provided
    if sorting_param == "desc":
        query = query.order_by(Book.title.desc())
    else:
        query = query.order_by(Book.title)


    #execute the query statement and retrieve the models
    query = query.order_by(Book.id)#select records and order by id
    books = db.session.scalars(query) #retrieve all the records
    # We could also write the line above as:
    # books = db.session.execute(query).scalars()
    response = []
    for book in books:
        response.append(book.to_dict())
    return response

@bp.get("/<book_id>")
def get_one_book_by_id(book_id):
    book = validate_model(Book,book_id)
    
    return book.to_dict()

@bp.put("/<book_id>")
def update_a_book_by_id(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    response = {"message": f"Book {book_id} successfully update"}

    return response 

@bp.delete("/<book_id>")
def delete_book_by_id(book_id):
    book = validate_model(Book,book_id)
    
    db.session.delete(book)
    db.session.commit()

    return {"message": f"Book {book_id} successfully deleted"}







# @bp.get("")
# def get_all_books():
#     books_response = []
#     for book in books:
#         books_response.append(
#             {
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description
#             }
#         )
#     return books_response

# @bp.get("/<book_id>")
# def get_one_book(book_id):
#     book = validate_model(book_id)
#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description,
#     }

# def validate_model(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         response = {"message": f"book {book_id} invalid"}
#         abort(make_response(response, 400))

#     for book in books:
#         if book.id == book_id:
#             return book

#     response = {"message": f"book {book_id} not found"}
#     abort(make_response(response, 404))