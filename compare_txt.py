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


def compare_dicts(dict1, dict2, filename1, filename2):
    for key in dict1:
        if key in dict2:
            if sorted(dict1[key]) != sorted(dict2[key]):
                print(
                    f"DIFF FILE NAME: {key} \n {filename1.split('/')[-1]}: {dict1[key]}, \n {filename2.split('/')[-1]}: {dict2[key]}\n"
                )
        else:
            print(f"{key} 只在 {filename1} 中存在")
    for key in dict2:
        if key not in dict1:
            print(f"{key} 只在 {filename2} 中存在")


# txt file path
filename1 = "./output/output-0.884.txt"
filename2 = "./output/bestpt.txt"
dict1 = read_file_to_dict(filename1)
dict2 = read_file_to_dict(filename2)

# Print Result
compare_dicts(dict1, dict2, filename1, filename2)
