import json
import csv
import os
import datetime
from json2xml import json2xml
from json2xml.utils import readfromstring, readfromjson

data = []
gateway_data_each_time = []
device_data_list_each_time = []
outdata = []

path_dir = "D:/2021"


in_file = "digitalTwin_data.log.20211202"
out_file = "data.1202.gt.csv"

heart_rate_idx = 2
step_count_idx = 3
device_wear_idx= 8
rssi_idx = 10

ff = open(out_file, "a")
#csvwriter = csv.writer(open(out_file,"w"))
csvwriter = csv.writer(open(out_file,"a"), lineterminator='\n')


def read_user_data(user_data,gateway_time,gateway_id):
    if user_data['type'] == 'b':
        band_data = user_data['d']
        heart_rate = band_data[heart_rate_idx]
        step_count = band_data[step_count_idx]
        device_wear = band_data[device_wear_idx]
        rssi_user = band_data[rssi_idx]
        out_data_for_user = [gateway_id,user_data['id'], user_data['dt'], heart_rate, step_count, device_wear, rssi_user, gateway_time]
        print(out_data_for_user)
        outdata.append(out_data_for_user)
        csvwriter.writerow(out_data_for_user)


def read_log_line_by_line(line_data):
    gateway_data_each_time = line_data['d'][0]
    print(gateway_data_each_time['bid'])  # print gateway bid
    print(gateway_data_each_time['dt'])
    gt = gateway_data_each_time['dt']
    gwid = gateway_data_each_time['bid']
    device_data_list_each_time = gateway_data_each_time['d']  # list

    for user in device_data_list_each_time:
        read_user_data(user,gt,gwid)
        #print("print!!")


in_filee = path_dir + '/' + in_file
with open(in_filee) as f:
    for line in f:
        try:
            read_log_line_by_line(json.loads(line.replace("'", "\"")))
        except:
            print('error on read data at line:')

data.append(json.loads(line.replace("'", "\"")))

csvwriter.writerow(data[0].keys())
for line in data:
    csvwriter.writerow(line.values())

print(json2xml.Json2xml(data).to_xml())
ff.write(json2xml.Json2xml(data).to_xml())