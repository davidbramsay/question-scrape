from scanner import scanner
from timeit import default_timer as timer
from markdownProcess import find_and_tag_questions
import html2text
import requests
import pickle


queries = ['baby questions', 'need to know about baby', 'new baby', 'what to expect baby']
outfile = 'baby_questions.pkl'
#search google and get query results
print 'searching Google for: ' + str(queries)
gstart = timer()
start = timer()

query_results = []

for q in queries:
    print q + '...'
    query_results.extend(scanner(q, 1, 4)) #search term, pages to scrape, num processes

end = timer()

print 'num results = %f' % len(query_results)
print 'time elapsed = ' + str(end-start) + ' sec'
print '...'

#now go through each query and get the raw html
print 'getting raw HTML from each website:'

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True

final_questions = []

for i, uri in enumerate(query_results):

    try:
        start = timer()
        r = requests.get(uri)
        end = timer()

        uri_body = h.handle(r.text)
        questions = find_and_tag_questions(uri_body)
        #print(uri_body)

        for j, _ in enumerate(questions):
            questions[j]['uri'] = uri

        print uri + '  ...' + str(end-start) + ' sec, ' + str(len(questions)) + ' questions found.'

        final_questions.extend(questions)

        if not i % 10: #every ten pages, save results to file
            print 'saving results...'
            with open(outfile,'wb') as f:
                pickle.dump(final_questions, f)

    except:
        pass

#save everything
with open(outfile,'wb') as f:
    pickle.dump(final_questions, f)

#print questions
for q in final_questions:

    likely_age = q['prev_age_string'] if q['prev_age_dist'] <= q['next_age_dist'] else q['next_age_dist']

    try:
        print q['question'] + '  ...' + str(likely_age)
    except:
        pass

gend = timer()
#final results
print '-----------------------------------------'
print 'total time: ' + str(gend-gstart) + ' sec'
print 'total websites: ' + str(len(query_results))
print 'total questions: ' + str(len(final_questions))
print '-----------------------------------------'

