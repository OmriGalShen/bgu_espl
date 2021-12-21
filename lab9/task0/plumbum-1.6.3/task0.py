from plumbum import local
import sys


def print_students(file):
    """A list of all students mentioned in the file."""
    print("List of of all students:")
    awk = local["awk"]["{print $1}"][file]
    print(awk())


def num_of_students(file):
    """The number of students is mentioned in the file."""
    print("The number of students:")
    awk = local["awk"]["END {print NR}"][file]
    print(awk())


def get_errors(file):
    awk = local["awk"]["{for(i=2;i<=NF;++i)print $i}"][file]  # remove students names
    sed1 = local["sed"]["s/[0-9]*//g"]  # remove numbers
    sed2 = local["sed"]["s/://g"]  # remove :
    sed3 = local["sed"]["s/|/\\n/g"]  # replace pipes with new line
    sed4 = local["sed"]["s/\./ /g"]  # remove dot
    sed5 = local["sed"]["s/ //g"]  # remove spaces
    sed6 = local["sed"]["s/\r//g"]  # remove '\r'
    grep = local["grep"]["\S"]  # remove blanks
    sort = local["sort"]
    return awk | sed1 | sed2 | sed3 | sed4 | sed5 | sed6 | grep | sort


def print_errors(file):
    """A list of all error codes mentioned in the file together with how many times
    each error code was mentioned.
    """
    print("Error list:")
    errors = get_errors(file)
    uniq = local["uniq"]["-c"]  # count unique errors
    res = errors | uniq
    print(res())


def unique_errors(file):
    """The number of unique error-codes found in the file."""
    print("The number of unique error-codes:")
    errors = get_errors(file)
    uniq = local["uniq"] # keep unique errors
    wc = local["wc"]["-w"]# count words
    res = errors | uniq | wc
    print(res())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task0.py <file.csv>")
        sys.exit()
    file = sys.argv[1]
    print_students(file)
    num_of_students(file)
    print_errors(file)
    unique_errors(file)
