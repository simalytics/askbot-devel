
import random

FILE = open('/usr/share/dict/british-english')
NUM_RECORDS = 50000
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
    titlelen = random.randint(5, TITLE_LENGTH)
    title = ""
    for j in range(0, titlelen):
        idx = random.randint(0, count)
        title += words[idx].strip() + ' '

    textlen = random.randint(80, POST_LENGTH)
    text = ""
    for j in range(0, textlen):
        idx = random.randint(0, count)
        text += words[idx].strip() + ' '

    if i % 100 == 0:
        sql_threads += ("; " if i else "") + sql_threads1 + \
        "SELECT datetime('now') as last_activity_at, \n" \
        "\"%s\" as title, \n" \
        "1 as approved, \n " \
        "'test1 test2' as tagnames, \n" \
        "1 as favourite_count, \n" \
        "'en' as language_code, \n" \
        "datetime('now') as added_at, \n" \
        "1 as last_activity_by_id\n" % title.strip()

        sql_posts += ("; " if i else "") + sql_posts1 + \
        "SELECT 0 as wiki, \n" \
        "\"%s\" as text, \n" \
        "%d as thread_id, \n" \
        "\"<p>%s</p>\" as html, \n" \
        "datetime('now') as added_at, \n" \
        "\"%s\" as summary, \n" \
        "1 as approved,\n" \
        "1 as author_id, \n" \
        "'question' as post_type,\n" \
        "0 as vote_up_count,\n" \
        "0 as offensive_flag_count, \n" \
        "0 as score, \n" \
        "0 as comment_count, \n" \
        "0 as vote_down_count, \n" \
        "0 as deleted, \n" \
        "0 as locked, \n" \
        "0 as is_anonymous \n" % (text.strip(), i+1, text.strip(), text[0:400].strip())
    else:
        sql_threads += "UNION SELECT datetime('now'), \"%s\", 1, 'test1 test2', 1, 'en', " \
        "datetime('now'), 1\n" % title.strip()


        sql_posts += "UNION SELECT 0 as wiki, \"%s\" as text, %d as thread_id, " \
        "\"<p>%s</p>\" as html, datetime('now') as added_at, \"%s\" as summary, " \
        "1 as author_id, 1 as approved, 'question' as post_type, 0 as vote_up_count," \
        "0 as vote_down_count, 0 as score, 0 as comment_count, 0 as offensive_flag_count \n, " \
        "0 as deleted, 0 as locked, 0 as is_anonymous\n" % \
        (text.strip(), i+1,
        text.strip(), text[0:400].strip())

print sql_threads + ';'
print sql_posts + ';'

