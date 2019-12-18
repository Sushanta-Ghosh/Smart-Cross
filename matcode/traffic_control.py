import time
import scipy.io as sio
import sys


def main():
    data_list = ['self_distance', 'v2_distance', 'v2_cmd', 'self_cmd', 'offset_theta', 'sensor_distance']

    local_data = {'self_distance': 0.0, 'v2_distance':0.0, 'v2_cmd': 3.0, 'self_cmd': 3.0}
    #initialize mat file values to begin

    sio.savemat('py_data.mat',local_data)
    decision_flag = False
    print("python main function")
    while True:
        try:
            try:
                #Each cycle of the control system, load in the .mat data file to make decisions
                py_data = sio.loadmat('py_data.mat')
                local_data = {data_list[0]: float(py_data[data_list[0]][0,0]),
                              data_list[1]: float(py_data[data_list[1]][0,0]),
                              data_list[2]: float(py_data[data_list[2]][0,0]),
                              data_list[3]: float(py_data[data_list[3]][0,0])}
                              
                print("self_distance = ", local_data['self_distance'])
                print("v2_distance = ", local_data['v2_distance'])
                              
                if (local_data['self_cmd'] == 1.0 and local_data['v2_cmd'] == 0.0): #Go to Leader Mode
                    print("Leader!")
                    
                    #py_data = sio.loadmat('py_data.mat')
                    #calculate command and drive mode based on vehicle distances
                    self_cmd, Drive_Mode = Leader(local_data['self_distance'], local_data['v2_cmd'])
                    
                    #add code to send necessary information to the other vehicle
##                    
##                    data_stripped = {data_list[0]: float(py_data[data_list[1]][0,0]),
##                                     data_list[1]: float(py_data[data_list[1]][0,0]),
##                                     data_list[2]: float(py_data[data_list[2]][0,0]),
##                                     data_list[3]: self_cmd}
                    local_data['self_cmd'] = self_cmd
                    try:
                        #save the updated information so it can be sent over network to the other vehicle
                        sio.savemat('py_data.mat',local_data)
                        #local_data = data_stripped #update local files
                        print(local_data)
                    except Exception:
                        time.sleep(0.035)
                    
                    
                elif (local_data['self_cmd'] == 0.0 and local_data['v2_cmd'] == 1.0) or local_data['v2_cmd'] == 2.0: #Go to Follower Mode
                    print("Follower Mode!")
                    
                    #py_data = sio.loadmat('py_data.mat')
                    #calculate command and drive mode based on vehicle distances
                    self_cmd, Drive_Mode = Follower(local_data['self_distance'])
                    local_data['self_cmd'] = self_cmd
                    #add code to send necessary information to the other vehicle
##                        
##                        data_stripped = {data_list[0]: float(py_data[data_list[1]][0,0]),
##                                         data_list[1]: float(py_data[data_list[1]][0,0]),
##                                         data_list[2]: float(py_data[data_list[2]][0,0]),
##                                         data_list[3]: self_cmd}
                    #save the updated information so it can be sent over network to the other vehicle
                    try:
                        sio.savemat('py_data.mat', local_data)
                        #local_data = data_stripped #update local files
                        print(local_data)
                    except Exception:
                        time.sleep(0.035)
                    
                elif local_data['self_cmd'] == 2.0: #Go to Idle Mode
                    print("Path Complete, Idling...")
                    self_cmd = 2.0
                    Drive_Mode = 0
                    local_data['self_cmd'] = self_cmd
                    try:
                        sio.savemat('py_data.mat',local_data)
                        #local_data = data_stripped #update local files
                        print(local_data)
                    except Exception:
                        time.sleep(0.035)
                
                #Otherwise Default to Decision mode until the above conditions are satisfied.
                else:
                    print("Decision Mode!")
              
                    #py_data = sio.loadmat('py_data.mat')
                    #calculate command and drive mode based on vehicle distances
                    self_cmd, Drive_Mode = make_decision(local_data['self_distance'], local_data['v2_distance'],decision_flag)
                    print("Command = ", self_cmd)
                    print("Drive_Mode = ", Drive_Mode)
                    
                    if (self_cmd or self_cmd == 0.0): #if we made a command decision, if not keep the same local_data values
                        local_data['self_cmd'] = self_cmd
                    try:
                        #save the updated information so it can be sent over network to the other vehicle
                        sio.savemat('py_data.mat',local_data)
                        #local_data = data_stripped #update local files
                        print(local_data)
                    except Exception:
                        time.sleep(0.035)
                
                time.sleep(1) #pause before re-scanning the control system
            except Exception:
                time.sleep(0.035)
        except (KeyboardInterrupt, EOFError):
            print("Shutting down Traffic Control Script ...")
            sys.exit(1)


#takes self_distance and v2_cmd as inputs, stops at intersection, waits until Follower is safe
def Leader(self_distance, v2_cmd):
    print("Self_distance = ", self_distance)
    if self_distance > 1: #stop the car if the camera has picked up the intersection
        Drive_Mode = 0
    else: #keep moving forward towards the intersection otherwise
        Drive_Mode = 1
    if v2_cmd > 1: #if Follower vehicle is safe, become the new Follower
        self_cmd = 0.0
    else: #stay in Leader mode otherwise
        self_cmd = 1.0
    print("Leader Command is ", self_cmd)
    return self_cmd, Drive_Mode



#takes self_distance and v2_cmd as inputs, stops at intersection, waits until Follower is safe
def Follower(self_distance):
    print("Self_distance = ", self_distance)
    if self_distance > 3: #stop the Follower car if it has reached the end of its path, send safe signal
        Drive_Mode = 0
        self_cmd = 2.0
    else: #keep moving in the forward path, stay in Follower Mode
        Drive_Mode = 1
        self_cmd = 0.0

    return self_cmd, Drive_Mode



def make_decision(self_distance, v2_distance,decision_flag):
    
    if (self_distance == v2_distance) and not(decision_flag):   #if decision has not yet taken place     
        self_cmd = 3.0
        Drive_Mode = 1
    elif self_distance > v2_distance: #self is Leader, indicate a decision has been made by self
        self_cmd = 1.0
        Drive_Mode = 1
        decision_flag = True
    elif self_distance < v2_distance: #self is Follower, indicate a decision has been made by self
        self_cmd = 0.0
        Drive_Mode = 1
        decision_flag = True
    else: #keep the command and drive mode the same
        self_cmd = False
        Drive_Mode = False

    return self_cmd, Drive_Mode



if __name__ == '__main__':
    main()        


