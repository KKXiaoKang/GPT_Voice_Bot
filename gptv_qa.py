import openai
import os

# 设置OpenAI API密钥
openai.api_key = '您的API密钥'

# 加载图像，这里假设图像是本地文件
file_path = 'path/to/your/image.jpg'
with open(file_path, 'rb') as f:
    image_data = f.read()

# 使用OpenAI的文件API上传图像，并获取文件ID
response = openai.File.create(file=image_data, purpose='answers')
file_id = response['id']

# 构造问答请求
question = "这张图片里有什么？"  # 这里写上您的问题

# 发送问答请求
answer = openai.Answer.create(
    model="gpt-4",  # 确保使用的是支持的模型
    question=question,
    file=file_id,
    examples_context="Photo of a dog in the park",
    examples=[["What is in this photo?", "A dog in a park"]],
    max_tokens=50
)

# 打印回答
print(answer['answers'][0])

# 将回答保存到本地文件
with open('answer.txt', 'w') as file:
    file.write(answer['answers'][0])

