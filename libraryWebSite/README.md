# ASP .NET MVC Project - Library Management System

## Project Overview
The Library Management System is a console application designed to manage books in a library. The application offers core functionalities such as adding new books, removing existing books, searching for books based on specific criteria, and listing all books in the library. This project is an exercise in object-oriented programming (OOP), simple data structures, and search algorithms.

The goal of this project is to create a simple, user-friendly console-based application for efficient book management. It is ideal as a prototype for managing a small library or an individual’s book collection.

---

## Features

### 1. Add Book
- Allows users to input the book's name, author, and publication year.
- Adds the book to the library as a `Book` object.

### 2. Remove Book
- Removes a book from the library based on its name.

### 3. Search by Name
- Searches for books in the library by their name.

### 4. Search by Author
- Searches for books in the library by their author.

### 5. List All Books
- Displays a list of all books currently in the library.

---

## Technical Details

### Object-Oriented Programming (OOP)
The system uses OOP principles to represent data as objects and implement modular functionalities.

#### Classes:
1. **Book Class**
   - Represents individual books.
   - **Attributes:**
     - `name`: The name of the book.
     - `author`: The author of the book.
     - `year`: The publication year of the book.

2. **Library Class**
   - Manages the collection of books and provides core functionalities.
   - **Attributes:**
     - `books`: A list containing all the books in the library.
   - **Methods:**
     - `addBooks`: Adds a new book to the library.
     - `removeBooks`: Removes a book from the library by name.
     - `searchByName`: Searches for books by their name.
     - `searchByAuthor`: Searches for books by their author.
     - `listBooks`: Lists all books in the library.

### Data Structures and Algorithms
- **List Data Structure:**
  - Books are stored in a Python list (`self.books`).
  - Each book is represented as a `Book` object within the list.
- **Search Algorithm:**
  - Used for searching books by name or author.

---

## Usage Scenarios

### Adding a Book
The user provides the name, author, and publication year of the book. The `addBooks` function converts this data into a `Book` object and adds it to the library's list of books.

### Removing a Book
The user specifies the name of the book they wish to remove. The `removeBooks` function searches the library’s book list for the matching name and removes the corresponding book.

### Searching for Books
- **By Name:** The user enters the name of the book. The `searchByName` function searches the list and displays matching results.
- **By Author:** The user enters the author’s name. The `searchByAuthor` function searches the list and displays books written by the specified author.

### Listing All Books
The `listBooks` function iterates through the library's book list and displays the details of each book in a user-friendly format.

---

## Project Requirements

### Development Environment
- **Language:** C#

### Functional Requirements
- The system must use OOP principles.
- Books must be stored in a list structure.
- Search functionalities must utilize a linear search algorithm.

---

## Future Improvements
- Implement a graphical user interface (GUI) for better user experience.
- Add persistent storage using a database or file system to save and load books.
- Improve search efficiency by implementing more advanced algorithms (e.g., binary search).

---

## How to Run
1. Clone the repository.
2. Ensure Visual Studio is installed on your system.
3. Run the `library_otomation.snl` in Visual Studio.

---

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

