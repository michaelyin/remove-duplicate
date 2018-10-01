from unittest import TestCase

import numpy as np
import MySQLdb
import _mysql

'''
test mysql db
update uxblog
for each api_monitor_log table, add a field 'size'
'''


class TestEquation(TestCase):
    def setUp(self):
        # Open database connection
        port = 3306
        self.db = MySQLdb.connect(host="host6",
                                  port=port,
                                  user="uxb",
                                  passwd="uxb123",
                                  db="uxblog",
                                  charset = 'utf8',
                                  use_unicode=True)

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

        months =[10, 11, 12]
        #months =[9]


        cnt = 0
        try:
            # Execute the SQL command
            #    id | bigint(20) | NO | PRI | NULL | auto_increment |
            # | create_t | datetime | NO | | NULL | |
            # | image_name | varchar(255) | NO | | NULL | |
            # | latex | varchar(255) | NO | | NULL | |
            # | verified | bit(1) | YES | | NULL | |
            # | file_name
            for month in months:

                query = "SHOW TABLES LIKE 'api_monitor_log_2018_" + str(month) + "%'"
                print query
                cursor.execute(query)
                tables = [v for (v,) in cursor]

                # Iterate over all tables
                for t in tables:
                    if t == 'api_monitor_log_2018_9_28':
                        continue
                    query = "ALTER TABLE " + t + " ADD COLUMN `size` int DEFAULT '0';"
                    print t, "add column 'size'"
                    cursor.execute(query)



        except:
            print "Error: unable to fecth data"
            raise

        print 'total records: ', len(tables)
