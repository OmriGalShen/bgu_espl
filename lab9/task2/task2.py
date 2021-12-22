import csv
import sys
import matplotlib.pyplot as plt
import os


def clear(): return os.system('clear')


def print_menu():
    clear()
    print()
    print("-------Task 2 Menu------------")
    print("1.Get movies by countries")  # task1a
    print("2.Get number of movies")  # task1b
    print("3.Print histogram")  # task1c
    print("4.Total duration")  # task2a
    print("5.Movies in genre")  # task2b
    print("6.Quit")
    print("-------------------------------")
    print()


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

    print("Number of movies in {} after {}: {}".format(
        country, year, movie_counter))


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
                    genre_dic[genre][1] += curr_duration # add to genre total duration
                else:
                    genre_dic[genre] = [1, curr_duration]  # new genre
        for key, value in genre_dic.items():
            avg_duration = value[1]/value[0] # avrage = total duration / count
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
    print("number of movies for each genre:")
    for key, value in genre_dic.items():
        print("%s|%d" % (key, value))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task2.py <file.csv>")
        sys.exit()
    input_file = sys.argv[1]

    while True:
        print_menu()
        choise = int(input("Enter action: "))

        if choise == 1:
            output_file = input("Enter output file (default:movies.stats): ")
            output_file = "movies.stats" if not output_file else output_file
            num_movies_by_countries(input_file, output_file)
            print("Results stored in:", output_file)
            input("\nPress Enter to continue\n")

        elif choise == 2:
            country = input("Enter country name(i.e USA): ")
            year = int(input("Enter release year(i.e 1917): "))
            num_of_movies(input_file, country, year)
            input("\nPress Enter to continue\n")

        elif choise == 3:
            print_histogram(input_file)
            input("\nPress Enter to continue\n")

        elif choise == 4:
            output_file = input("Enter output file (default:genre.stats): ")
            output_file = "genre.stats" if not output_file else output_file
            total_duration(input_file, output_file)
            print("Results stored in:", output_file)
            input("\nPress Enter to continue\n")

        elif choise == 5:
            country = input("Enter country name(i.e USA): ")
            num_of_movies_in_genre(input_file, country)
            input("\nPress Enter to continue\n")

        elif choise == 6:
            sys.exit()

        else:
            print("Invalid choise")
            input("\nPress Enter to continue\n")
