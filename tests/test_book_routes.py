import pytest

def test_get_all_books_with_two_records(client, two_saved_books):
    # Act: Send a GET request to the /books endpoint
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert isinstance(response_body, list)
    assert len(response_body) == 2

    # Define expected book data
    expected_books = [
        {"title": "Ocean Book", "description": "watr 4evr"},
        {"title": "Mountain Book", "description": "i luv 2 climb rocks"}
    ]

    # Extract title and description from each book in response
    actual_books = [{"title": book["title"], "description": book["description"]} for book in response_body]

    # Convert lists to sets of tuples for order-independent comparison
    assert set(tuple(book.items()) for book in actual_books) == set(tuple(book.items()) for book in expected_books)


def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_book(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

# When we have records and a `title` query in the request arguments, `get_all_books` returns a list containing only the `Book`s that match the query
def test_get_all_books_with_title_query_matching_none(client, two_saved_books):
    # Act
    data = {'title': 'Desert Book'}
    response = client.get("/books", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# When we have records and a `title` query in the request arguments, `get_all_books` returns a list containing only the `Book`s that match the query
def test_get_all_books_with_title_query_matching_one(client, two_saved_books):
    # Act
    data = {'title': 'Ocean Book'}
    response = client.get("/books", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0] == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }


def test_get_one_book_no_record(client):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "book 1 not found"}

# When we call `get_one_book` with a non-numeric ID, we get the expected error message
def test_get_one_book_invalid_id(client, two_saved_books):
    # Act
    response = client.get("/books/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "book cat invalid"}

def test_create_one_book(client):
    # Act
    response = client.post("/books", json={
        "title": "New Book",
        "description": "The Best!"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "New Book",
        "description": "The Best!"
    }

def test_create_one_book_no_title(client):
    # Arrange
    test_data = {"description": "The Best!"}

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'message': 'Invalid request: missing title'}

def test_create_one_book_no_description(client):
    # Arrange
    test_data = {"title": "New Book"}

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'message': 'Invalid request: missing description'}

def test_create_one_book_with_extra_keys(client):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "title": "New Book",
        "description": "The Best!",
        "another": "last value"
    }

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "New Book",
        "description": "The Best!"
    }