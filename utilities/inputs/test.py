# with open("test.AI", "r") as file:
#     data = file.readlines()[:]
#
# code_indicies = [{} for _ in range(len(data))]
# for i, line in enumerate(data):
#     data[i] = line = line.replace("\\033", "\033")
#     while "\033" in line:
#         start_index = line.find("\033")
#         end_index = line.find("m", start_index)
#         code = line[start_index:end_index + 1]
#         code_indicies[i][start_index] = code
#         line = line[:start_index] + line[end_index + 1:]
#         print("Found: " + code.replace("\033", "\\033") + " in line " + str(i) + " at index " + str(start_index))
#     print(line, end="", flush=True)
#
# print("Code indicies: ", code_indicies)
#
# for i, line in enumerate(data):
#     for j, char in enumerate(line):
#         if j in code_indicies[i]:
#             print(code_indicies[i][j], end="", flush=True)
#         print(char, end="", flush=True)
#
# print('\033[0m', end="", flush=True)
