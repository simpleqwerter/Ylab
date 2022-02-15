import base64
from io import StringIO, BytesIO

import flask
import matplotlib
matplotlib.use('Agg')

from forms import SquareForm
from figures import Square
import matplotlib.pyplot as plt
app = flask.Flask(__name__)




@app.route("/2dfigure/square", methods=['POST', 'GET'])
def square():
    if flask.request.method == 'POST':
        form = SquareForm()
        # if form.validate_on_submit():
        side = form.side.data
        square = form.square.data
        diagonal = form.diagonal.data
        r = form.r.data
        R = form.R.data
        perimetr = form.perimetr.data
        sq = Square(side=side, square=square, diagonal=diagonal, r=r, R=R, perimetr=perimetr)
        try:
            sq.calc()
            rectangle = plt.Rectangle((10, 10), width=sq.side, height=sq.side, fc='r', edgecolor='black')
            plt.gca().add_patch(rectangle)
            plt.axis('scaled')
            img = BytesIO()
            plt.savefig(img)
            img.seek(0)
            return flask.send_file(img,  mimetype='image/png')
        except BaseException as err:
            return f"square error is {err} | Invalid input, {form.errors}", 400
    form = SquareForm()
    return flask.render_template('question.html', form=form)


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = True
    app.config['SECRET_KEY'] = 'a really really really really long secret key'
    app.run(debug=True)