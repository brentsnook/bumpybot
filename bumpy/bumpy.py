import utils
import os
from waveapi import appengine_robot_runner
from waveapi import robot
from waveapi import events
from waveapi import element
from waveapi import simplejson as json
from feature_wavelet import FeatureWavelet

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
        return FeatureWavelet(wavelet).features()

    def push(self, url, content):
        wavelet = self._fetch_wavelet_from(url)
        FeatureWavelet(wavelet).update_using(content.split('=')[1])
        self._robot.submit(wavelet)

    def run(self, onRobotAddedHandler):
        self._robot.register_handler(events.WaveletSelfAdded, onRobotAddedHandler)
        appengine_robot_runner.run(self._robot)
       
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