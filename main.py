import requests
from requests.exceptions import RequestException
import re
import os
import xlrd
from xlrd import xldate_as_tuple
from fuzzywuzzy import process

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15',
}
data = {'课程名': {}, '上课老师': {}, '主修班级': {}}
name_col = 0
teacher_col = 0
sc_col = 0


def get_one_page(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
        return None
    except RequestException:
        return None


def countPoint(UrlPart):
    cnt = 0
    for i in UrlPart:
        if i != '.':
            break
        cnt += 1
    return cnt


def getNewXls():
    url = input('输入考试通知网址:').strip()
    html = get_one_page(url, headers=headers)
    if not html:
        exit('网页获取失败')
    als = re.findall('<a.*?href="(.*?)"', html, re.S)
    for a in als:
        if a.endswith('xls'):
            cnt = countPoint(a)
            url = '/'.join(url.split('/')[:-cnt]) + a[cnt:]
            print('get file path:' + url)
            break
    content = requests.get(url, headers).content
    with open('content.xls', 'wb') as f:
        f.write(content)
    print('download xls succeed!')


def init(sheet):
    global name_col, teacher_col, sc_col
    keys = sheet.row_values(0)
    for i in range(len(keys)):
        if keys[i] == '课程名':
            name_col = i
        elif keys[i] == '上课教师':
            teacher_col = i
        elif keys[i] == '主修班级':
            sc_col = i
    if not name_col or not teacher_col or not sc_col:
        exit('Unknown xls layout')
    ls = sheet.col_values(name_col)
    for i in range(1, len(ls)):
        if ls[i] not in data['课程名']:
            data['课程名'][ls[i]] = set()
        data['课程名'][ls[i]].add(i)
    ls = sheet.col_values(teacher_col)
    for i in range(1, len(ls)):
        if ls[i] not in data['上课老师']:
            data['上课老师'][ls[i]] = set()
        data['上课老师'][ls[i]].add(i)
    ls = sheet.col_values(sc_col)
    for i in range(1, len(ls)):
        cls = ls[i].split(',')
        for cl in cls:
            if cl not in data['主修班级']:
                data['主修班级'][cl] = set()
            data['主修班级'][cl].add(i)


def fm(string, ls):
    res = []
    match = '.*?'.join([i for i in string])
    for i in ls:
        if re.findall(match, i):
            res.append((i, 100))
    return res


if __name__ == '__main__':
    if not os.path.exists('content.xls'):
        getNewXls()
    xls = xlrd.open_workbook('content.xls')
    sheet = xls.sheet_by_index(0)
    init(sheet)
    keys = ['课程名', '上课老师', '主修班级']
    print('帮助:')
    print('    通过使用如下固定格式的与或表达式进行考试信息搜索：')
    print('                课程 & 教师 & 班级')
    print('    如果条件不足三个，则默认表达式后置条件缺省。')
    print('    ps1: xx&yy，为查找课程名为xx且授课教师为yy的信息。')
    print('    ps2: xx&&yy，为查找课程名为xx且班级为yy的信息。')
    print('    ps3: xx&yy&zz，为按课程、教师和班级三种条件查找。')
    while True:
        print('-' * 50)
        exp = input('输入搜索表达式:').split('&')
        if not ''.join(exp):
            break
        res_set = set()
        flag = False
        for i in range(len(exp)):
            if i < 3:
                aim = exp[i].strip()
                if not aim:
                    continue
                res = fm(aim, data[keys[i]].keys())
                if not res:
                    res = process.extract(aim, data[keys[i]].keys(), limit=3)
                ts = set()
                for mth in res:
                    if mth[1]:
                        ts = ts.union(data[keys[i]][mth[0]])
                if flag:
                    res_set = res_set.intersection(ts)
                else:
                    res_set = res_set.union(ts)
                    flag = True
            else:
                break
        print('查询结果:' + '' if flag else 'None')
        for line_num in res_set:
            line = sheet.row_values(line_num)
            print('-' * 50)
            print('课程名称：' + line[name_col])
            print('授课教师：' + line[teacher_col].replace('\n', ','))
            cls = line[sc_col].split(',')
            linkstr = ''
            for i in range(len(cls)):
                linkstr += cls[i]
                if i + 1 == len(cls):
                    break
                elif (i + 1) % 5 == 0:
                    linkstr += '\n' + ' ' * 9
                else:
                    linkstr += ','
            print('主修班级：' + linkstr)
            day = "%04d年%02d月%02d日" % xldate_as_tuple(line[4], 0)[:3]
            print('考试时间：' + day + '(周%s) ' % line[2] + line[5])
            print('考试地点：' + line[-1].replace('\n', ','))
