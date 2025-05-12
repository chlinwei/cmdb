from django.contrib import admin
from django.db.models import Count
from django.forms.models import model_to_dict

# Register your models here.
from django.http import HttpResponseRedirect
from cmdb.models import *

from django.shortcuts import redirect
from django.urls import reverse
from django.http import Http404

from django.contrib.admin.utils import unquote
from django.utils.html import format_html
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

    actions = ['clone_to_add']
    def get_name(self,obj):
        return obj.name
    def get_ssh_ip(self,obj):
        return obj.ssh_ip
    def get_rack_name(self, obj):
        return obj.rack.idc.name + '-' + obj.rack.name if obj.rack else '-' 

    #复制
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        clone_from_id = request.GET.get('clone_from')
        
        if clone_from_id:
            try:
                original_obj = self.get_object(request, unquote(clone_from_id))
                initial = model_to_dict(original_obj, exclude=['id', 'unique_field'])
                # 处理唯一字段（示例：名称追加'副本'）
                if 'name' in initial:
                    initial['name'] = f"{initial['name']}（副本）"
            except Http404:
                pass
        return initial
    def clone_to_add(self, request, queryset): 
        # 构造添加页面URL并附带克隆参数
        # 限制单选
        if queryset.count() != 1:
            self.message_user(request, "请选择单个对象进行克隆", level='ERROR')
            return
        obj = queryset.first()
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        add_url = reverse(f'admin:{app_label}_{model_name}_add') 
        params = f'?clone_from={obj.id}'  # 传递原对象ID
        return redirect(add_url + params)
        
        

    
    
    get_ssh_ip.short_description = 'SSH地址'
    get_ssh_ip.admin_order_field = 'ssh_ip'
    get_name.short_description = '主机名'
    get_name.admin_order_field = 'name'
    search_fields = ('name','ssh_ip',)

    get_rack_name.short_description = '机柜名称'    
    get_rack_name.admin_order_field = 'rack__name' 
    clone_to_add.short_description = '复制'
    clone_to_add.admin_order_field = 'clone_to_add'

    clone_to_add.size = 'smnall'
    clone_to_add.icon = 'far fa-clone'






@admin.register(BusinessLine)
class BusinessLineAdmin(BaseModelAdmin):
    list_display = ('get_name',)
    search_fields = ('name',)
    def get_name(self,obj):
        return obj.name
    get_name.short_description = '业务名'
    get_name.admin_order_field = 'name'
    





@admin.register(Project)
class ProjectAdmin(BaseModelAdmin):
    list_display = ('get_name','list_businesses',)
    search_fields = ('name',)
    def list_businesses(self,obj):
        links = []
        for business in obj.businesses.all():
            url = reverse('admin:cmdb_businessline_change', args=[business.id])  # 替换appname为实际应用名
            links.append(f'<a href="{url}">{business.name}</a>')
        return format_html(", ".join(links)) if links else "-"
    list_businesses.short_description = '所属业务线'
    def get_name(self,obj):
        return obj.name
    get_name.short_description = '项目名'
    get_name.admin_order_field = 'name'