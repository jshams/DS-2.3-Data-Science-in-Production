from flask import Flask
from flask_restplus import Api, Resource, fields
from fast_3x3_solve import solve

app = Flask(__name__)
api = Api(app)

user_board = api.model('Board', {
    'board': fields.String('ex: 1, 2, 3, 4, 5, 6, 7, 8, 0')
})

current_board = None


@api.route('/solve')
class Solve(Resource):
    def clean(self, user_input):
        inp_without_spaces = user_input.replace(' ', '')
        to_arr = inp_without_spaces.split(',')
        try:
            num_list = [int(s) for s in to_arr]
        except ValueError:
            return None
        if len(num_list) != 9:
            return None
        if sorted(num_list) != [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            return None
        return tuple(tuple(num_list[i: i + 3]) for i in range(0, 7, 3))

    def get(self):
        global current_board
        if current_board is None:
            return None, 200
        return solve(current_board), 200

    @api.expect(user_board)
    def post(self):
        cleaned_input = self.clean(api.payload['board'])
        if cleaned_input is None:
            return None, 404
        else:
            global current_board
            current_board = cleaned_input


if __name__ == '__main__':
    app.run(debug=True)
