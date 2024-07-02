import openai

# 设置OpenAI API密钥
openai.api_key = '您的API密钥'

# 初始化对话历史
dialogue_history = ""

# 定义一个函数来处理问答
def ask_question(question):
    global dialogue_history
    prompt = f"{dialogue_history}{question}\\nAI:"
    response = openai.Completion.create(
        engine="gpt-4", # 确保使用正确的模型
        prompt=prompt,
        max_tokens=150,  # 可调整为所需的回答长度
        stop=["\\n"]
    )
    answer = response.choices[0].text.strip()
    print(answer)
    # 更新对话历史
    dialogue_history += f"Human: {question}\\nAI: {answer}\\n"
    # 保存答案到本地文件
    with open('dialogue_history.txt', 'a') as file:
        file.write(f"Q: {question}\\nA: {answer}\\n\\n")
    return answer

# 例子：进行三轮问答
ask_question("What is the capital of France?")
ask_question("What is the population of Paris?")
ask_question("Tell me about the Eiffel Tower.")

# 请根据实际情况自由添加更多的问答轮次

