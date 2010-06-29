import utils
import types
import logging
import re
import os
import urllib
from waveapi import appengine_robot_runner
from waveapi import robot
from waveapi import events
from waveapi import element
from waveapi import simplejson as json

def _read_config():
    config_file = open(os.path.realpath('../config.json'), 'r')
    contents = config_file.read()
    config_file.close()
    return json.loads(contents)

CONFIG = _read_config()

def _setup_authentication(robot, wave_id):
    RPC = {'wavesandbox.com': 'http://www-opensocial-sandbox.googleusercontent.com/api/rpc',
         'googlewave.com': 'http://www-opensocial.googleusercontent.com/api/rpc'}
    robot.setup_oauth(CONFIG['oauth']['key'], CONFIG['oauth']['secret'], 
    server_rpc_base = RPC[utils._discover_server(wave_id)])

class Bumpy:
    
    ROBOT_URL = CONFIG['url']
    FEATURE = re.compile("\W*Feature:(.*)\n")
    STATUS_COLOURS = {
        'passed' : 'rgb(0,128,0)',
        'failed' : 'rgb(255,0,0)',
        'pending' : 'rgb(255,140,0)',
        'undefined' : 'rgb(255,140,0)',
        'skipped' : 'rgb(30,134,255)'
    }
    
    @classmethod
    def pull_url(self, wavelet):
        return self.ROBOT_URL + "/pull/" + utils._mangle_wave_id(wavelet.wave_id) 
    @classmethod
    def push_url(self, wavelet):
        return self.ROBOT_URL + "/push/" + utils._mangle_wave_id(wavelet.wave_id)      
  
    def __init__(self):
        self._initialize_robot()

    def pull(self, url):
        wavelet = self._fetch_wavelet_from(url)
        return self._features_from(wavelet.blips)

    def push(self, url, content):
        wavelet = self._fetch_wavelet_from(url)
        results = content.split('=')[1]
        features = json.loads(urllib.unquote(results))['features']
        
        for blip_id in features:
            blip = wavelet.blips[blip_id]
            feature = features[blip_id]

            if str(blip.version) == str(feature['version']):
                self._update_blip(blip, feature)
            else:
                logging.info('Could not update blip ' + blip.blip_id + ', incoming version (' + feature['version'] + ') not current (' + str(blip.version) + ')')
        
            self._robot.submit(wavelet)

    def run(self, onRobotAddedHandler):
        self._robot.register_handler(events.WaveletSelfAdded, onRobotAddedHandler)
        appengine_robot_runner.run(self._robot)

    def _features_from(self, blips):
        features = {}
        for blip_id in blips:
            blip = blips[blip_id]
            match = self.FEATURE.match(blip.text)
            if match:
                features[blip.blip_id] = {'name' : match.group(1), 'version' : str(blip.version), 'content' : blip.text}
        return json.dumps({'features' : features})

    def _update_blip(self, blip, feature):
        end_of_feature_name = self.FEATURE.search(blip.text).end() - 1
        self._metadata_blip(blip, end_of_feature_name).append('Ran ' + feature['finished'])
        self._highlight_steps(blip, feature)

    def _metadata_blip(self, blip, insertion_point):
        metadata_blip = None
        for child in blip.child_blips:
            if child.inline_blip_offset == insertion_point - 1:
                metadata_blip = child
                metadata_blip.all().delete()
                break
        if metadata_blip == None:
            metadata_blip = blip.insert_inline_blip(insertion_point)
        return metadata_blip
     
    def _highlight_steps(self, blip, feature):
        line_ranges = self._line_ranges(blip)
        for scenario in feature['scenarios']:
            for step in scenario['steps']:
                line_range = line_ranges[step['line'] - 1]
                logging.info("Line is " + str(step['line']))
                logging.info(str(line_range.value()))
                line_range.clear_annotation('style/color')
                line_range.annotate('style/color', self.STATUS_COLOURS[step['status']])
      
    def _line_ranges(self, blip):
        ranges = []
        start = 0
        for line in blip.text.splitlines(True):
            logging.info(str(start) + " to " + str(start + len(line)))
            ranges.append(blip.range(start, start + len(line)))
            start += len(line)
        
        return ranges
       
    def _fetch_wavelet_from(self, url):
        wave_id = utils.extract_wave_id(url)
        wavelet_id = utils.generate_wavelet_id_from_wave_id(wave_id)
        _setup_authentication(self._robot, wave_id)
        return self._robot.fetch_wavelet(wave_id, wavelet_id)

    def _initialize_robot(self):
        _robot = robot.Robot('Bumpy', 
            image_url=self.ROBOT_URL + '/assets/icon.png',
            profile_url=self.ROBOT_URL)
        self._robot = _robot