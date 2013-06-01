import random
import time

PRINT_THREAD = False
PRINT_POST = True
FILE = open('/usr/share/dict/british-english')
NUM_RECORDS = 50000
POST_LENGTH = 250
TITLE_LENGTH = 15

words = FILE.readlines()
count = len(words) - 1

sql_threads1 ="last_activity_at, title, approved, tagnames, favourite_count, language_code, added_at, last_activity_by_id, answer_count, view_count, closed, score, deleted\n"

sql_posts1 = "wiki, text, thread_id, html, added_at, summary, approved, author_id, " \
"post_type, vote_up_count, offensive_flag_count, score, comment_count," \
"vote_down_count, deleted, locked, is_anonymous, language_code\n"

sql_posts = sql_posts1
sql_threads = sql_threads1

for i in range(0, NUM_RECORDS):
    if PRINT_THREAD:
        titlelen = random.randint(5, TITLE_LENGTH)
        title = ""
        for j in range(0, titlelen):
            idx = random.randint(0, count)
            title += words[idx].strip() + ' '
        udata = title.decode("utf-8")
        title = udata.encode("ascii","ignore")
        sql_threads += (
        "%s," \
            "%s," \
            "True," \
            "test1 test2," \
            "1," \
            "en," \
            "%s," \
            "1,0,0,False,0,False\n" % (time.strftime('%Y-%m-%d %H:%M:%S %Z', time.gmtime()), title.strip(), time.strftime('%Y-%m-%d %H:%M:%S %Z', time.gmtime())))

    if PRINT_POST:
        textlen = random.randint(80, POST_LENGTH)
        text = ""
        for j in range(0, textlen):
            idx = random.randint(0, count)
            text += words[idx].strip() + ' '

        modtext = text
        udata = text.decode("utf-8")
        text=udata.encode("ascii","ignore")

        sql_posts += ("False, " \
            "%s," \
            "%d," \
            "<p>%s</p>,  " \
            "%s," \
            "%s," \
            "True," \
            "1," \
            "question, " \
            "0," \
            "0," \
            "0," \
            "0," \
            "0," \
            "False," \
            "False," \
            "False,en\n " % (modtext.strip(), i+1, modtext.strip(), time.strftime('%Y-%m-%d %H:%M:%S %Z', time.gmtime()), text[0:400].strip()))

if PRINT_THREAD:
    print sql_threads.strip()

if PRINT_POST:
    print sql_posts.strip()
