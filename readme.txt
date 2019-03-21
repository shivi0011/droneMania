hiii

http://www.svcl.ucsd.edu/projects/dronefollow/ --- good
https://www.sensefly.com/education/datasets/
https://www.instructables.com/id/Ultimate-Intelligent-Fully-Automatic-Drone-Robot-w/  -- bEST
https://www.instructables.com/id/The-Drone-Pi/  
https://sites.google.com/site/npaecopterguide/source-codes/mission-planner-source-code
https://javiermunhoz.com/blog/2017/09/09/open-source-uav-autopilot-with-ardupilot-and-pixhawk.html
https://community.nxp.com/thread/304221
http://www.einarsundgren.se/gstreamer-basic-real-time-streaming-tutorial/  -- best
https://www.youtube.com/watch?v=MCRKfXipAkU   -- video tut good

download this
https://www.crfs.com/blog/droning-on-about-rf/



http://gstreamer-devel.966125.n4.nabble.com/How-to-save-incoming-h264-stream-without-re-encoding-td1559487.html  ----
http://z25.org/static/_rd_/videostreaming_intro_plab/index.html    -- gstreamer tut
https://cgit.freedesktop.org/gstreamer/gst-plugins-good/tree/gst/rtp/README#n251
https://raspberrypi.stackexchange.com/questions/27082/how-to-stream-raspivid-to-linux-and-osx-using-gstreamer-vlc-or-netcat
https://stackoverflow.com/questions/25840509/how-to-save-a-rtsp-video-stream-to-mp4-file-via-gstreamer/25949095#25949095


In case anyone is interested, the code below is a simple way to get the pi to both send the stream and and record the video at the same time:
raspivid -t 999999 -h 720 -w 1080 -fps 25 -hf -b 2000000 -o - | tee YOURFILENAME.h264 | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=YOUR-PI-IP-ADDRESS port=5000 


------------------------------
If your rtspsrc stream is already encoded in H264, just write to mp4 container directly, instead of doing codec process.
Here is my gst-launch-1.0 command for recording rtsp to mp4:

$ gst-launch-1.0 -e rtspsrc location=rtsp://admin:pass@192.168.85.7/rtsph2641080p protocols=tcp ! rtph264depay ! h264parse ! mp4mux ! filesink location=~/camera.mp4
If you want to do something like modifying width, height (using videoscale), colorspace (using videoconvert), framerate (using capsfilter), etc., which should do based on capability of video/x-raw type, you should decode from video/x-h264 to video/x-raw.

And, after modifying, you should encode again before linking to mux element (like mp4mux, mpegtsmux, matroskamux, ...).

It seems like you are not sure when to use video decoder. Here simply share some experience of using video codec:

If source has been encoded, and I want to write to the container with the same encode, then the pipeline will like:

src ! ... ! mux ! filesink

If source has been encoded, and I want to write to the container with different encode, or I want to play with videosink, then the pipeline will like:

src ! decode ! ... ! encode ! mux ! filesink 
src ! decode ! ... ! videosink

If source hasn't been encoded (like videotestsrc), and I want to write to the container, then the pipeline will like:

src ! encode ! mux ! filesink
Note: It costs high cpu resources when doing codec ! So, if you don't need to do codec work, don't do that.

You can check out src, sink, mux, demux, enc, dec, convert, ..., etc. elements using convenient tool gst-inspect-1.0. For example:

$ gst-inspect-1.0 | grep mux
to show all available mux elements.

-------------------------------



COMMAND1:

gst-launch udpsrc port=5000 caps ="application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)MP4V-ES, profile-level-id=(string)6, config=(string)000001b006000001b59113000001000000012000c888800f528045a14103, payload=(int)96, ssrc=(guint)424830278, clock-base=(guint)2874253685, seqnum-base=(guint)43950" ! gstrtpjitterbuffer ! rtpmp4vdepay ! tee name=mpgvideo ! queue ! ffdec_mpeg4 ! ffmpegcolorspace ! videoscale ! autovideosink  mpgvideo. ! queue ! ffdec_mpeg4 ! ffmpegcolorspace  ! avimux ! filesink location=mympg.mp4

 

NOTE: In command 1 we just decode the video and storing to the server PC in this method the size of the video is too large

for eg: size of 1 min video is 2gb

 

COMMAND2:

 

gst-launch udpsrc port=5000 caps ="application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)MP4V-ES, profile-level-id=(string)6, config=(string)000001b006000001b59113000001000000012000c888800f528045a14103, payload=(int)96, ssrc=(guint)424830278, clock-base=(guint)2874253685, seqnum-base=(guint)43950" ! gstrtpjitterbuffer ! rtpmp4vdepay ! tee name=mpgvideo ! queue ! ffdec_mpeg4 ! ffmpegcolorspace ! videoscale ! autovideosink  mpgvideo. ! queue ! ffdec_mpeg4 ! ffmpegcolorspace ! ffenc_mpeg4  ! avimux ! filesink location=my1mpg.mp4

 

NOTE: In this command we encoding the video coming form the camera. In this method the video occupies less storage

for eg: for 1min video it occupies 7mb
---------------------------

TRY THESE
-------------
on the rpi:

raspivid -t 0 -w 1280 -h 720 -hf -ih -fps 20 -o - | nc -k -l 2222

on your computer:

mplayer -fps 200 -demuxer h264es ffmpeg://tcp://10.0.1.3:2222

supports reconnecting

------------------

OOM doesn't depend on size of images
OOM depends on network resolution (width= height= in cfg-file) and on ratio batch/subdivisions in cfg-file. GPU_memory_usage ~ width * height * batch / subdivisions
