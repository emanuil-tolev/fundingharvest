import feedparser
import logging

from fundingharvest.base import BaseHarvester

class RSSHarvester(BaseHarvester):
    def load_rss(self, feed_url):
        try:
            result = feedparser.parse(feed_url)
        except Exception as e:
            logging.error('Error while loading RSS feed, most likely due to the feed being inaccessible, or trying to run this without an internet connection.')
            return None

        if result.bozo:
            error_msg = result.bozo_exception.getMessage()
            error_line = result.bozo_exception.getLineNumber()
            logging.error('Error while loading RSS feed. bozo: {0.bozo}, error: "{error}" on line {line}'.format(result, error=error_msg, line=error_line))
            
            return None
        return result
