# 创建一个空字典来存储键值对
airc_type_dict = {}

# 打开并读取文件
file_name = "/Users/小巴的工作台/BBS_WORK_SPACE/Python_Workspace/Dynamic_Routing/airport/Datas/traffic/acft_types.txt"
with open(file_name, 'r') as file:
    for line in file:
        # 使用split方法将每一行分割为两部分
        key, value = line.strip().split()
        # 将键值对存储在字典中
        airc_type_dict[key] = value

# print(airc_type_dict)
