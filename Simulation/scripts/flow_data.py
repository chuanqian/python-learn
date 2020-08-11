import xlrd
import datetime
import os
import sys
LINE_DIC = {
    "1号线":"01",
    "2号线":"02",
    "3号线":"03",
    "4号线":'04',
    "5号线":'05',
    "6号线":'06',
    "7号线":'07',
    "8号线":'08',
}
if __name__ == "__main__":
    # django在启动的时候 就会往全局的大字典中设置一个键值对  值是暴露给用户的配置文件的路径字符串
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Simulation.settings.dev')
    # import django
    # django.setup()
    # from opera import models
    file = r"客流数据模板.xlsx"
    def read_excel():
        """读取excel文件"""
        data_list = []
        book = xlrd.open_workbook(filename=file)

        # 获取索引为3的sheet
        sheet0 = book.sheet_by_index(0)
        # 获取所有的行
        nrows = sheet0.nrows
        # 获取第2行到最后一行数据
        for i in range(2,nrows):
            row_data = sheet0.row_values(i)
            date = str(datetime.datetime.now().date())
            # print(str1)
            data_dic = {
                "scheme_id":"方案1",
                "line_id":LINE_DIC.get(row_data[1]),
                "dir":"1" if row_data[2] == "上行" else "2",
                "stat_tm":date+" "+row_data[3],
                "entry_quantity":int(row_data[4]),
                "exit_quantity":int(row_data[5]),
            }
            data_list.append(data_dic)
        return data_list
    res = read_excel()
    # for i in res:
    #     print(i)

    for data_dic in res:
        # 2020年6月12日 14:15:00
        print(data_dic)
        # try:
        #     models.FlowInOutDetail.objects.create(**data_dic)
        # except Exception as e:
        #     print(e)

    print("数据入库完成")
