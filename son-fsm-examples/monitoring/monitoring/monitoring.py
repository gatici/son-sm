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
from sonsmbase.smbase import sonSMbase

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("fsm-monitoring-1")
LOG.setLevel(logging.DEBUG)
logging.getLogger("son-mano-base:messaging").setLevel(logging.INFO)


class MonitoringFSM(sonSMbase):

    def __init__(self):

        """
        :param specific_manager_type: specifies the type of specific manager that could be either fsm or ssm.
        :param service_name: the name of the service that this specific manager belongs to.
        :param function_name: the name of the function that this specific manager belongs to, will be null in SSM case
        :param specific_manager_name: the actual name of specific manager (e.g., scaling, placement)
        :param id_number: the specific manager id number which is used to distinguish between multiple SSM/FSM
        that are created for the same objective (e.g., scaling with algorithm 1 and 2)
        :param version: version
        :param description: description
        """

        self.specific_manager_type = 'fsm'
        self.service_name = 'service1'
        self.function_name = 'function1'
        self.specific_manager_name = 'monitoring'
        self.id_number = '1'
        self.version = 'v0.1'
        self.description = "An FSM that subscribes to monitoring topic"

        super(self.__class__, self).__init__(specific_manager_type= self.specific_manager_type,
                                             service_name= self.service_name,
                                             function_name= self.function_name,
                                             specific_manager_name = self.specific_manager_name,
                                             id_number = self.id_number,
                                             version = self.version,
                                             description = self.description)

    def on_registration_ok(self):

        LOG.debug("Received registration ok event.")
        self.manoconn.subscribe(self.on_alert_received, 'son.monitoring')
        LOG.debug("Subscribed to son.monitoring topic.")

        # send the status to the SMR
        self.manoconn.publish(topic='specific.manager.registry.ssm.status', message=yaml.dump(
                                  {'name':self.specific_manager_id,'status':
                                      'Subscribed to son.monitoring topic, waiting for alert message'}))

    def on_alert_received(self, ch, method, props, response):

        alert = yaml.load(response)

        #filtering incoming alerts
        if alert['alertname'] == 'mon_rule_vm_cpu_usage_85_perc' and alert['exported_job'] == "vnf":
            LOG.info('Alert message received')

            # send the status to the SMR
            self.manoconn.publish(topic='specific.manager.registry.ssm.status',
                                  message=yaml.dump({'name':self.specific_manager_id, 'status':
                                      'cpu usage 85% alert message received'}))
            '''
            Now that the alert message is received, you can react to it by calling a function that performs your intent
            for this FSM.
            '''

def main():
    MonitoringFSM()

if __name__ == '__main__':
    main()
