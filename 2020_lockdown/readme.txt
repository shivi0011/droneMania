areas covered
----------------
1. Autonomous Drone + AI on jetson/nano 
   gone thru research paper published by NVIDIA on it. 
2. Deep Learning concepts like feed forward and back propagation. 
3. Explored various techniques available for automating the drone -- 4 ways are there -- MAVProxy, DroneSDK, DroneKit, Lua Scripting in Mission Planner.

4. Enable Jetson camera
   https://github.com/NVIDIA-AI-IOT/jetcam
   
5. How to run trailNet
   a. combine the pretrained weights --- https://github.com/NVIDIA-AI-IOT/redtail/tree/master/models/pretrained
   b. to generate stereo, use stereoDNN model --- https://github.com/NVIDIA-AI-IOT/redtail/tree/master/stereoDNN
   c. 
Modified version to work with Mission Planner -- generated DEM on the fly.

6. Change Detection using PCA and K-means as a clustering technique.
