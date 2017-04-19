# -*- coding: utf-8 -*-
import scrapy
import os,json,HTMLParser
import time
import MySQLdb
from scrapy.selector import Selector
from zhihu.items import UserItem
from zhihu.myconfig import UsersConfig
from zhihu.myconfig import DbConfig

class UsersSpider(scrapy.Spider):
    name = 'users'
    domain = 'https://www.zhihu.com/#signin'
    login_url = 'https://www.zhihu.com/login/email'
    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Host": "www.zhihu.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
            }

    def __init__(self, url= None):
        self.user_url = url
        self.conn = MySQLdb.connect(user = DbConfig['user'], passwd = DbConfig['passwd'], db = DbConfig['db'], host = DbConfig['host'], charset = 'utf8', use_unicode = True)
        self.cursor = self.conn.cursor()
        self.html_parser = HTMLParser.HTMLParser()
        

    def start_requests(self):
        yield scrapy.Request(
            url = self.domain,
            headers = self.headers,
            meta = {
                'proxy': UsersConfig['proxy'],
                'cookiejar': 1
            },
            callback = self.request_captcha
        )

    def request_captcha(self, response):
        _xsrf = response.css('input[name="_xsrf"]::attr(value)').extract()[0]
        captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + str(time.time() * 1000) + '&type=login'
        yield scrapy.Request(
            url = captcha_url,
            headers = self.headers,
            meta = {
                'proxy': UsersConfig['proxy'],
                'cookiejar': response.meta['cookiejar'],
                '_xsrf': _xsrf
            },
            callback = self.download_captcha
        )

    def download_captcha(self, response):
        with open('captcha.gif', 'wb') as fp:
            fp.write(response.body)
        os.system('start captcha.gif')
        print 'Please enter captcha: '
        captcha = raw_input()

        yield scrapy.FormRequest(
            url = self.login_url,
            headers = self.headers,
            formdata = {
                'email': UsersConfig['email'],
                'password': UsersConfig['password'],
                '_xsrf': response.meta['_xsrf'],
                'captcha': captcha
            },
            meta = {
                'proxy': UsersConfig['proxy'],
                'cookiejar': response.meta['cookiejar']
            },
            callback = self.request_zhihu
        )

    def request_zhihu(self, response):
        yield scrapy.Request(
            url = self.user_url + '/activities',
            headers = self.headers,
            meta = {
                'proxy': UsersConfig['proxy'],
                'cookiejar': response.meta['cookiejar'],
                'from': {
                    'sign': 'else',
                    'data': {}
                }
            },
            callback = self.user_item,
            dont_filter = True
        )

        yield scrapy.Request(
            url = self.user_url + '/followers',
            headers = self.headers,
            meta = {
                'proxy': UsersConfig['proxy'],
                'cookiejar': response.meta['cookiejar'],
                'from': {
                    'sign': 'else',
                    'data': {}
                }
            },
            callback = self.user_start,
            dont_filter = True
        )

    def user_start(self, response):
        sel_root = response.xpath('//div[@class="ContentItem-image"]/span/div/div/a/@href')
        if len(sel_root):
            for sel in sel_root:
                people_url = sel.extract()
                data = 'https://www.zhihu.com' + people_url
                sql = r"select * from `user` where url = '%s'" % (data) 
                print sql

                self.cursor.execute(sql)
                count = self.cursor.fetchone()
                print count

                if count is None:
                    yield scrapy.Request(
                        url = 'https://www.zhihu.com' + people_url + '/activities',
                        headers = self.headers,
                        meta = {
                            'proxy': UsersConfig['proxy'],
                            'cookiejar': response.meta['cookiejar'],
                            'from': {
                                'sign': 'else',
                                'data': {}
                            }
                        },
                        callback = self.user_item,
                        dont_filter = True
                    )

                    yield scrapy.Request(
                        url = 'https://www.zhihu.com' + people_url + '/followers',
                        headers = self.headers,
                        meta = {
                            'proxy': UsersConfig['proxy'],
                            'cookiejar': response.meta['cookiejar'],
                            'from': {
                                'sign': 'else',
                                'data': {}
                            }
                        },
                        callback = self.user_start,
                        dont_filter = True
                    )
                else:
                    continue

    def user_item(self, response):
        print "ccccc"
        sel = response.xpath('//div[@class="ProfileHeader-main"]')

        dataState = ''.join(sel.xpath('//div[@id="data"]/@data-state').extract())
        txt = self.html_parser.unescape(dataState) 
        jsonStr = json.dumps(txt)

        result = json.loads(jsonStr)
        result = json.loads(result)

        item = UserItem()

        item['url'] = response.url[:-11]
        tmp_name = item['url'].split("/")[-1]

        userInfo = result["entities"]["users"][str(tmp_name)]
        item['thankFromCount'] = userInfo['thankFromCount']
        item['followerCount']  = userInfo['followerCount']
        item['userType']       = userInfo['userType']
        item['articlesCount']  = userInfo['articlesCount']
        item['gender']         = userInfo['gender']
        item['voteupCount']    = userInfo['voteupCount']
        item['isBindSina']     = userInfo['isBindSina']
        item['logsCount']      = userInfo['logsCount']
        item['participatedLiveCount'] = userInfo['participatedLiveCount']
        item['avatarUrl']      = userInfo['avatarUrl'].replace('_is', '_xl', 1)
        item['headline']       = userInfo['headline']
        item['followingQuestionCount'] = userInfo['followingQuestionCount']
        item['commercialQuestionCount']= userInfo['commercialQuestionCount']
        item['markedAnswersText']      = userInfo['markedAnswersText']
        item['pinsCount']              = userInfo['pinsCount']
        item['thankToCount']           = userInfo['thankToCount']
        item['favoritedCount']         = userInfo['favoritedCount']
        item['thankedCount']           = userInfo['thankedCount']
        item['showSinaWeibo']          = userInfo['showSinaWeibo']
        item['urlToken']               = userInfo['urlToken']
        item['favoriteCount']          = userInfo['favoriteCount']
        item['voteToCount']            = userInfo['voteToCount']
        item['description']            = userInfo['description']
        if userInfo['educations']:
            school = userInfo['educations'][0].get('school')
            major  = userInfo['educations'][0].get('major')
            if not school is None:
                item['school'] = school.get('name', '')
            else:
                item['school'] = ''
            if not major is None:
                item['major']  = major.get('name', '')
            else:
                item['major']  = ''

        else:
            item['school']     = ''
            item['major']      = ''
        item['questionCount']  = userInfo['questionCount']
        item['answerCount']    = userInfo['answerCount']
        item['voteFromCount']  = userInfo['voteFromCount']
        if userInfo['employments']:
            company = userInfo['employments'][0].get('company')
            job     = userInfo['employments'][0].get('job')
            if not company is None:
                item['company'] = company.get('name', '')
            else:
                item['company'] = ''

            if not job is None:
                item['job']    =job.get('name', '')
            else:
                item['job']    =''
        else:
            item['company']    = ''
            item['job']        = ''

        item['mutualFolloweesCount']    = userInfo['mutualFolloweesCount']
        item['followingFavlistsCount']  = userInfo['followingFavlistsCount']
        item['markedAnswersCount']      = userInfo['markedAnswersCount']
        item['name']           = userInfo['name']
        if userInfo['locations']:
            item['locations']      = userInfo['locations'][0]['name'] if userInfo['locations'][0]['name'] else ''
        else:
            item['locations']      = ''
        item['followingColumnsCount']      = userInfo['followingColumnsCount']
        item['hostedLiveCount']            = userInfo['hostedLiveCount']
        item['isAdvertiser']               = userInfo['isAdvertiser']
        item['followingCount']             = userInfo['followingCount']
        item['followingTopicCount']        = userInfo['followingTopicCount']

        yield item
