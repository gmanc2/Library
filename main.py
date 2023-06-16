import csv #import csv to handle csvs
import colorama #import colorma incase its not installed in my instance I preinstalled with conda
from colorama import Fore, Style, init #from colorama import

init() # Initialize Colorama instance


class Book:  # create a class for the Book object so we don't have to worry about defining the book dictionary multiple times
    def __init__(self, isbn13, isbn10, author, genre, publisher, pub_year,
                 book_type, title):  # constructor method to initialize a Book object with its properties
        self.isbn13 = isbn13 # add the isbn13 property
        self.isbn10 = isbn10 # add the isbn10 property
        self.author = author # add the author property
        self.genre = genre # add the genre property
        self.publisher = publisher # add the publisher
        self.pub_year = pub_year #  add the publisher_year property
        self.book_type = book_type # add the book_type property
        self.title = title # add the title property

    def __str__(self):  # define pretty string representation using builtins.pyi
        return f"{self.title} by {self.author} ({self.pub_year}) - ISBN-13: {self.isbn13}, ISBN-10: {self.isbn10}, Genre: {self.genre}, Publisher: {self.publisher}, Type: {self.book_type}"


def add_book_dictionary(library, book): # add book to the dictionary called Library.
    library[book.title] = book
    print(f"Book '{book.title}' has been added to the library if not already present.") # by defualt won't add book with the exact same values also handled in manual_input


def add_book_to_file(library, book): # add book to file mostly for manual input if the user wants to make and use their own libarary book collection rather than using a presupplied one. Also for adding books read into the dictionary.
    with open("books.txt", "r") as file: # Open file with read permissions
        for line in file: #search the lines in the file
            if line.strip().split(',')[7] == book.title: # search after 7th comma for book title.
                print(f"Book '{book.title}' already exists in the file.")
                return
            elif line.strip().split(',')[0] == book.isbn13 or line.strip().split(',')[1] == book.isbn10: # search after 0th comma for book isbn13 and 1st comman for isbn10
                print(f"ISBN '{book.isbn13}' or '{book.isbn10}' already exists in the file.")
                return
        else:
            with open("books.txt", "a") as file: # Open file with append permissions
                file.write(f"{book.isbn13},{book.isbn10},{book.author},{book.genre},{book.publisher},{book.pub_year},{book.book_type},{book.title}\n") # write in the proper format
            print(f"Book '{book.title}' has also been added to the file books.txt") # add book to file won't add if isbn10-13/title (handled above)



def remove_book(library, title): # removes the book from the dictionary as well as the books file by simply rewriting all the lines that dont containt the exact book name
    if title in library:
        del library[title]
        with open("books.txt", "r") as file:
            lines = file.readlines()
        with open("books.txt", "w") as file:
            for line in lines:
                if line.strip().split(',')[7] != title:
                    file.write(line)
        print(Fore.RED + f"Book '{title}' has been removed from the library." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Book '{title}' not found in the library." + Style.RESET_ALL)


def search_book(library, title): # simple search function to search for books with exact matches or the search term in the title.
    exact_matches = {}  # exact matches dictionary
    containing_matches = {} # contains keyword dictionary

    for book_title in library: # loop for going through dictinonary
        if book_title == title: # exact match
            exact_matches[book_title] = library[book_title]
        elif title.lower() in book_title.lower(): # contains word
            containing_matches[book_title] = library[book_title]

    if exact_matches: # if there are exact matches print them
        print("Exact matches:")
        for title, book in exact_matches.items():
            print(f"{title}: {book}")

    else: # else tell the user no exact matches
        print(Fore.RED + f"No exact matches found for '{title}'." + Style.RESET_ALL)

    if containing_matches: # if a book contains the word they search
        print("Matches containing the search term:")
        for title, book in containing_matches.items():
            print(f"{title}: {book}")

    else: # else tell the user no book contains their word
        print(f"No books found containing '{title}'.")

    if not (exact_matches or containing_matches): # tell the user no exact matches or books contain the word they searched for
        print(Fore.RED + f"No books found matching or containing '{title}'." + Style.RESET_ALL)


def display_books(library): # simply display all the books in the dictionary calling back to our pretty __str__ function
    print("Library contains these books:")
    for book in library.values():
        print(book)


def read_books_from_txt(library, file_path): # read all the books in the speicfifed text file.
    with open(file_path, "r") as file: # open file with read permissions
        for line_num, line in enumerate(file, 1): # for loop that enumerates to keep track of the index
            line = line.strip() #strip white space if there is any (I kept adding white space by mistake and breaking it :()
            if not line: # skip blanks
                continue
            row = line.split(',') # split values by comma
            if len(row) != 8: # check to make sure there are 8 values
                print(f"Invalid line {line_num} in file: {line}")
                continue
            isbn13, isbn10, author, genre, publisher, pub_year, book_type, title = row # Extract the values from each row in the file
            add_book_dictionary(library, Book(isbn13, isbn10, author, genre, publisher, int(pub_year), book_type, title)) # add to the dictionary
            add_book_to_file(library, Book(isbn13, isbn10, author, genre, publisher, pub_year, book_type, title)) # add to the file
    display_books(library)


def read_books_from_csv(library, file_path): # Read all the books from the specified csv file.
    with open(file_path, "r") as file: # open file with read permissions
        csv_reader = csv.reader(file)
        next(csv_reader)  # skip the standard header row
        for line_num, row in enumerate(csv_reader, 2):  # start counting from line 2
            if len(row) != 8: # check to make sure there are 8 values
                print(f"Invalid line {line_num} in file: {row}")
                continue
            isbn13, isbn10, author, genre, publisher, pub_year, book_type, title = row # Extract the values from each row in the file
            add_book_dictionary(library, Book(isbn13, isbn10, author, genre, publisher, int(pub_year), book_type, title)) # add to the dictionary
            add_book_to_file(library, Book(isbn13, isbn10, author, genre, publisher, pub_year, book_type, title)) # add to the file
    display_books(library)


# Function to add a book to the library


def manual_input(library): # Manual input that took me forever because I kept messing up checking for existing books many many many times
    while True:
        try:
            title = input(Fore.LIGHTGREEN_EX + "Enter the book title (or 'q' to return to menu): ").strip() # allow user to quit during title entry if selected by mistake
            if title.lower() == 'q':
                break
            isbn13 = input("Enter the ISBN-13 (13 Digits): ").strip() # strip the whitespace because I kept doing that
            if not isbn13.isdigit() or len(isbn13) != 13:
                raise ValueError("Invalid ISBN-13 format. Please enter a 13-digit number.") # handle and rase the error
            isbn10 = input("Enter the ISBN-10 (10 Digits): ").strip() # strip the whitespace because I kept doing that
            if not isbn10.isdigit() or len(isbn10) != 10:
                raise ValueError("Invalid ISBN-10 format. Please enter a 10-digit number.") # handle and rase the error
            author = input("Enter the authors Full Name: ").strip() # strip the whitespace because I kept doing that
            genre = input("Enter the genre: ").strip() # strip the whitespace because I kept doing that
            publisher = input("Enter the publisher: ").strip() # strip the whitespace because I kept doing that
            pub_year = input("Enter the publication year (4 digits): ").strip() # strip the whitespace because I kept doing that
            if not pub_year.isdigit() or len(pub_year) != 4:
                raise ValueError("Invalid publication year format. Please enter a 4-digit number.") # handle and rase the error
            pub_year = int(pub_year)
            book_type = input("Enter the book type (Hardcover, Paper, E-book, Kindle): " + Style.RESET_ALL).strip() # strip the whitespace because I kept doing that
            add_book_dictionary(library, Book(isbn13, isbn10, author, genre, publisher, int(pub_year), book_type, title)) # add to dictionary
            add_book_to_file(library, Book(isbn13, isbn10, author, genre, publisher, pub_year, book_type, title)) # add to file
            display_books(library)
        except ValueError as e: # handle value error
            print(Fore.RED + str(e) + Style.RESET_ALL)
        except Exception as e: # handle other standard errors that could occur
            print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)


def main_menu(library): # simple main menu for selections and call their functions
    while True:
        print(Style.RESET_ALL + Fore.MAGENTA + "\nChoose an action:" + Style.RESET_ALL)
        print(Fore.GREEN + "1. Input books" + Style.RESET_ALL)
        print(Fore.BLUE + "2. Display all books" + Style.RESET_ALL)
        print(Fore.YELLOW + "3. Remove a book" + Style.RESET_ALL)
        print(Fore.CYAN + "4. Search for a book" + Style.RESET_ALL)
        print(Fore.RED + "5. Quit" + Style.RESET_ALL) # actually allow the user to quit instead of restarting the program.

        choice = int(input("Enter your choice (1, 2, 3, 4, or 5): "))

        if choice == 1:
            input_books_menu(library)
        elif choice == 2:
            display_books(library)
        elif choice == 3:
            title_to_remove = input("Enter the title of the book to remove: ").strip()
            remove_book(library, title_to_remove)
        elif choice == 4:
            title_to_search = input("Enter the title of the book to search for: ").strip()
            search_book(library, title_to_search)
        elif choice == 5:
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter a number 1-5." + Style.RESET_ALL)


def input_books_menu(library): # simple input menu for selections and call their functions/":
    while True:
        print(Style.RESET_ALL + Fore.MAGENTA + "\nChoose how you want to input books:" + Style.RESET_ALL)
        print(Fore.GREEN + "1. Read from a text file" + Style.RESET_ALL)
        print(Fore.BLUE + "2. Read from a CSV file" + Style.RESET_ALL)
        print(Fore.YELLOW + "3. Manually input books" + Style.RESET_ALL)
        print(Fore.RED + "4. Return to main menu" + Style.RESET_ALL) # return to the main menu easily instead of restarting program

        choice = int(input("Enter your choice (1, 2, 3, or 4): "))

        if choice == 1:
            txt_file_path = input(Fore.CYAN + "Enter the path to the text file: " + Style.RESET_ALL)
            read_books_from_txt(library, txt_file_path)
        elif choice == 2:
            csv_file_path = input(Fore.BLUE + "Enter the path to the CSV file: " + Style.RESET_ALL)
            read_books_from_csv(library, csv_file_path)
        elif choice == 3:
            manual_input(library)
        elif choice == 4:
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter a number 1-4." + Style.RESET_ALL)


# intialize library dictionary
library = {}
# call main menu to display
main_menu(library)
