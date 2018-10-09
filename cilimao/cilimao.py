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


import json
from urllib.parse import quote

from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter

class cilimao(object):
    name = 'cilimao'
    url = 'https://www.cilimao.me/api/search?size=10&sortDirections=desc&resourceType=1' \
          '&resourceSource=0&sortProperties=download_count'
    supported_categories = {
                            'all': '0',
                            'movies': '1',
                            'music': '2',
                            'books': '4'
                            }


    def download_torrent(self, info):
        print(download_file(info))

    def search(self, what, cat='all'):
        page = 1
        while page < 11:
            print(page)
            query = "".join((self.url, "&word=", quote(what),
                             "&resourceType=", self.supported_categories[cat]))
            if page > 1:
                query = query + "&page=" + str(page)
            response = retrieve_url(query)
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
                dict["size"] = (str(item['content_size']) + ' KB')
                dict["link"] = ("magnet:?xt=urn:btih:" + item['infohash'])
                dict["leech"] = ''
                dict["seeds"] = ''
                dict[''] = ('https://www.cilimao.me/information/' + item['infohash'])
                prettyPrinter(dict)
            page += 1
            total_page = resp['data']['result']['total_pages']
            if page > total_page:
                return


if __name__ == '__main__':
    cilimao = cilimao()
    cilimao.search('西游记', 'all')
