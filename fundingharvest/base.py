import logging
from datetime import datetime
import re
from unicodedata import normalize

from fundingharvest import dao

class BaseHarvester(object):
    DEFAULT_COPYRIGHT_LICENSE = {
        'type': 'default-copyright',
        'title': 'Default Copyright',
    }

    def slug_id(self, origin, title):
        """
        Generates a slug-like Elasticsearch id from a string, making
        sure it really is unique within the object's ES document type.

        This also ensures that opportunities don't multiply endlessly
        in the index since the id (currently based on source and title)
        would remain the same unless the title was changed, or the
        opportunity came from a different source.
        """
        return self.slugify(origin) + '.' + self.slugify(title)

    # derived from http://flask.pocoo.org/snippets/5/ (public domain)
    # changed delimiter to _ instead of - due to ES search problem on the -
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    def slugify(self, text, delim=u'_'):
        """Generates a slightly worse ASCII-only slug."""
        result = []

        try:
            text = unicode(text, errors="ignore")
        except TypeError:
            pass  # text is already a unicode object, no need to convert it

        for word in self._punct_re.split(text.lower()):
            word = normalize('NFKD', word).encode('ascii', 'ignore')
            if word:
                result.append(word)
        return unicode(delim.join(result))

    def check_results(self, record):
        must_be_present = ['title', 'url', 'origin']
        
        for key in must_be_present:
            if key not in record:
                return False
                
        return True
    
    def save(self, record):

        if not self.check_results(record):
            #string_record = json.dumps(record, indent=4)
            #logging.error("Record does not conform to format. Record data: \n" + string_record)
            return False

        record['id'] = self.slug_id(record['origin'], record['title'])

        dao.FundingOpp.upsert(record)
        return True
        
    def save_multiple(self, records):
        for record in records:
            self.save(record)
        
    def harvest(self):
        '''Abstract method, must be implemented by subclasses.'''
        raise NotImplementedError()


def run():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    
    from fundingharvest.cardiff_university import CardiffHarvester
    cardiff = CardiffHarvester()
    
    logging.info('Started')
    logging.info('Starting with Universities in the United Kingdom')
    logging.info('Starting with Cardiff University')
    
    logging.info('Harvesting START')
    now = datetime.now()
    cardiff_records = cardiff.harvest()
    cardiff_time = (datetime.now() - now).total_seconds()
    logging.info('Harvesting END. Took {0} seconds'.format(cardiff_time))
    
    if not cardiff_records:
        logging.error('Error while harvesting. Exiting.')
        return 1
    
    logging.info('Indexing results START')
    now = datetime.now()
    cardiff.save_multiple(cardiff_records)
    cardiff_time = (datetime.now() - now).total_seconds()
    logging.info('Indexing results END. Took {0} seconds'.format(cardiff_time))
    
if __name__ == "__main__":
    run()