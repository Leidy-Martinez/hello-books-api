from flask import Blueprint

hello_world_bp = Blueprint("hello_world", __name__)

# #@hello_world_bp.get("/")
# def say_hello_world():
#     return "Hello, World!"

@hello_world_bp.get("/hello/JSON")
def say_hello_json():
    return {
        "name": "Ada Lovelace",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    }