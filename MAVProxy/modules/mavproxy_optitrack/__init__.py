#!/usr/bin/env python
'''
Example Module
Peter Barker, September 2016

This module simply serves as a starting point for your own MAVProxy module.

1. copy this module sidewise (e.g. "cp mavproxy_example.py mavproxy_coolfeature.py"
2. replace all instances of "example" with whatever your module should be called
(e.g. "coolfeature")

3. trim (or comment) out any functionality you do not need
'''

import time
from pymavlink import mavutil
from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.lib import mp_util
from MAVProxy.modules.lib import mp_settings
from MAVProxy.modules.mavproxy_optitrack import NatNetClient

class optitrack(mp_module.MPModule):
    def __init__(self, mpstate):
        """Initialise module"""
        super(optitrack, self).__init__(mpstate, "optitrack", "optitrack", public=True)
        self.add_command('optitrack', self.cmd_optitrack, "optitrack control", ['<start>'])
        self.streaming_client = NatNetClient.NatNetClient()
        # Configure the streaming client to call our rigid body handler on the emulator to send data out.
        self.streaming_client.new_frame_listener = self.receive_new_frame
        self.streaming_client.rigid_body_listener = self.receive_rigid_body_frame

    # This is a callback function that gets connected to the NatNet client and called once per mocap frame.
    def receive_new_frame(self, data_dict):
        #print("receive_new_frame")
        pass

    # This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
    def receive_rigid_body_frame(self, new_id, position, rotation, tracking_valid):
        #print("receive_rigid_body_frame")
        if (tracking_valid):
            now = time.time()
            time_us = int(now * 1.0e6)
            self.master.mav.att_pos_mocap_send(time_us, (rotation[3], rotation[0], rotation[2], -rotation[1]), position[0], position[2], -position[1])

    def usage(self):
        '''show help on command line options'''
        return "Usage: example <status|set>"

    def cmd_start(self):
        print("optitrack start")
        self.streaming_client.setup_sdk()

    def cmd_optitrack(self, args):
        '''control behaviour of the module'''
        if len(args) == 0:
            print(self.usage())
        elif args[0] == "start":
            self.cmd_start()
        else:
            print(self.usage())

    def idle_task(self):
        '''called rapidly by mavproxy'''
        self.streaming_client.process_data_and_cmd()

    def mavlink_packet(self, m):
        '''handle mavlink packets'''
        pass

def init(mpstate):
    '''initialise module'''
    return optitrack(mpstate)
