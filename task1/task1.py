#!/usr/bin/env python

import time

time.sleep(2)

a = 5
b = 3

open('result/res.txt', 'w').write(str(a+b))