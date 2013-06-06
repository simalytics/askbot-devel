
import random

PRINT_THREAD = False
PRINT_POST = True
FILE = open('/usr/share/dict/british-english')
NUM_RECORDS = 50000
POST_LENGTH = 200
TITLE_LENGTH = 15

words = FILE.readlines()
count = len(words) - 1

sql_threads1 = "INSERT INTO askbot_thread " \
"(last_activity_at, title, approved, tagnames, favourite_count, language_code, added_at, last_activity_by_id, answer_count, view_count, closed, score, deleted) "

sql_posts1 = "INSERT INTO askbot_post "\
"(wiki, text, thread_id, html, added_at, summary, approved, author_id, " \
"post_type, vote_up_count, offensive_flag_count, score, comment_count," \
"vote_down_count, deleted, locked, is_anonymous, language_code) "

sql_posts = ""
sql_threads = ""

for i in range(0, NUM_RECORDS):
    if PRINT_THREAD:
        titlelen = random.randint(5, TITLE_LENGTH)
        title = ""
        for j in range(0, titlelen):
            idx = random.randint(0, count)
            title += words[idx].strip() + ' '

    if PRINT_POST:
        textlen = random.randint(80, POST_LENGTH)
        text = ""
        for j in range(0, textlen):
            idx = random.randint(0, count)
            text += words[idx].strip() + ' '

    if i % 200 == 0:
        if PRINT_THREAD:
            sql_threads += (";\n " if i else "") + sql_threads1 + \
            "VALUES (now(), " \
            "'%s', " \
            "True, " \
            "'test1 test2', " \
            "1, " \
            "'en', " \
            "now(), " \
            "1, 0, 0, False, 0, False) " % title.strip().replace("'","''")

        if PRINT_POST:
            modtext = text.replace("'","''")
            sql_posts += ("; " if i else "") + sql_posts1 + \
            "VALUES (False,  " \
            "'%s',  " \
            "%d,  " \
            "'<p>%s</p>',  " \
            "now(),  " \
            "'%s',  " \
            "True, " \
            "1,  " \
            "'question', " \
            "0, " \
            "0,  " \
            "0,  " \
            "0,  " \
            "0,  " \
            "False,  " \
            "False,  " \
            "False, 'en')  " % (modtext.strip(), i+1, modtext.strip(), text[0:400].strip().replace("'","''"))
    else:
        if PRINT_THREAD:

            sql_threads += ", (now(), '%s', True, 'test1 test2', 1, 'en', " \
            "now(), 1, 0, 0, False, 0, False) " % title.strip().replace("'","''")

        if PRINT_POST:
            modtext = text.replace("'","''")
            sql_posts += ", (False, '%s', %d, " \
            "'<p>%s</p>', now(), '%s', " \
            "True, 1, 'question', 0," \
            "0, 0, 0, 0  , " \
            "False, False, False, 'en') " % \
            (modtext.strip(), i+1,
            modtext.strip(), text[0:400].strip().replace("'","''"))

print sql_threads + ';'
print sql_posts + ';'

