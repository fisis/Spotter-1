#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 09 00:02:20 2012
@author: <Ronny Eichler> ronny.eichler@gmail.com

Track position LEDs and sync signal from camera or video file.

Usage:
    spotter.py --source SRC [--outfile DST] [options]
    spotter.py -h | --help

Options:
    -h --help           Show this screen
    -f --fps FPS        Fps for camera and video
    -s --source SRC     Path to file or device ID [default: 0]
    -S --Serial         Serial port to uC [default: None]
    -o --outfile DST    Path to video out file [default: None]
    -d --dims DIMS      Frame size [default: 320x200]
    -H --Headless       Run without interface
    -D --DEBUG          Verbose output

To do:
    - destination file name may consist of tokens to automatically create,
      i.e., %date%now%iterator3$fixedstring
    - track low res, but store full resolution
    - can never overwrite a file

#Example:
    --source 0 --dims 320x200 --outfile test.avi

"""

import cv2
import time
import multiprocessing
import logging
import copy
from lib.docopt import docopt
from lib.core import grabber, tracker, writer, chatter
import pickle
from PyQt4 import QtCore
import datalog

timings_filename = 'tracking_3LEDs.p'


class Spotter:

    # helper instances
    grabber = None
    writer = None
    tracker = None
    chatter = None
    dlogger=None

    # state variables
    record_to_file = True

    newest_frame = None  # fresh from the frame source; to be processed/written
    scaled_frame = None
    still_frame = None   # frame shown in GUI, may be an older one
    hsv_frame = None     # converted into HSV color space for tracking

    ts_start = None

    paused = False
    recording = False
    GUI_off=False
    FPStest=False
    datalogging=False
    active_shape_type='rectangle' # whichever shape was chosen to draw  on the screen (connects between TabRegions and GLFrame)

    #scale_resize = 0.5
    scale_tracking = 1.0



    def __init__(self, serial=None, *args, **kwargs):
        """

        :param source:
        :param dst:
        :param fps:
        :param size:
        :param serial:
        """
        self.log = logging.getLogger(__name__)
        self.log.info(str(multiprocessing.cpu_count()) + ' CPUs found')

        #try:
        #    import zmq  # ZeroMQ python bindings
        #except ImportError:
        #    zmq = None

        # Setup frame grabber object, fills frame buffer
        self.log.debug('Instantiating grabber...')
        self.grabber = grabber.Grabber(*args, **kwargs)

        # Writer writes frames from buffer to video file in a separate process.
        self.log.debug('Instantiating writer...')
        self.writer_queue = multiprocessing.Queue(16)
        self.writer_pipe, child_pipe = multiprocessing.Pipe()

        self.writer = multiprocessing.Process(target=writer.Writer,
                                              args=(self.grabber.fps, self.grabber.size,
                                                    self.writer_queue, child_pipe,))
        self.log.debug('Starting writer...')
        self.writer.start()
        self.log.debug('Instantiating data logger...')
        self.dlogger=datalog.DataLogger()

        # tracker object finds LEDs in frames
        self.log.debug('Instantiating tracker...')
        self.tracker = tracker.Tracker(adaptive_tracking=True)

        # chatter handles serial communication
        self.log.debug('Instantiating chatter...')
        self.chatter = chatter.Chatter(serial, auto=True)

        # self.timer2 = QtCore.QTimer()
        # self.timer2.timeout.connect(self.update)
        # SPOTTER_REFRESH_INTERVAL = int(1000.0 / self.grabber.capture.get(5))
        # self.timer2.start(SPOTTER_REFRESH_INTERVAL)
        self.stopwatch = QtCore.QElapsedTimer()
        self.stopwatch.start()
        p=self.chatter.pins('digital')
        if p is not None and len(p)>0:
            self.fpstest = self.tracker.trackFPS(p[-1])
        else:
            self.fpstest=None

    def update(self):
        slots = []
        logobjects = []

        #if it outputs the Frame signal on D3
        if self.FPStest == True and self.fpstest!=None:
            slots.append(self.fpstest.slot)

        # Get new frame
        self.newest_frame = self.grabber.grab()
        if self.newest_frame is not None:
            self.spotterelapsed = self.stopwatch.restart()
            self.newest_frame.interval = self.spotterelapsed
            #print self.newest_frame.interval
            # resize frame if necessary
          #  if self.scale_resize < 1.0:

             #   self.newest_frame.img = cv2.resize(self.newest_frame.img, (0, 0), fx=self.scale_resize,
            #                                     fy=self.scale_resize, interpolation=cv2.INTER_LINEAR)

            #with timerclass.Timer(False, self.timings) as t:


            #add an area to ignore
            self.newest_frame=self.tracker.mask_blindspots(self.newest_frame)
            # Find and update position of tracked object
            self.tracker.track_marker(self.newest_frame, method='hsv_thresh',
                                       scale=self.scale_tracking, elapsedtime=self.spotterelapsed)

            messages = []
            # Update positions of all objects
            for o in self.tracker.oois:
                #calculates marker position from LED's to object
                #with the kalman filter: updates the coordinates of the object after smoothing, predicts missing coordinates
                o.update_values(self.spotterelapsed)

                #updates the output values to the Arduino
                o.update_slots(self.chatter)

                slots.extend(o.linked_slots)
                messages.append('\t'.join([self.newest_frame.time_text,
                                           #str(self.newest_frame.tickstamp),
                                           str(o.label),
                                           str(o.position)]))
                #print o.linked_slots
            logobjects.append([self.newest_frame.time_text,[(str(o.label), str(o.getPositionX()),
                               str(o.getPositionY()), str(o.getSpeed()), str(o.getOrientation()),
                               str(o.getPositionY()), str(o.getSpeed()), str(o.getOrientation()),
                               [(str(l.label), str(l.position)) for l in o.getLinkedLEDs()]) for o in self.tracker.oois]])

            for l in self.tracker.leds:
                messages.append('\t'.join([self.newest_frame.time_text,
                                           #str(self.newest_frame.tickstamp),
                                           str(l.label),
                                           str(l.position)]))
            #print logobjects
            # Check Object-Region collisions
            for r in self.tracker.rois:
                r.update_slots(self.chatter)
                r.update_state()
                slots.extend(r.linked_slots)
            self.chatter.update_pins(slots)

            #if logging enabled, it adds a line in the log
            if self.datalogging==True:
                self.dlogger.update(slots, logobjects)

            # Check on writer process to prevent data loss and preserve reference
            if self.check_writer():
                if self.recording:
                    self.writer_pipe.send(['record'])
                    item = (copy.deepcopy(self.newest_frame), copy.deepcopy(messages))
                    self.writer_queue.put(item)
#               time.sleep(0.001)  # required, or may crash?

        # FIXME: Blocks if buffer runs full when writer crashes/closes
        self.writer_pipe.send(['alive'])
        return self.newest_frame

    @property
    def source_type(self):
        return self.newest_frame.source_type if self.newest_frame else None

    def check_writer(self):
        """ True if alive """
        return self.writer.is_alive()

    def start_writer(self, filename=None):
        size = (self.newest_frame.img.shape[1], self.newest_frame.img.shape[0])
        self.writer_pipe.send(['start', size, filename])
        self.recording = True

    def stop_writer(self):
        self.writer_pipe.send(['stop'])
        self.recording = False

    def stop_datalog(self):
        self.datalogging=False

    def start_datalog(self, filename=None):
        self.dlogger.start(filename)
        self.datalogging=True

    def exit(self):
        """ Graceful exit. Ha. Ha. Ha. Bottle of root beer anyone? """
        # closing grabber is straight forward, will release capture object
        if self.grabber is not None:
            self.grabber.close()

        # tracker has no volatile things to handle either
        if self.tracker is not None:
            self.tracker.close()

        # chatter HAS to close serial connection or all hell breaks loose!
        if self.chatter is not None:
            self.chatter.close()

        # writer is a bit trickier, may have frames left to stow away
        if self.writer is not None and self.writer.is_alive():
            self.writer_pipe.send(['terminate'])
            # gives the child process one second to finish up
            self.writer.join(1)
            # will be terminated otherwise
            if self.writer.is_alive():
                self.writer.terminate()
        #try:
        #    fc = self.grabber.frame_count
        #    tt = (time.clock() - self.ts_start)
        #    self.log.info('Done! Grabbed ' + str(fc) + ' frames in ' + str(tt) + 's, with ' + str(fc/tt) + ' fps')
        #except Exception, e:
        #    print e

        #outfile = open(timingfname, "wb")
        #pickle.dump(self.timings, outfile)

        #sys.exit(0)


#############################################################
if __name__ == "__main__":                                  #
#############################################################
    pass
#    # Command line parsing
#    arg_dict = docopt( __doc__, version=None )
#    DEBUG   = arg_dict['--DEBUG']
#    if DEBUG: print( arg_dict )
#
#    # Debug logging
#    log = logging.getLogger('ledtrack')
#    loghdl = logging.StreamHandler()#logging.FileHandler('ledtrack.log')
#    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s') #
#    loghdl.setFormatter(formatter)
#    log.addHandler(loghdl)
#    if DEBUG:
#        log.setLevel( logging.INFO ) #INFOERROR
#    else:
#        log.setLevel( logging.ERROR ) #INFOERROR
#
#    # no GUI, may later select GUI backend, i.e., Qt or cv2.highgui etc.
#    guistring = 'cv2.highgui' if not arg_dict['--Headless'] else arg_dict['--Headless']
#
#    # Frame size parameter string 'WIDTHxHEIGHT' to size tupple (WIDTH, HEIGHT)
#    size = (0, 0) if not arg_dict['--dims'] else tuple( arg_dict['--dims'].split('x') )
#
#    # Instantiating main class ... no shit, Sherlock!
#    main = Spotter( source      = arg_dict['--source'],
#                    destination = utils.dst_file_name( arg_dict['--outfile'] ),
#                    fps         = arg_dict['--fps'],
#                    size        = size,
#                    gui         = guistring,
#                    serial      = arg_dict['--Serial'])
#
#    # It's Math. 3rd grade Math. Wait time between frames, if any left
#    log.debug( 'fps: ' + str(main.grabber.fps) )
#    t = int(1000/main.grabber.fps)
#
#    # Main loop, runs until EOF or <ESCAPE> key pressed
#    log.debug( 'starting main loop' )
#    main.ts_start = time.clock()
#
#    while True:
#
#        # Get new frame
#        if main.grabber.grab_next():
#            main.newest_frame = main.grabber.framebuffer.pop()
#
#            # Check if writer process is still alive
#            # Otherwise might lose data without knowing!
#            # Copy numpy array, otherwise queue references same object
#            # like frame that will be worked on
#            if not main.writer == None and main.check_writer():
#                main.write_queue.put( main.newest_frame.copy() )
#                time.sleep( 0.001 ) # required, or may crash?
#
#            # Find and update position of tracked object
#            main.hsv_frame = cv2.cvtColor( main.newest_frame, cv2.COLOR_BGR2HSV )
#            main.tracker.trackLeds( main.hsv_frame, method = 'hsv_thresh' )
##            main.Object.updatePosition()
#
#            # send position of tracked object to serial port
##            if not main.Object.position is None:
##                main.tracker.chatter.send( main.Object.position )
#
#            # freezes frame being shown, but not frame being processed/written
#            main.gui.update( main.newest_frame )
#
#        else:
#            print 'No new frame returned!!! What does it mean??? We are going to die! Eventually!!!'
#
#        total_elapsed = ( time.clock() - main.grabber.ts_last_frame ) * 1000
#        t = int( 1000/main.grabber.fps - total_elapsed ) - 1
#        if t <= 0:
#            log.info('Missed next frame by: ' + str( t * -1. ) + ' ms')
#            t = 1
##        main.update()
#        main.gui.onKey( cv2.waitKey(t) )
#
##    sys.exit(app.exec_())
