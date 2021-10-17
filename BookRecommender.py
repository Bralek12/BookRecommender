import pandas as pd
import numpy as np


class BookRecommender:
    # This method is loading data from given datasets. Apart from original code my code may accept even another files on
    # the input if needed. Also we can specify separator.
    # Suggestion for further improvement - load the data by chunks not as whole. There may be some memory issues with
    # loading these dataset.
    @staticmethod
    def load_data(book_ratings='BX-Book-Ratings.csv', bx_books='BX-Books.csv', separator=";"):
        ratings = pd.read_csv(book_ratings, encoding='cp1251', sep=separator)
        ratings = ratings[ratings['Book-Rating'] != 0]
        books = pd.read_csv(bx_books, encoding='cp1251', sep=separator, error_bad_lines=False)
        dataset = pd.merge(ratings, books, on=['ISBN'])
        # I highly appreciate the author of original code set all the string in the data set to lowercase. I am not sure
        # if there may be a simpler / more effective method. Maybe call the method only on the relevant columns
        # Book-Title, Book-Author?
        # Efficiency - I decided to drop three columns from the dataset since I am not providing GUI in this code I do
        # not need last three columns with the links to the images of the books
        # We can also consider dropping another not used columns such as Year of publication etc.l
        dataset.drop(['Image-URL-S', 'Image-URL-M', 'Image-URL-L'], axis=1, inplace=True)
        return dataset.apply(lambda x: x.str.lower() if (x.dtype == 'object') else x)
    # This method provides us with the np array of unique readers. I decided to remove author name / wanna-be variable
    # in the original code. I think in this  code it is enough to sort users based whether they liked / read the given
    # book. To accept even authors the code may have to be more complicated. I provided partial solution to this in
    # a note in this method. Also the author would have to set on input.
    @staticmethod
    def get_unique_readers(data, book_title):
        book_title = book_title.lower()
        unique_readers = data['User-ID'][data['Book-Title'].apply(lambda title: title == book_title)].tolist()
        # Code for accepting author data['User-ID'][data['Book-Title'].apply(lambda title: title.lower == book_title)
        #                                           | data['Book-Author'].apply(lambda author:
        #                                           author == author_from_input)].tolist()
        return np.unique(unique_readers)
    # I again set this part of the code into method. Also I did not like the hard-coded threshold so I made it optional
    # to set new threshold in the higher level of the code.
    # Number of ratings per other books in dataset
    # Here I made only a slight change .agg("count") -> .count() since groupby object has already default method for
    # Returning count

    @staticmethod
    def create_pivot(final_dataset, threshold = 8):
        number_of_rating_per_book = final_dataset.groupby(['Book-Title']).agg('count').reset_index()
        # select only books which have actually higher number of ratings than threshold
        books_to_compare = number_of_rating_per_book['Book-Title'][number_of_rating_per_book['User-ID'] >= threshold]
        books_to_compare = books_to_compare.tolist()
        ratings_data_raw = final_dataset[['User-ID', 'Book-Rating', 'Book-Title']][
            final_dataset['Book-Title'].isin(books_to_compare)]
        # group by User and Book and compute mean
        ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean()
        # reset index to see User-ID in every row
        ratings_data_raw_nodup = ratings_data_raw_nodup.to_frame().reset_index()
        return ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')