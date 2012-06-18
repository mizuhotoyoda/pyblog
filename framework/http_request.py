#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import cgi
import os

from framework import base


class CHttpRequest(base.CBase):
    """CHttpRequest manages informations of a request to be sent from a user.
    """

    def __init__(self, app, start_response):
        base.CBase.__init__(self)
        self.app = app
        self.start_response = start_response
        self.status_code = 200
        self.headers = {'Content-type': 'text/html; charset=utf-8'}
        self.params = {}

        self.base_url = self.app.env['DOCUMENT_ROOT']
        if self.base_url[-1] != os.sep:  # 末尾にセパレーターを付ける.
            self.base_url += os.sep

    def is_get(self):
        """GET要求かどうか.

        GETの場合Trueを、それ以外はFalseを返却する.
        """
        if self.method.upper() == 'GET':  # GET
            return True
        else:
            return False

    def is_post(self):
        """POST要求かどうか.

        POSTの場合Trueを、それ以外はFalseを返却する.
        """
        if self.method.upper() == 'POST':  # POST
            return True
        else:
            return False

    def param(self, query):
        """QUERYパラメータを取得する.

        パラメータが存在しない場合は空文字返す.
        """
        if not query in self.params:
            return ""  # 要求されたqueryを保持していない.

        if self.is_get():  # GET
            return self.params[query][0]
        elif self.is_post():  # POST
            return self.params[query]
        else:
            raise Exception('unknown request method({0})'.format(self.method))

    def init_request(self):
        env = self.app.env

        # 現在このフレームワークではGETとPOSTだけ受け付けます.
        request_method_key = 'REQUEST_METHOD'
        if request_method_key in env:
            if env[request_method_key].upper() != "GET" and env[request_method_key].upper() != "POST":
                print 'この要求を処理できません'
                self.app.exit()  # GETとPOST以外はエラー終了.
        else:
            print 'この要求を処理できません'
            self.app.exit()  # Request methodが存在しない場合はエラー終了.

        self.method = env[request_method_key]

        self.analyze_parameter(env)

    def analyze_parameter(self, env):
        """GETおよびPOSTのパラメータを解析します。
        """
        if self.is_get():  # GET
            query_string_key = 'QUERY_STRING'
            if query_string_key in env:
                self.params = cgi.parse_qs(env[query_string_key])
        elif self.is_post():  # POST
            query_string_key = 'wsgi.input'
            if query_string_key in env:
                # content lengthが0の場合、引数なしでread()する.
                content_length = int(env.get('CONTENT_LENGTH', 0))
                if not content_length:
                    parsed_data = cgi.parse_qsl(env[query_string_key].read())
                else:
                    parsed_data = cgi.parse_qsl(env[query_string_key].read(content_length))

                self.params = dict(parsed_data)  # tupleデータをdict型に変換.
        else:
            raise Exception('unknown request method({0})'.format(self.method))

    def redirect(self, url):
        self.status_code = 301
        self.headers['Location'] = url
        self.output_response_header()

    def output_response_header(self):
        if not self.status_code:  # ステータスコードが設定されていない.
            return 0

        # statusコードの作成.
        status = '{0} {1}'.format(self.status_code, self.get_response_code(self.status_code))

        # レスポンスヘッダの生成.
        response = []
        for key, value in self.headers.items():
            tuple_value = key, value
            response.append(tuple_value)
        if self.start_response:
            self.start_response(status, response)
        else:  # start_responseが偽の場合、直接pinrtさせる.
            print 'Content-type: text/html; charset=utf-8'
            print ''

        self.status_code = 0

    @staticmethod
    def get_response_code(status_code):
        """status_codeで指定されたコードに対応する文字列を取得する.

        HTTP1.1のレスポンスコードは以下のRFC文書で定義されている。
        http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
        http://www.studyinghttp.net/rfc_ja/rfc2616#Sec10
        """

        status_code_table = {
                '200': 'OK',
                '201': 'Created',
                '202': 'Accepted',
                '203': 'Non-Authoritative Information',
                '204': 'No Content',
                '205': 'Reset Content',
                '206': 'Partial Content',
                '300': 'Multiple Choices',
                '301': 'Moved Permanently',
                '302': 'Found',
                '303': 'See Other',
                '304': 'Not Modified',
                '305': 'Use Proxy',
                '307': 'Temporary Redirect',
                '400': 'Bad Request',
                '401': 'Unauthorized',
                '403': 'Forbidden',
                '404': 'Not Found',
                '405': 'Method Not Allowed',
                '406': 'Not Acceptable',
                '407': 'Proxy Authentication Required',
                '408': 'Request Timeout',
                '409': 'Conflict',
                '410': 'Gone',
                '411': 'Length Required',
                '412': 'Precondition Failed',
                '413': 'Request Entity Too Large',
                '414': 'Request-URI Too Long',
                '415': 'Unsupported Media Type',
                '416': 'Requested Range Not Satisfiable',
                '417': 'Expectation Failed',
                '500': 'Internal Server Error',
                '501': 'Not Implemented',
                '502': 'Bad Gateway',
                '503': 'Service Unavailable',
                '504': 'Gateway Timeout',
                '505': 'HTTP Version Not Supported'}

        # int型の場合、str型に変換する.
        if isinstance(status_code, int):
            status_code = str(status_code)

        # 変換テーブルを使ってステータスコードを変換する.
        if isinstance(status_code, str):
            if status_code in status_code_table:
                return status_code_table[status_code]
            else:
                return None  # 変換テーブルにない.
        else:
            return None  # str型ではない場合.
