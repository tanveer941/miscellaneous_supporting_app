This repository contains some of the supporting applications based on Bsig and H5 parsers.    

# BSig supporting application
  - Run the file bsig_sig_val_publish.py file to start off the eCAL based application.
  - The subscriber and publisher topic names are defined in the constructor of the class.
  - The messages are transmitted over eCAL through protobuf.
  - The message structure is defined in Radar.proto
  - Compile the proto file using the command protoc -I=.\ --python_out=.\ Radar.proto
  - Bsig_app/publish_signals_bsig.py has the sample code to publish data to produce data from bsig files
  - The path of the bsig file, signal names list, object id count(number of objects) is published over a common topic.
  - The bsig_sig_val_publish.py will publish all the related data for common and object signals over eCAL.
  
 Note: Bsig_app/bsig_optimize/__init__.py has the sample code to read data for multiple signals from a bsig file
  
# H5 supporting application
  - Run the file H5_app/hfl_image_generator/h5_image_publisher.py
  - It is a generic application to publish images to Label tool 5G.
  ## How it works?
  - Run the file H5_app/hfl_image_generator/h5_image_publisher.py file to start off the eCAL based application.
  - Label tool publishes input message under the topic name 'channel_request' defined in topics.json
  - Ask for channel data(True).
  - It will read H5 file, fetches number of devices, channels and timestamps mapped to their channels.
  - Device, channel and respective time stamps is published under the topic name 'channel_response' defined in topics.json
  - Run H5_app/hfl_image_generator/hfl_test_device.py It has the sample code to publish data requesting H5 file to send the values.
  - Once user has channel and timestamp data, one could request image based on these parameters.
  - Publish device, channel and timestamp under the topic name 'hfl_request' defined in topics.json
  - The callback function would send the image as an encoded string under the topic name 'hfl_response' defined in topics.json
  
## .Exe creation by pyinstaller  
Use the command   
  - pyinstaller --onefile bsig_sig_val_publish.py --add-data _ecal_py_2_7_x86.pyd;.   
  - pyinstaller --onefile bsig_sig_val_publish.py --add-data _ecal_py_2_7_x86.pyd;.
  
