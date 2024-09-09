// Library Management System
// This module implements a simple library management system with classes for books and library operations.

/**
 * Enum representing the status of a book in the library.
 * @readonly
 * @enum {string}
 */
const BookStatus = {
  AVAILABLE: "Available",
  CHECKED_OUT: "Checked out",
};

/**
 * Represents a book in the library.
 */
class Book {
  /**
   * Create a book.
   * @param {string} title - The title of the book.
   * @param {string} author - The author of the book.
   * @param {string} isbn - The ISBN (International Standard Book Number) of the book.
   * @param {BookStatus} [status=BookStatus.AVAILABLE] - The current status of the book.
   */
  constructor(title, author, isbn, status = BookStatus.AVAILABLE) {
    this.title = title;
    this.author = author;
    this.isbn = isbn;
    this.status = status;
  }

  /**
   * Returns a string representation of the book.
   * @returns {string} A formatted string containing the book's title, author, ISBN, and status.
   */
  toString() {
    return `${this.title} by ${this.author} (ISBN: ${this.isbn}) - ${this.status}`;
  }
}

/**
 * Custom error for when a book is not found in the library.
 */
class BookNotFoundError extends Error {
  constructor(message) {
    super(message);
    this.name = "BookNotFoundError";
  }
}

/**
 * Custom error for when trying to add a book that already exists in the library.
 */
class BookAlreadyExistsError extends Error {
  constructor(message) {
    super(message);
    this.name = "BookAlreadyExistsError";
  }
}

/**
 * Represents a library and provides methods for managing books.
 */
class Library {
  /**
   * Create a library.
   */
  constructor() {
    this.books = {};
  }

  /**
   * Adds a book to the library.
   * @param {Book} book - The book to add to the library.
   * @throws {BookAlreadyExistsError} If a book with the same ISBN already exists in the library.
   */
  addBook(book) {
    if (this.books[book.isbn]) {
      throw new BookAlreadyExistsError(
        `Book with ISBN ${book.isbn} already exists in the library.`
      );
    }
    this.books[book.isbn] = book;
    console.log(`Book '${book.title}' added to the library.`);
  }

  /**
   * Removes a book from the library.
   * @param {string} isbn - The ISBN of the book to remove.
   * @throws {BookNotFoundError} If the book with the given ISBN is not found in the library.
   */
  removeBook(isbn) {
    if (!this.books[isbn]) {
      throw new BookNotFoundError(
        `Book with ISBN ${isbn} not found in the library.`
      );
    }
    const removedBook = this.books[isbn];
    delete this.books[isbn];
    console.log(`Book '${removedBook.title}' removed from the library.`);
  }

  /**
   * Searches for books in the library based on a search term.
   * @param {string} searchTerm - The term to search for in book titles and authors.
   * @returns {Book[]} An array of books matching the search term (case-insensitive).
   */
  searchBooks(searchTerm) {
    return Object.values(this.books).filter(
      (book) =>
        book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        book.author.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }

  /**
   * Displays the search results.
   * @param {Book[]} results - The array of books to display.
   */
  displaySearchResults(results) {
    if (results.length > 0) {
      console.log("Search Results:");
      results.forEach((book) => console.log(book.toString()));
    } else {
      console.log("No books found.");
    }
  }

  /**
   * Marks a book as borrowed (checked out) in the library.
   * @param {string} isbn - The ISBN of the book to borrow.
   * @throws {BookNotFoundError} If the book with the given ISBN is not found in the library.
   */
  borrowBook(isbn) {
    const book = this._getBook(isbn);
    if (book.status === BookStatus.AVAILABLE) {
      book.status = BookStatus.CHECKED_OUT;
      console.log(`You have borrowed '${book.title}'.`);
    } else {
      console.log(`Book '${book.title}' is not available.`);
    }
  }

  /**
   * Marks a book as returned (available) in the library.
   * @param {string} isbn - The ISBN of the book to return.
   * @throws {BookNotFoundError} If the book with the given ISBN is not found in the library.
   */
  returnBook(isbn) {
    const book = this._getBook(isbn);
    if (book.status === BookStatus.CHECKED_OUT) {
      book.status = BookStatus.AVAILABLE;
      console.log(`You have returned '${book.title}'.`);
    } else {
      console.log(`Book '${book.title}' was not checked out.`);
    }
  }

  /**
   * Retrieves a book from the library by its ISBN.
   * @param {string} isbn - The ISBN of the book to retrieve.
   * @returns {Book} The requested book.
   * @throws {BookNotFoundError} If the book with the given ISBN is not found in the library.
   * @private
   */
  _getBook(isbn) {
    const book = this.books[isbn];
    if (!book) {
      throw new BookNotFoundError(
        `Book with ISBN ${isbn} not found in the library.`
      );
    }
    return book;
  }
}

/**
 * Main function demonstrating the usage of the Library Management System.
 */
function main() {
  // Create a new library instance
  const library = new Library();

  // Create sample books
  const book1 = new Book(
    "The Great Gatsby",
    "F. Scott Fitzgerald",
    "1234567890"
  );
  const book2 = new Book("To Kill a Mockingbird", "Harper Lee", "0987654321");

  // Add books to the library
  try {
    library.addBook(book1);
    library.addBook(book2);
  } catch (e) {
    if (e instanceof BookAlreadyExistsError) {
      console.log(`Error: ${e.message}`);
    } else {
      throw e;
    }
  }

  // Search for books
  const searchResults = library.searchBooks("gatsby");
  library.displaySearchResults(searchResults);

  // Borrow a book
  try {
    library.borrowBook("1234567890");
  } catch (e) {
    if (e instanceof BookNotFoundError) {
      console.log(`Error: ${e.message}`);
    } else {
      throw e;
    }
  }

  // Return a book
  try {
    library.returnBook("1234567890");
  } catch (e) {
    if (e instanceof BookNotFoundError) {
      console.log(`Error: ${e.message}`);
    } else {
      throw e;
    }
  }
}

// Run the main function
main();
