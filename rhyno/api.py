import json
import requests
from . import utils

class Rhyno(object):
    def __init__(self, host):
        self.host = host

    '''EXCEPTIONS'''
    class ArticleAlreadyExists(Exception):
        def __init__(self, message):
            Exception.__init__(self, "Article is already ingested. %s" % message)

    def ingestible(self, verbose=False):
        '''
        returns list of ingestible DOIs as unicode
        '''
        r = requests.get(self.host + '/ingestible/', verify=False)
        if verbose:
            print(utils.report("GET /ingestible/", r))
        return json.loads(r.content)

    def ingest(self, doi, force_reingest=None, verbose=False):
        '''
        attempts to ingest ingestible article by DOI
        returns article metadata dict if successful
        '''
        payload = {
            'doi': doi
            }
        if force_reingest:
            payload['force_reingest'] = True

        r = requests.post(self.host + '/ingestible', data=payload, verify=False)

        if verbose:
            print(utils.report("POST /ingestible/ %s"% pretty_dict_repr(payload), r))
        return r.content

    def ingest_zip(self, archive_name, force_reingest=False, verbose=False):
        try:
            archive = open(archive_name, 'rb')
        except IOError as e:
            print(e)
            return -1
            
        files = {'archive': archive}

        payload = None
        if force_reingest:
            payload = {'force_reingest': True}
            
        r = requests.post(self.host + '/zip/', files=files, data=payload, verify=False)

        if verbose:
            print(utils.report("POST /zip/ %s"% utils.pretty_dict_repr(files), r))
        
        if r.status_code == 405:
            raise self.ArticleAlreadyExists('')
        return json.loads(r.content)

    def get_article(self, doi, verbose=False):
        r = requests.get(self.host + '/article/' + doi, verify=False)
        if verbose:
            print(utils.report("GET /ingestible/%s" % doi, r))
        
        return json.loads(r.content)

    def get_article_state(self, doi, verbose=False):
        r = requests.get(self.host + '/article/state/' + doi, verify=False)
        if verbose:
            print(utils.report("GET /article/state/%s" % doi, r))

        return json_loads(r.content)
