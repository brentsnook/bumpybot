from waveapi import events
from bumpy import Bumpy

def Main():
    Bumpy().run(OnRobotAdded)

def OnRobotAdded(event, wavelet):
    welcome = """
Thanks for inviting me!
    
Install the bumps gem and drop this into env.rb to get rolling:
  
  require 'bumps'

  Bumps.configure do
    pull_from '%s'
    push_to '%s'
  end  
"""
    wavelet.reply(welcome % (Bumpy.pull_url(wavelet), Bumpy.push_url(wavelet)))