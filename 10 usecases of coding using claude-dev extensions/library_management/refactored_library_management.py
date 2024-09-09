from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

class BookStatus(Enum):
    AVAILABLE = "Available"
    CHECKED_OUT = "Checked out"

@dataclass
class Book:
    title: str
    author: str
    isbn: str
    status: BookStatus = BookStatus.AVAILABLE

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status.value}"

class BookNotFoundError(Exception):
    """Raised when a book is not found in the library."""
    pass

class BookAlreadyExistsError(Exception):
    """Raised when trying to add a book that already exists in the library."""
    pass

class Library:
    def __init__(self):
        self.books: Dict[str, Book] = {}

    def add_book(self, book: Book) -> None:
        """
        Add a book to the library.
        
        Args:
            book (Book): The book to add.
        
        Raises:
            BookAlreadyExistsError: If the book already exists in the library.
        """
        if book.isbn in self.books:
            raise BookAlreadyExistsError(f"Book with ISBN {book.isbn} already exists in the library.")
        self.books[book.isbn] = book
        print(f"Book '{book.title}' added to the library.")

    def remove_book(self, isbn: str) -> None:
        """
        Remove a book from the library.
        
        Args:
            isbn (str): The ISBN of the book to remove.
        
        Raises:
            BookNotFoundError: If the book is not found in the library.
        """
        if isbn not in self.books:
            raise BookNotFoundError(f"Book with ISBN {isbn} not found in the library.")
        removed_book = self.books.pop(isbn)
        print(f"Book '{removed_book.title}' removed from the library.")

    def search_books(self, search_term: str) -> List[Book]:
        """
        Search for books in the library.
        
        Args:
            search_term (str): The term to search for in book titles and authors.
        
        Returns:
            List[Book]: A list of books matching the search term.
        """
        results = [book for book in self.books.values() if search_term.lower() in book.title.lower() or search_term.lower() in book.author.lower()]
        return results

    def display_search_results(self, results: List[Book]) -> None:
        """
        Display search results.
        
        Args:
            results (List[Book]): The list of books to display.
        """
        if results:
            print("Search Results:")
            for book in results:
                print(book)
        else:
            print("No books found.")

    def borrow_book(self, isbn: str) -> None:
        """
        Borrow a book from the library.
        
        Args:
            isbn (str): The ISBN of the book to borrow.
        
        Raises:
            BookNotFoundError: If the book is not found in the library.
        """
        book = self._get_book(isbn)
        if book.status == BookStatus.AVAILABLE:
            book.status = BookStatus.CHECKED_OUT
            print(f"You have borrowed '{book.title}'.")
        else:
            print(f"Book '{book.title}' is not available.")

    def return_book(self, isbn: str) -> None:
        """
        Return a book to the library.
        
        Args:
            isbn (str): The ISBN of the book to return.
        
        Raises:
            BookNotFoundError: If the book is not found in the library.
        """
        book = self._get_book(isbn)
        if book.status == BookStatus.CHECKED_OUT:
            book.status = BookStatus.AVAILABLE
            print(f"You have returned '{book.title}'.")
        else:
            print(f"Book '{book.title}' was not checked out.")

    def _get_book(self, isbn: str) -> Book:
        """
        Get a book from the library by ISBN.
        
        Args:
            isbn (str): The ISBN of the book to retrieve.
        
        Returns:
            Book: The requested book.
        
        Raises:
            BookNotFoundError: If the book is not found in the library.
        """
        book = self.books.get(isbn)
        if not book:
            raise BookNotFoundError(f"Book with ISBN {isbn} not found in the library.")
        return book

def main():
    # Sample usage of the Library system
    library = Library()

    # Adding books
    book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "1234567890")
    book2 = Book("To Kill a Mockingbird", "Harper Lee", "0987654321")
    
    try:
        library.add_book(book1)
        library.add_book(book2)
    except BookAlreadyExistsError as e:
        print(f"Error: {e}")

    # Searching for books
    search_results = library.search_books("gatsby")
    library.display_search_results(search_results)

    # Borrowing a book
    try:
        library.borrow_book("1234567890")
    except BookNotFoundError as e:
        print(f"Error: {e}")

    # Returning a book
    try:
        library.return_book("1234567890")
    except BookNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()