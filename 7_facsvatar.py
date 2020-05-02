#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

""" 
**Project Name:**      FACSvatar

**Product Home Page:** https://surafusoft.eu/facsvatar/

**Code Home Page:**    https://github.com/NumesSanguis/FACSvatar

**Authors:**           Stef VAN DER STRUIJK

**Copyright(c):**      GNU Lesser General Public License (LGPL)

Abstract
--------

All code that has the word "FACSvatar" in it or a such a comment close to it.
"""

""" 
**Project Name:**      FACSvatar plugin for FACSHuman facial expression creation tool

**Product Home Page:** 

**Code Home Page:**    

**Authors:**           Michaël GILBERT

**Copyright(c):**      Michaël GILBERT 2017

Abstract
--------

TODO
"""

import gui3d
import mh
import gui
import log
import getpath
import os
import humanmodifier
import modifierslider
import json
import image
from core import G
from progress import Progress
# import 7_FACSHuman2
import time
import zmq
import sys
#image rendering
from OpenGL.GL import *
import glmodule
import image
from image import Image
import image_operations as imgop
import datetime
###############################################
## Test de thread
###############################################
mhapi = gui3d.app.mhapi
QThread = mhapi.ui.QtCore.QThread

###############################################
## Class FACSvatar thread
###############################################

class FacsvatarThread(QThread):
    
    
    def __init__(self, modifiers_sliders, render):
        QThread.__init__(self, None)
        self.exiting = False
        self.sliders          = modifiers_sliders
        self.render           = render
        self.intensity        = 0

#zmq ################################################
        url = "tcp://{}:{}".format("127.0.0.1", "5571")  # 192.168.2.101
        ctx = zmq.Context.instance()
        self.socket = ctx.socket(zmq.SUB)
        self.socket.connect(url)
        self.socket.setsockopt(zmq.SUBSCRIBE, "".encode('ascii'))
#zmq ################################################
        
    def run(self):
        try:
            log.message('FACSvatar START')
            self.startListening()         
            while not self.exiting:
                msg = self.socket.recv_multipart()

                # check not finished; timestamp is empty (b'')
                if msg[1]:
                    # load message from bytes to json
                    facs_data = msg[2].decode('utf-8')

                    # load json formatted data
                    facs_data = json.loads(facs_data)
                    #log.message("FACSDATA_FRAME = %s", facs_data["frame"])

                    if facs_data["au_r"]['AU01'] != 0:
                       self.sliders['1'].onChanging(facs_data["au_r"]['AU01'])
                    if facs_data["au_r"]['AU02'] != 0:
                       self.sliders['2'].onChanging(facs_data["au_r"]['AU02'])
                    if facs_data["au_r"]['AU04'] != 0:
                       self.sliders['4'].onChanging(facs_data["au_r"]['AU04'])
                    if facs_data["au_r"]['AU05'] != 0:
                       self.sliders['5'].onChanging(facs_data["au_r"]['AU05'])
                    if facs_data["au_r"]['AU06'] != 0:
                       self.sliders['6'].onChanging(facs_data["au_r"]['AU06'])
                    if facs_data["au_r"]['AU07'] != 0:
                       self.sliders['7'].onChanging(facs_data["au_r"]['AU07'])
                    if facs_data["au_r"]['AU09'] != 0:
                       self.sliders['9'].onChanging(facs_data["au_r"]['AU09'])
                    if facs_data["au_r"]['AU10'] != 0:
                       self.sliders['10'].onChanging(facs_data["au_r"]['AU10'])
                    if facs_data["au_r"]['AU12'] != 0:
                       self.sliders['12'].onChanging(facs_data["au_r"]['AU12'])
                    if facs_data["au_r"]['AU14'] != 0:
                       self.sliders['14'].onChanging(facs_data["au_r"]['AU14'])
                    if facs_data["au_r"]['AU15'] != 0:
                       self.sliders['15'].onChanging(facs_data["au_r"]['AU15'])
                    if facs_data["au_r"]['AU17'] != 0:
                       self.sliders['17'].onChanging(facs_data["au_r"]['AU17'])
                    if facs_data["au_r"]['AU20'] != 0:
                       self.sliders['20'].onChanging(facs_data["au_r"]['AU20'])
                    if facs_data["au_r"]['AU23'] != 0:
                       self.sliders['23'].onChanging(facs_data["au_r"]['AU23'])
                    if facs_data["au_r"]['AU25'] != 0:
                       self.sliders['25'].onChanging(facs_data["au_r"]['AU25'])
                    if facs_data["au_r"]['AU26'] != 0:
                       self.sliders['26'].onChanging(facs_data["au_r"]['AU26'])
                    if facs_data["au_r"]['AU45'] != 0:
                       self.sliders['43'].onChanging(facs_data["au_r"]['AU45'])
                    if facs_data["au_r"]['AU61'] != 0:
                       self.sliders['61'].onChanging(facs_data["au_r"]['AU61'])
                    if facs_data["au_r"]['AU62'] != 0:
                       self.sliders['62'].onChanging(facs_data["au_r"]['AU62'])
                    if facs_data["au_r"]['AU63'] != 0:
                       self.sliders['63'].onChanging(facs_data["au_r"]['AU63'])
                    if facs_data["au_r"]['AU64'] != 0:
                       self.sliders['64'].onChanging(facs_data["au_r"]['AU64'])
                    #if self.render is True:
                    #self.renderFacsPicture()
                else:
                    pass
                    
                #self.render() 
                self.usleep(60)
                
        #log.message('letype %s et %s', self.intensity_slider, self.msg_box)
        except (RuntimeError, TypeError, NameError) as e:    
            self.stopListening()
            log.message('erreurs %s', e)
            pass           

     
    def text_box_assign(self, thebox):
        self.msg_box = thebox
        log.message('msg_box %s', self.msg_box)
        
    def startListening(self):
        self.exiting = False
        pass
    def stopListening(self):
        if not self.exiting:
            self.exiting = True
            #self.midiin.close_port()
            #del self.midiin
            log.message('FACSmidi STOP')
            

    def msgtxtbox(self, textbox):
        self.msg_txt = textbox
       
    
    def __del__(self):        
        self.stopListening()


            #gui3d.app.statusPersist("Image saved to %s", pic_file)
     
        
##########################################################################
# Main Class for FACSHuman plugin
##########################################################################



class FACSTest(gui3d.TaskView, object):
    
     
    def __init__(self, category, appFacsAnim):
        gui3d.TaskView.__init__(self, category, 'FACSvatar')
        self.facs_human = appFacsAnim.selectedHuman
        self.app = appFacsAnim
        ##########################################################################
        # .json Au's list loading
        ##########################################################################
  
        self.facs_code_names_path = getpath.getDataPath('FACSHuman')
        self.facs_code_names_file = self.facs_code_names_path + '/au.json'
        self.facs_code_names = json.loads(open(self.facs_code_names_file).read())

        box_facsvatar = self.addLeftWidget(gui.GroupBox('FACSvatar listener'))
#Box Midi
        self.facsvatar_start_stop = box_facsvatar.addWidget(gui.CheckBox('Start FACSvatar'))
        self.facsvatar_label = box_facsvatar.addWidget(gui.TextView('Listening STOPPED'))
        #self.facsvatar_render = box_facsvatar.addWidget(gui.CheckBox('Render video'))
        
        self.facs_modifiers = []
        self.facs_modifiers = G.app.selectedHuman.getModifiersByGroup('Upper Face AUs')
        self.facs_modifiers.extend(G.app.selectedHuman.getModifiersByGroup('Lower Face AUs'))
        self.facs_modifiers.extend(G.app.selectedHuman.getModifiersByGroup('Head Positions'))
        self.facs_modifiers.extend(G.app.selectedHuman.getModifiersByGroup('Eye Positions'))
        self.facs_modifiers.extend(G.app.selectedHuman.getModifiersByGroup('Lip Parting and Jaw Opening'))
        self.facs_modifiers.extend(G.app.selectedHuman.getModifiersByGroup('Miscellaneous AUs'))
        self.facs_modifiers.extend(G.app.selectedHuman.getModifiersByGroup('Emotions Blender'))

        self.modifiers_sliders = {}
        
        for mod in self.facs_modifiers:
            self.modifiers_sliders[mod.name] = modifierslider.ModifierSlider(modifier=mod, label=mod.name)
            #self.aus_list_items.addItem(self.facs_code_names[str(mod.name)], 'black', mod.name,  False)

            
# Midi Thread creation
        self.facsvatar_listener = FacsvatarThread(self.modifiers_sliders, self.renderFacsPicture)

        @self.facsvatar_start_stop.mhEvent
        def onClicked(event):
            if self.facsvatar_start_stop.selected:
                self.facsvatar_label.setText('START')
                #self.facsvatar_listener.slider_assign(self.animation_test)
                #self.facsvatar_listener.text_box_assign(self.midi_msg_received)
                self.facsvatar_listener.start()
            else:
                self.facsvatar_label.setText('STOP')
                self.facsvatar_listener.stopListening()

     #   def onClicked(event):
     #   @self.facsvatar_render.mhEvent
     #       self.renderFacsPicture()
        
    def renderFacsPicture(self, dir_images = None, pic_file = None, pic_file_reverse = None):
        #self.facs_human.applyAllTargets()
        #self.refreshAuSmoothSetting()
        self.renderingWidth = '500'
        self.renderingHeight = '500'
        
        self.grabPath = mh.getPath('grab')
        #log.message('self.grabPath = %s', self.grabPath)
        grabName = datetime.datetime.now().strftime('grab_%Y-%m-%d_%H.%M.%S.png')
        pic_file = os.path.join(self.grabPath, 'test', grabName)
        
        img_width, img_height  = int(self.renderingWidth), int(self.renderingHeight)
        glmodule.draw(False)
        img = glmodule.renderToBuffer(img_width, img_height)
        #log.message('img type = %s'. type(img))
        alphaImg = glmodule.renderAlphaMask(int(img_width), int(img_height))
        img = imgop.addAlpha(img, imgop.getChannel(alphaImg, 0))
        img = img.toQImage()
        img.save(pic_file)
        log.message("Image saved to %s", pic_file)
        del alphaImg
        del img

##########################################################################
# System calls
##########################################################################
        
    def onShow(self, event):
        gui3d.TaskView.onShow(self, event)
        
        #gui3d.app.setTargetCamera(131, 9)
        #gui3d.app.axisView([0.0, 0.0, 0.0])
        gui3d.app.statusPersist('FACSHuman a tool to create facial expression based on the Paul Ekman Facial Action Coding System')
        gui3d.app.backplaneGrid.setVisibility(False)
        gui3d.app.backgroundGradient.mesh.setColors([0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0])
        #G.app.setScene(scene.Scene(G.app.scene.file.path))
        # self.resetCamera()
        #facs_human.material.shader = getpath.getSysDataPath(self.taskViewShader) if self.taskViewShader else None array([  0.        ,   7.22596645,  18.91166067])

        
    def onHide(self, event):
        gui3d.app.statusPersist('')

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Modelling')
    taskview = category.addTask(FACSTest(category, app))

def unload(app):
    pass

    
