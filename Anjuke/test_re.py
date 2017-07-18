#coding=utf8
text='[ 良庆 五象大道 ] 金龙路8号(五象大道与宋厢路交汇处)'
test='a-H-c-d'
b=test.split('-')[1]
print b
test='a b c d'
#a=test.split(r'\s+')[1]
c=text.split(' ')[1]
print c
#print a

import re
s = 'a g t hj'
print re.split(r'\s+', s)[1]      # 结果: ['a', 'b', 'c', 'd', 'e']
print re.split(r'(\s+)', s)[1]   # 结果: ['a', ' ', 'b', ' ', 'c', ' ', 'd', ' ', 'e']

data="\xe4\xb8\xad\xe5\x9f\xba\xe5\xa4\xa7\xe5\x8e\xa6-\xe5\x85\xb4\xe5\xae\x81"
print data.decode("utf-8")