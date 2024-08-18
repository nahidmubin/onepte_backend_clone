from ninja import Schema
from typing import List, Literal

class PostsstanswerSchema(Schema):
    question_id: int
    username: str
    sst_answer: str = None
    ro_answer: List[Literal[1, 2, 3, 4, 5]] = None
    mcq_answer: List[Literal['A', 'B', 'C', 'D', 'E']] = None