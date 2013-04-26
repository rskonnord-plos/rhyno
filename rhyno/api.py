import json
import requests
from . import utils

API_HOST = 'https://webprod.plosjournals.org/api'

class Rhyno(object):
    def __init__(self, host=API_HOST, verify_ssl=False):
        self.host = host
        self.verify_ssl=verify_ssl

    '''EXCEPTIONS'''
    class Base405Error(Exception):
        def __init__(self, message):
            Exception.__init__(self, "Server responded with a 405: %s" % message)

    class Base404Error(Exception):
        def __init__(self, message):
            Exception.__init__(self, "Server responded with a 404: %s" % message)
            
    class Base500Error(Exception):
        def __init__(self, message):
            Exception.__init__(self, "Server responded with a 500: %s" % message)        

    @staticmethod
    def handle_error_codes(r):
        if r.status_code == 405:
            raise Rhyno.Base405Error(r.content)
        if r.status_code == 404:
            raise Rhyno.Base404Error(r.content)
        if r.status_code == 500:
            raise Rhyno.Base500Error(r.content)

    def ingestibles(self, verbose=False):
        '''
        returns list of ingestible filenames as unicode
        '''
        r = requests.get(self.host + '/ingestibles/', verify=self.verify_ssl)
        if verbose:
            print(utils.report("GET /ingestibles/", r))
        return json.loads(r.content)

    def ingest(self, filename, force_reingest=None, verbose=False):
        '''
        attempts to ingest ingestible article by package filename
        returns article metadata dict if successful
        '''
        payload = {
            'name': filename
            }
        if force_reingest:
            payload['force_reingest'] = True
        r = requests.post(self.host + '/ingestibles', data=payload, verify=self.verify_ssl)
        if verbose:
            print(utils.report("POST /ingestibles/ %s"% pretty_dict_repr(payload), r))

        self.handle_error_codes(r)
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
        r = requests.post(self.host + '/zip/', files=files, data=payload, verify=self.verify_ssl)
        if verbose:
            print(utils.report("POST /zip/ %s"% utils.pretty_dict_repr(files), r))
        self.handle_error_codes(r)
        return json.loads(r.content)

    def get_metadata(self, doi, verbose=False):
        r = requests.get(self.host + '/articles/' + doi, verify=self.verify_ssl)
        if verbose:
            print(utils.report("GET /articles/%s" % doi, r))
        self.handle_error_codes(r)        
        return json.loads(r.content)

    def _get_state(self, doi, verbose=False):
        r = requests.get(self.host + '/articles/%s' % doi, verify=self.verify_ssl)
        if verbose:
            print(utils.report("GET /articles/%s" % doi, r))
        self.handle_error_codes(r)
        return json.loads(r.content)
    
    def is_published(self, doi, verbose=False):
        return self._get_state(doi, verbose)['published']

    def _get_syndication_state(self, doi, target, verbose=False):
        return self._get_state(doi, verbose)['syndications'][target]['status']

    def get_crossref_syndication_state(self, doi, verbose=False):
        return self._get_syndication_state(doi, 'CROSSREF', verbose=verbose)

    def get_pmc_syndication_state(self, doi, verbose=False):
        return self._get_syndication_state(doi, 'PMC', verbose=verbose)

    def _base_publish(self, doi, publish, verbose=False):
        # has no effect on syndication because 'syndications' key is omitted
        payload = {
            'state': 'published'
            }
        r = requests.patch(self.host + '/articles/%s' % doi, data=json.dumps(payload), verify=self.verify_ssl)
        if verbose:
            print(utils.report("POST /articles/%s" % doi, r))
        self.handle_error_codes(r) 
        return json.loads(r.content)

    def publish(self, doi, verbose=False):
        self._base_publish(doi, publish=True, verbose=verbose)

    def unpublish(self, doi, verbose=False):
        self._base_publish(doi, publish=False, verbose=verbose)

    def _syndicate(self, doi, targets, verbose=False):
        payload = {
            'syndications': dict(
                (target, {'status': 'IN_PROGRESS'})
                for target in targets)
            }
        r = requests.patch(self.host + '/articles/%s' % doi, data=json.dumps(payload), verify=self.verify_ssl)
        if verbose:
            print(utils.report("PATCH /articles/%s" % doi, r))
        self.handle_error_codes(r) 
        return json.loads(r.content)

    def syndicate_pmc(self, doi, verbose=False):
        return self._syndicate(doi, ['PMC'], verbose=verbose)

    def syndicate_crossref(self, doi, verbose=False):
        return self._syndicate(doi, ['CROSSREF'], verbose=verbose)
