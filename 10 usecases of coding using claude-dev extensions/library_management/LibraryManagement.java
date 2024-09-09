import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Library Management System
 * This class implements a simple library management system with classes for books and library operations.
 */
public class LibraryManagement {

    /**
     * Enum representing the status of a book in the library.
     */
    public enum BookStatus {
        AVAILABLE("Available"),
        CHECKED_OUT("Checked out");

        private final String value;

        BookStatus(String value) {
            this.value = value;
        }

        @Override
        public String toString() {
            return value;
        }
    }

    /**
     * Represents a book in the library.
     */
    public static class Book {
        private final String title;
        private final String author;
        private final String isbn;
        private BookStatus status;

        /**
         * Create a book.
         * @param title The title of the book.
         * @param author The author of the book.
         * @param isbn The ISBN (International Standard Book Number) of the book.
         */
        public Book(String title, String author, String isbn) {
            this(title, author, isbn, BookStatus.AVAILABLE);
        }

        /**
         * Create a book with a specified status.
         * @param title The title of the book.
         * @param author The author of the book.
         * @param isbn The ISBN (International Standard Book Number) of the book.
         * @param status The current status of the book.
         */
        public Book(String title, String author, String isbn, BookStatus status) {
            this.title = title;
            this.author = author;
            this.isbn = isbn;
            this.status = status;
        }

        @Override
        public String toString() {
            return String.format("%s by %s (ISBN: %s) - %s", title, author, isbn, status);
        }
    }

    /**
     * Custom exception for when a book is not found in the library.
     */
    public static class BookNotFoundException extends Exception {
        public BookNotFoundException(String message) {
            super(message);
        }
    }

    /**
     * Custom exception for when trying to add a book that already exists in the library.
     */
    public static class BookAlreadyExistsException extends Exception {
        public BookAlreadyExistsException(String message) {
            super(message);
        }
    }

    /**
     * Represents a library and provides methods for managing books.
     */
    public static class Library {
        private final Map<String, Book> books;

        /**
         * Create a library.
         */
        public Library() {
            this.books = new HashMap<>();
        }

        /**
         * Adds a book to the library.
         * @param book The book to add to the library.
         * @throws BookAlreadyExistsException If a book with the same ISBN already exists in the library.
         */
        public void addBook(Book book) throws BookAlreadyExistsException {
            if (books.containsKey(book.isbn)) {
                throw new BookAlreadyExistsException("Book with ISBN " + book.isbn + " already exists in the library.");
            }
            books.put(book.isbn, book);
            System.out.println("Book '" + book.title + "' added to the library.");
        }

        /**
         * Removes a book from the library.
         * @param isbn The ISBN of the book to remove.
         * @throws BookNotFoundException If the book with the given ISBN is not found in the library.
         */
        public void removeBook(String isbn) throws BookNotFoundException {
            Book removedBook = books.remove(isbn);
            if (removedBook == null) {
                throw new BookNotFoundException("Book with ISBN " + isbn + " not found in the library.");
            }
            System.out.println("Book '" + removedBook.title + "' removed from the library.");
        }

        /**
         * Searches for books in the library based on a search term.
         * @param searchTerm The term to search for in book titles and authors.
         * @return A list of books matching the search term (case-insensitive).
         */
        public List<Book> searchBooks(String searchTerm) {
            List<Book> results = new ArrayList<>();
            for (Book book : books.values()) {
                if (book.title.toLowerCase().contains(searchTerm.toLowerCase()) ||
                    book.author.toLowerCase().contains(searchTerm.toLowerCase())) {
                    results.add(book);
                }
            }
            return results;
        }

        /**
         * Displays the search results.
         * @param results The list of books to display.
         */
        public void displaySearchResults(List<Book> results) {
            if (!results.isEmpty()) {
                System.out.println("Search Results:");
                for (Book book : results) {
                    System.out.println(book);
                }
            } else {
                System.out.println("No books found.");
            }
        }

        /**
         * Marks a book as borrowed (checked out) in the library.
         * @param isbn The ISBN of the book to borrow.
         * @throws BookNotFoundException If the book with the given ISBN is not found in the library.
         */
        public void borrowBook(String isbn) throws BookNotFoundException {
            Book book = getBook(isbn);
            if (book.status == BookStatus.AVAILABLE) {
                book.status = BookStatus.CHECKED_OUT;
                System.out.println("You have borrowed '" + book.title + "'.");
            } else {
                System.out.println("Book '" + book.title + "' is not available.");
            }
        }

        /**
         * Marks a book as returned (available) in the library.
         * @param isbn The ISBN of the book to return.
         * @throws BookNotFoundException If the book with the given ISBN is not found in the library.
         */
        public void returnBook(String isbn) throws BookNotFoundException {
            Book book = getBook(isbn);
            if (book.status == BookStatus.CHECKED_OUT) {
                book.status = BookStatus.AVAILABLE;
                System.out.println("You have returned '" + book.title + "'.");
            } else {
                System.out.println("Book '" + book.title + "' was not checked out.");
            }
        }

        /**
         * Retrieves a book from the library by its ISBN.
         * @param isbn The ISBN of the book to retrieve.
         * @return The requested book.
         * @throws BookNotFoundException If the book with the given ISBN is not found in the library.
         */
        private Book getBook(String isbn) throws BookNotFoundException {
            Book book = books.get(isbn);
            if (book == null) {
                throw new BookNotFoundException("Book with ISBN " + isbn + " not found in the library.");
            }
            return book;
        }
    }

    /**
     * Main method demonstrating the usage of the Library Management System.
     * @param args Command line arguments (not used).
     */
    public static void main(String[] args) {
        // Create a new library instance
        Library library = new Library();

        // Create sample books
        Book book1 = new Book("The Great Gatsby", "F. Scott Fitzgerald", "1234567890");
        Book book2 = new Book("To Kill a Mockingbird", "Harper Lee", "0987654321");
        
        // Add books to the library
        try {
            library.addBook(book1);
            library.addBook(book2);
        } catch (BookAlreadyExistsException e) {
            System.out.println("Error: " + e.getMessage());
        }

        // Search for books
        List<Book> searchResults = library.searchBooks("gatsby");
        library.displaySearchResults(searchResults);

        // Borrow a book
        try {
            library.borrowBook("1234567890");
        } catch (BookNotFoundException e) {
            System.out.println("Error: " + e.getMessage());
        }

        // Return a book
        try {
            library.returnBook("1234567890");
        } catch (BookNotFoundException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}