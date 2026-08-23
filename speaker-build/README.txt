The "snapclient" file contains the OPTS environment variable. It goes in /etc/default/snapclient. Note that it is defined with "plug:" which is a software layer to convert ALSA sample rates and formats. It uses a few extra CPU cycles but ensures correct conversion of your snapclient audio to the input type required by your USB audio endpoint. In my case, that's 44100:24bit to 44100:16bit.

The snapclient.svc is the service descriptor. Installing snapclient with apt places it by default in /lib/systemd/system/snapclient.service, at least on my Pi Zero. You can edit this file with sudo. I recommend putting a symlink to it in your home folder so you don't need to remember the filepath.

asound.conf is found in /etc/asound.conf. This is read by the ALSA audio backend in Linux and it sets up a software audio endpoint that does the stereo to mono conversion. If you are using two-channel audio, you don't need it, but it's required if you want to hear both channels mixed to a single speaker.



If you can find a Pi for a decent price, good luck in the setup! Gemini/ChatGPT are your friends in DIY home audio. May the force be with you.