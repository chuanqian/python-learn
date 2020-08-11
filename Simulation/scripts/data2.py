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
        sheet3 = book.sheet_by_index(2)
        # 获取所有的行
        nrows = sheet3.nrows
        # 获取第2行到最后一行数据
        for i in range(1,nrows):
            row_data = sheet3.row_values(i)
            date,time1 = row_data[2].split(" ")
            # 2020年6月12日 18:00:00
            str1 = "".join(time1.split(":"))
            # print(str1)
            data_dic = {
                "scheme_id":"方案1",
                # datetime.datetime.strptime  "%Y-%m-%d"
                # "data_dt":str(datetime.datetime.strptime("2020-06-12","%Y-%m-%d").date()),
                "line_id":row_data[0],
                "dir":str(row_data[1]),
                "stat_tm":date[0:4]+"-0"+date[5]+"-"+date[-3:-1]+" "+time1,
                "entry_quantity":int(row_data[3]),
                "exit_quantity":int(row_data[4]),
            }
            data_list.append(data_dic)
        return data_list
    res = read_excel()
    # for i in res:
    #     print(i)
    from opera import models

    for data_dic in res:
        # 2020年6月12日 14:15:00
        print(data_dic)
        try:
            models.FlowInOutDetail.objects.create(**data_dic)
        except Exception as e:
            print(e)

    print("数据入库完成")
