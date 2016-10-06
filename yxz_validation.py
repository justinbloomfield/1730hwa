import re

def yxz_test(path):
    valid_chars = re.compile('[0-9-]')
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

yxz_test("data_files/au1k.txt")
