from copy import deepcopy

from fundingharvest.rss import RSSHarvester

ESRC_FEED_URL = 'http://feeds.feedburner.com/ESRCCurrentFundingOpportunities?format=xml'
DEFAULT_COPYRIGHT_LICENSE = {
    'type': 'default-copyright',
    'title': 'Default Copyright',
}

class EsrcRssHarvester(RSSHarvester):
    feed_url = None
    
    def __init__(self, feed_url=ESRC_FEED_URL):
    # initialise with default URL from this module
    # unless a different URL is passed in
        self.feed_url = feed_url
        
    def harvest(self):
        records = []
        
        feed = self.load_rss(self.feed_url)
        if not feed:
            return None
            
        for entry in feed['entries']:
            record = {}
            record['title'] = entry['title']
            record['url'] = entry['feedburner_origlink']
            record['license'] = DEFAULT_COPYRIGHT_LICENSE
            record['origin'] = 'harvested'
            records.append(deepcopy(record))
        
        return records
