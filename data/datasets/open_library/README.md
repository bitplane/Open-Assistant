# Plan / notes

## Data filtering

1. Download the data
2. zip through it compressed
3. Filter authors and works that don't have a description or isn't a latest
   version
4. Make a list of interesting line numbers
5. Do a second pass, considering only interesting line numbers
6. Add authors and books to sqlite database

## Author data

{author.description}

They wrote {book.count} books

{#books} {book.title} {/books}

## Book data

{book.title} was written by {author.name}

...
