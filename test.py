#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 9:10
# @Author  : Ale
# @Site    : 
# @File    : test.py
# @Software: PyCharm


'''
网页版重复数据4条，手工删除：
大新金格锰业有限公司塘深渣库  删除序号：32
Already exist data 3
0 ['大新县兴湖锰矿合龙尾矿库', 35]  删除序号：35
1 ['靖西市华荣锰业有限公司尾矿库', 39]  删除序号：39
2 ['河池市金城江区五圩宏发选矿厂尾矿库', 51] 删除序号：33
'''

import xlrd
import collections # Counter类

FNAME_WEB = "web-data.xls"
CORPNAME_WEB = "企业名称"
TAILNAME_WEB = "尾矿库名称"

FNAME_LOCAL = "local-data.xlsx"
CORPNAME_LOCAL = "所属企业"
TAILNAME_LOCAL = "尾矿库名称"

ALREADY_EXIST_DATA_WEB = []
ALREADY_EXIST_DATA_LOCAL = []

DATA_DIC_WEB = {}
DATA_DIC_LOCAL = {}

LEVEL1_DATA_DIC_WEB = {}  # 去除完全同名尾矿库后的数据
LEVEL1_DATA_DIC_LOCAL = {}


def readFile(file_source):
    # 数据初始化
    fname = ''
    corpname = ''
    tailname = ''
    if file_source == 'WEB':
        fname = FNAME_WEB
        corpname = CORPNAME_WEB
        tailname = TAILNAME_WEB
        already_exist_data = ALREADY_EXIST_DATA_WEB
        data_dic = DATA_DIC_WEB
    else:
        fname = FNAME_LOCAL
        corpname = CORPNAME_LOCAL
        tailname = TAILNAME_LOCAL
        already_exist_data = ALREADY_EXIST_DATA_LOCAL
        data_dic = DATA_DIC_LOCAL

    bk = xlrd.open_workbook(fname)
    # 获取当前文档的表
    shxrange = range(bk.nsheets)
    # sh = range(bk.nsheets)

    nrows = 0
    ncols = 0

    try:
        sh = bk.sheet_by_name("Sheet1")
        nrows = sh.nrows
        ncols = sh.ncols
    except:
        print("no sheet in %s named Sheet1", format(fname))
        return

    # nrows = sh.nrows
    # ncols = sh.ncols

    print("\nRead file {0} successfully.".format(fname))
    print('nrows {0}, ncols {1}'.format(nrows, ncols))
    # 获取第一行第一列数据
    # cell_value = sh.cell_value(1, 1)

    # 获取列名
    # printColName(sh)   # '尾矿库\n运行情况'

    '''
    row_list = []
    # 获取各行数据（一般第一行是标题）
    for i in range(0, nrows):
        row_data = sh.row_values(i)
        row_list.append(row_data)
    print(row_list)
    '''
    corpname_index = getColIndex(corpname, ncols,sh)
    tailname_index = getColIndex(tailname, ncols, sh)

    # data_dic = {}
    # 获取企业名称数据（第一行是标题）
    for i in range(1, nrows):
        try:
            # print(data_dic)
            corp_data = sh.cell_value(i, corpname_index)
            tail_data = sh.cell_value(i, tailname_index)
            # 对于第一行数据的处理
            if i == 1:
                # local-data.xlsx仅添加在用库
                if file_source == 'LOCAL':
                    zaiyong_index = getColIndex('尾矿库\n运行情况', ncols, sh)
                    zaiyong_str = sh.cell_value(0, zaiyong_index)
                    if zaiyong_str == '在用':
                        pass
                    else:
                        continue
                '''
                    if zaiyong_str == '在用':
                        data_dic[tail_data] = corp_data
                        print("{0}  {1}  {2}".format(i, tail_data, data_dic[tail_data]))
                else:
                    data_dic[tail_data] = corp_data
                    print("{0}  {1}  {2}".format(i, tail_data, data_dic[tail_data]))
                '''
                data_dic[tail_data] = corp_data
                print("{0}  {1}  {2}".format(i, tail_data, data_dic[tail_data]))
                continue
            '''
            for (k,v) in list(data_dic.items()):  #  dictionary changed size during iteration => 字典转换为集合或列表
                if tail_data == k:
                    # print("Already exist data = {0}".format(k))
                    # print(k)
                    # print(tail_data)
                    ALREADY_EXIST_DATA.append([tail_data,i])
                    break
            '''
            getRepeatData(data_dic, tail_data, already_exist_data, i)  # 最大字符匹配

            # local-data.xlsx仅添加在用库
            if file_source == 'LOCAL':
                zaiyong_index = getColIndex('尾矿库\n运行情况', ncols, sh)
                zaiyong_str = sh.cell_value(i, zaiyong_index)
                if zaiyong_str == "在用":
                    pass
                else:
                    continue

            # 手工标记重复记录
            if file_source == 'WEB':
                if i == 32 or i == 33 or i == 35 or i == 39:
                    tail_data = tail_data + '-repeat'

            data_dic[tail_data] = corp_data
            print("{0}  {1}  {2}".format(i,tail_data, data_dic[tail_data]))
            '''
            corp_data = sh.cell_value(i, corpname_index)
            tail_data = sh.cell_value(i, tailname_index)
            data_dic[tail_data] = corp_data
            print("{0}  {1}  {2}".format(i,tail_data, data_dic[tail_data]))
            '''
        except:
            print("add dict err, i = {0}, value = {1}, {2}".format(i, tail_data, corp_data))

    # 打印统计结果
    print("Printing data (n = {0}): \n".format(len(list(data_dic))))
    if len(already_exist_data) > 0:
        l = len(already_exist_data)
        print("Already exist data {0}".format(l))
        for i in range(l):
            print("{0} {1}".format(i, already_exist_data[i]))


    # print(data_dic)


# 获取指定列名所在列索引
def getColIndex(colname, ncols,sh):
    colname_index = float('inf')
    for i in range(0,ncols):
        if colname == sh.cell_value(0, i):
            colname_index = i
    return colname_index


# 检查字典中是否有重复数据
def getRepeatData(data_dic, tail_data, already_exist_data, i):
    for (k, v) in list(data_dic.items()):  # dictionary changed size during iteration => 字典转换为集合或列表
        # 去除此前第33条记录手工标记的repeat字符
        if '-repeat' in k:
            k = str(k).split('-')[0]
            # print("get str \'-repeat\'")
        if tail_data == k:
            # print("Already exist data = {0}".format(k))
            # print(k)
            # print(tail_data)
            already_exist_data.append([tail_data, i])
            break


# 获取列名
def printColName(sh):
    print(sh.row_values(0))


def dicCompare():
    n = 0
    data_dic_web = DATA_DIC_WEB
    data_dic_local = DATA_DIC_LOCAL

    # 除去同名尾矿库
    for (k_web,v_web) in list(data_dic_web.items()):
        '''
        # for(k_local,v_local) in list(data_dic_local.items()):
        #     if k_web == k_local:
        #         print("get \"尾矿库名称\" equal data = {0} in web    {1} in local".format(k_web,k_local))
        #         del data_dic_local[k_web]
        #         del data_dic_web[k_web]
        #         n = n + 1
        '''
        if k_web in data_dic_local.keys():
            print("get \"尾矿库名称\" equal data = {0} in web    {0} in local".format(k_web))
            del data_dic_local[k_web]
            del data_dic_web[k_web]
            n = n + 1

    # 打印数据
    '''
    # print("Equal n = {0}".format(n))
    # print("\nLeft local data = \n")
    # i = 0
    # for (k,v) in data_dic_local.items():
    #     i = i + 1
    #     print("{0}  {1}          {2}".format(i, k, v))
    # print("\nLeft web data = \n")
    # i = 0
    # for (k, v) in data_dic_web.items():
    #     i = i + 1
    #     print("{0}  {1}          {2}".format(i, k, v))
    '''
    printData(n, data_dic_local, data_dic_web)

    n = 0
    print("\n")
    temp_dic_local = {}
    temp_dic_web = {}
    # 除去同名尾矿库后，在web剩余中先对比local查找同企业名称尾矿库
    for (k_web,v_web) in list(data_dic_web.items()):
        for(k_local,v_local) in list(data_dic_local.items()):
            if v_web == v_local:
                n = n + 1
                print("get \"企业名称\" equal data = {0} {1} in web    {2} {3} in local".format(k_web,v_web ,k_local ,v_local))
                # 避免一个企业多个尾矿库、增加字典报错的情况 分别做try
                try:
                    temp_dic_local[k_local] = v_local
                except:
                    pass
                try:
                    temp_dic_web[k_web] = v_web
                except:
                    pass

    # 通过差集获得不同名且企业名称不同的尾矿库
    for (k_web,v_web) in list(data_dic_web.items()):
        '''
        # for(k,v) in list(temp_dic_web.items()):
        #     if k_web == k:
        #         del data_dic_web[k_web]
        '''
        if k_web in temp_dic_web.keys():
            del data_dic_web[k_web]
    for (k_local,v_local) in list(data_dic_local.items()):
        '''
        # for(k,v) in list(temp_dic_local.items()):
        #     if k_local == k:
        #         del data_dic_local[k_local]
        '''
        if k_local in temp_dic_local.keys():
            del data_dic_local[k_local]


    # 打印数据
    '''
    # print("Equal n = {0}".format(n))
    # print("\nLeft local data = \n")
    # i = 0
    # for (k, v) in data_dic_local.items():
    #     i = i + 1
    #     print("{0}  {1}          {2}".format(i, k, v))
    # print("\nLeft web data = \n")
    # i = 0
    # for (k, v) in data_dic_web.items():
    #     i = i + 1
    #     print("{0}  {1}          {2}".format(i, k, v))
    '''
    printData(n, data_dic_local, data_dic_web)

    # 对剩余部分，用web数据依次遍历local数据(按key即尾矿库名称匹配)，按最大匹配(最多相同字符)推荐对应匹配项目
    '''
    计算公式 match = n , n 为 k_web 字符（含重复字符）在k_local的出现次数
    可能的情况：
    1. len(k_web) >= len(k_local) 
    2. len(k_web) < len(k_local) 
    3. 当k_web有重复字符时，n > len(k_web)
    '''
    '''
        # 1. 对尾矿库名称进行比较
    match_dic = {}
    for item_web in data_dic_web.items():
        temp_match_max_n = 0
        temp_match_max_item = ''
        for item_local in data_dic_local.items():
            n = 0
            # web 和 local 双向比较，取最大值，避免 web 或 local 某一端比较长的情况
            # 1. web 向 local 比较
            str_web = str(item_web[0]) + str(item_web[1])
            str_local = str(item_local[0]) + str(item_web[1])
            for character in str_web: # item 为 tuple
                if character in str_local:
                    n = n + 1
                    # 删除匹配character的第一个字符，避免重复比较
                    str_local = str_local.replace(character,'',1)
            # if n > temp_match_max_n:
            #     temp_match_max_n = n
            #     temp_match_max_item = item_local
            # 2. local 向 web 比较
            m = 0
            str_web = str(item_web[0]) + str(item_web[1])
            str_local = str(item_local[0]) + str(item_web[1])
            for character in str_local:  # item 为 tuple
                if character in str_web:
                    m = m + 1
                    str_web = str_web.replace(character, '', 1)
            if m >= n:
                if m > temp_match_max_n:
                    # print("m>=n")
                    temp_match_max_n = m
                    temp_match_max_item = item_local
            else:
                if n > temp_match_max_n:
                    temp_match_max_n = n
                    temp_match_max_item = item_local
        # local出现重复记录的，即temp_match_max_item，且 n 不相等的，取 n 最大值匹配
        print("temp_match_max_item = {0}, n = {1}".format(temp_match_max_item,temp_match_max_n))
        if match_dic == {}:
            match_dic[item_web[0]] = ([item_web, temp_match_max_item, temp_match_max_n])
        else:
            for v in list(match_dic.values()):
                # 若在字典中有重复匹配的情况
                if temp_match_max_item == v[1]:
                    # 若 n 值较大，则删除已登记的较小匹配条目，新增较大条目
                    \'''
                    最差的情况：n 顺序变大，无法筛选出不匹配记录
                    match list = 
                    1   ('南丹弘基贸易有限责任公司中心厂尾矿库', '南丹县弘基贸易责任公司中心选厂') in web     
                        ('南丹弘基贸易有限责任公司（中心厂尾矿库）', '南丹弘基贸易有限责任公司') in local,   match n = 33
                    2   ('蒙山县耀华矿业有限责任公司第一选矿厂尾矿库', '蒙山县耀华矿业责任有限公司') in web     
                        ('蒙山县耀华矿业有限责任公司（第一尾矿库）', '蒙山县耀华矿业有限责任公司') in local,   match n = 31
                    3   ('靖西市华荣锰业有限公司尾矿库', '靖西市华荣锰业有限公司') in web     
                        ('靖西市大西南锰业一分厂尾渣库（原靖西县大锰新材料有限公司尾渣库）', '靖西市大西南锰业有限公司') in local,   match n = 22
                    4   ('永福县新福大矿业有限公司苏桥选矿厂', '永福县新福大矿业有限公司（尾矿库专项）') in web     
                        ('永福县新福大矿业有限责任公司', '永福县新福大矿业有限责任公司') in local,   match n = 31
                    5   ('南丹县新兴矿业有限公司新兴尾矿库', '南丹新兴矿业有限公司') in web     
                        ('中信大锰矿业有限公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新分公司') in local,   match n = 20
                    6   ('中信大锰矿业有限责任公司天等锰矿分公司东平镇安堤尾矿库', '中信大锰天等锰矿分公司安堤尾矿库') in web     
                        ('中信大锰矿业有限公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新分公司') in local,   match n = 34
                    7   ('中信大锰矿业有限责任公司大新锰矿分公司布康排渣库', '中信大锰矿业有限责任公司大新锰矿分公司') in web     
                        ('中信大锰矿业有限公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新分公司') in local,   match n = 37
                    8   ('广西北山矿业发展有限责任公司尾矿库', '广西北山矿业发展有限责任公司尾矿库') in web     
                        ('桂林新源钽业有限责任公司高屋坪尾矿库（广西有色栗木矿业有限公司）', '桂林新源钽业有限责任公司（广西有色栗木矿业有限公司）') in local,   match n = 30
                    9   ('大新县兴湖锰矿合龙尾矿库', '南宁市高恒商业贸易有限公司大新县兴湖锰矿') in web     
                        ('大新县兴湖锰矿尾矿库', '大新县兴湖锰矿') in local,   match n = 30
                    10   ('中信大锰矿业有限责任公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新锰矿分公司') in web     
                        ('中信大锰矿业有限公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新分公司') in local,   match n = 41
                    11   ('资源县钨矿尾矿库', '资源县钨矿（整个矿区）') in web     
                        ('资源县钨矿2号尾矿库', '资源县钨矿') in local,   match n = 19
                    \'''
                    if temp_match_max_n > v[2]:
                        print("get greate n = {0}, temp_match_max_item = {1}".format(temp_match_max_n,temp_match_max_item))
                        del match_dic[v[0][0]]

                        match_dic[item_web[0]] = ([item_web, temp_match_max_item, temp_match_max_n])
                    # 若 n 值相等或变小，则跳过，不添加入字典（相等情况应进一步讨论）
                    else:
                        print("da")
                        continue
                # 若不在字典中则直接添加
                else:
                    match_dic[item_web[0]] = ([item_web, temp_match_max_item, temp_match_max_n])

        # match_dic[item_web[0]] = ([item_web,temp_match_max_item,temp_match_max_n])
    print("\nmatch list = ")
    i = 0
    for v in match_dic.values():
        i = i + 1
        print("{0}   {1} in web     \n    {2} in local,   match n = {3}".format(i, v[0],v[1], v[2]))
    '''

    # # 获取匹配字典，比较尾矿库+企业名称
    # match_dic = advancedCompare('all',data_dic_web, data_dic_local)
    # # 获取剩余数据
    # # (match_web_list, match_local_list) = getListFromDic(match_dic)
    # # for k in list(data_dic_web.keys()):
    # #     if k in match_web_list:
    # #         del data_dic_web[k]
    # # for k in list(data_dic_local.keys()):
    # #     if k in match_local_list:
    # #         del data_dic_local[k]
    # (data_dic_web, data_dic_local) = getLeftData(match_dic, data_dic_web, data_dic_local)
    # # 打印剩余数据
    # print("\n")
    # printData(0, data_dic_local, data_dic_web)
    #
    # # 加一层循环,比较企业名称
    # if len(data_dic_web) > 0:
    #     match_dic = advancedCompare('value_only',data_dic_web, data_dic_local)
    #     # 获取剩余数据
    #     # (match_web_list, match_local_list) = getListFromDic(match_dic)
    #     # for k in list(data_dic_web.keys()):
    #     #     if k in match_web_list:
    #     #         del data_dic_web[k]
    #     # for k in list(data_dic_local.keys()):
    #     #     if k in match_local_list:
    #     #         del data_dic_local[k]
    #     (data_dic_web,data_dic_local) = getLeftData(match_dic,data_dic_web,data_dic_local)
    # # 打印剩余数据
    # print("\n")
    # printData(0, data_dic_local, data_dic_web)

    mode = 0  # 0 = 尾矿库名称 + 企业名称  1 = 仅企业名称
    while len(data_dic_web) > 0:
        match_dic = advancedCompare(mode, data_dic_web, data_dic_local)
        (data_dic_web, data_dic_local) = getLeftData(match_dic, data_dic_web, data_dic_local)
        # 打印剩余数据
        print("\n")
        printData(0, data_dic_local, data_dic_web)
        mode = mode + 1


# 手工删除web中的重复数据
def delRepetedWebData():
    print("\nDel repeated datas in web:")
    for i in list(DATA_DIC_WEB.keys()):
        if '-repeat' in i:
            print(i)
            del DATA_DIC_WEB[i]
    # 打印数据
    print("\n")
    j = 0
    for (k,v) in DATA_DIC_WEB.items():
        print("{0}  {1}   {2}".format(j,k,v))
        j = j + 1
    print("\nClean web data n = {0}\n".format(len(DATA_DIC_WEB)))


# 打印数据
def printData(n, data_dic_local, data_dic_web):
    print("Equal n = {0}".format(n))
    print("\nLeft local data = \n")
    i = 0
    for (k, v) in data_dic_local.items():
        i = i + 1
        print("{0}  {1}          {2}".format(i, k, v))
    print("\nLeft web data = \n")
    i = 0
    for (k, v) in data_dic_web.items():
        i = i + 1
        print("{0}  {1}          {2}".format(i, k, v))


# 深入的语义比较
def advancedCompare(pattern,data_dic_web,data_dic_local):
    # 1. 对尾矿库名称进行比较
    match_dic = {}
    for item_web in data_dic_web.items():
        '''
        temp_match_max_n = 0
        temp_match_max_item = ''
        for item_local in data_dic_local.items():
            n = 0
            # web 和 local 双向比较，取最大值，避免 web 或 local 某一端比较长的情况
            # 1. web 向 local 比较
            str_web = str(item_web[0]) + str(item_web[1])
            str_local = str(item_local[0]) + str(item_web[1])
            for character in str_web:  # item 为 tuple
                if character in str_local:
                    n = n + 1
                    # 删除匹配character的第一个字符，避免重复比较
                    str_local = str_local.replace(character, '', 1)
            # if n > temp_match_max_n:
            #     temp_match_max_n = n
            #     temp_match_max_item = item_local
            # 2. local 向 web 比较
            m = 0
            str_web = str(item_web[0]) + str(item_web[1])
            str_local = str(item_local[0]) + str(item_web[1])
            for character in str_local:  # item 为 tuple
                if character in str_web:
                    m = m + 1
                    str_web = str_web.replace(character, '', 1)
            if m >= n:
                if m > temp_match_max_n:
                    # print("m>=n")
                    temp_match_max_n = m
                    temp_match_max_item = item_local
            else:
                if n > temp_match_max_n:
                    temp_match_max_n = n
                    temp_match_max_item = item_local
        '''

        temp_match_max_n = 0
        temp_match_max_item = ''
        for item_local in data_dic_local.items():
            n = 0
            # web 和 local 双向比较，短str向长str比较，获得最长匹配 n ，取 n = n / len(较短str)
            str_web = ''
            str_local = ''
            if pattern == 0:  # 尾矿库名称 + 企业名称
                str_web = str(item_web[0]) + str(item_web[1])
                str_local = str(item_local[0]) + str(item_local[1])
            if pattern == 1:  # 仅企业名称
                str_web = str(item_web[1])
                str_local = str(item_local[1])
            str_long = ''
            str_short = ''
            if len(str_web) >= len(str_local):
                str_long = str_web
                str_short = str_local
            else:
                str_long = str_local
                str_short = str_web
            for character in str_short:  # item 为 tuple
                if character in str_long:
                    n = n + 1
                    # 删除匹配character的第一个字符，避免重复比较
                    str_long = str_long.replace(character, '', 1)
            n = float(n/len(str_short))
            if n > temp_match_max_n:
                temp_match_max_n = n
                temp_match_max_item = item_local

        # local出现重复记录的，即temp_match_max_item，且 n 不相等的，取 n 最大值匹配
        # print("temp_match_max_item = {0}, n = {1}".format(temp_match_max_item, temp_match_max_n))
        if match_dic == {}:
            match_dic[item_web[0]] = ([item_web, temp_match_max_item, temp_match_max_n])
        else:
            add_flag = True
            for v in list(match_dic.values()):
                # 遍历到最后，扫描一遍
                # 若在字典中有重复匹配的情况
                # print("for temp_item = {0}, v[1] = {1}".format(temp_match_max_item,v[1]))
                if temp_match_max_item == v[1]:
                    # 扫描一遍发现相同项，则不执行最后的add
                    add_flag = False
                    # 若 n 值较大，则删除已登记的较小匹配条目，新增较大条目
                    '''
                    最差的情况：n 顺序变大，无法筛选出不匹配记录
                    match list = 
                    1   ('南丹弘基贸易有限责任公司中心厂尾矿库', '南丹县弘基贸易责任公司中心选厂') in web     
                        ('南丹弘基贸易有限责任公司（中心厂尾矿库）', '南丹弘基贸易有限责任公司') in local,   match n = 33
                    2   ('蒙山县耀华矿业有限责任公司第一选矿厂尾矿库', '蒙山县耀华矿业责任有限公司') in web     
                        ('蒙山县耀华矿业有限责任公司（第一尾矿库）', '蒙山县耀华矿业有限责任公司') in local,   match n = 31
                    3   ('靖西市华荣锰业有限公司尾矿库', '靖西市华荣锰业有限公司') in web     
                        ('靖西市大西南锰业一分厂尾渣库（原靖西县大锰新材料有限公司尾渣库）', '靖西市大西南锰业有限公司') in local,   match n = 22
                    4   ('永福县新福大矿业有限公司苏桥选矿厂', '永福县新福大矿业有限公司（尾矿库专项）') in web     
                        ('永福县新福大矿业有限责任公司', '永福县新福大矿业有限责任公司') in local,   match n = 31
                    5   ('南丹县新兴矿业有限公司新兴尾矿库', '南丹新兴矿业有限公司') in web     
                        ('中信大锰矿业有限公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新分公司') in local,   match n = 20
                    6   ('中信大锰矿业有限责任公司天等锰矿分公司东平镇安堤尾矿库', '中信大锰天等锰矿分公司安堤尾矿库') in web     
                        ('中信大锰矿业有限公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新分公司') in local,   match n = 34
                    7   ('中信大锰矿业有限责任公司大新锰矿分公司布康排渣库', '中信大锰矿业有限责任公司大新锰矿分公司') in web     
                        ('中信大锰矿业有限公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新分公司') in local,   match n = 37
                    8   ('广西北山矿业发展有限责任公司尾矿库', '广西北山矿业发展有限责任公司尾矿库') in web     
                        ('桂林新源钽业有限责任公司高屋坪尾矿库（广西有色栗木矿业有限公司）', '桂林新源钽业有限责任公司（广西有色栗木矿业有限公司）') in local,   match n = 30
                    9   ('大新县兴湖锰矿合龙尾矿库', '南宁市高恒商业贸易有限公司大新县兴湖锰矿') in web     
                        ('大新县兴湖锰矿尾矿库', '大新县兴湖锰矿') in local,   match n = 30
                    10   ('中信大锰矿业有限责任公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新锰矿分公司') in web     
                        ('中信大锰矿业有限公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新分公司') in local,   match n = 41
                    11   ('资源县钨矿尾矿库', '资源县钨矿（整个矿区）') in web     
                        ('资源县钨矿2号尾矿库', '资源县钨矿') in local,   match n = 19
                    '''
                    if temp_match_max_n > v[2]:
                        # print("get greater n = {0}, temp_match_max_item = {1}".format(temp_match_max_n,
                        #                                                              temp_match_max_item))
                        del match_dic[v[0][0]]
                        match_dic[item_web[0]] = ([item_web, temp_match_max_item, temp_match_max_n])
                    # 若 n 值相等或变小，则跳过，不添加入字典（相等情况应进一步讨论）
                    else:
                        # print("get lesser {0} {1}".format(temp_match_max_item,temp_match_max_n))
                        pass

            # 扫描一遍，若不在字典中则直接添加
            if add_flag:
                match_dic[item_web[0]] = ([item_web, temp_match_max_item, temp_match_max_n])
                # print("add new data {0} {1}".format(temp_match_max_item, temp_match_max_n))
                # print(len(match_dic))

    print("\nmatch list = ")
    i = 0
    for v in match_dic.values():
        i = i + 1
        print("{0}   {1} in web     \n    {2} in local,   match n = {3}".format(i, v[0], v[1], v[2]))

    return match_dic


# # 深入的语义比较 企业名称
# def advancedCompare2(data_dic_web,data_dic_local):
#     # 1. 对尾矿库名称进行比较
#     match_dic = {}
#     for item_web in data_dic_web.items():
#         '''
#         temp_match_max_n = 0
#         temp_match_max_item = ''
#         for item_local in data_dic_local.items():
#             n = 0
#             # web 和 local 双向比较，取最大值，避免 web 或 local 某一端比较长的情况
#             # 1. web 向 local 比较
#             str_web = str(item_web[0]) + str(item_web[1])
#             str_local = str(item_local[0]) + str(item_web[1])
#             for character in str_web:  # item 为 tuple
#                 if character in str_local:
#                     n = n + 1
#                     # 删除匹配character的第一个字符，避免重复比较
#                     str_local = str_local.replace(character, '', 1)
#             # if n > temp_match_max_n:
#             #     temp_match_max_n = n
#             #     temp_match_max_item = item_local
#             # 2. local 向 web 比较
#             m = 0
#             str_web = str(item_web[0]) + str(item_web[1])
#             str_local = str(item_local[0]) + str(item_web[1])
#             for character in str_local:  # item 为 tuple
#                 if character in str_web:
#                     m = m + 1
#                     str_web = str_web.replace(character, '', 1)
#             if m >= n:
#                 if m > temp_match_max_n:
#                     # print("m>=n")
#                     temp_match_max_n = m
#                     temp_match_max_item = item_local
#             else:
#                 if n > temp_match_max_n:
#                     temp_match_max_n = n
#                     temp_match_max_item = item_local
#         '''
#
#         temp_match_max_n = 0
#         temp_match_max_item = ''
#         for item_local in data_dic_local.items():
#             n = 0
#             # web 和 local 双向比较，短str向长str比较，获得最长匹配 n ，取 n = n / len(较短str)
#             str_web = str(item_web[1])
#             str_local = str(item_local[1])
#             str_long = ''
#             str_short = ''
#             if len(str_web) >= len(str_local):
#                 str_long = str_web
#                 str_short = str_local
#             else:
#                 str_long = str_local
#                 str_short = str_web
#             for character in str_short:  # item 为 tuple
#                 if character in str_long:
#                     n = n + 1
#                     # 删除匹配character的第一个字符，避免重复比较
#                     str_long = str_long.replace(character, '', 1)
#             n = float(n/len(str_short))
#             if n > temp_match_max_n:
#                 temp_match_max_n = n
#                 temp_match_max_item = item_local
#
#         # local出现重复记录的，即temp_match_max_item，且 n 不相等的，取 n 最大值匹配
#         # print("temp_match_max_item = {0}, n = {1}".format(temp_match_max_item, temp_match_max_n))
#         if match_dic == {}:
#             match_dic[item_web[0]] = ([item_web, temp_match_max_item, temp_match_max_n])
#         else:
#             add_flag = True
#             for v in list(match_dic.values()):
#                 # 遍历到最后，扫描一遍
#                 # 若在字典中有重复匹配的情况
#                 # print("for temp_item = {0}, v[1] = {1}".format(temp_match_max_item,v[1]))
#                 if temp_match_max_item == v[1]:
#                     # 扫描一遍发现相同项，则不执行最后的add
#                     add_flag = False
#                     # 若 n 值较大，则删除已登记的较小匹配条目，新增较大条目
#                     '''
#                     最差的情况：n 顺序变大，无法筛选出不匹配记录
#                     match list =
#                     1   ('南丹弘基贸易有限责任公司中心厂尾矿库', '南丹县弘基贸易责任公司中心选厂') in web
#                         ('南丹弘基贸易有限责任公司（中心厂尾矿库）', '南丹弘基贸易有限责任公司') in local,   match n = 33
#                     2   ('蒙山县耀华矿业有限责任公司第一选矿厂尾矿库', '蒙山县耀华矿业责任有限公司') in web
#                         ('蒙山县耀华矿业有限责任公司（第一尾矿库）', '蒙山县耀华矿业有限责任公司') in local,   match n = 31
#                     3   ('靖西市华荣锰业有限公司尾矿库', '靖西市华荣锰业有限公司') in web
#                         ('靖西市大西南锰业一分厂尾渣库（原靖西县大锰新材料有限公司尾渣库）', '靖西市大西南锰业有限公司') in local,   match n = 22
#                     4   ('永福县新福大矿业有限公司苏桥选矿厂', '永福县新福大矿业有限公司（尾矿库专项）') in web
#                         ('永福县新福大矿业有限责任公司', '永福县新福大矿业有限责任公司') in local,   match n = 31
#                     5   ('南丹县新兴矿业有限公司新兴尾矿库', '南丹新兴矿业有限公司') in web
#                         ('中信大锰矿业有限公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新分公司') in local,   match n = 20
#                     6   ('中信大锰矿业有限责任公司天等锰矿分公司东平镇安堤尾矿库', '中信大锰天等锰矿分公司安堤尾矿库') in web
#                         ('中信大锰矿业有限公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新分公司') in local,   match n = 34
#                     7   ('中信大锰矿业有限责任公司大新锰矿分公司布康排渣库', '中信大锰矿业有限责任公司大新锰矿分公司') in web
#                         ('中信大锰矿业有限公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新分公司') in local,   match n = 37
#                     8   ('广西北山矿业发展有限责任公司尾矿库', '广西北山矿业发展有限责任公司尾矿库') in web
#                         ('桂林新源钽业有限责任公司高屋坪尾矿库（广西有色栗木矿业有限公司）', '桂林新源钽业有限责任公司（广西有色栗木矿业有限公司）') in local,   match n = 30
#                     9   ('大新县兴湖锰矿合龙尾矿库', '南宁市高恒商业贸易有限公司大新县兴湖锰矿') in web
#                         ('大新县兴湖锰矿尾矿库', '大新县兴湖锰矿') in local,   match n = 30
#                     10   ('中信大锰矿业有限责任公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新锰矿分公司') in web
#                         ('中信大锰矿业有限公司大新锰矿分公司弄松尾矿库', '中信大锰矿业有限责任公司大新分公司') in local,   match n = 41
#                     11   ('资源县钨矿尾矿库', '资源县钨矿（整个矿区）') in web
#                         ('资源县钨矿2号尾矿库', '资源县钨矿') in local,   match n = 19
#                     '''
#                     if temp_match_max_n > v[2]:
#                         # print("get greater n = {0}, temp_match_max_item = {1}".format(temp_match_max_n,
#                         #                                                              temp_match_max_item))
#                         del match_dic[v[0][0]]
#                         match_dic[item_web[0]] = ([item_web, temp_match_max_item, temp_match_max_n])
#                     # 若 n 值相等或变小，则跳过，不添加入字典（相等情况应进一步讨论）
#                     else:
#                         # print("get lesser {0} {1}".format(temp_match_max_item,temp_match_max_n))
#                         pass
#
#             # 扫描一遍，若不在字典中则直接添加
#             if add_flag:
#                 match_dic[item_web[0]] = ([item_web, temp_match_max_item, temp_match_max_n])
#                 # print("add new data {0} {1}".format(temp_match_max_item, temp_match_max_n))
#                 # print(len(match_dic))
#
#     print("\nmatch list = ")
#     i = 0
#     for v in match_dic.values():
#         i = i + 1
#         print("{0}   {1} in web     \n    {2} in local,   match n = {3}".format(i, v[0], v[1], v[2]))
#
#     return match_dic


# 在 match_dic 中获取 web 和 local 的 list


def getListFromDic(match_dic):
    match_list = list(match_dic.values())
    match_web_list = []
    match_local_list = []
    for item in match_list:
        match_web_list.append(item[0][0])
        match_local_list.append(item[1][0])
    return match_web_list, match_local_list


def getLeftData(match_dic,data_dic_web,data_dic_local):
    (match_web_list, match_local_list) = getListFromDic(match_dic)
    for k in list(data_dic_web.keys()):
        if k in match_web_list:
            del data_dic_web[k]
    for k in list(data_dic_local.keys()):
        if k in match_local_list:
            del data_dic_local[k]
    return data_dic_web,data_dic_local


readFile('WEB')
readFile('LOCAL')

delRepetedWebData()

dicCompare()





