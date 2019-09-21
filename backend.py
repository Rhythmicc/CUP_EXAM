import os

try:
    import requests
except ModuleNotFoundError:
    os.system('pip3 install requests')
    import requests
from requests.exceptions import RequestException
try:
    import xlrd
except ModuleNotFoundError:
    os.system('pip3 install xlrd')
    import xlrd
from xlrd import xldate_as_tuple
import re
import sys

base_dir = sys.path[0]
if sys.platform.startswith('win'):
    dir_char = '\\'
else:
    dir_char = '/'
base_dir += dir_char
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15',
}
data = {'课程名': {}, '上课老师': {}, '主修班级': {}}
name_col = 0
teacher_col = 0
sc_col = 0
sheet = None


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


def getNewXls(url):
    html = get_one_page(url, headers=headers)
    if not html:
        return False
    title = re.findall('<h3>(.*?)</h3>', html, re.S)[0]
    als = re.findall('<a.*?href="(.*?)">.*?>(.*?)<', html, re.S)
    res = None
    for a in als:
        if a[0].endswith('xls'):
            cnt = countPoint(a[0])
            url = '/'.join(url.split('/')[:-cnt]) + a[0][cnt:]
            res = a
            break
    if not res:
        return False
    content = requests.get(url, headers).content
    with open(base_dir + 'content.xls', 'wb') as f:
        f.write(content)
    with open(base_dir + '.last_title.txt', 'w') as f:
        f.write(title + '\n')
        f.write(res[1] + '\n')
    return True


def init():
    xls = xlrd.open_workbook(base_dir + 'content.xls')
    global name_col, teacher_col, sc_col, sheet, data
    sheet = xls.sheet_by_index(0)
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
    data = {'课程名': {}, '上课老师': {}, '主修班级': {}}
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
        res += '主修班级：' + linkstr + '\n'
        day = "%04d年%02d月%02d日" % xldate_as_tuple(line[4], 0)[:3]
        res += '考试时间：' + day + '(周%s) ' % line[2] + line[5] + '\n'
        res += '考试地点：' + line[-1].replace('\n', ',') + '\n'
    del res_set
    return res


def pre_check():
    return os.path.exists(base_dir + 'content.xls')


def new_note_check():
    with open(base_dir + '.last_title.txt', 'r') as f:
        lines = f.readlines()
        title = lines[0].strip()
        filename = lines[1].strip()
    html = get_one_page('http://www.cup.edu.cn/jwc/Ttrends/index.htm', headers)
    if not html:
        return -1
    ls = re.findall('<li>(.*?)</li>', html, re.S)
    for i in ls:
        content = re.findall('<a.*?href="(.*?)">(.*?)</a>', i, re.S)
        if content:
            addr, new_title = content[0]
            if new_title == title:
                html = get_one_page('http://www.cup.edu.cn/jwc/Ttrends/' + addr, headers)
                aim_li = re.findall('<li.*?>(.*?)</li>', html, re.S)[-1]
                new_filename = re.findall('<font.*?>(.*?)</font>', aim_li, re.S)[0]
                if new_filename != filename:
                    return ['http://www.cup.edu.cn/jwc/Ttrends/' + addr, new_filename, 0]
                return 0
            if new_title.endswith('考试安排'):
                return ['http://www.cup.edu.cn/jwc/Ttrends/' + addr, new_title, 1]


def new_version():
    html = get_one_page('https://github.com/Rhythmicc/CUP_EXAM', headers)
    if not html:
        return None
    version, content = re.findall('New version (.*?)</h3>.*?<p>(.*?)</p>', html, re.S)[0]
    with open(base_dir + '.version', 'r') as f:
        this_ver = f.read().strip()
    if this_ver == version:
        return None
    else:
        return [version, content]


def update_version():
    package = requests.get('https://github.com/Rhythmicc/CUP_EXAM/archive/master.zip', headers).content
    with open(base_dir + 'exam.zip', 'wb') as f:
        f.write(package)
    root_dir = dir_char.join(base_dir.split(dir_char)[:-2]) + dir_char
    while os.system('unzip -o ' + base_dir + 'exam.zip -d ' + root_dir):
        if dir_char == '\\':
            package = requests.get('http://gnuwin32.sourceforge.net/downlinks/unzip.php', headers).content
            with open('unzip.exe', 'wb') as f:
                f.write(package)
            os.system('unzip.exe')
            exit('ERROR! No command "unzip", but do not worry about that, We have download it for you.')
        else:
            os.system('sudo apt-get install unzip')
    status = os.system('python3 ' + root_dir + 'CUP_EXAM-master/setup.py --direct')
    if status:
        os.system('python ' + root_dir + 'CUP_EXAM-master/setup.py --direct')
    if dir_char == '/':
        os.system('rm ' + base_dir + 'exam.zip')
    else:
        os.system('del ' + base_dir + 'exam.zip')


if __name__ == '__main__':
    update_version()
