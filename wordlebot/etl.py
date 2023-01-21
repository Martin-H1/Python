import glob
import sys

def scan_word(word, words):
    """
    Some words actually have multiple embedded words.
    This function splits them into multiple words.
    """
    idx = word.find("_")
    if idx != -1:
        words.append(word.split("_"))
    else:
        words.append(word)

def scan_line(line):
    """
    splits the line into two words and returns them in an array
    Argument:
    line -- the line of text to process
    """
    words = []
    idx = line.find(" ")
    if (idx != -1):
        scan_word(line[:idx], words)
        scan_word(line[idx+1:].replace("\n", ""), words)
    return words

def scan_file(filename):
    """
    Opens a file by name and tokenizes it a line at a time.
    Argument:
    filename -- the fully qualified name of the file.
    """
    print("Processing " + filename)

    words = []
    with open(filename) as sourcefile:
        for line in sourcefile:
            retval = scan_line(line)
            words.extend(retval)

    # use anonymous function to filter words
    words = list(filter(lambda x: (len(x) == 5), words))

    # remove duplicates
    words = list(dict.fromkeys(words))
    return words

def write_list(filename, words):
    with open(filename, "w") as of:
        for word in words:
            of.write(word + "\n")

# Get the list of all files and directories
path = r'C:\Program Files (x86)\WordNet\2.1\dict\*.exc'

words = []
files = glob.glob(path)
for file in files:
    words.extend(scan_file(file))
words.sort()
write_list("words.txt", words)
