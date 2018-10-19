# -*- coding: utf-8 -*-
import base64
import os
import sys
import requests
from unittest import TestCase
import time



class TestTokenService(TestCase):
    def setUp(self):
        # Open database connection
        self._url = 'http://titan:8080/parse'
        self.headers = dict()

        # headers['accept']='application/json;charset=UTF-8'
        self.headers['Content-Type'] = 'application/json;charset=UTF-8'


    def test_parse_svc(self):
        start = time.time()
        # _url = 'http://localhost:8080/api/audio'
        params = None

        data = dict()
        data['question'] = u"设非空集合<ux-mth>M</ux-mth>同时满足下列两个条件：．则下列结论正确的是（&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ）首先，针对<ux-mth>n</ux-mth>是否为奇数和偶数进行讨论，分为奇数和偶数，然后，根据集合之间的关系进行求解即可．解：若<ux-mth>n</ux-mth>为偶数，则集合中取出两数，使得其和为<ux-mth>n</ux-mth>，这样的数共有<ux-mth>\frac{n}{2}</ux-mth> 对，所以此时集合<ux-mth>M</ux-mth>的个数为 <ux-mth>2^{\frac{n}{2}}-1</ux-mth>个，若<ux-mth>n</ux-mth>为奇数，则单独取出中间的那个数，所以此时集合<ux-mth>M</ux-mth>的个数为<ux-mth>2^{\frac{n+1}{2}} -1</ux-mth>个，故选：B"
        lst_d = []
        data1 = dict()
        data1['question'] = u"<span>在一次运输任务中，一辆汽车将一批货物从甲地运往乙地，到达乙地卸货后返回，设汽车从甲地出发</span>&nbsp;<ux-mth>x(\rm h)</ux-mth>&nbsp;<span>时，汽车与甲地的距离为</span>&nbsp;<ux-mth>y(\rm km)</ux-mth>&nbsp;<span>, </span>&nbsp;<ux-mth>y</ux-mth>&nbsp;<span>与</span>&nbsp;<ux-mth>x</ux-mth>&nbsp;<span>的函数关系如图所示 . 根据图像信息，解答下列问题 :     </span><p></p><p><span>（1）这辆汽车的往、返速度是否相同 ? 请说明理由 ;     </span></p><p><span>（2）求返程中</span>&nbsp;<ux-mth>y</ux-mth>&nbsp;<span>与</span>&nbsp;<ux-mth>x</ux-mth>&nbsp;<span>之间的函数表达式 ;&nbsp;     </span></p><p><span>（3）求这辆汽车从甲地出发</span>&nbsp;<ux-mth>4\rm h</ux-mth>&nbsp;<span>时与甲地的距离&nbsp; . </span></p>"
        data2=dict()
        data2['question'] = u"下列表述：<span>①</span>综合法是由因导果法；<span>②</span>综合法是顺推法；<span>③</span>分拆法是拆果索因法；<span>④</span>分析法是间接证明法；<span>⑤</span>分析法是逆推法．其中正确的语句有（　　）&nbsp;<ux-mth>2</ux-mth>&nbsp;个<span></span>&nbsp;<ux-mth>3</ux-mth>&nbsp;个&nbsp;<ux-mth>4</ux-mth>&nbsp;<span>个</span><span></span>&nbsp;<ux-mth>5</ux-mth>&nbsp;<span>个</span>"
        lst_d.append(data)
        lst_d.append(data1)
        lst_d.append(data2)
        response = requests.request('post', self._url, json=lst_d, headers=self.headers, params=params)
        print type(response)

        print("Status code: %d" % (response.status_code))
        json = response.json()
        print type(json)
        rsp_utf8 = json[0][0]
        print "====>", rsp_utf8
        rsp_1 = json[1][0]
        print "rsp 1 ===> :", rsp_1
        s_lst = rsp_utf8.split(" ")
        '''
        for s in s_lst:
            print s.encode('utf-8')
        print 'total tokens', len(s_lst)
        '''
        end = time.time()
        print 'time elipsed: ', (end - start)



# Pass the image data to an encoding function.
def encode_image(imagename):
  with open(imagename, 'rb') as f:
      image_content = f.read()
  f.close()
  return base64.b64encode(image_content)


