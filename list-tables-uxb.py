import os
import hashlib
from collections import defaultdict
import csv
import codecs
import re

src_folder = "/home/michael/workspace-yoo/yoo/module/common/uxb-service"

def table_from(line):
    '''
    select * from 'table name'
    :param line:
    :return: table name
    '''
    ind = line.find("from")
    s1 = line[ind:len(line)]
    sArr = s1.split()
    if len(sArr) == 1: return ""
    t_name = sArr[1]
    if "select" in t_name:
        return ""
    if "`" in t_name:
        t_name = re.sub('[`]', '', t_name)
    return t_name

def table_update(line):
    ind = line.find("update")
    s1 = line[ind:len(line)]
    sArr = s1.split()
    if len(sArr) == 1: return ""
    t_name = sArr[1]
    if "select" in t_name: return ""
    if "`" in t_name:
        t_name = re.sub('[`]', '', t_name)
    return t_name

if __name__ == "__main__":
    """
    Starting block of script
    """

    # The dict will have a list as values
    md5_dict = defaultdict(list)

    file_types_inscope = ["sql"]

    sql_file_lst = []
    sql_files_cnt = 0
    table_set = set([])
    # Walk through all files and folders within directory
    for path, dirs, files in os.walk(src_folder):
        #print("Analyzing {}".format(path))
        for each_file in files:
            #print each_file
            if each_file.split(".")[-1].lower() in file_types_inscope:
                # The path variable gets updated for each subfolder
                file_path = os.path.join(os.path.abspath(path), each_file)
                if 'target' in file_path: continue
                if 'init' in file_path: continue
                if 'bin' in file_path: continue
                print file_path
                sql_file_lst.append(file_path)
                sql_files_cnt += 1
    print 'total sql files: ', sql_files_cnt

    cnt = 0
    for sql_file in sql_file_lst:
        f = codecs.open(sql_file, "r", "utf-8")

        for line in f:
            line = line.lower()
            if line.startswith("#"): continue
            if line.strip() == "": continue
            if line.startswith("create table"): continue
            if line.startswith("create index"): continue
            if "from (" in line or "from  (" in line: continue

            if " from " in line:
                print line
                t = table_from(line)
                table_set.add(t)
                cnt += 1

            if "update " in line:
                print line
                t = table_update(line)
                table_set.add(t)
                cnt += 1

    print "line cnt: ", cnt
    print "table size: ", len(table_set)

    for t in table_set:
        print t

