# cmdb/models/idc.py
from django.db import models

from .utils.basemodel import BaseModel
from account.models import User

class IDC(BaseModel):
    name = models.CharField('机房名称', max_length=64, unique=True)
    address = models.CharField('地址', max_length=255, blank=True)
    contact = models.CharField('联系人', max_length=32, blank=True)
    phone = models.CharField('联系电话', max_length=32, blank=True)
    email = models.EmailField('联系邮箱', blank=True)

    class Meta:
        db_table = 'cmdb_idc'
        verbose_name = 'IDC机房'
        verbose_name_plural = 'IDC机房'
        ordering = ['-id']
        unique_together = ('name',)

    def __str__(self):
        return self.name
    def rack_count(self):
        return self.rack_set.count()
    rack_count.short_description = '机柜数量'

class Rack(BaseModel):
    idc = models.ForeignKey('IDC', on_delete=models.CASCADE,verbose_name='所属机房')
    name = models.CharField(max_length=32)  # 如 "A01", "B02"

    class Meta:
        unique_together = ('idc', 'name')
        verbose_name = "机柜"
        verbose_name_plural = '机柜'
        ordering = ['-id']
        unique_together = ('name',)
    def __str__(self):
        return self.idc.name + '-' + self.name
    def server_count(self):
        return self.server_set.count()
    server_count.short_description = '服务器数量'






class SSHUser(BaseModel):
    STATUS = (
        ('0', u'启用'),
        ('1', u'停用'),
    )
    password = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='SSH 密码')

    class Meta:
        ordering = ['-id']
        unique_together = ['name']





class Server(BaseModel):
    STATUS = (
        ('0', u'下线'),
        ('1', u'在线'),
    )
    users = models.ManyToManyField(User, default='', null=True, blank=True, verbose_name='业务相关的用户')
    rack = models.ForeignKey(Rack, default='', null=True, blank=True, on_delete=models.SET_DEFAULT, verbose_name='所属机柜')
    ssh_user = models.ForeignKey(SSHUser, default='', null=True, blank=True, on_delete=models.SET_DEFAULT, verbose_name='SSH用户')
    ssh_ip = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='SSH IP地址/主机名')
    ssh_port = models.IntegerField(default=22, max_length=5, null=True, blank=True, verbose_name='SSH 端口')
    uuid = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='UUID')
    cpu = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='CPU')
    memory = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='内存')
    disk = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='磁盘大小')
    system_product = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='服务器类型')
    daq = models.TextField(default='', null=True, blank=True, verbose_name='数据采集')
    status = models.CharField(default='1', max_length=2, choices=STATUS, verbose_name='运行状态')

    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.name