import unittest
from optimized_library_management import Book, BookStatus, Library, BookNotFoundError, BookAlreadyExistsError

class TestLibraryManagement(unittest.TestCase):

    def setUp(self):
        self.library = Library()
        self.book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "1234567890")
        self.book2 = Book("To Kill a Mockingbird", "Harper Lee", "0987654321")

    def test_add_book(self):
        """Test adding a book to the library."""
        self.library.add_book(self.book1)
        self.assertIn(self.book1.isbn, self.library.books)
        self.assertEqual(self.library.books[self.book1.isbn], self.book1)

    def test_add_duplicate_book(self):
        """Test adding a duplicate book raises BookAlreadyExistsError."""
        self.library.add_book(self.book1)
        with self.assertRaises(BookAlreadyExistsError):
            self.library.add_book(self.book1)

    def test_remove_book(self):
        """Test removing a book from the library."""
        self.library.add_book(self.book1)
        self.library.remove_book(self.book1.isbn)
        self.assertNotIn(self.book1.isbn, self.library.books)

    def test_remove_nonexistent_book(self):
        """Test removing a non-existent book raises BookNotFoundError."""
        with self.assertRaises(BookNotFoundError):
            self.library.remove_book("nonexistent_isbn")

    def test_search_books(self):
        """Test searching for books by title or author."""
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        
        results = self.library.search_books("Gatsby")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.book1)

        results = self.library.search_books("Harper")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.book2)

        results = self.library.search_books("nonexistent")
        self.assertEqual(len(results), 0)

    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        self.library.add_book(self.book1)
        results = self.library.search_books("gatsby")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.book1)

    def test_borrow_book(self):
        """Test borrowing an available book."""
        self.library.add_book(self.book1)
        self.library.borrow_book(self.book1.isbn)
        self.assertEqual(self.book1.status, BookStatus.CHECKED_OUT)

    def test_borrow_unavailable_book(self):
        """Test borrowing an unavailable book."""
        self.library.add_book(self.book1)
        self.library.borrow_book(self.book1.isbn)
        self.library.borrow_book(self.book1.isbn)  # Try to borrow again
        self.assertEqual(self.book1.status, BookStatus.CHECKED_OUT)

    def test_borrow_nonexistent_book(self):
        """Test borrowing a non-existent book raises BookNotFoundError."""
        with self.assertRaises(BookNotFoundError):
            self.library.borrow_book("nonexistent_isbn")

    def test_return_book(self):
        """Test returning a borrowed book."""
        self.library.add_book(self.book1)
        self.library.borrow_book(self.book1.isbn)
        self.library.return_book(self.book1.isbn)
        self.assertEqual(self.book1.status, BookStatus.AVAILABLE)

    def test_return_available_book(self):
        """Test returning an already available book."""
        self.library.add_book(self.book1)
        self.library.return_book(self.book1.isbn)
        self.assertEqual(self.book1.status, BookStatus.AVAILABLE)

    def test_return_nonexistent_book(self):
        """Test returning a non-existent book raises BookNotFoundError."""
        with self.assertRaises(BookNotFoundError):
            self.library.return_book("nonexistent_isbn")

    def test_book_str_representation(self):
        """Test the string representation of a Book object."""
        expected_str = "The Great Gatsby by F. Scott Fitzgerald (ISBN: 1234567890) - Available"
        self.assertEqual(str(self.book1), expected_str)

    def test_library_with_multiple_books(self):
        """Test library operations with multiple books."""
        books = [
            Book("Book1", "Author1", "1111"),
            Book("Book2", "Author2", "2222"),
            Book("Book3", "Author3", "3333"),
        ]
        for book in books:
            self.library.add_book(book)
        
        self.assertEqual(len(self.library.books), 3)
        results = self.library.search_books("Book")
        self.assertEqual(len(results), 3)

    def test_search_books_caching(self):
        """Test that search results are cached."""
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)

        # Perform the same search twice
        results1 = self.library.search_books("Gatsby")
        results2 = self.library.search_books("Gatsby")

        # Check that the results are the same object (cached)
        self.assertIs(results1, results2)

if __name__ == '__main__':
    unittest.main()