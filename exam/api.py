from ninja import NinjaAPI
from ninja import NinjaAPI
from .models import Sst, Sstuseranswer, User
from .schema import PostsstanswerSchema
import random
from django.shortcuts import get_object_or_404

api = NinjaAPI()

#get the sst type question datas
@api.get("/api")
def get_sst(request, type: str = None):
    # Initializing an empty dictionary to add questions later on to return as JSON
    q_dict = {}

    # Checking if the user wants to get the SST type question
    if type == 'sst':
        questions = Sst.objects.all()
    
        for question in questions:
            q_dict[question.id] = {
                'id': question.id,
                'title': question.title,
                'audio_male_voice': question.audio_male_voice.url,
                'male_speaker_name': question.male_speaker_name,
                'audio_female_voice': question.audio_female_voice.url,
                'female_speaker_name': question.female_speaker_name
            }
    else:
        return {'message': 'Please use proper "type" query in url'}


    return q_dict


# Receive and Process answer
@api.post("/api")
def receive_answer(request, type: str, sstanswer: PostsstanswerSchema):
    if type == 'sst':
        question = get_object_or_404(Sst, id=sstanswer.question_id)
        user = get_object_or_404(User, username=sstanswer.username)
        content_score=random.randint(0,2)
        form_score=random.randint(0,2)
        grammar_score=random.randint(0,2)
        vocabulary_score=random.randint(0,2)
        spelling_score=random.randint(0,2)
        total_score= content_score + form_score + grammar_score + vocabulary_score + spelling_score

        user_answer = Sstuseranswer.objects.create(question=question, user=user, answer=sstanswer.answer,
                    content_score=content_score, form_score=form_score, grammar_score=grammar_score,
                    vocabulary_score= vocabulary_score, spelling_score=spelling_score, total_score=total_score)
        
        user_answer_dict = {
            'question_id': user_answer.question.id,
            'username': user_answer.user.username,
            'content_score': user_answer.content_score,
            'max_content_score': 2,
            'form_score': user_answer.form_score,
            'max_form_score': 2,
            'grammar_score': user_answer.grammar_score,
            'max_grammar_score': 2,
            'vocabulary_score': user_answer.vocabulary_score,
            'max_vocabulary_score': 2,
            'spelling_score': user_answer.spelling_score,
            'max_spelling_score': 2,
            'total_score': user_answer.total_score,
            'max_total_score': 10
        }
        return user_answer_dict
    
    else:
        return {'message': 'Please use proper "type" query in url'}
    

# Get all the answers of a user
@api.get("/api/answer")
def get_user_answer(request, type: str, username: str):
    if type == 'sst':
        user = get_object_or_404(User, username=username)
        answers = user.sst_answers_by_user.all()

        answer_dict = {}
        for answer in answers:
            answer_dict[answer.id] = {
                'question_id': answer.question.id,
                'question' : answer.question.title,
                'answer' : answer.answer,
                'content_score': answer.content_score,
                'max_content_score': 2,
                'form_score': answer.form_score,
                'max_form_score': 2,
                'grammar_score': answer.grammar_score,
                'max_grammar_score': 2,
                'vocabulary_score': answer.vocabulary_score,
                'max_vocabulary_score': 2,
                'spelling_score': answer.spelling_score,
                'max_spelling_score': 2,
                'total_score': answer.total_score,
                'max_total_score': 10
            }
        return answer_dict
    
    else:
        return {'message': 'Please use proper "type" query in url'}