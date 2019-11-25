import requests
from requests.exceptions import RequestException
import re
import os
import sys
import xlrd
from xlrd import xldate_as_tuple
__VERSION__ = '2.6'

base_dir = sys.path[0]
if sys.platform.startswith('win'):
    dir_char = '\\'
    base_dir = dir_char.join(base_dir.split(dir_char)[:-1])
else:
    dir_char = '/'
base_dir += dir_char
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/12.0.2 Safari/605.1.15',
}
data = {'课程名': {}, '上课老师': {}, '主修班级': {}}
name_col = 0
teacher_col = 0
sc_col = 0
sheet = None
try:
    with open(base_dir + '.last_title', 'r') as f:
        is_xls = f.readlines()[-1].strip().endswith('xls')
except:
    is_xls = False
real_file = base_dir + ('content.xls' if is_xls else 'content.xlsx')
title_bar = None


def get_one_page(url, Headers):
    try:
        response = requests.get(url, headers=Headers)
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


def getNewXls(url):
    html = get_one_page(url, Headers=headers)
    if not html:
        return False
    title = re.findall('<h3>(.*?)</h3>', html, re.S)[0]
    als = re.findall('<a.*?href="(.*?)">(.*?)<', html, re.S)
    res = None
    global is_xls
    for a in als:
        is_xls = a[0].endswith('xls')
        if is_xls or a[0].endswith('xlsx'):
            is_xls = a[0].endswith('xls')
            cnt = countPoint(a[0])
            url = '/'.join(url.split('/')[:-cnt]) + a[0][cnt:]
            res = a
            break
    if not res:
        return False
    content = requests.get(url, headers).content
    with open(real_file, 'wb') as file:
        file.write(content)
    with open(base_dir + '.last_title', 'w') as file:
        file.write(title + '\n')
        file.write(res[0] + '\n')
    return True


def init():
    xls = xlrd.open_workbook(real_file)
    global name_col, teacher_col, sc_col, sheet, data, title_bar
    sheet = xls.sheet_by_index(0)
    start_pos = 0
    while start_pos < 5:
        keys = [str(i).strip() for i in sheet.row_values(start_pos)]
        for i in range(len(keys)):
            if keys[i].startswith('课程名'):
                name_col = i
            elif keys[i].endswith('教师'):
                teacher_col = i
            elif keys[i].endswith('班级'):
                sc_col = i
        start_pos += 1
        if name_col and teacher_col and sc_col:
            title_bar = keys
            break
    if not name_col or not teacher_col or not sc_col:
        exit('Unknown xls layout')
    ls = sheet.col_values(name_col)
    data = {'课程名': {}, '上课老师': {}, '主修班级': {}}
    for i in range(start_pos, len(ls)):
        if ls[i] not in data['课程名']:
            data['课程名'][ls[i]] = set()
        data['课程名'][ls[i]].add(i)
    ls = sheet.col_values(teacher_col)
    for i in range(start_pos, len(ls)):
        if ls[i] not in data['上课老师']:
            data['上课老师'][ls[i]] = set()
        data['上课老师'][ls[i]].add(i)
    ls = sheet.col_values(sc_col)
    for i in range(start_pos, len(ls)):
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


def search(exp):
    if not pre_check():
        return None
    keys = ['课程名', '上课老师', '主修班级']
    res_set = set()
    flag = False
    exp = list(set(exp))
    for i in range(len(exp)):
        if i < 3:
            aim = exp[i].strip()
            if not aim:
                continue
            loop = 3
            ts = set()
            while loop:
                loop -= 1
                res = fm(aim, data[keys[loop]].keys())
                for mth in res:
                    if mth[1]:
                        ts = ts.union(data[keys[loop]][mth[0]])
            if flag:
                res_set = res_set.intersection(ts)
            else:
                res_set = res_set.union(ts)
                flag = True
        else:
            break
    res = ''
    for line_num in res_set:
        line = sheet.row_values(line_num)
        res += '-' * 50 + '\n'
        res += '课程名称：' + line[name_col] + '\n'
        res += '授课教师：' + line[teacher_col].replace('\n', ',') + '\n'
        if ',' in line[sc_col]:
            cls = line[sc_col].strip().split(',')
        else:
            cls = line[sc_col].strip().split()
        linkstr = ''
        for i in range(len(cls)):
            linkstr += cls[i]
            if i + 1 == len(cls):
                break
            elif (i + 1) % 5 == 0:
                linkstr += '\n' + ' ' * 9
            else:
                linkstr += ','
        res += '主修班级：' + linkstr + '\n'
        try:
            day = "%04d年%02d月%02d日" % xldate_as_tuple(line[4], 0)[:3]
            res += '考试时间：' + day + '(周%s) ' % line[2] + line[5] + '\n'
            res += '考试地点：' + line[-1].replace('\n', ',') + '\n'
        except:
            for i, v in enumerate(line):
                if not title_bar[i].strip():
                    continue
                if i != name_col and i != teacher_col and i != sc_col:
                    try:
                        v = v.strip()
                    except:
                        pass
                    res += title_bar[i] + ': %s\n' % v
    del res_set
    return res


def pre_check():
    return os.path.exists(base_dir + ('content.xls' if is_xls else 'content.xlsx'))


def new_note_check():
    try:
        with open(base_dir + '.last_title', 'r') as file:
            lines = file.readlines()
            title = lines[0].strip()
            filename = lines[1].strip()
    except:
        title = filename = '****'
    html = get_one_page('http://cup.edu.cn/jwc/jxjs/Ttrends/index.htm', headers)
    if not html:
        return -1
    ls = re.findall('<li>(.*?)</li>', html, re.S)
    for i in ls:
        content = re.findall('<a.*?href="(.*?)">(.*?)</a>', i, re.S)
        if content:
            addr, new_title = content[0]
            new_title = new_title.strip()
            if new_title == title:
                html = get_one_page('http://www.cup.edu.cn/jwc/jxjs/Ttrends/' + addr, headers)
                aim_li = re.findall('<li.*?>(.*?)</li>', html, re.S)[-1]
                new_filename = re.findall('<a href="(.*?)".*?>', aim_li, re.S)[0]
                if new_filename != filename:
                    return ['http://www.cup.edu.cn/jwc/jxjs/Ttrends/' + addr, new_filename, 0]
                return 0
            if new_title.endswith('考试安排'):
                return ['http://www.cup.edu.cn/jwc/jxjs/Ttrends/' + addr, new_title, 1]


def new_version():
    html = get_one_page('https://github.com/Rhythmicc/CUP_EXAM', headers)
    if not html:
        return None
    version, content = re.findall('New version (.*?)</h3>.*?<li>(.*?)</li>', html, re.S)[0]
    this_ver = __VERSION__
    if this_ver == version:
        return None
    else:
        return [version, content]


def update_version():
    os.system('pip install CUP_EXAM --upgrade')


if __name__ == '__main__':
    update_version()
