#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

from peewee import *

def get_u_input(prompt: str, options: list[str]) -> str:
    options = [option.lower() for option in options]
    while True:
        [print(option.capitalize()) for option in options]
        user_input = input(prompt).lower()
        if user_input in options:
            return user_input
        elif user_input == 'quit':
            quit(1)

def author_search(): 
    author_names = [author.pen_name for author in Author.select()]
    author_name = get_u_input('Choose an author:\n>>', author_names)
    author = Author.get(pen_name=author_name)
    author_publications = Publication.select().where(Publication.author_id == author.id)
    books = []
    for pub in author_publications:
        book = Book.get(id=pub.book_id)
        coauthor_ids = [coauth.author_id for coauth in Publication.select().where(Publication.book_id == pub.book_id).where(Publication.author_id != pub.author_id)]
        coauthors = []
        for coauthor in coauthor_ids:
            coauthors.append(Author.get(id=coauthor).pen_name)
        publisher = Publisher.get(id=book.publisher_id).name
        books.append({'title':book.title,'coauthors':coauthors, 'publisher':publisher})

    print(f'{author.name.capitalize()} also known as {author.pen_name.capitalize()} has written {len(books)} book{"s" if len(books) > 1 else ""}.')
    for book in books:
        print(f'{book["title"].capitalize()}:')
        if book['coauthors']:
            print(f'  coauthors:')
            for coauth in book['coauthors']:
                print(f'    {coauth.capitalize()}')
        print(f'  published by: {book["publisher"].capitalize()}')

def book_search(): 
    book_titles = [book.title for book in Book.select()]
    book_title = get_u_input('Choose a book:\n>>', book_titles)
    book = Book.get(title=book_title)
    author_ids = [pub.author_id for pub in Publication.select().where(Publication.book_id == book.id)]
    print(f'{book.title.capitalize()} published by {Publisher.get(id=book.publisher_id).name}.')
    print(f'  Written by:')
    for author_id in author_ids:
        print(f'    {Author.get(id=author_id).pen_name.capitalize()}')

def publisher_search():
    publisher_names = [publisher.name for publisher in Publisher.select()]
    publisher_name = get_u_input('Choose a publisher:\n>>', publisher_names)
    publisher = Publisher.get(name=publisher_name)
    book_ids = [book.id for book in Book.select().where(Book.publisher_id == publisher.id)]

    print(f'{publisher.name.capitalize()} has published {len(book_ids)} book{"s" if len(book_ids) > 1 else ""}.')
    for book_id in book_ids:
        book = Book.get(id=book_id)
        author_ids = [pub.author_id for pub in Publication.select().where(Publication.book_id == book.id)]
        print(f'  {book.title.capitalize()}')
        print(f'    Written by:')
        for author_id in author_ids:
            print(f'      {Author.get(id=author_id).pen_name.capitalize()}') 


def main():
    search_options = {'author': author_search, 'book': book_search, 'publisher': publisher_search}
    search_type = get_u_input('How would you like to search?\n>>', list(search_options.keys()))
    search_options[search_type]()


if __name__ == '__main__':
    with SqliteDatabase('authors.db') as db:

        class DBTable(Model):
            id = AutoField(primary_key=True)
            class Meta:
                database = db

        class Author(DBTable):
            name = CharField()
            pen_name = CharField()

        class Publisher(DBTable):
            name = CharField()

        class Book(DBTable):
            title = CharField()
            publisher_id = ForeignKeyField(Publisher, to_field='id')

        class Publication(DBTable):
            author_id = ForeignKeyField(Author, to_field='id')
            book_id = ForeignKeyField(Book, to_field='id')

        db.create_tables([Author, Publisher, Book, Publication])

        Author.get_or_create(name='billy',pen_name='boby')
        Author.get_or_create(name='joe',pen_name='smith\'n\'western')
        Author.get_or_create(name='john',pen_name='long john bronze')
        Author.get_or_create(name='joan',pen_name='de arc')
        Author.get_or_create(name='albert',pen_name='one third cup')
        Author.get_or_create(name='ken',pen_name='a hot hunk of meat')
        Author.get_or_create(name='andrew',pen_name='tate begone')

        Publisher.get_or_create(name='golden bindings llc')
        Publisher.get_or_create(name='parchment printer org')
        Publisher.get_or_create(name='spells and scrolls inc')

        Book.get_or_create(title='back woods witch brews',publisher_id=3)
        Book.get_or_create(title='the arc of war',publisher_id=1)
        Book.get_or_create(title='where it all went wrong',publisher_id=2)
        Book.get_or_create(title='the magic of lead and powder',publisher_id=1)
        Book.get_or_create(title='cooking with alchemy',publisher_id=3)
        Book.get_or_create(title='that one time my spell fizeled',publisher_id=3)

        Publication.get_or_create(author_id=1,book_id=1)
        Publication.get_or_create(author_id=5,book_id=1)
        Publication.get_or_create(author_id=4,book_id=2)
        Publication.get_or_create(author_id=3,book_id=2)
        Publication.get_or_create(author_id=7,book_id=3)
        Publication.get_or_create(author_id=6,book_id=3)
        Publication.get_or_create(author_id=2,book_id=4)
        Publication.get_or_create(author_id=5,book_id=5)
        Publication.get_or_create(author_id=1,book_id=5)
        Publication.get_or_create(author_id=5,book_id=6)
    
        main()

