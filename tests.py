import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

# 1 - Teste de unidade extra
def test_create_choice_with_invalid_text():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('', False)

    with pytest.raises(Exception):
        question.add_choice('a'*101, False)

    with pytest.raises(Exception):
        question.add_choice('a'*200, False)

# 2 Teste de unidade extra
def test_remove_choice():
    question = Question(title='q1')
    question.add_choice('a', False)
    
    question.remove_choice_by_id(1)
    
    assert len(question.choices) == 0

# 3 Teste de unidade extra
def test_remove_invalid_choice():
    question = Question(title='q1')
    question.add_choice('a', False)

    with pytest.raises(Exception):
        question.remove_choice_by_id(2)

# 4 Teste de unidade extra
def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)

    question.remove_all_choices()
    assert len(question.choices) == 0

# 5 Teste de unidade extra
def test_generate_choice_id():
    question = Question(title='q1')

    question.add_choice('a', False)
    question.add_choice('b', True)

    assert question.choices[0].id == 1
    assert question.choices[1].id == 2

# 6 Teste de unidade extra
def test_select_correct_choice():
    question = Question(title='q1', max_selections=1)
    question.add_choice('a', False)
    question.add_choice('b', True)

    selected_choice = question.select_choices([2])

    assert len(selected_choice) == 1
    assert selected_choice[0] == 2

# 7 Teste de unidade extra
def test_select_incorrect_choice():
    question = Question(title='q1', max_selections=1)
    question.add_choice('a', False)
    question.add_choice('b', True)

    selected_choice = question.select_choices([1])

    assert len(selected_choice) == 0

# 8 Teste de unidade extra
def test_select_multiple_choices():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', True)
    question.add_choice('b', False)
    question.add_choice('c', True)

    with pytest.raises(Exception):
        question.select_choices([1, 2, 3])

    selected_choices = question.select_choices([1, 3])

    assert len(selected_choices) == 2
    assert selected_choices[0] == 1
    assert selected_choices[1] == 3

# 9 Teste de unidade extra
def test_set_correct_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', False)

    question.set_correct_choices([2])

    assert not question.choices[0].is_correct
    assert question.choices[1].is_correct

# 10 Teste de unidade extra
def test_create_question_with_invalid_points():
    
    with pytest.raises(Exception):
        question = Question(title='q1', points=0)
    
    with pytest.raises(Exception):
        question = Question(title='q2', points=101)

@pytest.fixture
def pergunta_emb():
    question = Question(title='Qual é um avião da Embraer?', points=100, max_selections=1)
    question.add_choice('737-800 Max', False)
    question.add_choice('A350', False)
    question.add_choice('Praetor 600', True)
    question.add_choice('G550', False)
    return question

def test_select_correct_choice(pergunta_emb):
    selected_choices = pergunta_emb.select_choices([3])
    assert len(selected_choices) == 1
    assert selected_choices[0] == 3
    assert pergunta_emb.choices[2].is_correct

def test_select_more_than_max_choices(pergunta_emb):
    with pytest.raises(Exception):
        selected_choices = pergunta_emb.select_choices([1,2,3])
