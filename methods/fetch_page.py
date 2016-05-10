#coding:utf-8

import datetime, time
from urllib3 import PoolManager, Timeout
from util.logger import logger_tool
from util.send_mail import send_mail_util as send_mail

logger = logger_tool('fetch_page')


class Do:
    def __init__(self, url, **kwargs):
        self.url = url
        self.http = PoolManager()
        self.connect_timeout = kwargs['connect_timeout'] if kwargs['connect_timeout'] else 2.0
        self.read_timeout = kwargs['read_timeout'] if kwargs['read_timeout'] else 2.0
        self.available_status = kwargs['available_status'] if kwargs['available_status'] else '200,'
        self.alert_mail = kwargs['alert_mail']

        self._get()

    def _get(self):
        r = None
        try:
            start = time.perf_counter()
            r = self.http.request('GET', self.url, timeout=Timeout(connect=self.connect_timeout, read=self.read_timeout))
            end = time.perf_counter()
        except Exception as ex:
            send_mail(self.alert_mail, 'Request {} failed'.format(self.url), str(ex))

        available_status = self.available_status.split(',')

        if not r:
            return None
        if not hasattr(r, 'status'):
            return None

        if str(r.status) in available_status:
            logger.info(self.url, end-start)
        else:
            send_mail(self.alert_mail, '{} :{}'.format(self.url, r.status), '{}\r\n{}\r\n{}'.format(r.status, r.data, end-start))
