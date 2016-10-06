
import re


TIME = r'''[\d]{1,2}(:[\d]{2})?'''
# TIME_RANGE_BOTH = r'''{T}-{T}(a|p|ap)?'''.format(T=TIME)
# TIME_RANGE_START = r'''-{T}(a|p|ap)?'''.format(T=TIME)
# TIME_RANGE_END = r'''{T}-(a|p|ap)?'''.format(T=TIME)
# TIME_RANGE = r'''({TRB}|{TRS}|{TRE})'''.format(TRB=TIME_RANGE_BOTH, TRS=TIME_RANGE_START, TRE=TIME_RANGE_END)
TIME_RANGE = r'''({T}-{T}|{T}-|-{T})(a|p|ap)?'''.format(T=TIME)
TIME_RANGE_SET = r'''{TR}(,{TR})*'''.format(TR=TIME_RANGE)

DAYS = r'''[MTWRFSU]{1,7}'''
DAY_RANGE = r'''{D}-{D}'''.format(D=DAYS)
DAY_WILDCARD = r'''\*'''
DAY = r'''({D}|{DR}|{DW}){{1}}'''.format(D=DAYS, DR=DAY_RANGE, DW=DAY_WILDCARD)

DATE_DAY = r'''\d{1,2}'''
DATE_MONTH_DAY = r'''\d{{1,2}}/{DD}'''.format(DD=DATE_DAY)
DATE = r'''({DD}|{DMD})'''.format(DD=DATE_DAY, DMD=DATE_MONTH_DAY)
DATE_RANGE = r'''{D}-{D}'''.format(D=DATE)

SCHEDULE = r'''(({DR}{D}{TRS})|({D}{TRS})|({TRS}))'''.format(DR=DATE_RANGE, D=DAY, TRS=TIME_RANGE_SET)
SCHEDULE_SET = r'''{S}( {S})*'''.format(S=SCHEDULE)
SCHEDULE_LABEL = r'''[^:]{1,256}: '''

FULL_SCHEDULE = r'''{SL}{SS}'''.format(SL=SCHEDULE_LABEL, SS=SCHEDULE_SET)


print "TIME", TIME
print "TIME_RANGE", TIME_RANGE
print "TIME_RANGE_SET", TIME_RANGE_SET

print "DAYS", DAYS
print "DAY_RANGE", DAY_RANGE
print "DAY_WILDCARD", DAY_WILDCARD
print "DAY", DAY

print "DATE_DAY", DATE_DAY
print "DATE_MONTH_DAY", DATE_MONTH_DAY
print "DATE", DATE
print "DATE_RANGE", DATE_RANGE

print "SCHEDULE", SCHEDULE
print "SCHEDULE_SET", SCHEDULE_SET
print "SCHEDULE_LABEL", SCHEDULE_LABEL

print "FULL_SCHEDULE", FULL_SCHEDULE


TIME = re.compile(TIME)
TIME_RANGE = re.compile(TIME_RANGE)
TIME_RANGE_SET = re.compile(TIME_RANGE_SET)

DAYS = re.compile(DAYS)
DAY_RANGE = re.compile(DAY_RANGE)
DAY_WILDCARD = re.compile(DAY_WILDCARD)
DAY = re.compile(DAY)

DATE_DAY = re.compile(DATE_DAY)
DATE_MONTH_DAY = re.compile(DATE_MONTH_DAY)
DATE = re.compile(DATE)
DATE_RANGE = re.compile(DATE_RANGE)

SCHEDULE = re.compile(SCHEDULE)
SCHEDULE_SET = re.compile(SCHEDULE_SET)
SCHEDULE_LABEL = re.compile(SCHEDULE_LABEL)

FULL_SCHEDULE = re.compile(FULL_SCHEDULE)


print TIME.match("3:45")
print TIME_RANGE.match("3:45-8:30")
print TIME_RANGE.match("9-5a")
print TIME_RANGE.match("9-5p")
print TIME_RANGE.match("9-5ap")
print TIME_RANGE_SET.match("9-5,10-2,8-4")

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
print DATE_RANGE.match("20-21")
print DATE_RANGE.match("4/20-21")
print DATE_RANGE.match("4/20-4/21")

print SCHEDULE.match("9-5")
print SCHEDULE.match("M-R9-5")
print SCHEDULE.match("4/20-21M-R9-5")
print SCHEDULE_SET.match("9-5 10-6")
print SCHEDULE_SET.match("9-5 M-R10-6")
print SCHEDULE_SET.match("W-F9-5 M-R10-6")
print SCHEDULE_SET.match("W-F9-5 M-R10-6 4/20-21*9:30-5:30ap,10-6a,4-4:15p,9-9:01ap")
print SCHEDULE_LABEL.match("Matt's schedule!! <3: ")

print FULL_SCHEDULE.match("true work: 7/11-12/30M-F9-5p")
print FULL_SCHEDULE.match("work: M-F9-5p")
print FULL_SCHEDULE.match("busy: M-F7-9a,5-6p")
print FULL_SCHEDULE.match("free: M-F6:30-p S10- U12-8p")
print FULL_SCHEDULE.match("last semester: M-R4:30-9p R8-10p S1-4p")
