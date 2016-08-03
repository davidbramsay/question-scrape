from scanner import scanner
from timeit import default_timer as timer

start = timer()
results=scanner('david ramsay', 3, 3)
end = timer()

print results
print 'num results = %f' % len(results)
print 'time elapsed = ' + str(end-start) + ' sec'
