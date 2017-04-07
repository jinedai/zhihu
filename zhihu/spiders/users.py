# -*- coding: utf-8 -*-
import scrapy
import os
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
        sel_root = response.xpath('//div[@id="Profile-following"]/div/div[@class="List-item"]')
        if len(sel_root):
            for sel in sel_root:
                people_url = sel.xpath('//div[@class="ContentItem-image"]/span/div/div/a/@href').extract()[0]
                self.cursor.execute("""select id from user where url = %s """, ('https://www.zhihu.com' + people_url))
                count = self.cursor.fetchall()
                print count

                if not count:
                    print "aaaaa"
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

    def user_item(self, response):
        sel = response.xpath('//div[@class="ProfileHeader-main"]')

        item = UserItem()
        item['url'] = response.url[:-11]
        item['name'] = ''.join(sel.xpath('//span[@class="ProfileHeader-name"]/text()').extract())
        #item['bio'] = value(sel.xpath('//span[@class="bio"]/@title').extract()).encode('utf-8')
        item['location'] = ''.join(sel.xpath('//div[@class="ProfileHeader-detailValue"]/span/text()').extract())
        #item['business'] = value(sel.xpath('//span[contains(@class, "business")]/@title').extract()).encode('utf-8')
        item['gender'] = 1 if sel.xpath('//div[@class="ProfileHeader-info"]/div[@class="ProfileHeader-infoItem"]/div[@class="ProfileHeader-iconWrapper"]/svg[@class="Icon--male"]') else 0
        item['avatar'] = sel.xpath('//img[@class="Avatar Avatar--large UserAvatar-inner"]/@src').extract()[0]
        #item['education'] = value(sel.xpath('//span[contains(@class, "education")]/@title').extract()).encode('utf-8')
        #item['major'] = value(sel.xpath('//span[contains(@class, "education-extra")]/@title').extract()).encode('utf-8')
        #item['employment'] = value(sel.xpath('//span[contains(@class, "employment")]/@title').extract()).encode('utf-8')
        #item['position'] = value(sel.xpath('//span[contains(@class, "position")]/@title').extract()).encode('utf-8')
        #item['content'] = value(sel.xpath('//span[@class="content"]/text()').extract()).strip().encode('utf-8')
        #item['ask'] = int(sel.xpath('//div[contains(@class, "profile-navbar")]/a[2]/span[@class="num"]/text()').extract()[0])
        #item['answer'] = int(sel.xpath('//div[contains(@class, "profile-navbar")]/a[3]/span[@class="num"]/text()').extract()[0])
        #item['agree'] = int(sel.xpath('//span[@class="zm-profile-header-user-agree"]/strong/text()').extract()[0])
        #item['thanks'] = int(sel.xpath('//span[@class="zm-profile-header-user-thanks"]/strong/text()').extract()[0])

        yield item
