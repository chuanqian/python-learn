
def file_iterator(file_name, chunk_size=512):  # 用于形成二进制数据
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

import datetime
def get_data_list(first_time,second_time,second,ride_time):
    date = str(datetime.datetime.now().date())
    # print(date)  # "2020-07-28"
    start_time = first_time + ":00"
    end_time = second_time + ":00"
    stat_tm_str = date + " " + start_time
    end_tm_str = date + " " + end_time

    stat_tm = datetime.datetime.strptime(stat_tm_str, '%Y-%m-%d %X')
    end_tm = datetime.datetime.strptime(end_tm_str, '%Y-%m-%d %X')
    data_list = []
    while True:
        if stat_tm > end_tm:
            return data_list
        depart_time = stat_tm + datetime.timedelta(seconds=ride_time)
        data_dic = {
            "arrive_time":str(stat_tm),
            "depart_time":str(depart_time),
            "ride_time":ride_time,
        }
        data_list.append(data_dic)
        stat_tm = stat_tm + datetime.timedelta(seconds=second)
