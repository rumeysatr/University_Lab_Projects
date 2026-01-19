using library_otomation.Models;
using Microsoft.AspNetCore.Mvc;

namespace library_otomation.Controllers
{
    public class LibraryController : Controller
    {
        private readonly Library Lib; // lib nesnesi Dependency Injection ile oluşturulur

        // dependency injection: bir sınıfın başka bir sınıfı kullanabilmesi
        // için gerekli olan nesnenin dışarıdan verilmesi işlemidir

        public LibraryController(Library lib)
        {
            Lib = lib;
        }

        public ActionResult Index()
        {
            var books = Lib.ListAllBooks();
            return View();
        }

        public ActionResult ListBooks()
        {
            return View("listBooks", Lib.ListAllBooks());
        }

        public ActionResult Search()
        {
            return View("search", null);
        }

        public ActionResult RemoveBooks()
        {
            return View("removeBooks");
        }

        public ActionResult AddBooks()
        {
            return View("addBooks");
        }

        public ActionResult About()
        {
            return View("about");
        }

        [HttpPost]
        public IActionResult Add(string name, string author, string year)
        { 
            var book = new Book(year, name, author);
            Lib.addBook(book);
            TempData["Message"] = "Book added successfully";
            return RedirectToAction("addBooks");
        }
        [HttpPost]
        public IActionResult Remove(string name)
        {
            if (Lib.removeBook(name))
                TempData["Message"] = "Book removed successfully";
            else
                TempData["Message"] = "Book not found";
            return RedirectToAction("RemoveBooks");
        }
        
        [HttpGet("Search")]
        public IActionResult SearchByName(string name)
        {
            var books = Lib.SearchByName(name);
            return View("search", books);
        }

        [HttpGet("SearchByAuthor")]
        public IActionResult SearchByAuthor(string author)
        { 
            var books = Lib.SearchByAuthor(author);
            return View("search", books);
        }

        [HttpGet]
        public IActionResult ListAllBooks()
        {
            var books = Lib.ListAllBooks();
            return View(books);
        }
    }
}
