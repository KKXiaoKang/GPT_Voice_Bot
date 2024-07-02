import base64
import datetime
import requests
import os 
import sys
import json
import argparse
import yaml

import cv2 
sys.path.append("../../")
sys.path.append("../")
sys.path.append("./")

import cv2
from basic_structures.evnet_node import EventNode
from utils.agent_log import log_info, get_uuid

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def image_to_base64(image_np):
 
    image = cv2.imencode('.jpg',image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]
 
    return image_code

def video_understand(img, key_region=None, count=0, map_name_list=""):

    os.environ['http_proxy'] = "http://127.0.0.1:7890"
    os.environ['https_proxy'] = "http://127.0.0.1:7890"

    log_info("****************** Video Understand ********************")
    # Getting the base64 string
    # base64_image = encode_image(image_path)

    base64_image = image_to_base64(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    base64_key_region = image_to_base64(img)

    # image_to_base64(key_region)
    data_id = get_uuid()

    cv2.imwrite(f'/home/eilab/mzs/robo-agent-v2/robot_agent/models/outputs/4v-output/{data_id}-input1.jpg', img)
    # cv2.imwrite('/home/robotarts/data/output_pic/gpt2.jpg', key_region)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer your-openAI-key"
    }

    pre_know = """
    你是一个机器人助手，可以帮助用户做一些事情
    你可以使用如下工具: ['vacuum_return_to_bas) -> None. Usage: 扫地机器人返回基站,', 'vacuum_star) -> None. Usage: 扫地机器人打扫卫生,', 'vacuum_sto) -> None. Usage: 扫地机器人停止打扫任务,', 'vacuum_zoned_clean(pos: string) -> None. Usage: 扫地机器人清扫指定区域,', 'dialog_output(order: string) -> None. Usage: 输出语音，与用户交互,', 'finish(reason: string) -> None. Usage: Use this to shut down once you have accomplished all of your goals, or when there are insurmountable problems that make it impossible for you to finish your task.,', 'turn_off_light(order: string) -> None. Usage: 通过homekit关灯,', 'turn_on_light(brightness: string) -> None. Usage: 通过homekit开灯,'] 
    """

    log_info("*************map_name_list: ", map_name_list)

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f"{pre_know}. 常见的物体有桌子、台灯、矿泉水、橙色饮料、椅子、人,以下是你看的：图一是关键区域的图. 1. description: 请描述图片放到字典中，description为字典的key, 字典的value是对图片的详细描述，尽可能多的物体信息；2. name_state_dict: 按照目标检测的名字来命名图中的物体，并将物体中文名以及状态存到字典中，key为中文名，value是状态； 3. en_cn_dict: 输出图片中物体的中文名对应的英文名放到字典中，其中key是小写英文名，value是中文名； 输出的内容仅为json格式。"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            },
            # {
            # "type": "image_url",
            # "image_url": {
            #     "url": f"data:image/jpeg;base64,{base64_key_region}"
            # }
            # }
        ]
        }
    ],
    "max_tokens": 1000
    }

    b = json.dumps(payload, ensure_ascii=False)
    f2 = open(f'input2.json', 'w')
    f2.write(b)
    f2.close()

    data = {
      "description": "图片展示了一张的桌子，桌子上放着一盏台灯",
      "name_state_dict": {
        "桌子": "黑色，上面有物品",
        "矿泉水": "未开盖，放在桌上",
        "编织椅子": "黑色，无人使用"
      },
      "en_cn_dict": {
        "table": "桌子",
        "chair": "椅子"
      }
    }

    # response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    # log_info(response)
    # data = response.json()['choices'][0]['message']['content']

    log_info("picture desc: ", data)

    # index_start = data.find("{")
    # index_end = data.rfind("}")
    # data = eval(data[index_start:(index_end+1)])

    b = json.dumps(data, ensure_ascii=False)
    f2 = open(f'/home/eilab/mzs/robo-agent-v2/robot_agent/models/outputs/4v-output/{data_id}-out.json', 'w')
    f2.write(b)
    f2.close()

    description = data["description"]
    name = list(data["en_cn_dict"].values())
    data["video_events"] = EventNode(s=datetime.datetime.now(),
                              p="",
                              o=name,  source="video understand",
                              description=description, embedding_key=description,
                              poignancy=5, keywords=('insert_object', name, ""))

    data["en_name_list"] = [name.lower() for name in list(data["en_cn_dict"].keys())]

    return data


if __name__ == "__main__":
    # image_path = "../images/1.jpg"
    # img1 = cv2.imread(image_path)
    # # img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

    # image_path = "../images/1_keyregion.jpg"
    # img2 = cv2.imread(image_path)
    # # img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)


    image_path = "../images/test_imges/he_water.png"
    img1 = cv2.imread(image_path)
    # img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

    image_path = "../images/test_imges/he_water.png"
    img2 = cv2.imread(image_path)
    # img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

    # 5_keyregion.jpg
    gpt_result = video_understand(img1, img2)
    log_info("==================")



