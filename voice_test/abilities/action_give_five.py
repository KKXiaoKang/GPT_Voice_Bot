#!/usr/bin/env python3
import rospy
import rosbag
import numpy as np
import time
from typing import List
import requests
import json
from collections import defaultdict

from .registry import ability
from .utils import Replay
from .kuavoRobotSDK import kuavo


@ability(
    name="give_five",
    description="机器人击掌",
    parameters=[
        {
            "name": "obj_name",
            "description": "物品名称",
            "type": "str",
            "required": True
        }
    ],
    output_type="None",
)
async def give_five(obj_name: str):
    print("调用了give_five函数")
    # 初始化机器人
    robot_instance = kuavo("3_7_kuavo")
    
    # 控制进入到手臂规划模式
    robot_instance.set_robot_arm_ctl_mode(True)
    
    # 手臂归中
    robot_instance.set_robot_arm_recenter() 