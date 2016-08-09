import re
import sys

q_words = ['does','what','how','when','have']

def get_ages(markdown_source):
    #take in markdown string, get back a list of dicts of the form
    #a[0].index, a[0].age_string

    num_words= ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve', \
                'thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty', \
                'first', 'second', 'third', 'fourth','fifth','sixth','seventh','eighth','ninth','tenth', \
                'eleventh','twelfth','thirteenth','fourteenth','fifteenth','sixteenth','seventeenth','eighteenth','nineteenth']

    age_words= ['age', 'day','month','year', 'yo', 'y\.o\.']

    reg_age = r'[^ \t\n\r\f\v<>\.\!\?\*_]*(' + r'|'.join([word for word in age_words]) + r')[^ \t\n\r\f\v<>\.\!\?\*_]*'
    reg_num = r'[^ \t\n\r\f\v<>\.\!\?\*_]*([0-9]+|' + r'|'.join([word for word in num_words]) + r')[^ \t\n\r\f\v<>\.\!\?\*_]*'

    reg_pat_1 = r'(' + reg_age + r')\s(' + reg_num + r')'
    reg_pat_2 = r'(' + reg_num + r')\s(' + reg_age + r')'

    reg_pat = r'(' + reg_pat_1 + r')|(' + reg_pat_2 + r')'

    return_val = []

    for m in re.finditer(reg_pat, markdown_source, flags=re.IGNORECASE):
        return_val.append({'index': m.start(), 'age_string': m.group().replace('\n',' ').replace('\t',' ').strip(' #*')})

    return return_val


def get_questions(markdown_source):
    #take in markdown string, get back a list of dicts of the form
    #a[0].index, a[0].question
    reg_question = r'[^<>\.\?\!\n]+\?'

    return_val = []

    for m in re.finditer(reg_question, markdown_source, flags=re.IGNORECASE):
        return_val.append({'index': m.start(), 'question': m.group().replace('\n',' ').replace('\t',' ').strip(' #*')})

    return return_val


def get_headers(markdown_source):
    #take in markdown string, get back a list of dicts of the form
    #a[0].index_start, a[0].index_end
    reg_header = r'(^\#.*)|(\*+.+?\*+)|(_+.+?_+)'

    return_val = []

    for m in re.finditer(reg_header, markdown_source, flags=re.MULTILINE):
        return_val.append({'index_start': m.start(), 'index_end': m.end()})

    return return_val


def in_header(index, headers):
    #return true if index is within a header, false otherwise

    for h in headers:
        if (index >= h['index_start'] and index <= h['index_end']):
            return True

    return False


def find_and_tag_questions(markdown_source):
    #take in markdown string, get back a list of dicts of the form
    #a[0].index, a[0].question
    #a[0].prev_age_string, a[0].prev_age_in_header, a[0].prev_age_dist
    #a[0].next_age_string, a[0].next_age_in_header, a[0].next_age_dist

    ages = get_ages(markdown_source)
    headers = get_headers(markdown_source)
    questions = get_questions(markdown_source)


    curr_age_ind = 0

    for i, q in enumerate(questions):

        #find largest age index not past question
        while (curr_age_ind < len(ages)):
            if ages[curr_age_ind]['index'] < q['index']:
                curr_age_ind = curr_age_ind + 1
            else:
                break

        curr_q_ind = q['index'] + (len(q['question'])/2)

        if curr_age_ind == 0: #no before date
            questions[i]['prev_age_string'] = ''
            questions[i]['prev_age_in_header'] = False
            questions[i]['prev_age_dist'] = sys.maxint
            questions[i]['next_age_string'] = ages[0]['age_string']
            questions[i]['next_age_in_header'] = in_header(ages[0]['index'], headers)
            questions[i]['next_age_dist'] = abs( curr_q_ind - ( ages[0]['index'] + (len(ages[0]['age_string'])/2) ) )

        elif curr_age_ind == len(ages):  #no after date
            questions[i]['prev_age_string'] = ages[curr_age_ind-1]['age_string']
            questions[i]['prev_age_in_header'] = in_header(ages[curr_age_ind-1]['index'], headers)
            questions[i]['prev_age_dist'] = abs( curr_q_ind - ( ages[curr_age_ind-1]['index'] + (len(ages[curr_age_ind-1]['age_string'])/2) ) )
            questions[i]['next_age_string'] = ''
            questions[i]['next_age_in_header'] = False
            questions[i]['next_age_dist'] = sys.maxint

        else: #bookended by curr_age_ind-1, curr_age_ind
            questions[i]['prev_age_string'] = ages[curr_age_ind-1]['age_string']
            questions[i]['prev_age_in_header'] = in_header(ages[curr_age_ind-1]['index'], headers)
            questions[i]['prev_age_dist'] = abs( curr_q_ind - ( ages[curr_age_ind-1]['index'] + (len(ages[curr_age_ind-1]['age_string'])/2) ) )
            questions[i]['next_age_string'] = ages[curr_age_ind]['age_string']
            questions[i]['next_age_in_header'] = in_header(ages[curr_age_ind]['index'], headers)
            questions[i]['next_age_dist'] = abs( curr_q_ind - ( ages[curr_age_ind]['index'] + (len(ages[curr_age_ind]['age_string'])/2) ) )

    return questions

