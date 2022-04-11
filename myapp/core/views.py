from flask import render_template, request, Blueprint
from myapp.models import Book

core = Blueprint('core', __name__)

@core.route('/')
def index():
  page = request.args.get('page', 1, type=int)
  books = Book.query.order_by(Book.date.desc()).paginate(page=page, per_page=5)
  return render_template('index.html', books=books)

@core.route('/info')
def info():
  return render_template('info.html')