# import re

# def retain_chinese_characters(s):
#     # 定义匹配非汉字字符的正则表达式
#     non_chinese_characters = r'[^\\u4e00-\\u9fff]'
#     # 使用正则表达式删除非汉字字符
#     result = re.sub(non_chinese_characters, '', s)
#     return result

# # 测试字符串
# test_string = "你好，世界！这是一个测试：【ChatGPT】2024年。"
# # 调用函数并打印结果
# cleaned_string = retain_chinese_characters(test_string)
# print(cleaned_string)
# print(type(cleaned_string))
def remove_periods(s):
    # 删除字符串中的所有句号
    s.replace('！', '')
    s.replace('？', '')
    s.replace('。', '')
    s.replace('，', '')
    return s

# 示例字符串
test_string = "你好，世界！这是一个测试：【ChatGPT】！"
# 调用函数并输出结果
modified_string = remove_periods(test_string)
print(modified_string)
