use testdb;
delete from activity;
delete from askbot_post_groups;
delete from askbot_postrevision;
delete from askbot_post;
delete from favorite_question;
delete from askbot_thread_groups;
delete from askbot_thread;
alter table activity AUTO_INCREMENT=1;
alter table askbot_post_groups AUTO_INCREMENT=1;
alter table askbot_postrevision AUTO_INCREMENT=1;
alter table askbot_post AUTO_INCREMENT=1;
alter table favorite_question AUTO_INCREMENT=1;
alter table askbot_thread_groups AUTO_INCREMENT=1;
alter table askbot_thread AUTO_INCREMENT=1;
