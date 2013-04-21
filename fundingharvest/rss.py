import feedparser
import logging

from fundingharvest.base import BaseHarvester

class RSSHarvester(BaseHarvester):
    def load_rss(self, feed_url):
        result = feedparser.parse(feed_url)
        if result.bozo:
            error_msg = result.bozo_exception.getMessage()
            error_line = result.bozo_exception.getLineNumber()
            logging.error('Error while loading RSS feed. bozo: {0.bozo}, error: "{error}" on line {line}'.format(result, error=error_msg, line=error_line))
            
            return None
        return result
