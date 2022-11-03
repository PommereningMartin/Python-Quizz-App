from flask import Flask, render_template, request
from service.category_service import CategoryService

app = Flask(__name__)
catService = CategoryService()


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html', categories=catService.get_categories())


@app.route('/question')
def question_for_category():
    category = request.args.get('category')
    question = catService.question(category)
    return render_template('question.html', category=category, question=question)


@app.route('/answer', methods=['POST'])
def check_answer():
    if request.method == 'POST':
        question_id = request.json.get('question')
        given_answer = request.json.get('answer')
        return {'answer': catService.check_answer(question_id, given_answer)}
    return {}


if __name__ == '__main__':
    app.run(debug=True)
