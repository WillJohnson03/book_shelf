from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db 
from myapp.models import Book
from myapp.books.forms import BookForm

books = Blueprint('books', __name__)

@books.route('/create', methods=['GET', 'POST'])
@login_required
def add_book():
  form = BookForm()
  if form.validate_on_submit():
    book = Book(title=form.title.data, author=form.author.data, summary=form.summary.data, user_id=current_user.id)
    db.session.add(book)
    db.session.commit()
    flash('Book Added')
    print('Book was added')
    return redirect(url_for('core.index'))
  return render_template('add_book.html', form=form)
  

@books.route('/<int:book_id>')
def book(book_id):
  book = Book.query.get_or_404(book_id) 
  return render_template('book.html', title=book.title, date=book.date, book=book)

@books.route('/<int:book_id>/update', methods=['GET','POST'])
@login_required
def update(book_id):
  book = Book.query.get_or_404(book_id)

  if book.owner != current_user:
    abort(403)

  form = BookForm()

  if form.validate_on_submit():
    book.title = form.title.data
    book.author = form.author.data
    book.summary = form.summary.data
    db.session.commit()
    flash('Book Updated')
    return redirect(url_for('books.add_book',book_id=book.id))

  elif request.method == 'GET':
    form.title.data = book.title
    form.author.data = book.author
    form.summary.data = book.summary

  return render_template('add_book.html',title='Updating',form=form)

@books.route('/<int:book_id>/delete',methods=['GET','POST'])
@login_required
def delete_book(book_id):

    book = Book.query.get_or_404(book_id)
    if book.owner != current_user:
        abort(403)

    db.session.delete(book)
    db.session.commit()
    flash('Book Deleted')
    return redirect(url_for('core.index'))