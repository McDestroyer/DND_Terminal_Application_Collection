# import time
#
# with open("test.AI", "r") as file:
#     data = file.readlines()[:]
#     code_indicies = [{}] * len(data)
#     for i, line in enumerate(data):
#         while "\\033" in line:
#             start_index = line.find("\\033")
#             end_index = line.find("m", start_index)
#             code = line[start_index:end_index + 1]
#             code_indicies[i][start_index] = code.replace("\\033", "\033")
#             # line.replace(code, "", 1)
#             line = line[:start_index] + line[end_index + 1:]
#             print("Found: " + code.replace("\\033", "\033") + code)
#
#     print('\033[0m', end="", flush=True)

with open("test.AI", "r") as file:
    data = file.readlines()[:]
    code_indicies = [{}] * len(data)
    for i, line in enumerate(data):
        line = line.replace("\\033", "\033")
        while "\033" in line:
            start_index = line.find("\033")
            end_index = line.find("m", start_index)
            code = line[start_index:end_index + 1]
            code_indicies[i][start_index] = code
            line = line[:start_index] + line[end_index + 1:]
            print("Found: " + code.replace("\\033", "\033") + code)

        print(line)

    print('\033[0m', end="", flush=True)
