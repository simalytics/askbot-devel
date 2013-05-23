
import random

PRINT_THREAD = True
PRINT_POST = True
FILE = open('/usr/share/dict/british-english')
NUM_RECORDS = 15000
POST_LENGTH = 250
TITLE_LENGTH = 15

words = FILE.readlines()
count = len(words) - 1

sql_threads1 = "INSERT INTO askbot_thread " \
"(last_activity_at, title, approved, tagnames, favourite_count, language_code, added_at, last_activity_by_id) \n"

sql_posts1 = "INSERT INTO askbot_post "\
"(wiki, text, thread_id, html, added_at, summary, approved, author_id, " \
"post_type, vote_up_count, offensive_flag_count, score, comment_count," \
"vote_down_count, deleted, locked, is_anonymous)\n"

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
            sql_threads += ("; " if i else "") + sql_threads1 + \
            "VALUES (now(), \n" \
            "\"%s\", \n" \
            "1, \n " \
            "'test1 test2', \n" \
            "1, \n" \
            "'en', \n" \
            "now(), \n" \
            "1)\n" % title.strip()

        if PRINT_POST:
            sql_posts += ("; " if i else "") + sql_posts1 + \
            "VALUES (0, \n" \
            "\"%s\", \n" \
            "%d, \n" \
            "\"<p>%s</p>\", \n" \
            "now(), \n" \
            "\"%s\", \n" \
            "1,\n" \
            "1, \n" \
            "'question',\n" \
            "0,\n" \
            "0, \n" \
            "0, \n" \
            "0, \n" \
            "0, \n" \
            "0, \n" \
            "0, \n" \
            "0) \n" % (text.strip(), i+1, text.strip(), text[0:400].strip())
    else:
        if PRINT_THREAD:

            sql_threads += ", (now(), \"%s\", 1, 'test1 test2', 1, 'en', " \
            "now(), 1)\n" % title.strip()

        if PRINT_POST:
            sql_posts += ", (0, \"%s\", %d, " \
            "\"<p>%s</p>\", now(), \"%s\", " \
            "1, 1, 'question', 0," \
            "0, 0, 0, 0 \n, " \
            "0, 0, 0)\n" % \
            (text.strip(), i+1,
            text.strip(), text[0:400].strip())

print "USE testdb;"
print sql_threads + ';'
print sql_posts + ';'

