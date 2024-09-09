class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True

    def __str__(self):
        status = "Available" if self.is_available else "Checked out"
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {status}"


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Book '{book.title}' added to the library.")

    def remove_book(self, isbn):
        book_to_remove = next((book for book in self.books if book.isbn == isbn), None)
        if book_to_remove:
            self.books.remove(book_to_remove)
            print(f"Book '{book_to_remove.title}' removed from the library.")
        else:
            print("Book not found.")

    def search_books(self, search_term):
        results = [book for book in self.books if search_term.lower() in book.title.lower() or search_term.lower() in book.author.lower()]
        if results:
            print("Search Results:")
            for book in results:
                print(book)
        else:
            print("No books found.")

    def borrow_book(self, isbn):
        book_to_borrow = next((book for book in self.books if book.isbn == isbn and book.is_available), None)
        if book_to_borrow:
            book_to_borrow.is_available = False
            print(f"You have borrowed '{book_to_borrow.title}'.")
        else:
            print("Book is not available or not found.")

    def return_book(self, isbn):
        book_to_return = next((book for book in self.books if book.isbn == isbn), None)
        if book_to_return:
            book_to_return.is_available = True
            print(f"You have returned '{book_to_return.title}'.")
        else:
            print("Book not found.")

if __name__ == "__main__":
    # Sample usage of the Library system
    library = Library()

    # Adding books
    book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "1234567890")
    book2 = Book("To Kill a Mockingbird", "Harper Lee", "0987654321")
    library.add_book(book1)
    library.add_book(book2)

    # Searching for books
    library.search_books("gatsby")

    # Borrowing a book
    library.borrow_book("1234567890")

    # Returning a book
    library.return_book("1234567890")
