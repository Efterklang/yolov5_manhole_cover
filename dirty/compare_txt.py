def read_file_to_dict(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    result_dict = {}
    for line in lines:
        parts = line.split()
        if parts[0] in result_dict:
            result_dict[parts[0]].append(parts[1])
        else:
            result_dict[parts[0]] = [parts[1]]
    return result_dict


def compare_dicts(filename1, filename2):
    i = 0
    dict1 = read_file_to_dict(filename1)
    dict2 = read_file_to_dict(filename2)
    for key in dict1:
        if key in dict2:
            if sorted(dict1[key]) != sorted(dict2[key]):
                print(
                    f"DIFF FILE NAME: test/{key} \n {filename1.split('/')[-1]}: {dict1[key]}, \n {filename2.split('/')[-1]}: {dict2[key]}\n"
                )
                i += 1
        else:
            print(f"{key} Only existed in {filename1}\n")
    for key in dict2:
        if key not in dict1:
            print(f"{key} Only existed in {filename2}\n")
    print(f"Total {i} different files\n")


# txt file path
filename1 = "./out/output.txt"
filename2 = "./output/output.txt"

# Print Result
compare_dicts(filename1, filename2)
