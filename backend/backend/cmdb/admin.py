from django.contrib import admin
from django.db.models import Count
from django.contrib import messages

# Register your models here.
from django.http import HttpResponseRedirect
from cmdb.models import *

from urllib.parse import urlencode



class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ('create_time', 'update_time')





@admin.register(IDC)
class IDCAdmin(BaseModelAdmin):
    list_display = ('name', 'address','rack_count', 'contact', 'phone', 'email','remark')
    search_fields = ('name', 'contact')
    def get_queryset(self, request):
        # 添加虚拟字段_rack_count用于排序
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_rack_count=Count('rack'))  # 统计关联机柜数量:ml-citation{ref="4,8" data="citationList"}
        return queryset
    def rack_count(self, obj):
        # 返回注解字段值
        return obj._rack_count
    rack_count.admin_order_field = '_rack_count'  # 绑定排序字段:ml-citation{ref="8" data="citationList"}
    rack_count.short_description = '机柜数量'
    




@admin.register(Rack)
class RackAdmin(BaseModelAdmin):
    list_display = ('name','server_count')
    search_fields = ('name',)
    def get_queryset(self, request):
        # 添加虚拟字段_rack_count用于排序
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_server_count=Count('server'))  
        return queryset
    def server_count(self, obj):
        # 返回注解字段值
        return obj._server_count
    server_count.admin_order_field = '_server_count'
    server_count.short_description = '服务器数量'
  
    


@admin.register(SSHUser)
class SSHUserAdmin(BaseModelAdmin):
    list_display = ('get_name',)
    def get_name(self,obj):
        return obj.name
    get_name.short_description = "用户名"
    get_name.admin_order_field = 'name'
    search_fields = ('name',)

@admin.register(Server)
class ServerAdmin(BaseModelAdmin):
    list_display = ('get_name','get_ssh_ip','get_rack_name','system_product','status','remark',)

    
  
    

    def get_name(self,obj):
        return obj.name
    def get_ssh_ip(self,obj):
        return obj.ssh_ip
    def get_rack_name(self, obj):
        return obj.rack.idc.name + '-' + obj.rack.name if obj.rack else '-' 

    #复制
    save_as=True
    def save_model(self, request, obj, form, change): 
        if '_saveasnew' in request.POST:
            original_pk = request.resolver_match.kwargs['object_id']
            original = obj._meta.concrete_model.objects.get(id=original_pk)
            # Iterate through all it's properties
            obj.save()
        
        
        #创建新对象（排除ID）
        
        name=f"{original.name}_副本",
        rack=original.rack,
        ssh_user=original.ssh_user,
        ssh_ip=original.ssh_ip,
        ssh_port=original.ssh_port,
        uuid='',  # 清空唯一标识
        cpu=original.cpu,
        memory=original.memory,
        disk=original.disk,
        system_product=original.system_product,
        daq=original.daq,
        status=original.status,
        remark=original.remark
    
    
    get_ssh_ip.short_description = 'SSH地址'
    get_ssh_ip.admin_order_field = 'ssh_ip'
    get_name.short_description = '主机名'
    get_name.admin_order_field = 'name'
    search_fields = ('name','ssh_ip',)

    get_rack_name.short_description = '机柜名称'    
    get_rack_name.admin_order_field = 'rack__name' 

