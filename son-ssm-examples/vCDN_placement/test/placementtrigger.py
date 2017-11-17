"""
Copyright (c) 2015 SONATA-NFV
ALL RIGHTS RESERVED.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written
permission.
This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through
the Horizon 2020 and 5G-PPP programmes. The authors would like to
acknowledge the contributions of their colleagues of the SONATA
partner consortium (www.sonata-nfv.eu).
"""

import logging
import yaml
import time
from sonmanobase import messaging

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("placement-trigger")
LOG.setLevel(logging.DEBUG)
logging.getLogger("son-mano-base:messaging").setLevel(logging.INFO)


class fakealert(object):
    def __init__(self):

        self.name = 'placement-trigger'
        self.version = '0.1'
        self.description = 'description'

        LOG.info("Starting triggering placement SSM:...")

        # create and initialize broker connection
        self.manoconn = messaging.ManoBrokerRequestResponseConnection(self.name)

        self.path_descriptors = 'test/test_descriptors/'
        self.end = False

        self.publish_nsd()

        self.run()

    def run(self):

        # go into infinity loop

        while self.end == False:
            time.sleep(1)

    def publish_nsd(self):

        LOG.info("Sending placement request")

        vnfd1 = yaml.load(open('vCC-vnfd.yml', 'r'))
        vnfd2 = yaml.load(open('vtc-nfd.yml', 'r'))
        vnfd3 = yaml.load(open('vtu-nfd.yml', 'r'))

        topology = [{"vim_uuid": "1234","vim_city": "Athens","vim_name": "abcd", "vim_endpoint": "12", "memory_total":
                    32, "memory_used": 12,"core_total": 43, "core_used": 23}, {"vim_uuid": "1235","vim_city": "Aveiro","vim_name": "abcd", "vim_endpoint": "12", "memory_total":
                    50, "memory_used": 10,"core_total": 65, "core_used": 30}]

        nap = {'ingress':[{"location":'Athens',"nap":''}],'egress':[{"location":'Aveiro',"nap":''}]}

        vnfds = [vnfd1,vnfd2,vnfd3]

        nsd = {}

        uuid = "1234"

        message = {"nsd":nsd, "topology": topology, "uuid": uuid, "vnfds":vnfds, "nap":nap}



        self.manoconn.call_async(self.on_publish_response,
                                 'placement.ssm.'+uuid,
                                 yaml.dump(message))

    def on_publish_response(self, ch, method, props, response):

        response = yaml.load(str(response))
        if type(response) == dict:
            print(response)

def main():
    fakealert()


if __name__ == '__main__':
    main()