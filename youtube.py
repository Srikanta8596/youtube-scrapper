from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
import os
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
from scrapper.youtube_scrapper import scrapper
from database.sql import sqlOperation


youtube = Flask(__name__)


@youtube.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")


@youtube.route("/videos" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            channel_id = request.form['content']
            youtube_url="https://www.youtube.com/"
            youtube_video_url = youtube_url + '@'+ channel_id + "/videos"

            ineuron_scrapper_obj=scrapper(driver_path=r'\chromedriver.exe')
            #ineuron_scrapper_obj=scrapper()
            driver=ineuron_scrapper_obj.run_driver()
            

            videos=ineuron_scrapper_obj.channel_videos(youtube_video_url,driver)
    
            return render_template('result.html', videos=videos[0:(len(videos)-1)])


        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    else:
        return render_template('index.html')


@youtube.route("/video_detail" , methods = ['POST' , 'GET'])

def result():
     if request.method == 'POST':
        try:
            video_url = request.form['url']
            logging.info(f"Video URL: {video_url}")

            # ineuron_scrapper_obj=scrapper(driver_path=r'\chromedriver.exe')
            ineuron_scrapper_obj=scrapper()
            driver=ineuron_scrapper_obj.run_driver()

            video_info=ineuron_scrapper_obj.video_detail(video_url,driver)

            user_and_comments = video_info['User_comment']

            # SQL COMMAND FOR DATA INSERTION IN MYSQL DATABASE
            try:
                #insert in VBD(VIDEO BASIC DETAIL) TABLE
                try:
                    sql_obj=sqlOperation()
                    con=sql_obj.connect_db()
                    sql_obj.insert_vbd(con,video_title=video_info['title'],video_owner=video_info['Owner'],total_comment=video_info['Total comments'],total_likes=video_info['Total likes'],video_description = video_info['Description'])
                    
                    logging.info("Inserted successfully in VBD table")
                except Exception as e:
                    logging.info("Inserted unsuccessfully in VBD table")
                    logging.error(e)
                    
                
                try:
                    video_owner=video_info['Owner']
                    for ele in user_and_comments:
                        sql_obj.insert_lc(con,video_owner=video_owner,user=ele['user'],comment=ele['comment'])
                        logging.info("Inserted successfully in LC table")                     
                    
                except:
                    logging.info("Inserted unsuccessfully in LC table")

            except:
                logging.info("Not able to insert in sql table")
                

            return render_template('video_detail.html', video_info=video_info,user_and_comments=user_and_comments[0:len(user_and_comments)-1])

        except Exception as e:
            logging.info(e)
        
     else:
        return render_template('index.html')



if __name__=="__main__":
    youtube.run(host="0.0.0.0",port=5000)

