import json
import uuid
import UserDict
import httplib
from datetime import datetime

import pyes

from fundingharvest.config import config

def init_db():
    conn, db = get_conn()
    try:
        conn.create_index(db)
    except pyes.exceptions.IndexAlreadyExistsException:
        pass

def get_conn():
    host = "127.0.0.1:9200"
    db_name = "fundfind"
#    host = config["ELASTIC_SEARCH_HOST"]
#    db_name = config["ELASTIC_SEARCH_DB"]
#    print host, db_name
    conn = pyes.ES([host])
    return conn, db_name


class DomainObject(UserDict.IterableUserDict):
    # set __type__ on inheriting class to determine elasticsearch object
    __type__ = None

    def __init__(self, **kwargs):
        '''Initialize a domain object with key/value pairs of attributes.
        '''
        # IterableUserDict expects internal dictionary to be on data attribute
        self.data = dict(kwargs)

    @property
    def id(self):
        '''Get id of this object.'''
        return self.data.get('id', None)

    def save(self):
        '''Save to backend storage.'''
        # TODO: refresh object with result of save
        if 'modified' in self.data:
            self.data['modified'] = datetime.now().isoformat()
        return self.upsert(self.data)

    @classmethod
    def pull(cls, id_):
        '''Retrieve object by id.'''
        conn, db = get_conn()
        
        out = conn.get(db, cls.__type__, id_)
        return cls(**out['_source'])

    @classmethod
    def delete(cls, id_):
        '''Delete object by id.'''
        conn, db = get_conn()
        out = conn.delete(db, cls.__type__, id_)
        return cls(out['_source']['ok'])

    @classmethod
    def upsert(cls, data):
        '''Update backend object with a dictionary of data.
        If no id is supplied an uuid id will be created before saving.'''
        conn, db = get_conn()
        if 'id' in data:
            id_ = data['id']
        else:
            id_ = uuid.uuid4().hex
            data['id'] = id_
            
        if 'created' not in data and 'modified' not in data:
            data['created'] = datetime.now().isoformat()
            data['modified'] = datetime.now().isoformat()
            
        conn.index(data, db, cls.__type__, id_)
        return cls(**data)
        
    @classmethod
    def delete_by_query(cls, query):
        url = "127.0.0.1:9200"
        loc = fundfind + "/" + cls.__type__ + "/_query?q=" + query
        conn = httplib.HTTPConnection(url)
        conn.request('DELETE', loc)
        resp = conn.getresponse()
        return resp.read()
        
    @classmethod
    def query(cls, q='', terms=None, facet_fields=None, flt=False, **kwargs):
        '''Perform a query on backend.

        :param q: maps to query_string parameter.
        :param terms: dictionary of terms to filter on. values should be lists.
        :param facet_fields: we need a proper comment on this TODO
        :param kwargs: any keyword args as per
            http://www.elasticsearch.org/guide/reference/api/search/uri-request.html
        '''
        conn, db = get_conn()
        if not q:
            ourq = pyes.query.MatchAllQuery()
        else:
            if flt:
                ourq = pyes.query.FuzzyLikeThisQuery(like_text=q,**kwargs)
            else:
                ourq = pyes.query.StringQuery(q, default_operator='AND')
        
        if terms:
            for term in terms:
                for val in terms[term]:
                    termq = pyes.query.TermQuery(term, val)
                    ourq = pyes.query.BoolQuery(must=[ourq,termq])
        
        ourq = ourq.search(**kwargs)
        if facet_fields:
            for item in facet_fields:
                ourq.facet.add_term_facet(item['key'], size=item.get('size',100), order=item.get('order',"count"))
        out = conn.search(ourq, db, cls.__type__)
        return out

    @classmethod
    def raw_query(self, query_string):
        if not query_string:
            msg = json.dumps({
                'error': "Query endpoint. Please provide elastic search query parameters - see http://www.elasticsearch.org/guide/reference/api/search/uri-request.html"
                })
            return msg

        host = "127.0.0.1:9200"
        db_path = "fundfind"
        fullpath = '/' + db_path + '/' + self.__type__ + '/_search' + '?' + query_string
        c =  httplib.HTTPConnection(host)
        c.request('GET', fullpath)
        result = c.getresponse()
        # pass through the result raw
        return result.read()

class Funder(DomainObject):
    __type__ = 'funder'
    
class FundingOpp(DomainObject):
    __type__ = 'funding_opportunity'