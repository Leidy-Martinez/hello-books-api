from flask import Blueprint, abort, make_response, request
from app.models.book import Book
from app.routes.route_utilities import validate_model,create_model,get_models_with_filters
from ..db import db

bp = Blueprint("bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()
    return create_model(Book,request_body)

@bp.get("")
def get_all_books():
    return get_models_with_filters(Book, request.args)

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
    book.author = request_body.get("author")
    db.session.commit()

    response = {"message": f"Book {book_id} successfully update"}

    return response 

@bp.delete("/<book_id>")
def delete_book_by_id(book_id):
    book = validate_model(Book,book_id)
    db.session.delete(book)
    db.session.commit()

    return {"message": f"Book {book_id} successfully deleted"}