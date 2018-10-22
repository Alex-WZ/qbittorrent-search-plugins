# VERSION: 1.00
# AUTHORS: Alex WZ (wenzhen.ly@gmail.com)

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the author nor the names of its contributors may be
#      used to endorse or promote products derived from this software without
#      specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


from urllib.parse import quote
from helpers import retrieve_url
from novaprinter import prettyPrinter
import json


class cilimao(object):
    """ Search engine class """
    name = 'cilimao'
    url = 'https://www.cilimao.me'
    supported_categories = {'all': 'all', 'movies': '1', 'music': '2', 'books': '4'}

    def search(self, what, cat='all'):
        """ Performs search """
        page = 1
        while page < 11:
            query = "".join((self.url, "/api/search?size=10&sortDirections=desc&sortProperties=download_count",
                             "&resourceType=1&resourceSource=0", "&word=", quote(what)))
            if page > 1:
                query = query + "&page=" + str(page)
            response = retrieve_url(query)
            if response == '':
                continue

            resp = json.loads(response)
            if resp['status'] != 'ok':
                return
            if len(resp['data']) == 0:
                return
            if len(resp['data']['result']['content']) == 0:
                return
            for item in resp['data']['result']['content']:
                if item == 'ad':
                    continue
                dict = dict = {"engine_url": self.url}
                dict['name'] = item['title']
                dict["size"] = (str(item['content_size']) + ' B')
                dict["link"] = ("magnet:?xt=urn:btih:" + item['infohash'] + "&dn=" + item['title'])
                dict["leech"] = ''
                dict["seeds"] = ''
                dict['desc_link'] = ('https://www.cilimao.me/information/' + item['infohash'])
                prettyPrinter(dict)
            page += 1
            total_page = resp['data']['result']['total_pages']
            if page > total_page:
                return
        return


if __name__ == '__main__':
    cilimao = cilimao()
    cilimao.search('The Godfather', 'all')
