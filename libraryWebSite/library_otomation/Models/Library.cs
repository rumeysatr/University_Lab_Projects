using System.ComponentModel.DataAnnotations;

namespace library_otomation.Models
{
    public class Library
    {
        private List<Book> Books ;

        public Library()
        {
            Books = new List<Book>();
        }

        public void addBook(Book book)
        { 
            Books.Add(book);
        }
                                //dönüş değeri bool yapılabilir 
        public bool removeBook(string name)
        {
            if (Books.RemoveAll(book => book.Name == name) == 1)
            {
                return true;
            }
            return false;
        }


        public List<Book> SearchByName(string name)
        {
            return Books.FindAll(book => book.Name.Equals(name, StringComparison.OrdinalIgnoreCase));
        }

        public List<Book> SearchByAuthor(string author)
        {
            return Books.FindAll(book => book.Author.Equals(author, StringComparison.OrdinalIgnoreCase));
        }


        public List<Book> ListAllBooks()
        {
            return Books;
        }
    }
}
