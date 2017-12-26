from django.conf.urls import url
from online.views import views, v_table, offical

urlpatterns = [
    url(r'^test/$',                       views.test,                      name='test'),
    url(r'^home/$',                       views.home,                      name='home'),
    url(r'^index/$',                      views.index,
        name='index'),
    url(r'^ajax/$',                       views.ajax,                      name='ajax'),
    url(r'ajax_test_add',                 views.ajax_test_add,
        name='ajax_test_add'),
    url(r'ajax_test_api_test',            views.ajax_test_api_test,
        name='ajax_test_api_test'),
    url(r'^ajax_table/$',                 v_table.ajax_table,
        name='ajax_table'),
    url(r'ajax_table_company',            v_table.ajax_table_company,
        name='ajax_table_company'),
    url(r'^test_tree/$',                  v_table.test_tree,
        name='test_tree'),
    url(r'ajax_jquery_tree',              v_table.ajax_jquery_tree,
        name='ajax_jquery_tree'),
    url(r'^bt_test01/$',                  v_table.bt_test01,
        name='bt_test01'),

    # ------------------------------------以下为正式系统URL----------------------------------------

    # 登陆界面
    url(r'^$',                            offical.login,
        name='login'),
    # 注销
    url(r'^logout/$',                     offical.logout,
        name='logout'),

    # 主界面
    url(r'^overview/$',                   offical.overview,
        name='overview'),

    # 图表界面
    url(r'^big_Pie/$',                    offical.big_Pie,
        name='big_Pie'),

    # 表格界面
    url(r'^tableFrame/(\w*/*)$',
        offical.tableFrame,              name='tableFrame'),

    # 表单群界面
    url(r'^inputFrame/(\w*/*)$',
        offical.inputFrame,              name='inputFrame'),

    # 附件界面
    url(r'^attachFrame/(\w*/*)$',
        offical.attachFrame,             name='attachFrame'),

    # ajax
    url(r'ajax_table_data',               offical.ajax_table_data,
        name='ajax_table_data'),
    url(r'ajax_tree_data',                offical.ajax_tree_data,
        name='ajax_tree_data'),
    url(r'ajax_treeTable',                offical.ajax_treeTable,
        name='ajax_treeTable'),
    url(r'getDataForOverview',            offical.getDataForOverview,
        name='getDataForOverview'),
    url(r'get_Pie_Data',                  offical.get_Pie_Data,
        name='get_Pie_Data'),
    url(r'list_file',                     offical.list_file,
        name='list_file'),
    url(r'get_file_url',                  offical.get_file_url,
        name='get_file_url'),




]
