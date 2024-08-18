from ninja import Schema
from ninja.orm import create_schema
from .models import Sst, Sstuseranswer
from typing import List

SstSchema = create_schema(Sst)

class PostsstanswerSchema(Schema):
    question_id: int
    username: str
    sst_answer: str = None
    ro_answer: List[int] = None