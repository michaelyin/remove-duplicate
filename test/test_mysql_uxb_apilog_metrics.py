from unittest import TestCase

import numpy as np
import MySQLdb

from scipy import stats

'''
test mysql db
update uxblog
for each api_monitor_log table, add a field 'size'
'''


def print_stats(time_list):
    lst = map(int, time_list)
    np_a = np.asarray(lst)
    print 'max:', max(lst), ', mean: ', sum(lst) / len(lst), ', min: ', min(lst), \
        ', 98%: ', np.percentile(np_a, 98), ', 50%: ', np.percentile(np_a, 50), \
        ', 2 sec. percentile: ', stats.percentileofscore(np_a, 2000)


class TestEquation(TestCase):
    def setUp(self):
        # Open database connection
        port = 3306
        self.db = MySQLdb.connect(host="host6",
                                  port=port,
                                  user="uxb",
                                  passwd="uxb123",
                                  db="uxblog",
                                  charset='utf8',
                                  use_unicode=True)
        self.api_mon = '11'
        self.api_days = ['25', '26', '27']

    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        print "\nTest:tearDown_:begin"
        # disconnect from server
        self.db.close()

    def test_mysql(self):
        '''
        test fancy index
        array of indices on the matrix
        used a lot in 2-D matrix value update
        :return:
        '''

        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()
        api_list = ["/zy/m/s/hk/2/view", \
                    "/zy/m/s/hk/2/commit",\
                    "/zy/m/s/hk/4/indexHk",\
                    "/zy/m/t/hk/2/detail",\
                    "/zy/m/t/hk/book/2/questions2",\
                    "/zy/m/s/hk/3/view",\
                    "/f/latex/img", \
                    "/fs/%"]

        cnt = 0
        for api in api_list:
            print "===> api: ", api
            for api_day in self.api_days:
                try:

                    query = "select cost_time from api_monitor_log_2018_" + \
                            self.api_mon + '_' + api_day + " where api=" + \
                            "'" + api + "'"
                    if '%' in api:
                        query = "select cost_time from api_monitor_log_2018_" + \
                            self.api_mon + '_' + api_day + " where api like " + \
                            "'" + api + "'"
                    print query
                    cursor.execute(query)
                    results = cursor.fetchall()
                    ct_list = []
                    for row in results:
                        ct = row[0]
                        # print type(ct)
                        ct_list.append(ct)
                    print_stats(ct_list)



                except:
                    print "Error: unable to fecth data"
                    raise

                print 'total records: ', len(results)
                print '\n'
