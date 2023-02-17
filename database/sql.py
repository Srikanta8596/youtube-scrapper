import mysql.connector
import logging
from database.configuration import *

class sqlOperation:
    def __init__(self):
        self.host=SQL_HOST
        self.user=SQL_USER_NAME
        self.password=SQL_PASSWORD
        self.auth_plugin= SQL_AUTH_PLUGIN
        self.db_name=SQL_DATABASE_NAME
        self.auto_commit=AUTO_COMMIT
        self.table_name_vbd=SQL_TABLE_NAME_VBD
        self.table_name_lc=SQL_TABLE_NAME_LC

    def connect_db(self):
        con=mysql.connector.connect(    
            host=self.host,
            user=self.user,
            password = self.password,
            auth_plugin= self.auth_plugin,
            autocommit=self.auto_commit
            )
        return con
    def creat_db(self,con):
        if (con.is_connected()):
            cur=con.cursor()
            logging.info( "Database is connected")
            #if database not avaialbe create database
            try:
                db_creation_command= f'create database {self.db_name}'
                cur.execute(db_creation_command)
            except Exception as e:
                logging.info(e)
                logging.info("Database exist")
        else:
            logging.info( "Mysql is not connected")


    def create_table(self,con):
        
        if (con.is_connected()):
            cur=con.cursor()
            use_database_command=f'use {self.db_name}'
            cur.execute(use_database_command)
            try:
                create_table_vbd_command= f'create table {self.table_name_vbd} (video_title varchar(1000),total_comments int, total_likes int,  video_description varchar(10000))'
                cur.execute(create_table_vbd_command)
                create_table_lc_command= f'create table {self.table_name_lc} (video_title varchar(1000),user varchar(50), comment varchar(2000))'
                cur.execute(create_table_lc_command)
            except Exception as e:
                logging.info(e)
                logging.info("Table exist")
        else:
            logging.info( "Mysql is not connected")



    def insert_lc(self,con, video_owner, user, comment):
        #print(con.is_connected())
        if (con.is_connected()):
            cur=con.cursor()
            use_database_command=f'use {self.db_name}'
            cur.execute(use_database_command)
            try:
                insert_in_lc_table_command= f'insert into {self.table_name_lc} values ( "{video_owner }", "{user}","{comment}")'
                cur.execute(insert_in_lc_table_command)
            except Exception as e:
                logging.info("Unable insert the element in vbd table: ",e)
        else:
            logging.info( "Mysql is not connected")



    def insert_vbd(self,con, video_title,video_owner, total_comment, total_likes, video_description):
        # print(con.is_connected())
        # print('title',video_title,video_owner, total_comment, total_likes)
        # print(video_description)
        if (con.is_connected()):
            cur=con.cursor()
            use_database_command=f'use {self.db_name}'
            cur.execute(use_database_command)
            insert_in_vbd_table_command= f'insert into {self.table_name_vbd} values ( "{video_title}", "{video_owner}","{total_comment}","{total_likes}","{video_description}")'
            logging.info(f'VBD insert command: {insert_in_vbd_table_command}')
            try:

                cur.execute(insert_in_vbd_table_command)
            except Exception as e:
                logging.info("Unable insert the element in vbd table: ",e)
        else:
            logging.info( "Mysql is not connected")
