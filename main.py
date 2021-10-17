from BookRecommender import BookRecommender
import pandas as pd


# In the first place I decided to rewrite the code in a class because this way we can overcome many problems such as
# memory overload etc. Also getting the methods into class is a good practice apart from hardcoding everything into one
# file

# Pros and Cons of the original code:
# Pros: - Code uses interesting approach how to work with the data on input since the data on input are not as complex
#         as they could be. In this case I would suggest to use some more complex data sources in further improvements
#         of this code.
# Cons: - The original code is quite a bit complex with minimum comment on how the code should work.
#       - Many of the data are hard-coded - we cannot change the book-title on the input, links  to data-source files,
#         neither data-separators etc.
#       - The code is written in single file and there are not methods or classes which may be a dangerous if working
#         with large data files (memory overflow), it is much less readable and almost not re-usable.
#       - Names of variables are often "not neutral". The author of the original code used for example name of variable
#         books_of_tolkien_readers which does not refer to the data in general but specifically on the data the author
#         got from the input book title "fellowship of the ring...."
#       - Data on the input are not clean. There at least 4 lines with problematic data
#       - Original code crashed in the moment I try to run it :D
#       - There is no input for the original code

# There should be main method in all well-written apps / runtime codes
def main():
    # Again I think parts of the code should be meaningfully written into functions/methods
    base_data = BookRecommender.load_data()

    def get_pivot_for_title(book_title):
        uniques = BookRecommender.get_unique_readers(base_data, book_title)
        final_dataset = base_data[(base_data['User-ID'].isin(uniques))]
        return BookRecommender.create_pivot(final_dataset)

    # The original code was supposed to accept more book (LOTR trilogy) but still there of list of len == 1 on the input
    # which makes using for loop totally redundant. I decided to set the correlation only for one title. If needed for
    # more titles I would recommend using for loop with the correlator method I am providing in this code.
    def correlator(pivot_table, book_title):
        # Take out the selected book from correlation dataframe
        book_title = book_title.lower()
        dataset_of_other_books = pivot_table.copy(deep=False)
        dataset_of_other_books.drop([book_title], axis=1, inplace=True)
        # empty lists
        book_titles, correlations, average_rating = [], [], []
        # corr computation
        for title in list(dataset_of_other_books.columns.values):
            book_titles.append(title.title())
            correlations.append(pivot_table[book_title].corr(dataset_of_other_books[title]))
            tab = (base_data[base_data['Book-Title'] == title].groupby(['Book-Title']).mean())
            average_rating.append(tab['Book-Rating'].min())
        # final dataframe of all correlation of each book
        correlation_table = pd.DataFrame(list(zip(book_titles, correlations, average_rating)),
                                         columns=['book', 'corr', "avg_rating"])

        correlation_table = correlation_table.sort_values('corr', ascending=False).reset_index(drop=True).round(2)
        correlation_table.index = correlation_table.index + 1
        # top 10 books with highest corr
        print(correlation_table.head(10))
        # worst 10 books # I am actually not why should we look for the "worst" correlations. Since there is a
        # threshold on the number of reviews for correlation most of the "least correlated titles" are not even in
        # the dataset
        # worst_list.append(correlation_table.sort_values('corr', ascending=False).tail(10))

    # Here I prepared simple input/output interface for usage in terminal line. I set everything into functions.
    def start_search():
        titles = set(base_data["Book-Title"])
        while True:
            title = str(input("Insert name of your favourite book (or Exit for exit): "))
            if title.lower() == "exit":
                print("Ok, I am terminating myself :)")
                break
            elif title.lower() in titles:
                print("Your book is here!")
                correlator(get_pivot_for_title(title), title)
            else:
                print(f'I am sorry, I do not know book {title} or you gave me invalid input!')

    start_search()


if __name__ == "__main__":
    main()

# Other improvement of the code:
# 1.) There is a problem with searching for books which have less than 8 ratings. This is a case of most of the books
#     in the given dataset. To overcome this I would suggest using different (maybe younger) dataset maybe some
#     free data set from Kaggle.com
# 2.) The correlation for recommending books is an interesting approach. I would suggest that we could also create
#     some index of rating / num of rating / readers etc. so the people looking for new book could have more information
#     while choosing new book to read :)
# 3.) For output it would be simple to code output for csv or some graphical output. I did not implement this because
#     (unfortunately) I did not manage to start coding the GUI/front-end of the app

