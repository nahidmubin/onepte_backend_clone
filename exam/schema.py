from ninja import Schema
from typing import List, Literal

class AnswerSchema(Schema):
    """AnswerSchema is a Schema to validate request for all type of Question i.e.
    Summarize Spoken Text (SST), Re-Order Paragraph(RO) and Reading Multiple
    Choice (Multiple) (RMMCQ). It includes a username field to relate the answer
    to a user."""
    
    question_id: int
    username: str
    sst_answer: str = None
    ro_answer: List[Literal[1, 2, 3, 4, 5]] = None
    mcq_answer: List[Literal['A', 'B', 'C', 'D', 'E']] = None