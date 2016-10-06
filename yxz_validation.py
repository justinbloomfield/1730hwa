import re #for regex checking 

def yxz_test(path):
    """
    Takes the path to the file, and checks that it contains the correct number of entries per line and only valid characters. Quits when file is found to be invalid, stating the error.
    """
    valid_chars = re.compile('[0-9\.\-]') #characters 0 through 9 
    with open(path, "r") as test:
        for line in test:
            blocks = line.split()
            if len(blocks) == 3:
                for item in blocks:
                    if valid_chars.match(item):
                        pass
                    else:
                        print("Invalid characters")
                        return False
            else:
                print("Invalid file format")
                return False
    print("Valid file")
    return True

