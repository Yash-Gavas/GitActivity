from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

class Library:
    def __init__(self):
        self.books = []
        self.issued_books = {}
        self.load_data()

    def add_book(self, title, author):
        book = {"Title": title, "Author": author}
        self.books.append(book)
        self.save_data()

    def delete_book(self, title):
        for book in self.books:
            if book["Title"].lower() == title.lower():
                self.books.remove(book)
                self.save_data()
                return True
        return False

    def issue_book(self, title, usn):
        for book in self.books:
            if book["Title"].lower() == title.lower():
                if title in self.issued_books:
                    return "Book already issued."
                self.issued_books[title] = usn
                self.save_data()
                return "Book issued successfully."
        return "Book not found."

    def return_book(self, title):
        if title in self.issued_books:
            del self.issued_books[title]
            self.save_data()
            return "Book returned successfully."
        return "Book was not issued."

    def save_data(self):
        if not os.path.exists("data"):
            os.mkdir("data")
        with open("data/books.json", "w") as file:
            json.dump({"books": self.books, "issued_books": self.issued_books}, file)

    def load_data(self):
        if os.path.exists("data/books.json"):
            with open("data/books.json", "r") as file:
                try:
                    data = json.load(file)
                    self.books = data.get("books", [])
                    self.issued_books = data.get("issued_books", {})
                except json.JSONDecodeError:
                    self.books = []
                    self.issued_books = {}
        else:
            self.books = []
            self.issued_books = {}



library = Library()

@app.route('/')
def index():
    search_query = request.args.get('search', '')
    filtered_books = [book for book in library.books if search_query.lower() in book['Title'].lower()]
    return render_template('index.html', books=filtered_books, issued_books=library.issued_books, search_query=search_query)

@app.route('/add-book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    library.add_book(title, author)
    return redirect(url_for('index'))

@app.route('/delete-book/<title>', methods=['POST'])
def delete_book(title):
    library.delete_book(title)
    return redirect(url_for('index'))

@app.route('/issue-book', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        title = request.form.get('issue-title', '').strip()
        usn = request.form.get('usn', '').strip()
        if not title or not usn:
            result = "Invalid input. Please provide both Title and USN."
        else:
            result = library.issue_book(title, usn)
        return render_template('issue-book.html', result=result, books=library.books)
    return render_template('issue-book.html', books=library.books)

@app.route('/return-book', methods=['POST'])
def return_book():
    title = request.form['return-title']
    result = library.return_book(title)
    return redirect(url_for('index'))

@app.route('/issued-books')
def issued_books():
    try:
        app.logger.debug(f"Issued books data: {library.issued_books}")
        return render_template('issued-books.html', issued_books=library.issued_books)
    except Exception as e:
        app.logger.error(f"Error displaying issued books: {e}")
        return "An error occurred while displaying issued books", 500




if __name__ == '__main__':
    app.run(debug=True)
