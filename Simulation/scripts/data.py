import xlrd
import datetime
import os
import sys

if __name__ == "__main__":
    # django在启动的时候 就会往全局的大字典中设置一个键值对  值是暴露给用户的配置文件的路径字符串
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Simulation.settings.dev')
    import django
    django.setup()
    from opera import models
    file = r"苏州火车站数据6.15v2.0.xlsx"
    def read_excel():
        """读取excel文件"""
        data_list = []
        book = xlrd.open_workbook(filename=file)

        # 获取索引为3的sheet
        sheet3 = book.sheet_by_index(3)
        # 获取所有的行
        nrows = sheet3.nrows
        # 获取第2行到最后一行数据
        for i in range(2,nrows):
            row_data = sheet3.row_values(i)
            data_dic = {
                "scheme_id":"方案1",
                # "data_dt":datetime.datetime.strptime(row_data[3].split(" ")[0],"%Y-%m-%d").date(),
                "line_id":row_data[0],
                "global_code":int(row_data[1]),
                "dir":row_data[2],
                "arrive_time":datetime.datetime.strptime(row_data[3],"%Y-%m-%d %X"),
                "depart_time":datetime.datetime.strptime(row_data[4],"%Y-%m-%d %X"),
                "ride_time":int(row_data[5]),
                "up_number":int(row_data[6]),
                "down_number":int(row_data[7]),
                "arrive_load_rate":float(row_data[8]),
                "depart_load_rate": 32
            }
            data_list.append(data_dic)
        return data_list

    res = read_excel()
    from opera import models

    for data_dic in res:
        print(data_dic)
        try:
            models.TrainData.objects.create(**data_dic)
        except Exception as e:
            print(e)

    print("数据入库完成")
