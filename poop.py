def file_editor(filename, data=None, read=False, write=False):
    """
    Makes it easier to read/write/append data from/to a file
    :param data: Data to be added to file (in this case it's text)
    :param filename: path to file
    :param read: Bool
    :param write: Bool (if selected then overwrites, otherwise appends)
    :return: if read is selected then it returns a list of the string data
    """
    if read:
        opened_file = open(filename, "r")
        temp_data = opened_file.readlines()
        opened_file.close()
        return temp_data

    elif data is not None:
        if not write:
            opened_file = open(filename, "a+")
            opened_file.write(data + "\n")
            opened_file.close()

        elif write:
            opened_file = open(filename, "w+")
            opened_file.write(data + "\n")
            opened_file.close()
    else:
        return


file_path = "C:\\Users\\Aziz\\Desktop\\data.txt"

data = file_editor(file_path,  read=True)

print("Printing Current Data in file: ")

for x in range(len(data)):
    print(str(x + 1) + ". " + data[x], end="")

print("\n\nOverwriting File:\n\n")

data = "New Data"

file_editor(file_path, data=data, write=True)

data = file_editor(file_path, read=True)

for x in range(len(data)):
    print(str(x + 1) + ". " + data[x], end="")
