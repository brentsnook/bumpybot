import types
import logging
import re
import urllib
from waveapi import simplejson as json

class FeatureWavelet:
    
    FEATURE = re.compile("\W*Feature:(.*)\n")
    STATUS_COLOURS = {
        'passed' : 'rgb(0,128,0)',
        'failed' : 'rgb(255,0,0)',
        'pending' : 'rgb(255,140,0)',
        'undefined' : 'rgb(255,140,0)',
        'skipped' : 'rgb(30,134,255)'
    }

    def __init__(self, wavelet):
        self._wavelet = wavelet
    
    def features(self):
        features = {}
        blips = self._wavelet.blips
        for blip_id in blips:
            blip = blips[blip_id]
            match = self.FEATURE.match(blip.text)
            if match:
                features[blip.blip_id] = {'name' : match.group(1), 'version' : str(blip.version), 'content' : blip.text}
        return json.dumps({'features' : features})    
    
    def update_using(self, results):
        features = json.loads(urllib.unquote(results))['features']
      
        for blip_id in features:
            blip = self._wavelet.blips[blip_id]
            feature = features[blip_id]

            if str(blip.version) == str(feature['version']):
                self._update_blip(blip, feature)
            else:
                logging.info('Could not update blip ' + blip.blip_id + ', incoming version (' + feature['version'] + ') not current (' + str(blip.version) + ')')
      
    def _update_blip(self, blip, feature):
        end_of_feature_name = self.FEATURE.search(blip.text).end() - 1
        self._highlight_steps(blip, feature)
        # add metadata after otherwise first highlight is one character short (blip adds a single space)
        self._metadata_blip(blip, end_of_feature_name).append('Ran ' + feature['finished'])

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