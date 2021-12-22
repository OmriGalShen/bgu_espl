import tkinter as tk
import csv
import sys
import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog


def num_movies_by_countries(input_file, output_file):  # task1a
    """Calculate the number of movies that have been presented in each country ( Note, that
    movie can be presented in more than one country ) and output it to movies.stats in the
    following format: country_name|number_of_movies.
    """
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        file_list = list(csv.reader(infile))[1:]  # skip first line
        country_dic = {}
        for row in file_list:
            countries = str(row[5]).split(', ')
            for country in countries:
                if country in country_dic:
                    country_dic[country] += 1
                else:
                    country_dic[country] = 1
        for key, value in country_dic.items():
            outfile.write("%s|%s\n" % (key, value))


def num_of_movies(input_file, country, year):  # task1b
    """Calculate the number of movies presented in a
    specific country that is released after a
    specific date."""
    movie_counter = 0
    with open(input_file, "r") as infile:
        file_list = list(csv.reader(infile))[1:]  # skip first line
        for row in file_list:
            curr_year = int(row[2])
            countries = str(row[5]).split(', ')
            for curr_country in countries:
                if curr_country == country and year <= curr_year:
                    movie_counter += 1
    msg = "Number of movies in {} after {}: {}".format(
        country, year, movie_counter)
    messagebox.showinfo(message=msg)


def print_histogram(input_file):  # task1c
    """Draw a histogram of the number of movies presented each year, see this page."""
    with open(input_file, "r") as infile:
        file_list = list(csv.reader(infile))[1:]  # skip first line
        year_list = [int(item[2]) for item in file_list]
        num_bins = max(year_list)-min(year_list)+1
        n, bins, patches = plt.hist(
            year_list, num_bins, facecolor="blue", alpha=0.5)
        plt.show()


def total_duration(input_file, output_file):  # task2a
    """Calculate the total duration of movies for each genre. Output it to genre.stats in the
    following format: genre|average duration.
    """
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        file_list = list(csv.reader(infile))[1:]  # skip first line
        genre_dic = {}
        for row in file_list:
            curr_duration = int(row[4])
            genres = str(row[3]).split(', ')
            for genre in genres:
                if genre in genre_dic:  # already defined genre
                    genre_dic[genre][0] += 1  # add to genre counter
                    # add to genre total duration
                    genre_dic[genre][1] += curr_duration
                else:
                    genre_dic[genre] = [1, curr_duration]  # new genre
        for key, value in genre_dic.items():
            avg_duration = value[1]/value[0]  # avrage = total duration / count
            outfile.write("%s|%f\n" % (key, avg_duration))


def num_of_movies_in_genre(input_file, country):  # task2b
    """For a specific country calculate the number of movies for each genre movie that has
    been published in this country.
    """
    genre_dic = {}
    with open(input_file, "r") as infile:
        file_list = list(csv.reader(infile))[1:]  # skip first line
        for row in file_list:
            countries = str(row[5]).split(', ')
            if country in countries:
                genres = str(row[3]).split(', ')
                for genre in genres:
                    if genre in genre_dic:  # already defined genre
                        genre_dic[genre] += 1  # add to genre counter
                    else:
                        genre_dic[genre] = 1  # new genre
    msg = "number of movies for each genre:\n"
    for key, value in genre_dic.items():
        msg += "%s|%d\n" % (key, value)
    messagebox.showinfo(message=msg)


def button_func1(input_file):
    output_file = simpledialog.askstring(title="output file",
                                         prompt="Enter output file:",
                                         initialvalue='movies.stats')
    num_movies_by_countries(input_file, output_file)
    msg = "Results stored in:" + output_file
    messagebox.showinfo(message=msg)


def button_func2(input_file):
    country = simpledialog.askstring(title="country name",
                                     prompt="Enter country name:",
                                     initialvalue='USA')
    year = simpledialog.askinteger(title="release year",
                                         prompt="Enter release year:",
                                         initialvalue='1948')
    num_of_movies(input_file, country, year)


def button_func4(input_file):
    output_file = simpledialog.askstring(title="output file",
                                         prompt="Enter output file:",
                                         initialvalue='genre.stats')
    total_duration(input_file, output_file)
    msg = "Results stored in:" + output_file
    messagebox.showinfo(message=msg)


def button_func5(input_file):
    country = simpledialog.askstring(title="country name",
                                     prompt="Enter country name:",
                                     initialvalue='USA')
    num_of_movies_in_genre(input_file, country)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task2.py <file.csv>")
        sys.exit()
    input_file = sys.argv[1]
    window = tk.Tk()
    window.eval('tk::PlaceWindow . center')
    label = tk.Label(
        text="-------Task 3 Menu------------",
        width=25,
        height=5,
    ).pack()
    button1 = tk.Button(
        text="1.Get movies by countries",
        width=25,
        height=5,
        command=lambda: button_func1(input_file)
    ).pack()
    button2 = tk.Button(
        text="2.Get number of movies",
        width=25,
        height=5,
        command=lambda: button_func2(input_file)
    ).pack()
    button3 = tk.Button(
        text="3.Print histogram",
        width=25,
        height=5,
        command=lambda: print_histogram(input_file)
    ).pack()
    button4 = tk.Button(
        text="4.Total duration",
        width=25,
        height=5,
        command=lambda: button_func4(input_file)
    ).pack()
    button5 = tk.Button(
        text="5.Movies in genre",
        width=25,
        height=5,
        command=lambda: button_func5(input_file)
    ).pack()
    button6 = tk.Button(
        text="6.Quit",
        width=25,
        height=5,
        command=lambda: sys.exit()
    ).pack()
    window.mainloop()
