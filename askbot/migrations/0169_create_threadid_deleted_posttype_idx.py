from south.v2 import BaseMigration
from south.db import db
import askbot


class Migration(BaseMigration):

    def forwards(self, orm):
        db_engine_name = askbot.get_database_engine_name()
        if "mysql" in db_engine_name or "sqlite" in db_engine_name:
            db.execute("CREATE INDEX deleted_posttype_threadid ON askbot_post (deleted, post_type, thread_id);")
            print "Created an INDEX deleted_posttype_threadid ..."

    def backwards(self, orm):
        db_engine_name = askbot.get_database_engine_name()
        if "mysql" in db_engine_name:
            db.execute("DROP INDEX deleted_posttype_threadid ON askbot_post")
            print "Dropped INDEX deleted_posttype_threadid ..."
        elif "sqlite" in db_engine_name:
            db.execute("DROP INDEX deleted_posttype_threadid")
            print "Dropped INDEX deleted_posttype_threadid ..."
