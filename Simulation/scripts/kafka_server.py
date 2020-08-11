# -*- coding: utf-8 -*-
import json
import time
from kafka import KafkaProducer
list = '192.168.30.41:9092'
# 就是吧txt里面的文件，写入kafka中，然后用kafka的接收端去获取服务端发送的数据
# 生产者
producer = KafkaProducer(bootstrap_servers=list)

file = './10.txt'

f = open(file, 'r')

while True:
    result = f.readline()
    if result == "" or result is None:
        break

    result.replace("\n", "")
    msg_list = result.split('"')
    msg = []
    send_msg = {}
    for i in msg_list:
        if i == "{" or i == "}" or i == ":{" or i == ":" or i == "}," or i == ",":
            continue
        msg.append(i)

    msgHead_dict = {}
    msgHead_dict[msg[1]] = int(msg[2][1:-1])
    msgHead_dict[msg[3]] = int(msg[4][1:-1])
    msgHead_dict[msg[5]] = msg[6]
    msgbody_dict = {}
    msgbody_dict[msg[8]] = int(msg[9][1:-1])
    msgbody_dict[msg[10]] = int(msg[11][1:-1])
    msgbody_dict[msg[12]] = int(msg[13][1:-1])
    msgbody_dict[msg[14]] = int(msg[15][1:-1])
    msgbody_dict[msg[16]] = msg[17]
    msgbody_dict[msg[18]] = msg[19]
    msgbody_dict[msg[20]] = msg[21]
    msgbody_dict[msg[22]] = int(msg[23][1:-1])
    msgbody_dict[msg[24]] = msg[25][1:-1]
    msgbody_dict[msg[26]] = msg[27][1:-1]
    msgbody_dict[msg[28]] = msg[29][1:-1]
    msgbody_dict[msg[30]] = ""
    msgbody_dict[msg[32]] = int(msg[33][1:-1])
    msgbody_dict[msg[34]] = int(msg[35][1:-1])
    msgbody_dict[msg[36]] = int(msg[37][1:-3])

    send_msg["msgHead"] = msgHead_dict
    send_msg["msgBody"] = msgbody_dict

    msg = json.dumps(send_msg)
    producer.send('LINE10_ATS', msg, partition=0)
    print("send msg")
    time.sleep(1)
producer.close()

msg_dict = {
    "msgHead": {
        "msgId": "2002",
        "lineId": "17",
        "sendTime": "201910261650"
    },
    "msgBody": {
        "winHandle": "4118",
        "devName": "G07D",
        "globalId": "1005",
        "destinationId": "01",
        "otpTime": "-105"
    }
}