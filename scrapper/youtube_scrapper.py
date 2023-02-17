import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import logging
class scrapper:
    def __init__(self):
        #self.driver_path=driver_path
        pass

    def run_driver(self): 
        try:
            option = webdriver.ChromeOptions()
            #option.binary_location = os.environ.get("GOOGLE_CHROME_BIN")  # For cloud
            option.add_argument('--headless')
            option.add_argument('-no-sandbox')
            option.add_argument("--mute-audio")
            option.add_argument("--disable-extensions")
            option.add_argument('-disable-dev-shm-usage')
            #driver = webdriver.Chrome(service = Service(executable_path = os.environ.get("CHROMEDRIVER_PATH")), options = option)  # For cloud
            #logging.info(f"Driver path: {self.driver_path}" )
            #driver = webdriver.Chrome(self.driver_path, options=option) # For testing in windows
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
            return driver
        except Exception as e:
            logging.info(e)
            logging.info("Run driver is not working")

    def channel_videos(self,channel_url: str,driver):
        try:
            logging.info(f"channel path: {channel_url}")
            driver.get(channel_url)
            # channel_title = driver.find_element(By.XPATH, '//yt-formatted-string[contains(@class, "ytd-channel-name")]').text
            # handle = driver.find_element(By.XPATH, '//yt-formatted-string[@id="channel-handle"]').text
            # subscriber_count = driver.find_element(By.XPATH, '//yt-formatted-string[@id="subscriber-count"]').text
        except:
            logging.info("Incorrect channel path")
        
        #Infinity loop
        try:

            WAIT_IN_SECONDS = 5
            last_height = driver.execute_script("return document.documentElement.scrollHeight")

            while True:
                # Scroll to the bottom of page
                driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
                # Wait for new videos to show up
                time.sleep(WAIT_IN_SECONDS)
                # Calculate new document height and compare it with last height
                new_height = driver.execute_script("return document.documentElement.scrollHeight")
                logging.info(f"last height: {last_height},new height: {new_height}" )
                if new_height == last_height:
                    break
                last_height = new_height
        except:
            logging.info("Infinity loop is not working")

        try:
            thumbnails = driver.find_elements(By.XPATH, '//a[@id="thumbnail"]/yt-image/img')
        except:
            logging.info("Error in thumb_nail")
        
        try:
            views = driver.find_elements(By.XPATH,'//div[@id="metadata-line"]/span[1]')
        except:
            logging.info("Error in views")

        try:
            titles = driver.find_elements(By.ID, "video-title")
        except:
             logging.info("Error in title")

        try:
            links = driver.find_elements(By.ID, "video-title-link")
        except:
             logging.info("Error in links")
        
        try:

            videos = []
            for title, view, thumb, link in zip(titles, views, thumbnails, links):
                video_dict = {
                    'title': title.text,
                    'views': view.text,
                    'thumbnail': thumb.get_attribute('src'),
                    'link': link.get_attribute('href')
                }
                videos.append(video_dict)
            logging.info("Successfully created videos file")
        except:
            logging.info("Unable to create the dictionary file")
        
        return videos

    def video_detail(self,video_url: str,driver):
        try:
            logging.info(f"channel path: {video_url}")
            driver.get(video_url)
            time.sleep(5)
        except:
            logging.info("Incorrect video url")
        try:
            #infinity scroll
            WAIT_IN_SECONDS = 5
            last_height = driver.execute_script("return document.documentElement.scrollHeight")

            while True:
                # Scroll to the bottom of page
                driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
                # Wait for new videos to show up
                time.sleep(WAIT_IN_SECONDS)

                # Calculate new document height and compare it with last height
                new_height = driver.execute_script("return document.documentElement.scrollHeight")
                logging.info(f"last height: {last_height},new height: {new_height}" )
                if new_height == last_height:
                    break
                last_height = new_height
        except:
            logging.info("Infinity loop is not working")

        try:
            page_start=-1*(last_height)
            driver.execute_script("window.scrollTo(0, arguments[0]);",page_start)
            time.sleep(5)
            driver.execute_script('window.scrollBy(0,500);')
            time.sleep(5)
        except:
            logging.info("Unable scroll up")
        try:
            ## title of video
            video_title = driver.find_element(By.NAME, 'title').get_attribute('content')
            logging.info("Successfully got the video title")
        except:
            logging.info("Unable got the video title")
            
        ## owner of video
        try:
            video_owner = driver.find_elements(By.XPATH, '//*[@id="text"]/a')
            owner_name=video_owner[0].text
            logging.info("Successfully got the video owner")
        except:
            logging.info("Unable got the video owner")
        
        # total comments with replies
        try:
            video_comment_with_replies = int(driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text)
            logging.info("Successfully got the total comments")
        except:
            logging.info("Unable got the total comments")
        
        try:
            # total number of likes
            total_likes_ele = driver.find_element(By.XPATH, '//*[@id="segmented-like-button"]')
            total_likes = int(total_likes_ele.text)
            logging.info("Successfully got the total number of likes")
        except:
            logging.info("Unable got the total number of likes")
        try:
            ## Scraping all the comments
            users = driver.find_elements(By.XPATH, '//*[@id="author-text"]/span')
            comments = driver.find_elements(By.XPATH, '//*[@id="content-text"]')
            user_comment=[]
            for user,comment in zip(users,comments):
                video_comment={
                    'user': user.text,
                    'comment':comment.text
                }
                user_comment.append(video_comment)
            logging.info("Successfully srapped username and comment")
        except:
            logging.info("Unable to scrap username and comment")
        
        try:
            #Video description
            show_more=driver.find_element(By.ID,"expand")
            show_more.click()
        except Exception:
            logging.info("View more is not there")
            pass
        try:
            description=driver.find_element(By.ID,"description-inner").text 
            logging.info("Successfully scraped the video description")
        except:
            logging.info("Unable to scrap video description") 
        try:      
            #Detail video in the dictionary format
            video_info={}
            video_info['title'] = video_title
            video_info['Owner'] = owner_name
            video_info['Total comments'] = video_comment_with_replies
            video_info['Total likes'] = total_likes
            video_info['Description'] = description
            video_info['User_comment'] = user_comment
            logging.info("Successfully video detail dictionary created")
        except:
            logging.info("Unable to creare video dictionary")    
        
        return video_info


    
