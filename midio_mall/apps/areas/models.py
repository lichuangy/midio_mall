from django.db import models

# Create your models here.
class Area(models.Model):
    """省市区"""
    name = models.CharField(max_length=20,verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True, verbose_name='上级行政区')
    class Meta:
        db_table = "tb_areas"
        verbose_name = "省市区"
        verbose_name_plural = "省市区"

    def __str__(self):
        return self.name

"""
查询省的信息
Area.objects.filter(parent__isnull=True)
Area.objects.filter(parent_id__isnull=True)
Area.objects.filter(parent_id=None)

查询市信息
Area.objects.filter(parent=130000)

查询区县信息
Area.objects.filter(parent=130600)

获取省
province=Area.objects.get(id=130000)
 通过省获取市
province.subs.all()

获取市
city=Area.objects.get(id=130600)
通过市获取县区
city.subs.all()

"""


