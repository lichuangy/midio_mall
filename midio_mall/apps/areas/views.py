import http.cookiejar

from django.shortcuts import render

from django.http.response import JsonResponse
from django.views import View

# Create your views here.
"""
    需求：
        获取省份信息
    
    前端：
        页面加载的时候，会发送axios请求，来获取省份信息
    后端
        请求          不需要请求参数
        业务逻辑       查询省份信息
        响应          Json
        
    路由   areas/
    步骤
        # 1.查询省份信息
        # 2.将对象转换成字典
        # 3.返回响应
"""
"""
    # 缓存的功能实现 1.导入模块
    from django.core.cache import cache
            # 获取缓存的数据
            province_list = cache.get('province')
            # 判断缓存是否有数据，如果没有则执行👇
            if province_list is None:
                pass
            # 缓存的功能实现 保存缓存数据
            # cache.set(key,value,expire)
            # cache.set('province': province_list, 24 * 3600)
"""
from apps.areas.models import Area
# 缓存的功能实现 1.导入模块
from django.core.cache import cache
class AreasView(View):
    def get(self, request):
        # 获取缓存的数据
        province_list = cache.get('province')
        # 判断缓存是否有数据，如果没有则执行👇
        if province_list is None:
            # 1.查询省份信息，得到的是一个对象
            provinces = Area.objects.filter(parent=None)
            province_list = []
            # 2.将对象转换成字典列表
            for province in provinces:
                province_list.append({'id': province.id,
                                      'name': province.name})
            # 缓存的功能实现 保存缓存数据
            cache.set('province',province_list, 24 * 3600)
        # 3.返回响应
        return JsonResponse({"code":0,'errmsg':'ok','province_list':province_list})

"""
    需求：
    获取 市区县信息
    
    前端：
        当修改省市的时候，会发送axios请求，获取下一级的信息
    
    后端
        请求          传递省份id 市id
        业务逻辑       根据id查询信息，将查询结果转换为字典列表
        响应          Json
        
    路由   areas/id
    步骤
        # 1.获取省份🆔id，市🆔id，查询省份信息
        # 2.将对象转换成字典
        # 3.返回响应
"""

class CityView(View):
    def get(self, request, id):
        data_list = cache.get('city:%s'%id)
        if data_list is None:
            city = Area.objects.get(id=id)
            surname = city.subs.all()
            data_list=[]
            for item in surname:
                data_list.append( {
                        'id': item.id,
                        'name': item.name
                    })
            cache.set('city:%s'%id,data_list,24*3600)
        return JsonResponse({'code':0,'errmsg': 'ok','sub_data':{'subs': data_list}})
# 1.获取省份🆔id，市🆔id，查询省份信息
# 2.将对象转换成字典
# 3.返回响应