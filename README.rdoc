= Bumpybot v0.0.1

* http://github.com/brentsnook/bumps
* http://groups.google.com/group/bumps-for-cucumber
* http://fuglylogic.com/2009/07/20/bumps-remote-features-for-cucumber/

== Description

A Google Wave robot for the remote management of {Cucumber}[http://cukes.info] features.

Bumpybot allows you to collaborate on your features within a wave while still allowing them to be run. Bumpybot will update your wave with the latest results of each Cucumber run by:

* adding an inline comment to the end of the feature name stating when the feature last ran
* colouring each step to indicate its status

Bumpybot has been designed to work with {Bumps}[http://github.com/brentsnook/bumps].

*Note that this Robot is spike code - it has no test coverage and is not guaranteed to work*. A more stable version is in the works.

Remember:

* *Bumpybot will make your features public* - it will expose your feature content to the outside world, even if your wave is private. Authentication is on the cards for later.

== Using Bumpybot

First create a wave and invite *bumpybot@appspot.com*. Bumpybot will post some instructions on how to configure Cucumber and {Bumps}[http://github.com/brentsnook/bumps].

Add some Cucumber features to your wave, making sure that each one is in a new blip.

Once you have configured Cucumber as instructed, run it as normal. Bumpybot should update your wave with the results of the Cucumber run.

== Deploying Bumpybot

You can also deploy your own version of Bumpybot.

Copy *config.json.example* to *config.json*. You will need to {register your robot}[http://code.google.com/apis/wave/extensions/robots/operations.html#ActiveRobotAPI] and fill out your config accordingly.

Deploy your version of Bumpybot and invite it to a wave.

== License

(The MIT License)

Copyright (c) 2010 Brent Snook http://fuglylogic.com

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.