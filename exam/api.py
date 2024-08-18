from ninja import NinjaAPI
from ninja import NinjaAPI
from .models import Sst, Sstuseranswer, User, Ro, Rouseranswer, Mcq, Mcquseranswer
from .schema import PostsstanswerSchema
import random
from django.shortcuts import get_object_or_404

api = NinjaAPI()

#get the questions
@api.get("/api")
def get_question(request, type: str = None, id: int = None):
    # Initializing an empty dictionary to add questions later on to return as JSON
    question_bank = {}

    if not id:
        if type == 'sst':
            questions = Sst.objects.all()
        elif type == 'ro':
            questions = Ro.objects.all()
        elif type == 'mcq':
            questions = Mcq.objects.all()
        else:
            return {'message': 'Please use proper "type" query in url'}
        
        for i, question in enumerate(questions):
            question_bank[i+1] = {
                'id': question.id,
                'title': question.title
            }
    else:
        if type == 'sst':
            question = get_object_or_404(Sst, id=id)

            question_bank['id'] = question.id
            question_bank['title'] = question.title
            question_bank['audio_male_voice'] = question.audio_male_voice.url
            question_bank['male_speaker_name'] = question.male_speaker_name
            question_bank['audio_female_voice'] = question.audio_female_voice.url
            question_bank['female_speaker_name'] = question.female_speaker_name

        elif type == 'ro':
            question = get_object_or_404(Ro, id=id)

            question_bank['id'] = question.id
            question_bank['title'] = question.title
            question_bank['paragraphs'] = question.paragraphs

        elif type == 'mcq':
            question = get_object_or_404(Mcq, id=id)

            question_bank['id'] = question.id
            question_bank['title'] = question.title
            question_bank['passage'] = question.passage
            question_bank['options'] = question.options

        else:
            return {'message': 'Please use proper "type" query in url'}
        
        

    return question_bank


# Receive and Process answer
@api.post("/api")
def receive_answer(request, type: str, submission: PostsstanswerSchema):
    if type == 'sst':
        question = get_object_or_404(Sst, id=submission.question_id)
        user = get_object_or_404(User, username=submission.username)
        content_score=random.randint(0,2)
        form_score=random.randint(0,2)
        grammar_score=random.randint(0,2)
        vocabulary_score=random.randint(0,2)
        spelling_score=random.randint(0,2)
        total_score= content_score + form_score + grammar_score + vocabulary_score + spelling_score

        user_answer = Sstuseranswer.objects.create(question=question, user=user, answer=submission.sst_answer,
                    content_score=content_score, form_score=form_score, grammar_score=grammar_score,
                    vocabulary_score= vocabulary_score, spelling_score=spelling_score, total_score=total_score)
        
        user_answer_dict = {
            'question_id': user_answer.question.id,
            'username': user_answer.user.username,
            'answer': user_answer.answer,
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
    
    elif type == 'ro':
        question = get_object_or_404(Ro, id=submission.question_id)
        user = get_object_or_404(User, username=submission.username)
        order = question.correct_order

        max_score = len(order) - 1
        answer = submission.ro_answer

        score = 0
        for i in range(len(answer)-1):
            if (order.index(answer[i+1]) - order.index(answer[i])) == 1:
                score += 1

        user_answer = Rouseranswer.objects.create(question=question, user=user,
                        answer=answer, score=score, max_score=max_score)
        
        user_answer_dict = {
            'question_id': user_answer.question.id,
            'username': user_answer.user.username,
            'answer': user_answer.answer,
            'score': user_answer.score,
            'max_score': user_answer.max_score
        }

    elif type == 'mcq':
        question = get_object_or_404(Mcq, id=submission.question_id)
        user = get_object_or_404(User, username=submission.username)
        correct_choice = question.correct_choice
        max_score = len(correct_choice)
        answer = submission.mcq_answer

        score = 0
        for choice in answer:
            if choice in correct_choice:
                score += 1
            else:
                score -= 1
        if score < 0:
            score = 0

        user_answer = Mcquseranswer.objects.create(question=question, user=user,
                        answer=answer, score=score, max_score=max_score)
        
        user_answer_dict = {
            'question_id': user_answer.question.id,
            'username': user_answer.user.username,
            'answer': user_answer.answer,
            'score': user_answer.score,
            'max_score': user_answer.max_score
        }

    else:
        return {'message': 'Please use proper "type" query in url'}

    return user_answer_dict



# Get all the answers of a user
@api.get("/api/answer")
def get_user_answer(request, type: str, username: str):
    user = get_object_or_404(User, username=username)
    if type == 'sst':
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
    
    elif type == 'ro' or type == 'mcq':

        if type == 'ro':
            answers = user.ro_answers_by_user.all()
        else:
            answers = user.mcq_answers_by_user.all()

        answer_dict = {}
        for answer in answers:
            answer_dict[answer.id] = {
                'question_id': answer.question.id,
                'question': answer.question.title,
                'answer': answer.answer,
                'score': answer.score,
                'max_score': answer.max_score
            }
    
    else:
        return {'message': 'Please use proper "type" query in url'}
    
    return answer_dict