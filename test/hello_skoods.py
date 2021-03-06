import airsim

import time
import os
import numpy as np
import cv2

# connect to the AirSim simulator 
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()

for idx in range(3):
    # get state of the car
    car_state = client.getCarState()
    print("Speed %d, Gear %d" % (car_state.speed, car_state.gear))

    # go forward for 3 seconds
    car_controls.throttle = 0.5
    car_controls.steering = 0
    client.setCarControls(car_controls)
    print("Go Forward")
    time.sleep(3)   # let car drive a bit

    # Go forward + steer right for 0.5 seconds
    car_controls.throttle = 0.5
    car_controls.steering = 1
    client.setCarControls(car_controls)
    print("Go Forward, steer right")
    time.sleep(0.5)   # let car drive a bit

    # Go forward + steer left for 0.5 seconds
    car_controls.throttle = 0.5
    car_controls.steering = -1
    client.setCarControls(car_controls)
    print("Go Forward, steer left")
    time.sleep(0.5)   # let car drive a bit

    # apply breaks for 5 seconds
    car_controls.brake = 1
    client.setCarControls(car_controls)
    print("Apply break")
    time.sleep(5)   # let car drive a bit
    car_controls.brake = 0 #remove break

    # go reverse for 3 seconds
    car_controls.throttle = -0.5
    car_controls.is_manual_gear = True;
    car_controls.manual_gear = -1
    car_controls.steering = 0
    client.setCarControls(car_controls)
    print("Go reverse")
    time.sleep(3)   # let car drive a bit
    car_controls.is_manual_gear = False; # change back gear to auto
    car_controls.manual_gear = 0  
    
    # get camera images from the car
    responses = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.DepthVis),  #depth visualization image
        airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, True), #depth in perspective projection
        airsim.ImageRequest("1", airsim.ImageType.Scene), #scene vision image in png format
        airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)])  #scene vision image in uncompressed RGBA array
    print('Retrieved images: %d', len(responses))

    for response in responses:
        filename = 'c:/temp/skoods' + str(idx)
        if not os.path.exists('c:/temp/'):
            os.makedirs('c:/temp/')
        if response.pixels_as_float:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
            airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response))
        elif response.compress: #png format
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
        else: #uncompressed array
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) #get numpy array
            img_rgba = img1d.reshape(response.height, response.width, 4) #reshape array to 4 channel image array H X W X 4
            img_rgba = np.flipud(img_rgba) #original image is flipped vertically
            img_rgba[:,:,1:2] = 100 #just for fun add little bit of green in all pixels
            airsim.write_png(os.path.normpath(filename + '.greener.png'), img_rgba) #write to png 


#restore to original state
client.reset()

client.enableApiControl(False) # you can drive again with the arrows


            
