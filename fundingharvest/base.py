import logging
import json
from datetime import datetime

from fundingharvest import dao

class BaseHarvester(object):
    
    def check_results(self, record):
        must_be_present = ['title', 'url']
        
        for key in must_be_present:
            if key not in record:
                return False
                
        return True
    
    def save(self, record):
        if not self.check_results(record):
            #string_record = json.dumps(record, indent=4)
            #logging.error("Record does not conform to format. Record data: \n" + string_record)
            return False
        
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
    
    from fundingharvest.rcuk_esrc import EsrcRssHarvester
    esrc = EsrcRssHarvester()
    
    logging.info('Started')
    logging.info('Starting with Research Councils United Kingdom')
    logging.info('Starting with Economic and Social Research Council')
    
    logging.info('Harvesting START')
    now = datetime.now()
    esrc_records = esrc.harvest()
    esrc_time = (datetime.now() - now).total_seconds()
    logging.info('Harvesting END. Took {0} seconds'.format(esrc_time))
    
    logging.info('Indexing results START')
    now = datetime.now()
    esrc.save_multiple(esrc_records)
    esrc_time = (datetime.now() - now).total_seconds()
    logging.info('Indexing results END. Took {0} seconds'.format(esrc_time))
    
if __name__ == "__main__":
    run()