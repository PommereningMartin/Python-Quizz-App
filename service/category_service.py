class CategoryService(object):
    categories = {
        'TECHNIK': 'Technik',
        'WIRTSCHAFT': 'Wirtschaft',
        'POLITIK': 'Politik',
        'KUNST': 'Kunst',
    }
    questions = [
        {
            'id': 1,
            'cat': 'TECHNIK',
            'text': 'Wieviel ist 1+1?',
            'possibleAnswers': ['0', '1', '2', '3'],
            'correctAnswer': '2'},
        {
            'id': 2,
            'cat': 'TECHNIK',
            'text': 'Wieviel ist 1+2?',
            'possibleAnswers': ['0', '1', '2', '3'],
            'correctAnswer': '3'},
        {
            'id': 3,
            'cat': 'TECHNIK',
            'text': 'Wieviel ist 1+3?',
            'possibleAnswers': ['1', '2', '3', '4'],
            'correctAnswer': '4'},
    ]

    def __init__(self):
        pass

    def get_categories(self):
        return self.categories

    def question(self, category):
        for question in self.questions:
            for key in question:
                if question['cat'] == category:
                    return question

    def check_answer(self, question_id, given_answer):
        for question in self.questions:
            if question.get('id') == question_id:
                return question.get('correctAnswer') == given_answer
