import pickle
import enchant

processfile = 'baby_questions.pkl'

'''
def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)
'''

def english(question):
    #check if more than 4 words that are english
    words = question.split()
    words[-1] = words[-1][:-1] #remove question mark

    num_english_words = 0
    d = enchant.Dict('en_US')

    for w in words:
        if w:
            if d.check(w):
                num_english_words += 1

    if (num_english_words > 3) and (len(words)-num_english_words < 4):
        return True
    else:
        return False


def delete_duplicates(questions):
    #delete and return array without duplicate questions
    seen_questions = set()
    new_questions = []
    for d in questions:
        q = d['question']
        if q not in seen_questions:
            seen_questions.add(q)
            new_questions.append(d)

    return new_questions

def mergeSort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i]['count'] < righthalf[j]['count']:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1


def get_words(questions):
    #return a dict of the words, with the number of words and
    #the index of the question that has it, ordered from most common to least
    #[{'the':{'count':750,'question_indices': [0, 4, 5]}, {'art':{'count':23,'question_indices':[6, 4]}]
    word_array={}
    for i, q in enumerate(questions):

        words = q['question'].split()

        for w in words:
            if w in word_array:
                word_array[w]['count'] += 1
                word_array[w]['question_indices'].append(i)
            else:
                word_array[w]={'count': 1, 'question_indices': [i]}

    print word_array
    word_list = []
    for key, val in word_array.iteritems():
        print 'key:: ' + key
        print 'val:: ' + str(val)
        append_item = {'word': key}
        append_item.update(val)
        print 'updated: ' + str(append_item)
        word_list.append(append_item)

    print word_list

    mergeSort(word_list)

    return word_list

questions = pickle.load( open( processfile, "rb" ) )

#delete duplicate questions
questions = delete_duplicates(questions)

#check if question has 3 english words in it before we consider it a question
questions = [q for q in questions if english(q['question'])]

word_list = get_words(questions)
print word_list

'''
#resave questions
with open(processfile,'wb') as f:
    pickle.dump(final_questions, f)
'''

for q in questions:

    likely_age = q['prev_age_string'] if q['prev_age_dist'] <= q['next_age_dist'] else q['next_age_dist']

    try:
        print q['question'] + '  ...' + str(likely_age)
    except:
        pass
