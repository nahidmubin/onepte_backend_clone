from ninja import Schema
from ninja.orm import create_schema
from .models import Sst, Sstuseranswer

SstSchema = create_schema(Sst)

class PostsstanswerSchema(Schema):
    question_id: int
    username: str
    answer: str