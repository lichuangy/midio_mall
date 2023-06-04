from django.shortcuts import render

# Create your views here.

#######upload image########
# from fdfs_client.client import Fdfs_client
# # 1. create client
# client = Fdfs_client('utils/fastdfs/client.conf')
#
# client.upload_by_filename('/home/lc/桌面/image/c.png')

# 首页商品展示的实现
from django.views import View
from utils.goods import get_categories
from apps.contents.models import ContentCategory
class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        # 查询商品频道和分类
        categories = get_categories()

        contents = {}
        content_categorise = ContentCategory.objects.all()
        for cat in content_categorise:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        # 渲染模板的上下文
        context = {
            'categories': categories,
            'contents':contents

        }
        return render(request, 'index.html', context)


"""
需求：
    根据点击的分类来获取分类数据（有排序有分页）
前端：
    前端会发送一个axios中，分类id在路由中
    分页的页码（第几页数据），每页多少条数据，排序也会传递过来
后端：
    请求：接收参数
    业务逻辑：根据需求查询数据，将对象数据转换为字典数据，返回响应
    响应：JSON

    路由：GET      /list/category_id/skus/
    步骤：
        1.接收参数
        2.获取分类id
        3.根据分类id进行分类数据的查询验证
        4.获取面包屑数据
        5.查询分类对应的sku数据，然后排序，然后分页
        6.返回响应
"""

from apps.goods.models import GoodsCategory, SKU
from django.http import JsonResponse
from utils.goods import get_breadcrumb
from django.core.paginator import Paginator
class ListView(View):
    def get(self,request,category_id):
        # 1.接收参数
        # 排序字段
        ordering = request.GET.get('ordering')
        page_size = request.GET.get('page_size')
        page = request.GET.get('page')
        # 2.获取分类id
        # 3.根据分类id进行分类数据的查询验证
        try:
            category=GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({'code':400,'errmsg':'can shu que shi!'})
        # 4.获取面包屑数据
        breadcrumb=get_breadcrumb(category)
        # 5.查询分类对应的sku数据，然后排序，然后分页
        skus=SKU.objects.filter(category=category,is_launched=True).order_by(ordering)
        # 每页几条数据
        paginator=Paginator(skus,per_page=page_size)
        # 获取指定页的数据
        page_skus = paginator.page(page)
        sku_list=[]
        # 将对象转换为字典
        for sku in page_skus:
            sku_list.append({
                'id':sku.id,
                'name':sku.name,
                'price':sku.price,
                # 该处的sku.default_image.url访问默认存储类的url方法
                'default_image_url': 'http://192.168.44.130:8888/'+sku.default_image_url,
            })

        # 获取总页码
        total_page = paginator.num_pages
        # 6.返回响应
        return JsonResponse({
                'code':0,
                'errmsg':'ok',
                 'breadcrumb': breadcrumb,  # 面包屑导航
                'list':sku_list,
                'count':total_page
        })

# ##############################搜索功能的实现#################
"""
搜索：
1.不实用like
2.使用全文检索
3.全文检索需要配合搜索引擎来实现
4.搜索引擎

原理：对数据进行拆分
我爱北京天安门                 我爱，北京，天安门
王红姑娘，我内里挂念你             王红姑娘，我爱你，睡不着觉，挂念你
我夜里睡不着觉                 我，睡不着觉，夜里

5.Elasticsearch
进行分词操作，将一句话拆分为多个单词或字
6.数据  <--------Haystack---------> elasticsearch

"""

"""
数据《---haystack---》elasticsearch
借助于haystack帮助我们查询数据
"""
from haystack.views import SearchView


# 该搜索类继承自SearchView没有as_view()方法
class SearchView(SearchView):
    # 该方法取自SearchView中的源码
    def create_response(self):
        # 获取搜索的结果---抄写SearchView中的源代码，产生响应返回给服务器
        # 理解为context为 haystack 对接 elasticSearch后查询到的 响应结果
        context = self.get_context()
        # 该如何知道context中有那些数据呢
        # 添加断点来进行分析---调试问题，解决问题
        sku_list = []
        # 利用断点查到 获取商品列表为 context['page'].object_list
        for sku in context['page'].object_list:
            sku_list.append({
                # 前4个为context下page中的内容
                'id': sku.object.id,
                'name': sku.object.name,
                'price': sku.object.price,
                # 该处的url为访问fastfds中storage的方法
                'default_image_url': 'http://192.168.44.130:8888/' + sku.object.default_image_url,
                # 下面三个为context下的内容---------------------------
                'searchkey': context.get('query'),
                'page_size': context['page'].paginator.num_pages,  # 当前页面页码
                'count': context['page'].paginator.count  # 查询到的结果数量
            })
        # 这里后端需求的数据中，只需求了相关数据，并没有要求code和errmsg
        return JsonResponse(sku_list, safe=False)
    # HAYSTACK_SEARCH_RESULTS_PER_PAGE = 5  # 设置分页，每页显示五条
