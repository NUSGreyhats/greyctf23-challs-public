import os

from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, flash
from stackVM import StackVM
from flask_sqlalchemy import SQLAlchemy
from functools import cache


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
FLAG = os.environ.get('FLAG', 'grey{test_flag}')


@cache
def fib(n):
    curr, next = 0, 1
    for _ in range(n):
        curr, next = next, curr + next
    return curr


# Test case for fib
test_cases = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40,
              45, 50, 55, 60, 75, 90, 100, 150, 200, 250, 300, 350, 400, 450, 500,
              550, 555, 560]

teams = sorted([
    "u0K++",
    "NUSHmallows",
    "ItzyBitzySpider",
    "MATE",
    "youtiaos",
    "no rev/pwn no life",
    "Social Engineering Experts",
    "DiceGang",
    "Team berries",
    "Penguin",
    "idek",
    "ヨミビトシラズ",
    "VMP",
    "🦈 SLIGHT_SHARK 🙂",
    "r3kapig",
    "purf3ct",
    "NUS Greyhats",
])


class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(), nullable=False)
    passed = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    execution_len = db.Column(db.Integer, nullable=False)

    def __lt__(self, other):
        """Sorts by cases passed first, then by code length"""
        if self.passed == other.passed:
            return self.length < other.length
        return self.passed > other.passed

    def __eq__(self, other):
        """Check if name, passed, code and score are the same"""
        return self.name == other.name and self.passed == other.passed and self.code == other.code and self.length == other.score

    def __repr__(self):
        return f"Score({self.name}, {self.code}, {self.passed}, {self.length})"


def init_store() -> None:
    """Initialize the db with all teams"""
    with app.app_context():
        db.create_all()
        # Add all teams to the db
        for team in teams:
            db.session.add(
                Score(name=team, code='', passed=0, length=0, execution_len=0)
            )
        db.session.commit()


def store_result(score: Score) -> None:
    """Store the score for the team"""
    db.session.add(score)
    db.session.commit()


def get_scores() -> list:
    """Get the max score for all teams"""
    scores = []
    for team in teams:
        # Get max score for each team (passed first followed by min length)
        score = Score.query.filter_by(name=team).order_by(
            Score.passed.desc(),
            Score.length.asc(),
            Score.execution_len.asc(),
        ).first()
        scores.append(score)
    return sorted(scores)


def ExecuteCode(name: str, code: str) -> Score:
    """Execute the code for the stack VM and return the top stack element"""
    passed = 0
    exec_len = 0
    bytecode = StackVM.compile(code)
    for arg in test_cases:
        res = fib(arg)
        vm = StackVM()
        result = vm.run(bytecode, [arg])
        if result == res:
            passed += 1
        exec_len += vm.line_execution
    return Score(name=name, code=code, passed=passed, length=len(bytecode), execution_len=exec_len)


@app.route('/')
def index() -> Response:
    # Get the scores from each team and sort them
    scores = get_scores()
    scores.sort()
    return render_template(
        'index.html',
        scores=scores,
        teams=teams,
        total_tests=len(test_cases)
    )


@app.route('/api/stackvm', methods=['POST'])
def stackvm() -> Response:
    if request.method != 'POST':
        return jsonify({'error': 'Invalid request method'}), 405

    data = request.form
    if 'code' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    code = data.get('code', None)
    name = data.get('name', None)
    if None in [code, name]:
        return jsonify({'error': 'Invalid request'}), 400

    if name not in teams:
        return jsonify({'error': 'Invalid team name'}), 400

    code = code.strip()
    if not code:
        return jsonify({'error': 'Invalid request'}), 400

    test_results = ExecuteCode(name, code)
    store_result(test_results)
    flash(f'Passed {test_results.passed} tests', 'success')
    if test_results.passed >= len(test_cases):
        flash(f'Congratulations! You have passed all test cases, here is your solve flag: {FLAG}', 'success')

    return redirect(url_for('index'))


init_store()
if __name__ == '__main__':
    app.run(debug=True)
