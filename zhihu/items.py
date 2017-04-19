# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    url            = scrapy.Field()
    thankFromCount = scrapy.Field()
    followerCount = scrapy.Field()
    userType      = scrapy.Field()
    articlesCount = scrapy.Field()
    gender        = scrapy.Field()
    voteupCount   = scrapy.Field()
    isBindSina    = scrapy.Field()
    logsCount     = scrapy.Field()
    participatedLiveCount = scrapy.Field()
    avatarUrl     = scrapy.Field()
    headline      = scrapy.Field()
    followingQuestionCount = scrapy.Field()
    commercialQuestionCount = scrapy.Field()
    markedAnswersText = scrapy.Field()
    pinsCount         = scrapy.Field()
    thankToCount      = scrapy.Field()
    favoritedCount    = scrapy.Field()
    thankedCount      = scrapy.Field()
    showSinaWeibo     = scrapy.Field()
    urlToken          = scrapy.Field()
    favoriteCount     = scrapy.Field()
    voteToCount       = scrapy.Field()
    description       = scrapy.Field()
    school            = scrapy.Field()
    major             = scrapy.Field()
    questionCount     = scrapy.Field()
    answerCount       = scrapy.Field()
    voteFromCount     = scrapy.Field()
    company           = scrapy.Field()
    job               = scrapy.Field()
    mutualFolloweesCount  = scrapy.Field()
    followingFavlistsCount = scrapy.Field()
    markedAnswersCount     = scrapy.Field()
    name                   = scrapy.Field()
    locations              = scrapy.Field()
    followingColumnsCount  = scrapy.Field()
    hostedLiveCount        = scrapy.Field()
    isAdvertiser           = scrapy.Field()
    followingCount         = scrapy.Field()
    followingTopicCount    = scrapy.Field()

    timestamp              = scrapy.Field()
    domain                 = scrapy.Field()
    spider                 = scrapy.Field()
