import sys
sys.path.append('../')
from Common.project_library import *
import random

project_identifier = 'P3B' 
ip_address = '169.254.175.138'
hardware = False

short_tower_angle = 270 
tall_tower_angle = 0 
drop_tube_angle = 180 

bot_camera_angle = -21.5 

bin1_offset = 0.1 
bin1_color = [1,0,0] 
bin2_offset = 0.15
bin2_color = [0,1,0]
bin3_offset = 0.2
bin3_color = [0,0,1]
bin4_offset = 0.25
bin4_color = [0,1,1]

#--------------- DO NOT modify the information below -----------------------------

if project_identifier == 'P0':
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    bot = qbot(0.1,ip_address,QLabs,None,hardware)
    
elif project_identifier in ["P2A","P2B"]:
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    arm = qarm(project_identifier,ip_address,QLabs,hardware)

elif project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration,None, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    
elif project_identifier == 'P3B':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    qbot_configuration = [bot_camera_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color]]
    configuration_information = [table_configuration,qbot_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bins = bins(bin_configuration)
    bot = qbot(0.1,ip_address,QLabs,bins,hardware)
    

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

#initial home position when bot spawns
home_position = bot.position() 

#initialization of updated variables
#desired_id = 0
num_of_loops = 0
previous_container_id = 0
previous_container = ("",0,"")

#generates container onto sorting station
def dispense(random_container_id):

# By: James Ensley

    current_container = table.dispense_container(random_container_id,True)
    time.sleep(1)

    return current_container #current container is referring to the container most recently dispensed

#loads container(s) onto qbot
def load():  

# By: James Ensley

    global num_of_loops
    global previous_container
    global previous_container_id
    
    #initialization of variables
    num_on_qbot = 0
    mass_on_qbot = 0
    desired_id = 0 #place holder/id we want to sort/recycle
    current_id = 0 #updated id after each new container
    done = False

    #containers position on qbot after loading
    first_container_pos = [0.057, -0.536, 0.486]
    second_container_pos = [-0.037, -0.539, 0.472]
    third_container_pos = [-0.13, -0.522, 0.5]

    #rotates bc its easier to reach
    time.sleep(2)
    bot.rotate(90)
    
    #also i don't really need the seperate boolean variable, i believe i can just say 'while False:'
    #continues loading till reaches given parameters (3 containers on qbot or exceeds 90g)
    
    while (done == False):

        print("START SORTING")
        
        #num_on_qbot starts at 0 hence why its <= 2
        if (num_on_qbot <= 2 and mass_on_qbot < 90): 

            #if bot is reset after loop
            if (num_on_qbot == 0 and num_of_loops >= 1):
                current_container = previous_container
                current_id = previous_container_id
                print("NOW SORTING CONTAINER ID = " + str(previous_container_id))

            #first initial run through
            elif (num_on_qbot == 0 and num_of_loops == 0):
                random_container_id = random.randint(1,6)
                previous_container_id = random_container_id
                current_container = dispense(random_container_id)
                current_id = random_container_id

            #more than one container on qbot
            elif (num_on_qbot >= 1): 
                random_container_id = random.randint(1,6)
                previous_container_id = random_container_id
                current_container = dispense(random_container_id)
                current_id = random_container_id

            #automatically sets each new container as the previous container so when current_id != desired_id
            #or in the case when the potential mass >= 90 so then it wouldn't go through the cases again
            previous_container = current_container
            
            #when they match with desired pick it up
            if (num_on_qbot == 0 or current_id == desired_id): 

                #if current_id == desired_id
                if (num_on_qbot != 0):
                    
                    #tests to make sure the next containers mass wont cause the total to exceed 90g
                    potential_mass = mass_on_qbot + int(current_container[1])
                    print("POTENTIAL MASS = " + str(potential_mass))
            
                    if (potential_mass >= 90):
                        print("EXCEEDS 90g IF LOADED, SO STOP!")
                        num_of_loops = num_of_loops + 1
                        return current_container
                    
                    print(str(current_id) + " = " + str(desired_id) + " AND LESS THAN 90g, SO PICK IT UP!")
                
                #qarm picks up container 
                arm.move_arm(0.604,0.0,0.284)
                time.sleep(1)
                arm.control_gripper(40)
                time.sleep(1)
                arm.move_arm(0.621, 0.0, 0.351)
                time.sleep(1)
                arm.move_arm(0.599, -0.161, 0.351)
                time.sleep(1)
                arm.move_arm(-0.047, -0.301, 0.766)
                time.sleep(1)

                #indiviual containers placement on qbot
                
                #first container
                if (num_on_qbot == 0):
                    arm.move_arm(first_container_pos[0],first_container_pos[1],first_container_pos[2])

                    time.sleep(3)
                    arm.control_gripper(-40)
                    time.sleep(3)
                    arm.move_arm(-0.0, -0.071, 0.883)
                    time.sleep(1)
                    arm.home()
                    
                #second container
                elif (num_on_qbot == 1):
                    arm.move_arm(second_container_pos[0],second_container_pos[1],second_container_pos[2])

                    time.sleep(3)
                    arm.control_gripper(-18)
                    time.sleep(3)
                    arm.move_arm(-0.0, -0.071, 0.883)
                    time.sleep(1)
                    arm.home()
                    
                #third container (includes extra movements to prevent knocking)
                elif (num_on_qbot == 2):
                    arm.move_arm(-0.228, -0.412, 0.685)
                    time.sleep(1)
                    arm.move_arm(-0.251, -0.453, 0.59)
                    time.sleep(1)
                    arm.move_arm(third_container_pos[0],third_container_pos[1],third_container_pos[2])
                    
                    time.sleep(3)
                    arm.control_gripper(-25)
                    time.sleep(3)
                    arm.move_arm(-0.0, -0.071, 0.883)
                    time.sleep(1)
                    arm.home()

                #type of first container picked up must be the same as the rest
                if(num_on_qbot == 0): 

                    #can think of container_on_bot as the container tuple that comes with the desired_id
                    #or the tuple of the container currently on the bot
                    container_on_bot = current_container 
                    desired_id = current_id
                    
                #update/output variables
                num_on_qbot = num_on_qbot + 1
                mass_on_qbot = mass_on_qbot + int(current_container[1])
                print("MASS CURRENTLY ON QBOT = " + str(mass_on_qbot))

            else:  #if not the same container id
                
                num_of_loops = num_of_loops + 1
                num_on_qbot = 0
                mass_on_qbot = 0
                
                print("STOP SORTING")
                print("NUMBER OF TIMES GONE THROUGH = " + str(num_of_loops))
                print("NEXT RUN SORT CONTAINER ID = " + str(previous_container_id))
                print("NOW GO TO " + str(container_on_bot[2]))
                
                return container_on_bot
        else: #reaches 3 containers

            #in the event 3 containers are on the bot, leaving no containers left on the sorting station
            #otherwise no containers will be left on the sorting station, causing issues

            random_container_id = random.randint(1,6)
            previous_container_id = random_container_id
            current_container = dispense(random_container_id)
            
            num_of_loops = num_of_loops + 1
            num_on_qbot = 0
            mass_on_qbot = 0
            
            print("STOP SORTING")
            print("NUMBER OF TIMES GONE THROUGH = " + str(num_of_loops))
            print("NEXT RUN SORT CONTAINER ID = " + str(previous_container_id))
            print("NOW GO TO " + str(container_on_bot[2]))
            
            return container_on_bot
        

#deposits containers into their destined recycling bin
def deposit():

# By: Shafwan Fahim

    print("DUMPING")

    bot.deactivate_ultrasonic_sensor()
    bot.deactivate_color_sensor()

    bot.activate_linear_actuator()

    #stop and dump containers
    bot.stop()
    time.sleep(3)
    bot.rotate_hopper(42)
    time.sleep(3)
    bot.rotate_hopper(0)
    bot.deactivate_linear_actuator() 

#transfers containers to their corresponding recycling bins
def transfer(container_on_bot):

# By: Shafwan Fahim

    desired_bin = 0
    time.sleep(3)
    following_line = True
    bot.rotate(-90)
    
    #activatates bin identification sensors
    bot.activate_ultrasonic_sensor()
    bot.activate_color_sensor()

    #containers distances/colours (definitely could change these to lists like desired = [id, ultra, colour]
    if (container_on_bot[2] == "Bin01"):
        desired_bin = 1
        desired_ultra = bin1_offset
        desired_col = bin1_color
    elif (container_on_bot[2] == "Bin02"):
        desired_bin = 2
        desired_ultra = bin2_offset
        desired_col = bin2_color
    elif (container_on_bot[2] == "Bin03"):
        desired_bin = 3
        desired_ultra = bin3_offset
        desired_col = bin3_color
    elif (container_on_bot[2] == "Bin04"):
        desired_bin = 4
        desired_ultra = bin4_offset
        desired_col = bin4_color

    print("MOVING TO BIN ID = " + str(desired_bin))
    
    while(following_line == True):

        #active ultrasonic/colour input from sensors
        ultrasonic_input = bot.read_ultrasonic_sensor()
        color_input = bot.read_color_sensor()

        #active infared sensors input
        ir_sensor = bot.line_following_sensors()
        right_ir = ir_sensor[0]
        left_ir = ir_sensor[1]

        #line following algorithm
        if (left_ir == 1 and right_ir == 1):
            bot.set_wheel_speed([0.05,0.05])
        elif (left_ir == 1 and right_ir == 0):
            bot.set_wheel_speed([0.05,0.025])
        elif (left_ir == 0 and right_ir == 1):
            bot.set_wheel_speed([0.025,0.05])
        
        #if reaches desired colour/ultrasonic sensor input for corresponding bin 
        if (color_input[0] == desired_col):
            #bot.activate_ultrasonic_sensor()
            if (ultrasonic_input <= desired_ultra):

                #different positioning for each bin when reaches destination
                #red (metal)
                if (desired_bin == 1):
                    bot.rotate(15)
                    time.sleep(2)
                    bot.forward_time(2)
                    deposit() 
                    # The hopper is then rotated a second time for this specific bin,  
                    # This is to account for static friction and irregularities in quanser and make sure all conatiners are dumped properly
                    bot.activate_linear_actuator() 
                    time.sleep(1.5)
                    bot.rotate_hopper(57)
                    time.sleep(2)
                    bot.rotate_hopper(0)
                    bot.deactivate_linear_actuator()
                #green (plastic)
                elif (desired_bin == 2):
                    bot.forward_time(3)
                    time.sleep(2)
                    bot.rotate(10)
                    deposit()
                #blue (paper)
                elif (desired_bin == 3):
                    bot.forward_time(3)
                    bot.rotate(-90)
                    time.sleep(2)
                    bot.forward_time(0.5)
                    bot.rotate(95)
                    deposit()
                #cyan (garbage)
                elif (desired_bin == 4):
                    bot.forward_time(3.5) 
                    bot.rotate(-90)
                    time.sleep(2)
                    bot.forward_time(0.42)
                    bot.rotate(95)
                    deposit()
                bot.stop()
                following_line = False
       
    
#returns q-bot home after depositing containers, continuing to follow line
def home():

# By: James Ensley   

    print("GOING HOME NOW")
    
    following_line = True
    
    while(following_line == True):

        #active infared sensors input
        ir_sensor = bot.line_following_sensors()
        right_ir = ir_sensor[0]
        left_ir = ir_sensor[1]

        #line following algorithm
        if (left_ir == 1 and right_ir == 1):
            bot.set_wheel_speed([0.05,0.05])
        elif (left_ir == 1 and right_ir == 0):
            bot.set_wheel_speed([0.05,0.025])
        elif (left_ir == 0 and right_ir == 1):
            bot.set_wheel_speed([0.025,0.05])
        else:
            print("line is lost")

        #definitely could find the different between with a 0.1 diff however its inconsistent
        x = abs(float(home_position[0]) - float(bot.position()[0]))

        """
        #y = abs(float(home_position[1]) - float(bot.position()[1]))
        #z = abs(float(home_position[2]) - float(bot.position()[2]))
        """

        #when current qbots position reaches home, stop the qbot
        if (x <= 0.1 and float(bot.position()[1]) <= 0.1 and float(bot.position()[1]) > 0):
            
            bot.rotate(-90)
            bot.forward_time(0.35)
            bot.rotate(93)
            print("YOU MADE IT!")
            bot.stop()
            following_line = False
            break

#function to combine all previous functions together
def main():

# By: Shafwan Fahim

    keep_going = True

    while(keep_going == True):
        if (num_of_loops >= 1):
            continue_looping = input("Do you wish to continue? Please Enter 'Yes' or 'No': ")
            if (continue_looping == 'Yes'): # use wishes to continue, therefore, recycle/sort the last container left on the table
                container_on_bot = load() 
                transfer(container_on_bot)
                home()
            elif (continue_looping == 'No'): # use wishes to stop, so break
                keep_going == False
                break
            else: # user inputs invalid string like 'yes' or 'no', making them required to input again
                continue_looping = input("Please enter valid input, 'Yes' or 'No' : ")
                if (continue_looping == 'Yes'): # use wishes to continue, therefore, recycle/sort the last container left on the table
                    container_on_bot = load() 
                    transfer(container_on_bot)
                    home()
                elif (continue_looping == 'No'): # use wishes to stop, so break
                    keep_going == False
                    break 
        if (num_of_loops == 0):
            container_on_bot = load()
            transfer(container_on_bot)
            home()

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
