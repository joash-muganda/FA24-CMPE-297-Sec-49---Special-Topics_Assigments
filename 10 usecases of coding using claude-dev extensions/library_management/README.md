# Library Management System

## Overview

This Python module implements a simple library management system with classes for books and library operations. It provides functionality for adding, removing, searching, borrowing, and returning books in a library.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Module Structure](#module-structure)
4. [Classes](#classes)
5. [Exceptions](#exceptions)
6. [Functions](#functions)

## Installation

No additional installation is required beyond a standard Python environment (Python 3.7+).

## Usage

To use the Library Management System, import the necessary classes and create a `Library` instance:

```python
from optimized_library_management import Library, Book, BookStatus, BookNotFoundError, BookAlreadyExistsError

# Create a library
library = Library()

# Create and add books
book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "1234567890")
book2 = Book("To Kill a Mockingbird", "Harper Lee", "0987654321")

try:
    library.add_book(book1)
    library.add_book(book2)
except BookAlreadyExistsError as e:
    print(f"Error: {e}")

# Search for books
results = library.search_books("Gatsby")
library.display_search_results(results)

# Borrow and return books
try:
    library.borrow_book("1234567890")
    library.return_book("1234567890")
except BookNotFoundError as e:
    print(f"Error: {e}")
```

## Module Structure

The module consists of the following main components:

- `BookStatus`: An enumeration representing the status of a book.
- `Book`: A dataclass representing a book.
- `Library`: A class managing the collection of books and operations on them.
- Custom exceptions: `BookNotFoundError` and `BookAlreadyExistsError`.
- A `main()` function demonstrating the usage of the Library Management System.

## Classes

### BookStatus

An enumeration representing the status of a book in the library.

- `AVAILABLE`: The book is available for borrowing.
- `CHECKED_OUT`: The book has been borrowed and is not currently available.

### Book

Represents a book in the library.

Attributes:

- `title` (str): The title of the book.
- `author` (str): The author of the book.
- `isbn` (str): The ISBN (International Standard Book Number) of the book.
- `status` (BookStatus): The current status of the book (default is AVAILABLE).

Methods:

- `__str__()`: Returns a string representation of the book.

### Library

Represents a library and provides methods for managing books.

Methods:

- `__init__()`: Initializes an empty library with an OrderedDict to store books.
- `add_book(book: Book) -> None`: Adds a book to the library.
- `remove_book(isbn: str) -> None`: Removes a book from the library.
- `search_books(search_term: str) -> List[Book]`: Searches for books in the library based on a search term.
- `display_search_results(results: List[Book]) -> None`: Displays the search results.
- `borrow_book(isbn: str) -> None`: Marks a book as borrowed (checked out) in the library.
- `return_book(isbn: str) -> None`: Marks a book as returned (available) in the library.
- `_get_book(isbn: str) -> Book`: Retrieves a book from the library by its ISBN.

## Exceptions

### BookNotFoundError

Custom exception raised when a book is not found in the library.

### BookAlreadyExistsError

Custom exception raised when trying to add a book that already exists in the library.

## Functions

### main()

Main function demonstrating the usage of the Library Management System.

This function creates a sample library, adds books, performs searches, and demonstrates borrowing and returning books.

## Performance Optimizations

1. The `Book` class uses `__slots__` to reduce memory usage.
2. The `Library` class uses an `OrderedDict` to maintain insertion order of books.
3. The `search_books` method is decorated with `@lru_cache` to cache recent search results.
4. String comparisons in `search_books` use sets for faster lookups.

## Error Handling

The module uses custom exceptions (`BookNotFoundError` and `BookAlreadyExistsError`) to handle specific error cases. These exceptions are raised and caught in appropriate places to provide meaningful error messages to the user.

## Conclusion

This Library Management System provides a simple yet efficient way to manage a collection of books. It demonstrates the use of Python's data structures, enums, dataclasses, and error handling mechanisms to create a functional and optimized system.
