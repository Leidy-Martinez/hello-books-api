from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from ..db import db

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.post("")
def create_book():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]

    new_book = Book(title=title, description=description)
    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }
    return response, 201

@books_bp.get("")
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
        response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
        )
    return response

@books_bp.get("/<book_id>")
def get_one_book_by_id(book_id):
    book = validate_book(book_id)
    
    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }
        
def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        response = {"message": f"book {book_id} invalid"}
        abort(make_response(response, 400))

    #execute the query statement and retrieve the models
    query = db.select(Book).where(Book.id == book_id) #select records with an id = book_id
    book = db.session.scalar(query) #retrieve only one record book_id
    # We could also write the line above as:
    # books = db.session.execute(query).scalars()

    if not book:
        response = {"message": f"book {book_id} not found"}
        abort(make_response(response, 404))

    return book

@books_bp.put("/<book_id>")
def update_a_book_by_id(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@books_bp.delete("/<book_id>")
def delete_book_by_id(book_id):
    book = validate_book(book_id)
    
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")






# @books_bp.get("")
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

# @books_bp.get("/<book_id>")
# def get_one_book(book_id):
#     book = validate_book(book_id)
#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description,
#     }

# def validate_book(book_id):
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