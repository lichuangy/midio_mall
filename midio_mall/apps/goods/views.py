from django.shortcuts import render

# Create your views here.

#######upload image########
# from fdfs_client.client import Fdfs_client
# # 1. create client
# client = Fdfs_client('utils/fastdfs/client.conf')
#
# client.upload_by_filename('/home/lc/桌面/image/c.png')

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



