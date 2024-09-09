# Library Management System
# This module implements a simple library management system with classes for books and library operations.

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

class BookStatus(Enum):
    """
    Enum representing the status of a book in the library.
    
    AVAILABLE: The book is available for borrowing.
    CHECKED_OUT: The book has been borrowed and is not currently available.
    """
    AVAILABLE = "Available"
    CHECKED_OUT = "Checked out"

@dataclass
class Book:
    """
    Represents a book in the library.
    
    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        isbn (str): The ISBN (International Standard Book Number) of the book.
        status (BookStatus): The current status of the book (default is AVAILABLE).
    """
    title: str
    author: str
    isbn: str
    status: BookStatus = BookStatus.AVAILABLE

    def __str__(self) -> str:
        """
        Returns a string representation of the book.
        
        Returns:
            str: A formatted string containing the book's title, author, ISBN, and status.
        """
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status.value}"

class BookNotFoundError(Exception):
    """
    Custom exception raised when a book is not found in the library.
    """
    pass

class BookAlreadyExistsError(Exception):
    """
    Custom exception raised when trying to add a book that already exists in the library.
    """
    pass

class Library:
    """
    Represents a library and provides methods for managing books.
    """

    def __init__(self):
        """
        Initializes an empty library with a dictionary to store books.
        """
        self.books: Dict[str, Book] = {}

    def add_book(self, book: Book) -> None:
        """
        Adds a book to the library.
        
        Args:
            book (Book): The book to add to the library.
        
        Raises:
            BookAlreadyExistsError: If a book with the same ISBN already exists in the library.
        """
        if book.isbn in self.books:
            raise BookAlreadyExistsError(f"Book with ISBN {book.isbn} already exists in the library.")
        self.books[book.isbn] = book
        print(f"Book '{book.title}' added to the library.")

    def remove_book(self, isbn: str) -> None:
        """
        Removes a book from the library.
        
        Args:
            isbn (str): The ISBN of the book to remove.
        
        Raises:
            BookNotFoundError: If the book with the given ISBN is not found in the library.
        """
        if isbn not in self.books:
            raise BookNotFoundError(f"Book with ISBN {isbn} not found in the library.")
        removed_book = self.books.pop(isbn)
        print(f"Book '{removed_book.title}' removed from the library.")

    def search_books(self, search_term: str) -> List[Book]:
        """
        Searches for books in the library based on a search term.
        
        Args:
            search_term (str): The term to search for in book titles and authors.
        
        Returns:
            List[Book]: A list of books matching the search term (case-insensitive).
        """
        results = [book for book in self.books.values() if search_term.lower() in book.title.lower() or search_term.lower() in book.author.lower()]
        return results

    def display_search_results(self, results: List[Book]) -> None:
        """
        Displays the search results.
        
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
        Marks a book as borrowed (checked out) in the library.
        
        Args:
            isbn (str): The ISBN of the book to borrow.
        
        Raises:
            BookNotFoundError: If the book with the given ISBN is not found in the library.
        """
        book = self._get_book(isbn)
        if book.status == BookStatus.AVAILABLE:
            book.status = BookStatus.CHECKED_OUT
            print(f"You have borrowed '{book.title}'.")
        else:
            print(f"Book '{book.title}' is not available.")

    def return_book(self, isbn: str) -> None:
        """
        Marks a book as returned (available) in the library.
        
        Args:
            isbn (str): The ISBN of the book to return.
        
        Raises:
            BookNotFoundError: If the book with the given ISBN is not found in the library.
        """
        book = self._get_book(isbn)
        if book.status == BookStatus.CHECKED_OUT:
            book.status = BookStatus.AVAILABLE
            print(f"You have returned '{book.title}'.")
        else:
            print(f"Book '{book.title}' was not checked out.")

    def _get_book(self, isbn: str) -> Book:
        """
        Retrieves a book from the library by its ISBN.
        
        Args:
            isbn (str): The ISBN of the book to retrieve.
        
        Returns:
            Book: The requested book.
        
        Raises:
            BookNotFoundError: If the book with the given ISBN is not found in the library.
        """
        book = self.books.get(isbn)
        if not book:
            raise BookNotFoundError(f"Book with ISBN {isbn} not found in the library.")
        return book

def main():
    """
    Main function demonstrating the usage of the Library Management System.
    """
    # Create a new library instance
    library = Library()

    # Create sample books
    book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "1234567890")
    book2 = Book("To Kill a Mockingbird", "Harper Lee", "0987654321")
    
    # Add books to the library
    try:
        library.add_book(book1)
        library.add_book(book2)
    except BookAlreadyExistsError as e:
        print(f"Error: {e}")

    # Search for books
    search_results = library.search_books("gatsby")
    library.display_search_results(search_results)

    # Borrow a book
    try:
        library.borrow_book("1234567890")
    except BookNotFoundError as e:
        print(f"Error: {e}")

    # Return a book
    try:
        library.return_book("1234567890")
    except BookNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()