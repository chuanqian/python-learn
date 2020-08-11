from rest_framework.response import Response

# 自定义响应模块 生成一个对象
class APIResponse(Response):
    # 响应状态码，响应字符串,响应资源(数据)，网络状态码，响应头，响应异常处理，
    def __init__(self,data_status=1,data_msg='ok',results=None,http_status=None,headers=None,exception=False,**kwargs):
        data = {
            'status':data_status,
            'msg':data_msg
        }
        if results is not None:
            data['results'] = results
        data.update(kwargs)
        super().__init__(data=data,status=http_status,headers=headers,exception=exception)


