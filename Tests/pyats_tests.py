#!/bin/env python

#
# import statements
#
import re
import logging
from ats import aetest
from ats.log.utils import banner




#
# create a logger for this testscript
#
logger = logging.getLogger(__name__)

#
# Common Setup Section
#

class common_setup(aetest.CommonSetup):
    '''Common Setup Section

    Defines subsections that performs configuration common to the entire script.

    '''

    @aetest.subsection
    def check_topology(self,
                       testbed,
                       router1_name = 'router1',
                       router2_name = 'router2',
                       switch1_name = 'switch1',
                       switch2_name = 'switch2',
                       asa_name = 'asa'
                       ):
        '''
        check that we have at least two devices and a link between the devices
        If so, mark the next subsection for looping.
        '''

        # abort/fail the testscript if no testbed was provided
        if not testbed or not testbed.devices:
            self.failed('No testbed was provided to script launch',
                        goto = ['exit'])

        # abort/fail the testscript if no matching device was provided
        for device_name in (router1_name, router2_name, switch1_name, switch2_name, asa_name):
            if device_name not in testbed:
                self.failed('testbed needs to contain device {device_name}'.format(
                                        device_name=device_name,
                                    ),
                            goto = ['exit'])

        router1 = testbed.devices[router1_name]
        router2 = testbed.devices[router2_name]
        switch1 = testbed.devices[switch1_name]
        switch2 = testbed.devices[switch2_name]
        asa = testbed.devices[asa_name]

        # add them to testscript parameters
        self.parent.parameters.update(router1=router1, router2=router2, switch1=switch1, switch2=switch2, asa=asa)



    @aetest.subsection
    def establish_connections(self, steps, router1, router2, switch1, switch2, asa):
        '''
        establish connection to all devices
        '''

        with steps.start('Connecting to Router-1'):
            router1.connect()

        with steps.start('Connecting to Router-2'):
            router2.connect()

        with steps.start('Connecting to Switch-1'):
            switch1.connect()

        with steps.start('Connecting to Switch-2'):
            switch2.connect()

        with steps.start('Connecting to asa'):
            asa.connect()

        # abort/fail the testscript if any device isn't connected
        if not router1.connected or not router2.connected or not switch1.connected or not switch2.connected or not asa.connected:
            self.failed('One of the devices could not be connected to',
                        goto = ['exit'])


# MainTestcases
class MainTestcases(aetest.Testcase):
    ''' Route test'''
    @aetest.test.loop(device=('router1','router2'))
    def routecheck(self, device):
        try:
            routes = self.parameters[device].api.get_routes()
            print (routes, len(routes))
            if (len(routes) != 10):
                self.failed('routes are less', goto = ['exit'])
        except Exception as e:
            print (e)
    
    '''Ping test'''
    @aetest.test.loop(device=('router1','router2'), destination=('192.168.4.2','192.168.3.2'))
    def ping(self, device, destination):
        try:
            # store command result for later usage
            result = self.parameters[device].ping(destination)

        except Exception as e:
            # abort/fail the testscript if ping command returns any exception
            # such as connection timeout or command failure
            self.failed('Ping {} from device {} failed with error: {}'.format(
                                destination,
                                device,
                                str(e),
                            ),
                        goto = ['exit'])
        else:
            # extract success rate from ping result with regular expression
            match = re.search(r'Success rate is (?P<rate>\d+) percent', result)
            success_rate = match.group('rate')
            # log the success rate
            logger.info(banner('Ping {} with success rate of {}%'.format(
                                        destination,
                                        success_rate,
                                    )
                               )
                        )


class common_cleanup(aetest.CommonCleanup):
    '''disconnect from devices'''
    @aetest.subsection
    def disconnect(self, steps, router1, router2, switch1, switch2, asa):
        '''disconnect from both devices'''

        with steps.start('Disconnecting from Router-1'):
            router1.disconnect()

        with steps.start('Disconnecting from Router-2'):
            router2.disconnect()

        with steps.start('Disconnecting from Switch-1'):
            switch1.disconnect()

        with steps.start('Disconnecting from Switch-2'):
            switch2.disconnect()

        with steps.start('Disconnecting from asa'):
            asa.disconnect()

        if router1.connected or router2.connected or switch1.connected or switch2.connected or asa.connected:
            # abort/fail the testscript if device connection still exists
            self.failed('One of the two devices could not be disconnected from',
                        goto = ['exit'])


if __name__ == '__main__':

    # local imports
    import argparse
    from ats.topology import loader

    parser = argparse.ArgumentParser(description = "standalone parser")
    parser.add_argument('--testbed', dest = 'testbed',
                        type = loader.load)
    # parse args
    args, unknown = parser.parse_known_args()

    # and pass all arguments to aetest.main() as kwargs
    aetest.main(**vars(args))