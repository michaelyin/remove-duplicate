# -*- coding: utf-8 -*-
from unittest import TestCase

import MySQLdb

'''
test mysql db
titan上的parse改为并行后现在处理速度是大约一秒钟处理4道题。
大概还剩42万道题。估计还需要29.5小时。
python -m unittest test.test_mysql_titan_uxb_question.TestQuestionTable.test_iter_q_t_0
'''


class TestQuestionTable(TestCase):
    def setUp(self):
        # Open database connection

        # Open database connection
        db_host = 'titan'
        port = 3308
        self.db = MySQLdb.connect(host=db_host,
                                  port=port,
                                  user="uxb",
                                  passwd="uxb123",
                                  db="uxb",
                                  charset='utf8',
                                  use_unicode=True)

    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        print "\nTest:tearDown_:begin"
        # disconnect from server
        self.db.close()
    def test_iter_q_t_0(self):
        self.iter_q_table(0)
    def test_iter_q_t_1(self):
        self.iter_q_table(1)
    def test_iter_q_t_2(self):
        self.iter_q_table(2)

    def iter_q_table(self, remainder):
        '''
        iterate all Qs, and find out the max length of the con·cat·e·nating choice_* and content
        :return:
        '''
        cursor = self.db.cursor()
        cursor.execute("select id, content, choice_a, choice_b, choice_c, choice_d, choice_e, choice_f from question where tokens is NULL")
        numrows = cursor.rowcount
        max_total_len = 1
        questions = cursor.fetchall()
        id_list =[]
        q_str_list = []
        for q in questions:
            id, choice_a, choice_b, choice_c, choice_d, choice_e, choice_f, content = q
            row = q
            print q[0]
            id_list.append(q[0])
            q_str = self.assemble_q_str(row)
            q_str_list.append(q_str)

            num = 32

            if len(id_list) < num:
                continue
            id_tokens_list = parse_svc(id_list, q_str_list)
            self.persist_q_token_list(id_tokens_list)

            id_list = []
            q_str_list = []

        if len(id_list) > 0:
            id_tokens_list = parse_svc(id_list, q_str_list)
            self.persist_q_token_list(id_tokens_list)



    def persist_q_token_list(self, id_tokens_list):
        '''

        :param id_tokens_list: it_tokens pair list
        :return:
        '''
        cursor = self.db.cursor()
        print 'tokens len: ', len(id_tokens_list)
        for id_tokens in id_tokens_list:
            print "id: ", id_tokens[0]
            print "tokens: ", id_tokens[1]
            cursor.execute("UPDATE question SET tokens =%s, update_at=now() WHERE id =%s", (id_tokens[1], id_tokens[0]))
        self.db.commit()
        print 'done commit!'

    def assemble_q_str(self, row):
        total_len = 0
        q_str = ''
        for idx in xrange(1, 8):
            if row[idx] is not None:
                total_len = total_len + len(row[idx])
                q_str = q_str + row[idx]
        print 'q str: ', q_str
        return q_str


    def test_q_null_value(self):
        cursor = self.db.cursor()
        cursorUpdate = self.db.cursor()
        cursor.execute("select id, choice_a, choice_b, choice_c, choice_d, choice_e, choice_f, content, length(choice_a), length(content) from question where id = 300995")
        numrows = cursor.rowcount

        for x in xrange(0, numrows):
            row = cursor.fetchone()
            print row[0], "-->", row[1], row[2], row[3], row[4], row[5], row[6], row[7]
            print 'choice_a:', row[1]
            print 'choice_b:', row[2]
            print 'choice_c:', row[3]
            print 'choice_d:', row[4]
            print 'choice_e:', row[5]
            print 'choice_f:', row[6]
            print 'content:',  row[7]
            print 'length of choice_a: ', row[8]
            print 'length of content: ', row[9]
            print 'lenght of choice_a (python): ', len(row[1])
            print 'length of choice_f (python):', row[6]
            print "choice_f is None: ", row[6] is None
            print 'type of choice_e: ', type(row[5])

        print 'total rows: ', numrows

    def test_q_order_by(self):
        '''
        test fancy index
        array of indices on the matrix
        used a lot in 2-D matrix value update
        :return:
        '''

        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()

        sql = "select id, content from question order by create_at desc limit 40;"

        cnt = 0
        try:
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            print 'total records: ', len(results)
            max_size = 1
            for row in results:
                cnt = cnt +1
                id, scg = row[0], row[1]
                #print 'type of verified: ', type(verified)
                # Now print fetched result
                temp_s = len(scg)
                print 'saving scg... ', id, 'content length: ', temp_s
                if temp_s > max_size:
                    max_size = temp_s
                self.save_scg_2_file(cnt, scg)
                #if cnt>10: break

        except:
            print "Error: unable to fecth data"
            raise

        print 'total records: ', len(results)
        print 'max content size: ', max_size

    def save_scg_2_file(self, i, scg):
        import codecs

        textfile = codecs.open(str(i) + '_content.txt', "w", "utf-8")
        #textfile = open( str(i) + '_scg.txt', 'w')
        textfile.write(scg)
        textfile.close()

import requests
headers = dict()
headers['Content-Type'] = 'application/json;charset=UTF-8'
def parse_svc(id_list, q_strs):
    '''

    :param q_strs: list of q_str
    :return:
    '''
    params = None
    data_list = []
    number_q = len(id_list)

    for idx in xrange(0, number_q):
        data = dict()
        data['question'] = q_strs[idx]
        data['qid'] = id_list[idx]
        data_list.append(data)
    response = requests.request('post', 'http://titan:8080/parse', json=data_list, headers=headers, params=params)
    print type(response)

    print("Status code: %d" % (response.status_code))
    resp_jsons = response.json()

    return [(id_tokens['qid'],id_tokens['parsed'][0]) for id_tokens in resp_jsons]