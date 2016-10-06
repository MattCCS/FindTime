
import re


TIME = r'''[\d]{1,2}(:[\d]{2})?'''
TIME_RANGE = r'''(({T}-{T})|({T}-)|(-{T}))(a|p|ap)?'''.format(T=TIME)
TIME_RANGE_SET = r'''{TR}(,{TR})*'''.format(TR=TIME_RANGE)

DAY_SINGLE = r'''[MTWRFSU]{1}'''
DAYS = r'''[MTWRFSU]{1,7}'''
DAY_RANGE = r'''{DS}-{DS}'''.format(DS=DAY_SINGLE)
DAY_WILDCARD = r'''\*'''
DAY = r'''(({D})|({DR})|({DW}))'''.format(D=DAYS, DR=DAY_RANGE, DW=DAY_WILDCARD)

DATE_DAY = r'''\d{1,2}'''
DATE_MONTH_DAY = r'''\d{{1,2}}/{DD}'''.format(DD=DATE_DAY)
DATE = r'''({DD})|({DMD})'''.format(DD=DATE_DAY, DMD=DATE_MONTH_DAY)
DATE_RANGE = r'''{DMD}-{D}'''.format(DMD=DATE_MONTH_DAY, D=DATE)


print "TIME: {}\n".format(TIME)
print "TIME_RANGE: {}\n".format(TIME_RANGE)
print "TIME_RANGE_SET: {}\n".format(TIME_RANGE_SET)

print "DAY_SINGLE: {}\n".format(DAY_SINGLE)
print "DAYS: {}\n".format(DAYS)
print "DAY_RANGE: {}\n".format(DAY_RANGE)
print "DAY_WILDCARD: {}\n".format(DAY_WILDCARD)
print "DAY: {}\n".format(DAY)

print "DATE_DAY: {}\n".format(DATE_DAY)
print "DATE_MONTH_DAY: {}\n".format(DATE_MONTH_DAY)
print "DATE: {}\n".format(DATE)
print "DATE_RANGE: {}\n".format(DATE_RANGE)


TIME = re.compile(TIME)
TIME_RANGE = re.compile(TIME_RANGE)
TIME_RANGE_SET = re.compile(TIME_RANGE_SET)

DAY_SINGLE = re.compile(DAY_SINGLE)
DAYS = re.compile(DAYS)
DAY_RANGE = re.compile(DAY_RANGE)
DAY_WILDCARD = re.compile(DAY_WILDCARD)
DAY = re.compile(DAY)

DATE_DAY = re.compile(DATE_DAY)
DATE_MONTH_DAY = re.compile(DATE_MONTH_DAY)
DATE = re.compile(DATE)
DATE_RANGE = re.compile(DATE_RANGE)


print TIME.match("3:45")
print TIME_RANGE.match("3:45-8:30")
print TIME_RANGE.match("9-5a")
print TIME_RANGE.match("9-5p")
print TIME_RANGE.match("9-5ap")
print TIME_RANGE_SET.match("9-5,10-2,8-4")

print DAY_SINGLE.match("MWR")
print DAYS.match("MWR")
print DAY_RANGE.match("M-R")
print DAY_WILDCARD.match("*")
print DAY.match("MWR")
print DAY.match("M-R")
print DAY.match("*")

print DATE_DAY.match("20")
print DATE_MONTH_DAY.match("4/20")
print DATE.match("20")
print DATE.match("4/20")
print DATE_RANGE.match("20-21") == None
print DATE_RANGE.match("4/20-21")
print DATE_RANGE.match("4/20-4/21")
