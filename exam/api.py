from ninja import NinjaAPI
from .models import Sst, Sstanswer, User, Ro, Roanswer, Mcq, Mcqanswer
from .schema import AnswerSchema
import random
from django.shortcuts import get_object_or_404

#generate ninjaApi object to create apis.
api = NinjaAPI()

#Endpoint to retrieve question
@api.get("/api")
def get_question(request, type: str = None, id: int = None):
    """This function returns questions depending on the 'type' and 'id' query
    parameter. If no value is provided for id and value of type is given then it
    returns all the questions of that specific type with questions's 'id and
    'title' Only. If there is a value for 'id' along with its type, the function
    returns the details of the question of that id."""

    # Initializing an empty dictionary to add questions later on to return as JSON
    question_bank = {}

    # If no id provided, return all the questions of the provided 'type'
    if not id:
        if type == 'sst':
            questions = Sst.objects.all()
        elif type == 'ro':
            questions = Ro.objects.all()
        elif type == 'mcq':
            questions = Mcq.objects.all()
        #Return error message if correct 'type' isn't provided
        else:
            return {'message': "Please use proper 'type' query in url"}
        
        # Unpacking the questions and adding to the question_bank dict
        for i, question in enumerate(questions):
            question_bank[i+1] = {
                'id': question.id,
                'title': question.title
            }

    # id is provided. Return details pf question of that id with the given type.
    else:
        if type == 'sst':
            # if there is no question of the provided id, return an error message
            question = get_object_or_404(Sst, id=id)
            #if question found, unpack it and add to the question_bank dict
            question_bank['id'] = question.id
            question_bank['title'] = question.title
            question_bank['audio_male_voice'] = question.audio_male_voice.url
            question_bank['male_speaker_name'] = question.male_speaker_name
            question_bank['audio_female_voice'] = question.audio_female_voice.url
            question_bank['female_speaker_name'] = question.female_speaker_name

        elif type == 'ro':
            # if there is no question of the provided id, return an error message
            question = get_object_or_404(Ro, id=id)
            #if question found, unpack it and add to the question_bank dict
            question_bank['id'] = question.id
            question_bank['title'] = question.title
            question_bank['paragraphs'] = question.paragraphs

        elif type == 'mcq':
            # if there is no question of the provided id, return an error message
            question = get_object_or_404(Mcq, id=id)
            #if question found, unpack it and add to the question_bank dict
            question_bank['id'] = question.id
            question_bank['title'] = question.title
            question_bank['passage'] = question.passage
            question_bank['options'] = question.options

        #Return error message if correct 'type' isn't provided
        else:
            return {'message': "Please use proper 'type' query in url"}

    # Finally return the questions as dictionary which will be serialized and send as JSON
    return question_bank


#Endpoint to submit answer
@api.post("/api")
def submit_answer(request, type: str, submission: AnswerSchema):
    """This function receives answer, relates it with the question of provided
    'type' and a user, generates score. It receives data as 'submission' parameter
    validates with AnswerSchema."""

    # Check the type parameter and relate the answer to the correct type of question
    if type == 'sst':
        # if there is no question and user of the provided ids, return an error message
        question = get_object_or_404(Sst, id=submission.question_id)
        user = get_object_or_404(User, username=submission.username)
        #generate random score for the components
        content_score=random.randint(0,2)
        form_score=random.randint(0,2)
        grammar_score=random.randint(0,2)
        vocabulary_score=random.randint(0,2)
        spelling_score=random.randint(0,2)
        #total score is the sum of the component score
        total_score= content_score + form_score + grammar_score + vocabulary_score + spelling_score

        # Generate tha Sstanswer object to save it in the database
        user_answer = Sstanswer.objects.create(question=question, user=user, answer=submission.sst_answer,
                    content_score=content_score, form_score=form_score, grammar_score=grammar_score,
                    vocabulary_score= vocabulary_score, spelling_score=spelling_score, total_score=total_score)
        
        # unpack the created answer object and to add to a dict to return as JSON
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
        # if there is no question and user of the provided ids, return an error message
        question = get_object_or_404(Ro, id=submission.question_id)
        user = get_object_or_404(User, username=submission.username)
        #Maximum score is the number of correct pair of order i.e. number of orders - 1
        order = question.correct_order
        max_score = len(order) - 1

        answer = submission.ro_answer

        # Check for correct pairs of order and generate score
        score = 0
        for i in range(len(answer)-1):
            if (order.index(answer[i+1]) - order.index(answer[i])) == 1:
                score += 1

        # Generate tha Roanswer object to save it in the database
        user_answer = Roanswer.objects.create(question=question, user=user,
                        answer=answer, score=score, max_score=max_score)
        
        # unpack the created answer object and to add to a dict to return as JSON
        user_answer_dict = {
            'question_id': user_answer.question.id,
            'username': user_answer.user.username,
            'answer': user_answer.answer,
            'score': user_answer.score,
            'max_score': user_answer.max_score
        }

    elif type == 'mcq':
        # if there is no question and user of the provided ids, return an error message
        question = get_object_or_404(Mcq, id=submission.question_id)
        user = get_object_or_404(User, username=submission.username)
        #Maximum score is the number of total possible correct choices
        correct_choice = question.correct_choice
        max_score = len(correct_choice)

        answer = submission.mcq_answer
        # Check for correct choices and generate score
        score = 0
        for choice in answer:
            if choice in correct_choice:
                score += 1
            else:
                score -= 1
        # if score becomes negative, make it 0. As minimum score is 0.
        if score < 0:
            score = 0

        # Generate tha Mcqanswer object to save it in the database
        user_answer = Mcqanswer.objects.create(question=question, user=user,
                        answer=answer, score=score, max_score=max_score)
        
        # unpack the created answer object and to add to a dict to return as JSON
        user_answer_dict = {
            'question_id': user_answer.question.id,
            'username': user_answer.user.username,
            'answer': user_answer.answer,
            'score': user_answer.score,
            'max_score': user_answer.max_score
        }
    
    
    #Return error message if correct 'type' isn't provided
    else:
        return {'message': 'Please use proper "type" query in url'}

    # Return the submitted answer
    return user_answer_dict



# Get all the answers of a user
@api.get("/api/answer")
def get_user_answer(request, type: str, username: str):
    """This functions returns all the answer submitted by a user and the scores
    for a particular question type. The function takes 'username' parameter to
    get the the user and 'type' parameter to get the type."""

    # if there is no user of the provided username, return an error message
    user = get_object_or_404(User, username=username)
    if type == 'sst':
        # Get all the answer of the provided type
        answers = user.sst_answers_by_user.all()

        answer_dict = {}
        for i, answer in enumerate(answers):
            # Unpack each answer and add to the answer_dict to return it as JSON later on
            answer_dict[i] = {
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
        # Get all the answer of the provided type
        if type == 'ro':
            answers = user.ro_answers_by_user.all()
        else:
            answers = user.mcq_answers_by_user.all()

        answer_dict = {}
        for answer in answers:
            # Unpack each answer and add to the answer_dict to return it as JSON later on
            answer_dict[answer.id] = {
                'question_id': answer.question.id,
                'question': answer.question.title,
                'answer': answer.answer,
                'score': answer.score,
                'max_score': answer.max_score
            }
    
    #Return error message if correct 'type' isn't provided
    else:
        return {'message': 'Please use proper "type" query in url'}
    
    # Return all the answers
    return answer_dict