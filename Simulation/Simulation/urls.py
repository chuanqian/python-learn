from django.contrib import admin
from django.urls import path, re_path, include
# 对静态文件提供外界访问接口
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('station/', include('station_info.urls')),
    path('opera/', include('opera.urls')),
    path('pasic/', include('passbasic.urls')),
    path('chart/', include('chart.urls')),
    # 上传的文件是根据MEDIA_ROOT的路径下的
    re_path('^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})
]
