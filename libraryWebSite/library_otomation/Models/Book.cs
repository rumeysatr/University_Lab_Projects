using System.ComponentModel.DataAnnotations;

namespace library_otomation.Models
{
    public class Book
    {
        public static int ID { get; set; }
        public string Year { get; set; }
        public string Name { get; set; }
        public string Author { get; set; }

        public Book() { }           //.NET model blinding için default constructor olmalı
                                    // model blinding : bir modelin bir view'e bağlanması ve view'den model'e otomatik veri alınmasıdır
        public Book(string year, string name, string author)
        {
            this.Year = year;
            this.Name = name;           //istersek bunu da kullanabiliriz
            this.Author = author;
            ID++;
        }

    }
}
