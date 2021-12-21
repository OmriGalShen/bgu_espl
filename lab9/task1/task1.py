import csv
import sys


def num_movies_by_countries(input, output):
    """Calculate the number of movies that have been presented in each country ( Note, that
    movie can be presented in more than one country ) and output it to movies.stats in the
    following format: country_name|number_of_movies.
    """
    with open(input, "r") as infile, open(output, "w") as outfile:
        country_dic = {}
        file_reader = csv.reader(infile)
        for row in list(file_reader)[1:]:  # skip first line
            country = row[-1]
            if country in country_dic:
                country_dic[country] += 1
            else:
                country_dic[country] = 1
        for key, value in country_dic.items():
            outfile.write("%s:%s\n" % (key, value))


def num_of_movies(input, country, year):
    """Calculate the number of movies presented in a
    specific country that is released after a
    specific date."""
    counter = 0
    with open(input, "r") as infile:
        file_reader = csv.reader(infile)
        for row in list(file_reader)[1:]:  # skip first line
            curr_country = row[-1]
            curr_year = int(row[2])
            if curr_country == country and year <= curr_year:
                counter += 1
    print("Number of movies in {} after {}: {}".format(country,year,counter))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python task1.py <file.csv> <output_file>")
        sys.exit()
    input = sys.argv[1]
    output = sys.argv[2]
    num_movies_by_countries(input, output)
    country = raw_input("Enter country name(i.e USA): ")
    year = int(raw_input("Enter release year(i.e 1917): "))
    num_of_movies(input, country, year)
