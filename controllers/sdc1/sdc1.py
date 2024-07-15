from controller import Robot

bot = Robot()

timestep = 64

# getting devices
cam = bot.getDevice('camera')
left_wheel = bot.getDevice('left_front_wheel')
right_wheel = bot.getDevice('right_front_wheel')
l_steer = bot.getDevice('left_steer')
r_steer = bot.getDevice('right_steer')

# initialisations
cam.enable(timestep)
left_wheel.setPosition(float('inf'))
right_wheel.setPosition(float('inf'))
l_steer.setPosition(10)
r_steer.setPosition(10)
left_wheel.setVelocity(20)
right_wheel.setVelocity(20)

# main loop
while bot.step(timestep) != -1:

    # image data
    img = cam.getImage()
    image_width = cam.getWidth()
    image_height = cam.getHeight()
    
    # processing image, method 1
    # getting average position of yellow pixels
    # getting total yellow pixels
    
    x_yellow = []
    for x in range(0, image_width):
        for y in range(0, image_height):
            red_val = cam.imageGetRed(img, image_width, x, y)
            green_val = cam.imageGetGreen(img, image_width, x, y)
            blue_val = cam.imageGetBlue(img, image_width, x, y)
            if red_val > 170 and green_val > 150 and blue_val > 40:
                x_yellow.append(x)
    
    # finding average of yellow pixels
    if x_yellow: # if there are any yellow pixels
        x_total = 0
        for x in x_yellow:
            x_total = x_total + x
        x_average = x_total / len(x_yellow)
    
    # rotating steering angle so that yellow lane remains in the center
    x_center = image_width / 2
    
    
    if x_average < x_center: # max pixels are on the left, take a left turn
        l_steer.setPosition(-0.11)
        r_steer.setPosition(-0.11)
    elif x_average > x_center: # max pixels are on the right, take right turn
        l_steer.setPosition(0.21)
        r_steer.setPosition(0.13)
        
    # move forward
    left_wheel.setVelocity(80)
    right_wheel.setVelocity(80)
