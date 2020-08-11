from django.test import TestCase

# Create your tests here.

# import datetime
# def get_data_list(first_time,second_time,second,ride_time):
#     date = str(datetime.datetime.now().date())
#     # print(date)  # "2020-07-28"
#     start_time = first_time + ":00"
#     end_time = second_time + ":00"
#     stat_tm_str = date + " " + start_time
#     end_tm_str = date + " " + end_time
#
#     stat_tm = datetime.datetime.strptime(stat_tm_str, '%Y-%m-%d %X')
#     end_tm = datetime.datetime.strptime(end_tm_str, '%Y-%m-%d %X')
#     data_list = []
#     while True:
#         if stat_tm > end_tm:
#             return data_list
#         depart_time = stat_tm + datetime.timedelta(seconds=ride_time)
#         data_dic = {
#             "arrive_time":str(stat_tm),
#             "depart_time":str(depart_time)
#         }
#         data_list.append(data_dic)
#         stat_tm = stat_tm + datetime.timedelta(seconds=second)
#
# res = get_data_list(125,45)
# for i in res:
#     print(i)

#
# start = 1
# for i in range(100):
#     print(start)
#     start += 1

# import datetime
# date = datetime.datetime.now().date()
# arrive_time = str(date) +" "+str("09:00:00")
# depart_time = str(date) +" "+str("09:00:40")
# ride_time = datetime.datetime.strptime(depart_time,"%Y-%m-%d %X") - datetime.datetime.strptime(arrive_time,"%Y-%m-%d %X")
# print(arrive_time)
# print(depart_time)
# print(int(ride_time.seconds))
l = [1,2,3,4,5]
res = l.pop()
print(res)


