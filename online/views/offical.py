# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-11-30 10:53:03
# @Last Modified by:   Administrator
# @Last Modified time: 2017-12-21 09:19:49
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.http import JsonResponse
from django import forms
from django.urls import reverse
import logging
import datetime
from online.models import *
from .db_api import *

# from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def logUserOperation(request, logname, how='', what=''):
    if logname == 'read':
        return
    logging.getLogger(logname).info('《【%s《】《【%s《】《【%s《】《【%s《】《【%s《】' % (
        str(datetime.datetime.now()), 
        request.META.get('HTTP_X_FORWARDED_FOR').split(',')[-1].strip() if request.META.get('HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR'),
        request.session.get('username'), 
        how, 
        what,
    ))

# 表单
class UserForm(forms.Form): 
    username = forms.CharField(label='用户名', max_length=50)
    password = forms.CharField(label='密　码', max_length=50, widget=forms.PasswordInput())

# --------------------页面--------------------
dict_Eng_Chn = {'Company':     '单位',
                'Init':        '立项',
                'Bidding':     '招标',
                'Contract':    '合同',
                'Alteration':  '变更',
                'SubContract': '分包合同',
                'Budget':      '预算',
                'Payment':     '付款',
}

def login(request):
    '''
        This href is the entrance of system.
    '''
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            password_hash = hash_sha256(password)
            #获取的表单数据与数据库进行比较
            user = table_User.objects.filter(用户名__exact=username, 密码__exact=password_hash)
            if user:
                # 将username写入session
                request.session['username'] = username
                request.session.set_expiry(0)
                #比较成功，跳转至URL: overview                
                logUserOperation(request, 'login_out', sys._getframe().f_code.co_name)
                response = HttpResponseRedirect(reverse('overview'))
                return response
            else:
                # 比较失败，返回登陆页面
                Cnt = '用户名不存在，或密码输入错误<br/>'
                Cnt += '<a href="/online">继续登陆<a>'
                return HttpResponse(Cnt)
    else:
        uf = UserForm()
    return render(request, 'login.html', {'uf':uf})

def logout(request):
    '''
        This href will log you out from system.
    '''
    logUserOperation(request, 'login_out', sys._getframe().f_code.co_name)
    # 清空session
    request.session['username'] = ''
    #比较成功，跳转至登录页
    response = HttpResponseRedirect(reverse('login'))
    return response

def overview(request):
    '''
        The Subjective page of the system.
        To visit this, you must have "can_Visit_Overview"-permission.
    '''
    username = request.session.get('username')
    if not getUserPermission(username).can_Visit_Overview():
        Cnt = '您没有权限登入系统<br/>'
        Cnt += '''<a href="/online">登陆<a>'''
        return HttpResponse(Cnt)
    else:
        return render(request, 'overview.html', {'username': username})

def big_Pie(request):
    '''
        A page which can zoom chart.
        You can check more detail of chart in this page.
        To visit this, you must have "can_Visit_Overview"-permission.
    '''
    if not getUserPermission(request.session.get('username')).can_Visit_Overview():
        Cnt = '您没有权限查看放大数据图<br/>'
        return HttpResponse(Cnt)
    else:
        return render(request, 'big_Pie.html')

def tableFrame(request, key_table):
    '''
        A page which can display list of data.
        This page contains 3 divs. A table, a tree and a condition search form.
        To visit this, you must have "can_Visit_Table(key_table)"-permission.
    '''
    if not getUserPermission(request.session.get('username')).can_Visit_Table(dict_Eng_Chn.get(key_table)):
        Cnt = '您没有权限查看<%s>信息<br/>' % dict_Eng_Chn.get(key_table)
        return HttpResponse(Cnt)
    else:
        return render(request, 'tableFrame.html')

def inputFrame(request, key_table):
    '''
        A page which can display details of an item.
        This page contains several inputs and a few buttons.
        You can new/edit/check information of very item.
        To visit this, you must have "can_Visit_Table(key_table)"-permission.
    '''
    if not getUserPermission(request.session.get('username')).can_Visit_Table(dict_Eng_Chn.get(key_table)):
        Cnt = '您没有权限查看<%s>信息<br/>' % dict_Eng_Chn.get(key_table)
        return HttpResponse(Cnt)
    else:
        return render(request, 'inputFrame.html')

def attachFrame(request, key_table):
    '''
        A page which can display attachments-list of an item.
        This page contains a table and a few buttons.
        You can download/upload/delete attachemnt files of very item.
        To visit this, you must have "can_Get_Attachment_List(key_table)"-permission.
    '''
    if not getUserPermission(request.session.get('username')).can_Get_Attachment_List(dict_Eng_Chn.get(key_table)):
        Cnt = '您没有权限查看<%s>附件信息<br/>' % dict_Eng_Chn.get(key_table)
        return HttpResponse(Cnt)
    else:
        return render(request, 'attachFrame.html')



# --------------------AJAX--------------------
def ajax_treeTable(request):
    '''
        There is no argument to input.
        To visit this, you must have "can_Visit_Overview()"-permission.
        If you have permission, return a JSON like [{}, {}, {}...],
        Otherwise, return a string 'No Permission'.
    '''
    if not getUserPermission(request.session.get('username')).can_Visit_Overview():
        Cnt = 'No Permission'
        return HttpResponse(Cnt)
    else:
        return_json = format_Details_By_Tree()
        logUserOperation(request, 'read', sys._getframe().f_code.co_name)
        return HttpResponse(json.dumps(return_json, ensure_ascii=False, cls=CJsonEncoder), content_type='application/json')

def getDataForOverview(request):
    '''
        There is 1 argument(UDID) to input.
        UDID is the only identification code of an item.
        This function can return a string which describes the item's overview from searching database by UDID.
        To use this funciton, you must have "can_Visit_Overview()"-permission.
        Otherwise, return a string 'No Permission'.
    '''
    if not getUserPermission(request.session.get('username')).can_Visit_Overview():
        Cnt = 'No Permission'
        return HttpResponse(Cnt)
    else:
        # 取得被点击项的立项识别码
        try:
            UDID = int(request.POST.get('UDID'))
            assert UDID > 0
        except:        
            return HttpResponse('')
        # 根据该立项识别码查询数据库
        Init_Infos = read_For_Initiation_GridDialog('WHERE 立项识别码=%s', [UDID])
        Count_Children = get_Children_Count(UDID)
        Bidding_Infos = read_For_Bidding_GridDialog('WHERE 立项识别码=%s', [UDID])
        Contract_Infos = read_For_Contract_GridDialog('WHERE 立项识别码=%s', [UDID])
        list_selfAndGrandchildren = [UDID] + get_All_Grandchildren_UDID(UDID)
        Count_Payment = get_Count_Payment(list_selfAndGrandchildren)
        Payed = get_Sum_Money_Payment(list_selfAndGrandchildren)
        # 构造字符串
        mystring = '本项目编号：{}，项目名称：{}{}'.format(UDID, Init_Infos[0].get('项目名称'), Init_Infos[0].get('分项名称') or '')
        if Init_Infos[0].get('父项立项识别码'):
            mystring += '</br>本项目父项：{}{}'.format(Init_Infos[0].get('父项项目名称'), Init_Infos[0].get('父项分项名称') or '')
        mystring += '</br>建设单位：{}，代建单位：{}'.format(Init_Infos[0].get('建设单位名称'), Init_Infos[0].get('代建单位名称') or '')
        if Count_Children:
            mystring += '</br>本项目共有{}个子项'.format(Count_Children)
        else:
            mystring += '</br>本项目无子项'
        if Contract_Infos:
            mystring += '</br>本项目签订的合同名称：{}，合同类别：{}'.format(Contract_Infos[0].get('合同名称'), Contract_Infos[0].get('合同类别'))
        else:
            mystring += '</br>本项目未签订合同'
        if Bidding_Infos:
            mystring += '</br>通过<strong>{}</strong>方式确定了供应商：<strong>{}</strong>'.format(Bidding_Infos[0].get('招标方式'), Bidding_Infos[0].get('中标单位名称'))
        mystring += '</br>本项目概算：<strong>{}</strong>万元'.format(thousands(float(Init_Infos[0].get('项目概算') or 0)))
        if Count_Payment:
            mystring += '</br>截至目前，本项目已付款{}次，共支付<strong>{}</strong>万元'.format(Count_Payment, thousands(Payed))
        else:
            mystring += '</br>截至目前，本项目尚未开始付款'
        mystring += '。'
        # 输出字符串
        result = str(mystring)
        logUserOperation(request, 'read', sys._getframe().f_code.co_name, 
            'UDID={}'.format(UDID))
        return HttpResponse(result)

def get_Pie_Data(request):
    '''
        There is 1 argument(UDID) to input.
        UDID is the only identification code of an item.
        This function can return a JSON which can draw a pie-chart from searching database by UDID.
        Return chart will be Estimate-Distribution with the item's children, or will be Payment-Information without the item's children.
        To use this funciton, you must have "can_Visit_Overview()"-permission.
        Otherwise, return a string 'No Permission'.
    '''
    if not getUserPermission(request.session.get('username')).can_Visit_Overview():
        Cnt = 'No Permission'
        return HttpResponse(Cnt)
    else:
        # 取得被点击项的立项识别码
        try:
            UDID = int(request.POST.get('UDID'))
            assert UDID > 0
        except:        
            return HttpResponse(json.dumps({}, ensure_ascii=False), content_type='application/json')
        try:
            Init_obj = table_Initiation.objects.filter(立项识别码=UDID)
            assert Init_obj
        except:
            return
        this_project = Init_obj[0].项目名称
        this_estimate = float(Init_obj[0].项目概算 or 0.0)
        if Init_obj[0].分项名称:
            this_project += '-' + Init_obj[0].分项名称
        # 检查该立项下是否有子项
        if get_Children_Count(UDID):    # 若有 输出概算分配图
            title_text = '概算分配'
            subTitle_text = this_project
            item_describe = '额度'
            chart_data = []
            children_UDIDs = list(x.get('立项识别码') for x in table_Initiation.objects.filter(父项立项识别码=UDID).values('立项识别码'))
            undistributed_estimate = float(this_estimate or 0.0)
            for each_UDID in children_UDIDs:
                each_Init_obj = table_Initiation.objects.filter(立项识别码=each_UDID)[0]
                project = each_Init_obj.分项名称 or each_Init_obj.项目名称
                estimate = float(each_Init_obj.项目概算 or 0.0)
                undistributed_estimate -= estimate
                chart_data.append({'value': estimate, 'name': project})
            undistributed_estimate = max(undistributed_estimate, 0.0)
            if undistributed_estimate > 0:
                chart_data.append({'value': undistributed_estimate, 'name': '未分配概算'})
        else:                           # 若无 输出付款比例图
            title_text = '付款情况'
            subTitle_text = this_project
            item_describe = '额度'
            chart_data = []
            # 此处求应付额，分两种，有合同或无合同
            Contract_obj = table_Contract.objects.filter(立项识别码=UDID)
            if Contract_obj:
                payable = float(Contract_obj[0].合同值_最新值 or 0.0)
            else:
                payable = float(Init_obj[0].项目概算 or 0.0)
            Payment_obj = table_Payment.objects.filter(立项识别码=UDID)
            notYet_payment = float(payable or 0.0)
            for each_payment in Payment_obj:
                reason = each_payment.付款事由
                payment = float(each_payment.本次付款额 or 0.0)
                chart_data.append({'value': payment, 'name': reason})
                notYet_payment -= payment
            notYet_payment = max(notYet_payment, 0.0)
            if notYet_payment > 0:
                chart_data.append({'value': notYet_payment, 'name': '未付款额'})
        logUserOperation(request, 'read', sys._getframe().f_code.co_name, 
            'UDID={}'.format(UDID))
        return HttpResponse(json.dumps({'mySeries': chart_data, 'myTitle': title_text, 'mySubTitle': subTitle_text, 'myDescribe': item_describe}, 
                                        ensure_ascii=False), content_type='application/json')

def list_file(request):
    '''
        There is 2 arguments(UDID, key_frame) to input.
        UDID is the only identification code of an item.
        key_frame is classify(单位/立项/合同...) of an item.
        This function can return a JSON which contain a list of very item's attachment-files.
        To use this funciton, you must have "can_Get_Attachment_List(key_frame)"-permission.
        Otherwise, return a string 'No Permission'.
    '''
    key_frame = request.POST.get('key_frame') or ''
    if not getUserPermission(request.session.get('username')).can_Get_Attachment_List(key_frame):
        Cnt = 'No Permission'
        return HttpResponse(Cnt)
    else:
        # 取得云端某文件夹下的文件名列表
        try:
            UDID = int(request.POST.get('UDID'))
            assert UDID > 0
        except:        
            return HttpResponse(json.dumps({}, ensure_ascii=False), content_type='application/json')
        file_list = operateOSS().listfile(key_frame, UDID)
        logUserOperation(request, 'read', sys._getframe().f_code.co_name, 
            'key_frame={}, UDID={}'.format(key_frame, UDID))
        return HttpResponse(json.dumps({'file_list': file_list,}, 
                                        ensure_ascii=False), content_type='application/json')

def get_file_url(request):
    '''
        There is 3 arguments(UDID, key_frame, filename) to input.
        UDID is the only identification code of an item.
        key_frame is classify(单位/立项/合同...) of an item.
        Filename is the name of the selected file.
        This function can return a JSON which contain a string which is a URL-address.
        To use this funciton, you must have "can_Download_Attachment(key_frame)"-permission.
        Otherwise, return a string 'No Permission'.
    '''
    key_frame = request.POST.get('key_frame') or ''
    if not getUserPermission(request.session.get('username')).can_Download_Attachment(key_frame):
        Cnt = 'No Permission'
        return HttpResponse(Cnt)
    else:
        # 取得云端某文件的路径
        try:
            UDID = int(request.POST.get('UDID'))
            assert UDID > 0
        except:
            logUserOperation(request, 'read', sys._getframe().f_code.co_name, 'GET_FAILED')
            return HttpResponse(json.dumps({}, ensure_ascii=False), content_type='application/json')
        filename = request.POST.get('filename')
        url_file = operateOSS().get_file_url(key_frame, UDID, filename)
        logUserOperation(request, 'read', sys._getframe().f_code.co_name, 
            'url_file={}'.format(url_file))
        return HttpResponse(json.dumps({'url_file': url_file,}, 
                                        ensure_ascii=False), content_type='application/json')

def ajax_table_data(request):
    '''
        There is 2 argument(key_table, Init_UDID) to input.        
        key_table is classify(单位/立项/合同...) of an item.
        Init_UDID is the subject UDID of very item.
        This function can find out all children and grandchildren of very item, and give a list with all details of them.
        To use this funciton, you must have "can_Read_Table(key_table)"-permission.
        If you have permission, return a JSON like [{}, {}, {}...],
        Otherwise, return a string 'No Permission'.
    '''
    key_table = request.POST.get('key_table') or ''
    if not getUserPermission(request.session.get('username')).can_Read_Table(key_table):
        Cnt = 'No Permission'
        return HttpResponse(Cnt)
    dict_Head = {
        '单位':     uc.CompanyColLabels,
        '立项':     uc.InitiationColLabels,
        '招标':     uc.BiddingColLabels,
        '合同':     uc.ContractColLabels,
        '分包合同': uc.SubContractColLabels,
        '变更':     uc.AlterationColLabels,
        '预算':     uc.BudgetColLabels,
        '付款':     uc.PaymentColLabels,
    }
    dict_Type = {
        '单位':     uc.CompanyColLabels_Type,
        '立项':     uc.InitiationColLabels_Type,
        '招标':     uc.BiddingColLabels_Type,
        '合同':     uc.ContractColLabels_Type,
        '分包合同': uc.SubContractColLabels_Type,
        '变更':     uc.AlterationColLabels_Type,
        '预算':     uc.BudgetColLabels_Type,
        '付款':     uc.PaymentColLabels_Type,
    }
    dict_API = {
        '单位':     read_For_Company_GridDialog,
        '立项':     read_For_Initiation_GridDialog,
        '招标':     read_For_Bidding_GridDialog,
        '合同':     read_For_Contract_GridDialog,
        '分包合同': read_For_SubContract_GridDialog,
        '变更':     read_For_Alteration_GridDialog,
        '预算':     read_For_Budget_GridDialog,
        '付款':     read_For_Payment_GridDialog,
    }
    try:
        Init_UDID = int(request.POST.get('Init_UDID'))    # 取得被点击的tree-item的id，即立项识别码
        assert Init_UDID > 0
        logUserOperation(request, 'read', sys._getframe().f_code.co_name, 
            'key_table={}, Init_UDID={}'.format(key_table, Init_UDID))
        # 取得该立项下全部后代节点
        if key_table == '预算':
            grandchildern_ids = get_All_Budget_Grandchildren_UDID(Init_UDID)
            t_rows = dict_API[key_table]('where 预算识别码 in %s', [grandchildern_ids + [Init_UDID]])
        else:
            grandchildern_ids = get_All_Grandchildren_UDID(Init_UDID)
            t_rows = dict_API[key_table]('where 立项识别码 in %s', [grandchildern_ids + [Init_UDID]])
    except:
        logUserOperation(request, 'read', sys._getframe().f_code.co_name, 
            'key_table={}'.format(key_table))
        t_rows = dict_API[key_table]()
    t_head = dict_Head[key_table]
    t_type = dict_Type[key_table]
    return_json = {'t_head': json.dumps(t_head, ensure_ascii=False, cls=CJsonEncoder),
                   't_type': json.dumps(t_type, ensure_ascii=False, cls=CJsonEncoder),
                   't_rows': json.dumps(t_rows, ensure_ascii=False, cls=CJsonEncoder),
                  }
    
    return HttpResponse(json.dumps(return_json, ensure_ascii=False, cls=CJsonEncoder), content_type='application/json')

def ajax_tree_data(request):
    '''
        There is 1 argument(key_tree) to input.
        This function only cares whether the argument is '预算', if not the argument will be '立项'.
        To use this funciton, you must have "can_Read_Table('预算')"-permission.
        If you have permission, return a JSON like [{'Id':XXX, 'PId':OOO, 'name': YYY}, {}, {}...],
        Otherwise, return a string 'No Permission'.
    '''
    key_tree = request.POST.get('key_tree')
    if key_tree == '预算' and not getUserPermission(request.session.get('username')).can_Read_Table('预算'):
        Cnt = 'No Permission'
        return HttpResponse(Cnt)
    dict_API = {
        '立项':     read_For_TreeList,
        '预算':     read_Budget_For_TreeList,
    }
    return_json = dict_API[key_tree]()
    logUserOperation(request, 'read', sys._getframe().f_code.co_name, 
        'key_tree={}'.format(key_tree))
    return HttpResponse(json.dumps(return_json, ensure_ascii=False, cls=CJsonEncoder), content_type='application/json')