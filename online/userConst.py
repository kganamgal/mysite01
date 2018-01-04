# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-11-06 10:28:31
# @Last Modified by:   Administrator
# @Last Modified time: 2017-12-12 15:54:55

# Log
LogFields = 'WHO HOW WHAT'.split()
LogFields_Type = '字符串型 字符串型 字符串型'.split()

# Company
Size_Label_Company_MaintainDialog = (80, 20)
CompanyColLabels = '单位识别码 单位名称 单位类别 单位性质 法定代表人 注册资金 单位资质 银行账号 联系人 联系方式 单位备注'.split()
CompanyColLabels_Type = '整数型 字符串型 字符串型 字符串型 字符串型 浮点型 字符串型 字符串型 字符串型 字符串型 文本型'.split()
CompanyFields = '单位识别码 单位名称 单位类别 单位性质 法定代表人 注册资金 单位资质 银行账号 联系人 联系方式 单位备注'.split()
CompanyFields_Type = '整数型 字符串型 字符串型 字符串型 字符串型 浮点型 字符串型 字符串型 字符串型 字符串型 文本型'.split()

# Initiation
InitiationColLabels =      ['立项识别码', '项目名称', '分项名称', '项目概算', '父项立项识别码', '父项项目名称', '父项分项名称', '父项项目概算', '项目概算上限', '建设单位识别码', '建设单位名称', '代建单位识别码', '代建单位名称', '立项文件名称', '立项时间', '已分配概算', '未分配概算', '概算分配比', '概算已付款额', '概算可付余额', '概算付款比', '立项备注']
InitiationColLabels_Type = ['整数型',     '字符串型', '字符串型', '浮点型',  '整数型',        '字符串型',    '字符串型',     '浮点型',      '浮点型',      '整数型',          '字符串型',     '整数型',        '字符串型',    '文本型',      '日期型',   '浮点型',     '浮点型',    '百分比',  '浮点型',       '浮点型',      '百分比',    '文本型']
InitiationFields = '立项识别码 项目名称 分项名称 父项立项识别码 建设单位识别码 代建单位识别码 立项文件名称 立项时间 项目概算 立项备注'.split()
InitiationFields_Type = '整数型 字符串型 字符串型 整数型 整数型 整数型 字符串型 日期型 浮点型 文本型'.split()

# Bidding
Size_Label_Bidding_MaintainDialog = (130, 20)
BiddingColLabels =      ['招标识别码', '招标方式', '项目名称', '分项名称', '中标价', '中标单位名称', '项目概算', '预算控制价', '立项识别码', '招标单位识别码', '招标单位名称', '招标代理识别码', '招标代理单位名称', '招标文件定稿时间', '公告邀请函发出时间', '开标时间', '中标通知书发出时间', '中标单位识别码', '招标备注']
BiddingColLabels_Type = ['整数型',     '字符串型', '字符串型', '字符串型', '浮点型', '字符串型',     '浮点型',   '浮点型',     '整数型',     '整数型',         '字符串型',     '整数型',         '字符串型',         '日期型',           '日期型',             '日期型',   '日期型',             '整数型',         '文本型']
BiddingFields = '招标识别码 立项识别码 招标方式 招标单位识别码 招标代理识别码 预算控制价 招标文件定稿时间 公告邀请函发出时间 开标时间 中标通知书发出时间 中标单位识别码 中标价 招标备注'.split()
BiddingFields_Type = '整数型 整数型 字符串型 整数型 整数型 浮点型 日期型 日期型 日期型 日期型 整数型 浮点型 文本型'.split()

# Contract
ContractColLabels =      ['合同识别码', '合同类别', '合同编号', '合同名称', '合同主要内容', '合同值_最新值', '立项识别码', '项目名称', '分项名称', '招标识别码', '招标方式', '项目概算', '中标价', '甲方识别码', '甲方单位名称', '乙方识别码', '乙方单位名称', '丙方识别码', '丙方单位名称', '丁方识别码', '丁方单位名称', '合同签订时间', '合同值_签订时', '合同值_最终值', '已付款', '已付款占概算', '已付款占合同', '形象进度', '支付上限', '开工时间', '竣工合格时间', '保修结束时间', '审计完成时间', '合同备注']
ContractColLabels_Type = ['整数型',     '字符串型', '字符串型', '字符串型', '文本型',       '浮点型',        '整数型',     '字符串型', '字符串型', '整数型',     '字符串型', '浮点型',   '浮点型', '整数型',     '字符串型',     '整数型',     '字符串型',     '整数型',     '字符串型',     '整数型',     '字符串型',     '日期型',       '浮点型',        '浮点型',        '浮点型', '百分比',       '百分比',       '文本型',   '浮点型',   '日期型',   '日期型',       '日期型',       '日期型',       '文本型']
ContractFields = '合同识别码 立项识别码 招标识别码 合同编号 合同名称 合同主要内容 合同类别 甲方识别码 乙方识别码 丙方识别码 丁方识别码 合同签订时间 合同值_签订时 合同值_最新值 合同值_最终值 形象进度 支付上限 开工时间 竣工合格时间 保修结束时间 审计完成时间 合同备注'.split()
ContractFields_Type = '整数型 整数型 整数型 字符串型 字符串型 字符串型 字符串型 整数型 整数型 整数型 整数型 日期型 浮点型 浮点型 浮点型 字符串型 浮点型 日期型 日期型 日期型 日期型 文本型'.split()

# Budget
BudgetColLabels =      ['预算识别码', '预算名称', '预算周期', '预算总额', '预算上限', '预算已付额', '预算余额', '父项预算识别码', '父项预算名称', '父项预算周期', '父项预算额', '预算已付比', '已分配预算', '未分配预算', '预算分配比', '预算备注']
BudgetColLabels_Type = ['整数型',     '字符串型', '字符串型', '浮点型',  '浮点型',   '浮点型',     '浮点型',   '整数型',         '字符串型',   '字符串型',   '浮点型',    '百分比',      '浮点型',     '浮点型',    '百分比',    '字符串型']
BudgetFields = '预算识别码 父项预算识别码 预算名称 预算周期 预算总额 预算备注'.split()
BudgetFields_Type = '整数型 整数型 字符串型 字符串型 浮点型 字符串型'.split()

# Payment
PaymentColLabels =      ['付款识别码', '付款登记时间', '付款支付时间', '付款事由', '收款单位名称', '本次付款额', '立项识别码', '项目名称', '分项名称', '合同识别码', '合同名称', '合同类别', '合同编号', '付款批次', '付款单位识别码', '付款单位名称', '付款单位账号', '收款单位识别码', '收款单位账号', '预算识别码', '预算名称', '预算周期', '付款时预算总额', '付款时项目概算', '付款时合同付款上限', '付款时合同值', '付款时预算余额', '付款时概算余额', '付款时合同可付余额', '付款时合同未付额', '付款时预算已付额', '付款时合同已付额', '付款时概算已付额', '付款时预算已付比', '付款时合同已付比', '付款时概算已付比', '付款时形象进度', '预算本次付款比', '合同本次付款比', '概算本次付款比', '预算累付比', '合同累付比', '概算累付比', '付款备注']
PaymentColLabels_Type = ['整数型',     '日期型',       '日期型',       '文本型',   '字符串型',     '浮点型',     '整数型',     '字符串型', '字符串型', '整数型',     '字符串型', '字符串型', '字符串型', '整数型',   '整数型',         '字符串型',     '字符串型',     '整数型',         '字符串型',     '整数型',     '字符串型', '字符串型', '浮点型',         '浮点型',         '浮点型',             '浮点型',       '浮点型',         '浮点型',         '浮点型',             '浮点型',           '浮点型',           '浮点型',           '浮点型',           '百分比',           '百分比',           '百分比',           '字符串型',       '百分比',         '百分比',         '百分比',         '百分比',     '百分比',     '百分比',     '文本型']
PaymentFields = '付款识别码 付款登记时间 付款支付时间 立项识别码 合同识别码 付款事由 付款单位识别码 收款单位识别码 预算识别码 付款时预算总额 付款时项目概算 付款时合同付款上限 付款时合同值 付款时预算余额 付款时概算余额 付款时合同可付余额 付款时合同未付额 付款时预算已付额 付款时合同已付额 付款时概算已付额 付款时形象进度 本次付款额 付款备注'.split()
PaymentFields_Type = '整数型 日期型 日期型 整数型 整数型 字符串型 整数型 整数型 整数型 浮点型 浮点型 浮点型 浮点型 浮点型 浮点型 浮点型 浮点型 浮点型 浮点型 浮点型 字符串型 浮点型 文本型'.split()

# SubContract
SubContractColLabels = '分包合同识别码 立项识别码 项目名称 分项名称 合同识别码 总包合同编号 总包合同名称 总包合同主要内容 总包合同类别 总包合同值 分包合同编号 分包合同名称 分包合同主要内容 分包合同类别 甲方识别码 甲方单位名称 乙方识别码 乙方单位名称 丙方识别码 丙方单位名称 丁方识别码 丁方单位名称 分包合同签订时间 分包合同值_签订时 分包合同值_最新值 分包合同值_最终值 分包合同备注'.split()
SubContractColLabels_Type = '整数型 整数型 字符串型 字符串型 整数型 字符串型 字符串型 字符串型 字符串型 浮点型 字符串型 字符串型 字符串型 字符串型 整数型 字符串型 整数型 字符串型 整数型 字符串型 整数型 字符串型 日期型 浮点型 浮点型 浮点型 文本型'.split()
SubContractFields = '分包合同识别码 立项识别码 合同识别码 分包合同编号 分包合同名称 分包合同主要内容 分包合同类别 甲方识别码 乙方识别码 丙方识别码 丁方识别码 分包合同签订时间 分包合同值_签订时 分包合同值_最新值 分包合同值_最终值 分包合同备注'.split()
SubContractFields_Type = '整数型 整数型 整数型 字符串型 字符串型 字符串型 字符串型 整数型 整数型 整数型 整数型 日期型 浮点型 浮点型 浮点型 文本型'.split()

# Alteration
AlterationColLabels = '变更识别码 立项识别码 项目名称 分项名称 合同识别码 合同编号 合同名称 合同类别 合同值_签订时 甲方识别码 甲方单位名称 乙方识别码 乙方单位名称 丙方识别码 丙方单位名称 丁方识别码 丁方单位名称 变更类型 变更编号 变更主题 变更登记日期 变更生效日期 变更原因 预估变更额度 预估变更率 变更额度 变更率 变更备注'.split()
AlterationColLabels_Type = '整数型 整数型 字符串型 字符串型 整数型 字符串型 字符串型 字符串型 浮点型 整数型 字符串型 整数型 字符串型 整数型 字符串型 整数型 字符串型 字符串型 字符串型 字符串型 日期型 日期型 字符串型 浮点型 百分比 浮点型 百分比 文本型'.split()
AlterationFields = '变更识别码 立项识别码 合同识别码 变更类型 变更编号 变更主题 变更登记日期 变更生效日期 变更原因 预估变更额度 变更额度 变更备注'.split()
AlterationFields_Type = '整数型 整数型 整数型 字符串型 字符串型 字符串型 日期型 日期型 字符串型 浮点型 浮点型 文本型'.split()