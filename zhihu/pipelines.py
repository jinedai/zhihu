# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from zhihu.myconfig import DbConfig

class UserPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user = DbConfig['user'], passwd = DbConfig['passwd'], db = DbConfig['db'], host = DbConfig['host'], charset = 'utf8', use_unicode = True)
        self.cursor = self.conn.cursor()
        # self.cursor.execute('truncate table weather;')
        # self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """INSERT IGNORE INTO user (url, thankfromcount, followercount, usertype, articlescount, gender, voteupcount, isbindsina, logscount, participatedlivecount, avatarurl, headline, followingquestioncount, commercialquestioncount, markedanswerstext, pinscount, thanktocount, favoritedcount, thankedcount, showsinaweibo, urltoken, favoritecount, votetocount, description, school, major, questioncount, answercount, votefromcount, company, job, mutualfolloweescount, followingfavlistscount, markedanswerscount, name, locations, followingcolumscount, hostedlivecount, isadvertiser, followingcount, followingtopiccount, createtime)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    item['url'],
                    item['thankFromCount'],
                    item['followerCount'],
                    item['userType'],      
                    item['articlesCount'],
                    item['gender'],        
                    item['voteupCount'],   
                    item['isBindSina'],    
                    item['logsCount'],     
                    item['participatedLiveCount'], 
                    item['avatarUrl'],     
                    item['headline'],      
                    item['followingQuestionCount'], 
                    item['commercialQuestionCount'],
                    item['markedAnswersText'],
                    item['pinsCount'],         
                    item['thankToCount'],      
                    item['favoritedCount'],    
                    item['thankedCount'],      
                    item['showSinaWeibo'],     
                    item['urlToken'],          
                    item['favoriteCount'],     
                    item['voteToCount'],       
                    item['description'],       
                    item['school'],            
                    item['major'],             
                    item['questionCount'],     
                    item['answerCount'],       
                    item['voteFromCount'],     
                    item['company'],           
                    item['job'],               
                    item['mutualFolloweesCount'],  
                    item['followingFavlistsCount'], 
                    item['markedAnswersCount'],     
                    item['name'],                   
                    item['locations'],             
                    item['followingColumnsCount'],  
                    item['hostedLiveCount'],        
                    item['isAdvertiser'],           
                    item['followingCount'],         
                    item['followingTopicCount'],    
                    item['timestamp'],    
                )
            )
            self.conn.commit()
            print 'bbbbbbbbbbbbbbbbb'
        except MySQLdb.Error, e:
            print 'Error %d %s' % (e.args[0], e.args[1])

        return item
