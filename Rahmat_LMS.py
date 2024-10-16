from datetime import datetime, timedelta

# Define classes for User, Book, and Library System

class User:
    def __init__(self, user_id, name, email, user_type):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.user_type = user_type  # "member" or "admin"
        self.borrowed_books = []
    
    def borrow_book(self, book):
        if len(self.borrowed_books) < 5:  # Max 5 books can be borrowed
            book.borrow(self)
            self.borrowed_books.append((book, datetime.now() + timedelta(days=14)))  # Borrow for 14 days
            print(f"{self.name} borrowed {book.title}")
        else:
            print(f"{self.name} cannot borrow more than 5 books.")

    def return_book(self, book):
        for borrowed_book, due_date in self.borrowed_books:
            if borrowed_book == book:
                book.return_book()
                self.borrowed_books.remove((book, due_date))
                print(f"{self.name} returned {book.title}")
                break
        else:
            print(f"{self.name} does not have {book.title} borrowed.")

    def check_due_dates(self):
        for book, due_date in self.borrowed_books:
            if due_date < datetime.now():
                print(f"{book.title} is overdue!")
            else:
                print(f"{book.title} is due on {due_date.date()}")

class Book:
    def __init__(self, book_id, title, author, isbn, genre):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.borrowed_by = None

    def borrow(self, user):
        if self.borrowed_by is None:
            self.borrowed_by = user
            print(f"{self.title} is now borrowed by {user.name}")
        else:
            print(f"{self.title} is currently borrowed by {self.borrowed_by.name}")

    def return_book(self):
        if self.borrowed_by:
            print(f"{self.title} has been returned by {self.borrowed_by.name}")
            self.borrowed_by = None
        else:
            print(f"{self.title} is not currently borrowed.")

class LibrarySystem:
    def __init__(self):
        self.users = []
        self.books = []
    
    def add_user(self, name, email, user_type="member"):
        user_id = len(self.users) + 1
        user = User(user_id, name, email, user_type)
        self.users.append(user)
        print(f"User {name} added with ID {user_id}")

    def add_book(self, title, author, isbn, genre):
        book_id = len(self.books) + 1
        book = Book(book_id, title, author, isbn, genre)
        self.books.append(book)
        print(f"Book '{title}' added with ID {book_id}")

    def find_book(self, keyword):
        results = [book for book in self.books if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower()]
        if results:
            print(f"Books found for '{keyword}':")
            for book in results:
                print(f"{book.book_id}: {book.title} by {book.author}")
        else:
            print(f"No books found for '{keyword}'")

    def borrow_book(self, user_id, book_id):
        user = self.get_user_by_id(user_id)
        book = self.get_book_by_id(book_id)
        if user and book:
            user.borrow_book(book)

    def return_book(self, user_id, book_id):
        user = self.get_user_by_id(user_id)
        book = self.get_book_by_id(book_id)
        if user and book:
            user.return_book(book)

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        print(f"User with ID {user_id} not found")
        return None

    def get_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        print(f"Book with ID {book_id} not found")
        return None

    def check_overdue_books(self):
        print("Checking overdue books...")
        for user in self.users:
            user.check_due_dates()

# Interactive system to allow input from users
def main():
    # Initialize the library system
    library = LibrarySystem()

    while True:
        print("\nLibrary Management System")
        print("1. Add User")
        print("2. Add Book")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Search Book")
        print("6. Check Overdue Books")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            # Add User
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            user_type = input("Enter user type (member/admin): ").lower()
            library.add_user(name, email, user_type)
        
        elif choice == '2':
            # Add Book
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            isbn = input("Enter ISBN: ")
            genre = input("Enter genre: ")
            library.add_book(title, author, isbn, genre)
        
        elif choice == '3':
            # Borrow Book
            try:
                user_id = int(input("Enter user ID: "))
                book_id = int(input("Enter book ID: "))
                library.borrow_book(user_id, book_id)
            except ValueError:
                print("Please enter valid numeric IDs.")
        
        elif choice == '4':
            # Return Book
            try:
                user_id = int(input("Enter user ID: "))
                book_id = int(input("Enter book ID: "))
                library.return_book(user_id, book_id)
            except ValueError:
                print("Please enter valid numeric IDs.")
        
        elif choice == '5':
            # Search Book
            keyword = input("Enter keyword to search for books (title/author): ")
            library.find_book(keyword)
        
        elif choice == '6':
            # Check Overdue Books
            library.check_overdue_books()
        
        elif choice == '7':
            # Exit
            print("Exiting the system...")
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
