import csv
import sys
import matplotlib.pyplot as plt
import os

clear = lambda: os.system('clear')


def num_movies_by_countries(input_file, output_file):
    """Calculate the number of movies that have been presented in each country ( Note, that
    movie can be presented in more than one country ) and output it to movies.stats in the
    following format: country_name|number_of_movies.
    """
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        file_list = list(csv.reader(infile))[1:] # skip first line
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


def num_of_movies(input_file, country, year):
    """Calculate the number of movies presented in a
    specific country that is released after a
    specific date."""
    counter = 0
    with open(input_file, "r") as infile:
        file_list = list(csv.reader(infile))[1:] # skip first line
        for row in file_list:  
            curr_country = row[-1]
            curr_year = int(row[2])
            if curr_country == country and year <= curr_year:
                counter += 1
    print("Number of movies in {} after {}: {}".format(country, year, counter))


def print_histogram(input_file):
    """Draw a histogram of the number of movies presented each year, see this page."""
    with open(input_file, "r") as infile:
        file_list = list(csv.reader(infile))[1:] # skip first line
        year_list = [int(item[2]) for item in file_list]
        num_bins = max(year_list)-min(year_list)+1
        n, bins, patches = plt.hist(year_list, num_bins, facecolor="blue", alpha=0.5)
        plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task1.py <file.csv>")
        sys.exit()
    input_file = sys.argv[1]
    while True:
        clear()
        print()
        print("-------Task 1 Menu------------")
        print("1.Get movies by countries")
        print("2.Get number of movies")
        print("3.Print histogram")
        print("4.Quit")
        print("-------------------------------")
        print()
        choise = int(input("Enter action: "))
        if choise == 1:
            output_file = input("Enter output file (movies.stats): ")
            num_movies_by_countries(input_file, output_file)
            print("Results stored in:",output_file)
            input("Press Enter to continue\n")
        elif choise == 2:
            country = input("Enter country name(i.e USA): ")
            year = int(input("Enter release year(i.e 1917): "))
            num_of_movies(input_file, country, year)
            input("Press Enter to continue\n")
            continue
        elif choise == 3:
            print_histogram(input_file)
            input("Press Enter to continue\n")
            continue
        elif choise == 4:
            sys.exit()
        else:
            print("Invalid choise")
            input("Press Enter to continue\n")
            continue
