rumps
=====

**R**\ idiculously **U**\ ncomplicated **m**\ acOS **P**\ ython **S**\ tatusbar apps.

.. image:: https://raw.github.com/jaredks/rumps/master/examples/rumps_example.png

.. code-block:: python

    import rumps

    class AwesomeStatusBarApp(rumps.App):
        @rumps.clicked("Preferences")
        def prefs(self, _):
            rumps.alert("jk! no preferences available!")

        @rumps.clicked("Silly button")
        def onoff(self, sender):
            sender.state = not sender.state

        @rumps.clicked("Say hi")
        def sayhi(self, _):
            rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

    if __name__ == "__main__":
        AwesomeStatusBarApp("Awesome App").run()

How fun!?

``rumps`` can greatly shorten the code required to generate a working app. No ``PyObjC`` underscore syntax required!


Use case
--------

``rumps`` is for any console-based program that would benefit from a simple configuration toolbar or launch menu.

Good for:

* Notification-center-based app
* Controlling daemons / launching separate programs
* Updating simple info from web APIs on a timer

Not good for:

* Any app that is first and foremost a GUI application


Required
--------

* PyObjC
* Python 2.6+

Mac OS X 10.6 was shipped with Python 2.6 as the default version and PyObjC has been included in the default Python
since Mac OS X 10.5. If you're using Mac OS X 10.6+ and the default Python that came with it, then ``rumps`` should be
good to go!


Recommended
-----------

* py2app

For creating standalone apps, just make sure to include ``rumps`` in the ``packages`` list. Most simple statusbar-based
apps are just "background" apps (no icon in the dock; inability to tab to the application) so it is likely that you
would want to set ``'LSUIElement'`` to ``True``. A basic ``setup.py`` would look like,

.. code-block:: python

    from setuptools import setup

    APP = ['example_class.py']
    DATA_FILES = []
    OPTIONS = {
        'argv_emulation': True,
        'plist': {
            'LSUIElement': True,
        },
        'packages': ['rumps'],
    }

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )

With this you can then create a standalone,

.. code-block:: bash

    python setup.py py2app


Installation
------------

Using pip,

.. code-block:: bash

    pip install rumps

Or from source,

.. code-block:: bash

    python setup.py install

Both of which will require ``sudo`` if installing in a system-wide location.


Virtual Environments
--------------------

There are issues with using ``virtualenv`` because of the way the Python
executable is copied. Although ``rumps`` attempts to apply a fix (hack) during
the install process, it is not suggested to use ``virtualenv``.

To ensure proper functionality, either use ``venv`` (packaged with Python 3) or
create a standalone app using ``py2app``.

.. code-block:: bash

    python3 -m venv env


Documentation
-------------

Documentation is available at http://rumps.readthedocs.org


License
-------

"Modified BSD License". See LICENSE for details. Copyright Jared Suttles, 2020.

Works Made With rumps
---------------------

`20twenty20 - eohomegrownapps
<https://github.com/eohomegrownapps/20twenty20/>`_

`42-CanITakeCoffee - avallete
<https://github.com/avallete/42-CanITakeCoffee/>`_

`air-quality-app - grtfou
<https://github.com/grtfou/air-quality-app/>`_

`Airplane - C-Codes
<https://github.com/C-Codes/Airplane/>`_

`allbar - raphaelhuefner
<https://github.com/raphaelhuefner/allbar/>`_

`allofthelights - kenkeiter
<https://github.com/kenkeiter/allofthelights/>`_

`attendee-tool-mlh - Bucknalla
<https://github.com/Bucknalla/attendee-tool-mlh/>`_

`Auroratain - Matt-McConway
<https://github.com/Matt-McConway/Auroratain/>`_

`AutoSSP - viktyz
<https://github.com/viktyz/AutoSSP/>`_

`AutoVPN - shadyabhi
<https://github.com/shadyabhi/AutoVPN/>`_

`BackgroundsForReddit - karlaugsten
<https://github.com/karlaugsten/BackgroundsForReddit/>`_

`bink - e40
<https://github.com/e40/bink/>`_

`bitracker - JZChen
<https://github.com/JZChen/bitracker/>`_

`BluetoothEvent - lostman-github
<https://github.com/lostman-github/BluetoothEvent/>`_

`break-timer - jjmojojjmojo
<https://github.com/jjmojojjmojo/break-timer/>`_

`breaker - amloewi
<https://github.com/amloewi/breaker/>`_

`bundle-checker - jeffgodwyll
<https://github.com/jeffgodwyll/bundle-checker/>`_

`c1t1 - e9t
<https://github.com/e9t/c1t1/>`_

`CamAlert - MrBananaPants
<https://github.com/MrBananaPants/CamAlert/>`_

`camsketch - pdubroy
<https://github.com/pdubroy/camsketch/>`_

`casita - david-kuehn
<https://github.com/david-kuehn/casita/>`_

`ChargeMon - RhetTbull
<https://github.com/RhetTbull/ChargeMon/>`_

`ComicStreamer - beville
<https://github.com/beville/ComicStreamer/>`_

`commitwatch - chrisfosterelli
<https://github.com/chrisfosterelli/commitwatch/>`_

`ComMute - cwverhey
<https://github.com/cwverhey/ComMute/>`_

`computer-time - rbrich
<https://github.com/rbrich/computer-time/>`_

`crypto-ticker-macOS - mqulateen
<https://github.com/mqulateen/crypto-ticker-macOS/>`_

`cryptocoin-quotes - Sayan98
<https://github.com/Sayan98/cryptocoin-quotes/>`_

`cuco - jjuanda
<https://github.com/jjuanda/cuco/>`_

`currency-converter - ahmedelgohary
<https://github.com/ahmedelgohary/currency-converter/>`_

`dns.app - damln
<https://github.com/damln/dns.app/>`_

`Dokky - rogierkn
<https://github.com/rogierkn/Dokky/>`_

`dolar_bitcoin - celis
<https://github.com/celis/dolar_bitcoin/>`_

`duplicati - duplicati
<https://github.com/duplicati/duplicati/>`_

`dysonMacOS - fhenwood
<https://github.com/fhenwood/dysonMacOS>`_

`earth - nickrobson
<https://github.com/nickrobson/earth/>`_

`ForceNapClone - hroftgit
<https://github.com/hroftgit/ForceNapClone/>`_

`freelan-bar - privacee
<https://github.com/privacee/freelan-bar/>`_

`g-assistant-mac - agucova
<https://github.com/agucova/g-assistant-mac/>`_

`gapa - ozlerhakan
<https://github.com/ozlerhakan/gapa/>`_

`GitSyncApp - jachin
<https://github.com/jachin/GitSyncApp/>`_

`Gumpy - RobGraham
<https://github.com/RobGraham/Gumpy/>`_

`Habitus - kmundnic
<https://github.com/kmundnic/Habitus/>`_

`HalfCaff - dougn
<https://github.com/dougn/HalfCaff/>`_

`happymac - laffra
<https://github.com/laffra/happymac/>`_

`harmenubar - vekkt0r
<https://github.com/vekkt0r/harmenubar/>`_

`hatarake - kfdm-archive
<https://github.com/kfdm-archive/hatarake/>`_

`HipStatus - jamfit
<https://github.com/jamfit/HipStatus/>`_

`hp-lorem - jamesrampton
<https://github.com/jamesrampton/hp-lorem/>`_

`hs100-status-bar - craig-davis
<https://github.com/craig-davis/hs100-status-bar/>`_

`iBatteryStats - saket13
<https://github.com/saket13/iBatteryStats/>`_

`iBrew - Tristan79
<https://github.com/Tristan79/iBrew/>`_

`idiot - snare
<https://github.com/snare/idiot/>`_

`interlocking - jrauch
<https://github.com/jrauch/interlocking/>`_

`istat - Lingdu0
<https://github.com/Lingdu0/istat/>`_

`keynote_snap - sasn0
<https://github.com/sasn0/keynote_snap/>`_

`Keypad - jelmer04
<https://github.com/jelmer04/Keypad/>`_

`keyringo - tokenizecx
<https://github.com/tokenizecx/keyringo/>`_

`kizkiz - TkTech
<https://github.com/TkTech/kizkiz/>`_

`koinex-status-ticker - kirantambe
<https://github.com/kirantambe/koinex-status-ticker/>`_

`leaguefriend - pandarison
<https://github.com/pandarison/leaguefriend/>`_

`LifxController - mitchmcdee
<https://github.com/mitchmcdee/LifxController/>`_

`lil_ip_toolbar - mchlrtkwski
<https://github.com/mchlrtkwski/lil_ip_toolbar/>`_

`mac-shrew - mejmo
<https://github.com/mejmo/mac-shrew/>`_

`MacFaceID - vkalia602
<https://github.com/vkalia602/MacFaceID/>`_

`majo-v - r4lv
<https://github.com/r4lv/majo-v/>`_

`MBatteryApp - Elliot-Potts
<https://github.com/Elliot-Potts/MBatteryApp/>`_

`McBing - bagabont
<https://github.com/bagabont/McBing/>`_

`Memcode - aroraenterprise
<https://github.com/aroraenterprise/Memcode/>`_

`memdam - joshalbrecht
<https://github.com/joshalbrecht/memdam/>`_

`MenuBarGmail - rcmdnk
<https://github.com/rcmdnk/MenuBarGmail/>`_

`MenuPing - Julien Bordet
<https://github.com/julienbordet/MenuPing/>`_

`midi2dmx - davidbistolas
<https://github.com/davidbistolas/midi2dmx/>`_

`monero-ticker - Cisplatin
<https://github.com/Cisplatin/monero-ticker/>`_

`MoodLight - kretash
<https://github.com/kretash/MoodLight/>`_

`MoonTicker - skxu
<https://github.com/skxu/MoonTicker/>`_

`musicbar - russelg
<https://github.com/russelg/musicbar/>`_

`narcissist - helmholtz
<https://github.com/helmholtz/narcissist/>`_

`Noise-Line - Dnncha
<https://github.com/Dnncha/Noise-Line/>`_

`nowplaying_statusbar - MataiulS
<https://github.com/MataiulS/nowplaying>`_

`obmenka - vlakin
<https://github.com/vlakin/obmenka/>`_

`OnAir - henrik242
<https://github.com/henrik242/OnAir/>`_

`org-clock-dashboard - srid
<https://github.com/srid/org-clock-dashboard/>`_

`osx-bamboo-plan-status - spalter
<https://github.com/spalter/osx-bamboo-plan-status/>`_

`osx-myair - CameronEx
<https://github.com/CameronEx/osx-myair/>`_

`PennAppsX - yousufmsoliman
<https://github.com/yousufmsoliman/PennAppsX/>`_

`phd - ChrisCummins
<https://github.com/ChrisCummins/phd/>`_

`pokemon-go-status - pboardman
<https://github.com/pboardman/pokemon-go-status/>`_

`polly - interrogator
<https://github.com/interrogator/polly/>`_

`pompy - camilopayan
<https://github.com/camilopayan/pompy/>`_

`project_screen_to_lifx - emiraga
<https://github.com/emiraga/project_screen_to_lifx/>`_

`PSPEWC-mac - jacquesCedric
<https://github.com/jacquesCedric/PSPEWC-mac/>`_

`py-Timey - asakasinsky
<https://github.com/asakasinsky/py-Timey/>`_

`pymodoro - volflow
<https://github.com/volflow/pymodoro/>`_

`pySplash - Egregors
<https://github.com/Egregors/pySplash/>`_

`quick-grayscale - shubhamjain
<https://github.com/shubhamjain/quick-grayscale/>`_

`quiet - hiroshi
<https://github.com/hiroshi/quiet/>`_

`Radio-Crowd - EliMendelson
<https://github.com/EliMendelson/Radio-Crowd/>`_

`RadioBar - wass3r
<https://github.com/wass3r/RadioBar/>`_

`RadioBar (fork) - mdbraber
<https://github.com/mdbraber/radiobar/>`_

`rescuetime_statusbar - MauriceZ
<https://github.com/MauriceZ/rescuetime_statusbar/>`_

`rideindegochecker - josepvalls
<https://github.com/josepvalls/rideindegochecker/>`_

`RitsWifi - fang2hou
<https://github.com/fang2hou/RitsWifi/>`_

`safety-bar - pyupio
<https://github.com/pyupio/safety-bar/>`_

`SAT-Vocab-Quizzer - Legoben
<https://github.com/Legoben/SAT-Vocab-Quizzer/>`_

`sb-translate - leandroltavares
<https://github.com/leandroltavares/sb-translate>`_

`sharfoo - furqan-shakoor
<https://github.com/furqan-shakoor/sharfoo/>`_
 
`ShortyURLShortener - Naktrem
<https://github.com/Naktrem/ShortyURLShortener/>`_

`shotput - amussey
<https://github.com/amussey/shotput/>`_

`SingMenuData - ponyfleisch
<https://github.com/ponyfleisch/SingMenuData/>`_

`slack-status-bar - ericwb
<https://github.com/ericwb/slack-status-bar/>`_

`slackify - nikodraca
<https://github.com/nikodraca/slackify/>`_

`Snapgrid - VladUsatii
<https://github.com/VladUsatii/snapgrid/>`_

`snippets - quillford
<https://github.com/quillford/snippets/>`_

`sonostus - sarkkine
<https://github.com/sarkkine/sonostus/>`_

`Spaceapi-Desktop - UrLab
<https://github.com/UrLab/Spaceapi-Desktop/>`_

`SpaceSwitcher - SankaitLaroiya
<https://github.com/SankaitLaroiya/SpaceSwitcher/>`_

`SpotifyLyrics - yask123
<https://github.com/yask123/SpotifyLyrics/>`_

`steemticker-osx - ZachC16
<https://github.com/ZachC16/steemticker-osx/>`_

`Timebar - devonkong
<https://github.com/devonkong/timebar>`_

`Timebox - visini
<https://github.com/visini/timebox/>`_

`Telkom-ADSL-Data-Usage - parautenbach
<https://github.com/parautenbach/Telkom-ADSL-Data-Usage/>`_

`Telton - Yywww
<https://github.com/Yywww/Telton/>`_

`Textinator - RhetTbull
<https://github.com/RhetTbull/textinator/>`_

`these-days - hahayes
<https://github.com/hahayes/these-days/>`_

`time-tracking - willsgrigg
<https://github.com/willsgrigg/time-tracking/>`_

`timerbar - uberalex
<https://github.com/uberalex/timerbar/>`_

`tracker - jtxx000
<https://github.com/jtxx000/tracker/>`_

`TrojanA - chrisxiao
<https://github.com/chrisxiao/TrojanA/>`_

`umma - mankoff
<https://github.com/mankoff/umma/>`_

`upbrew - stchris
<https://github.com/stchris/upbrew/>`_

`uptimeIndicator - paulaborde
<https://github.com/paulaborde/uptimeIndicator/>`_

`urstatus - kysely
<https://github.com/kysely/urstatus/>`_

`uStatus - kdungs
<https://github.com/kdungs/uStatus/>`_

`VagrantBar - kingsdigitallab
<https://github.com/kingsdigitallab/VagrantBar/>`_

`voiceplay - tb0hdan
<https://github.com/tb0hdan/voiceplay/>`_

`volsbb - akigugale
<https://github.com/akigugale/volsbb/>`_

`Volumio_bar - volderette
<https://github.com/volderette/Volumio_bar/>`_

`votingpowerbar - therealwolf42
<https://github.com/therealwolf42/votingpowerbar/>`_

`VPN Handler - tsarenkotxt
<https://github.com/tsarenkotxt/vpn-handler/>`_

`WakeTime App - dleicht
<https://github.com/dleicht/waketime/>`_

`WallpDesk - L3rchal
<https://github.com/L3rchal/WallpDesk/>`_

`webcronic - josselinauguste
<https://github.com/josselinauguste/webcronic/>`_

`Whale - amka
<https://github.com/amka/Whale/>`_

`WhyFi - OzTamir
<https://github.com/OzTamir/WhyFi/>`_

`WordTime - Demonstrandum
<https://github.com/Demonstrandum/WordTime/>`_

`work_time_percent_applet - Benhgift
<https://github.com/Benhgift/work_time_percent_applet/>`_

`WorkWise - 8ern4ard
<https://github.com/8ern4ard/WorkWise/>`_

`xCodea - lowne
<https://github.com/lowne/xCodea/>`_

`yaca - drproteus
<https://github.com/drproteus/yaca/>`_

`Zero - beejhuff
<https://github.com/beejhuff/Zero/>`_

Submit a pull request to add your own!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Contributing
------------

If you've submitted a pull request and need it reviewed, please request a review from `@daredoes
<https://github.com/daredoes/>`_ (contributing in free time, so please be patient)
