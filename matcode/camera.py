import time
import scipy.io as sio

data_list = ['self_distance', 'v2_distance', 'v2_cmd', 'self_cmd', 'offset_theta', 'sensor_distance']

while True:
    try:
        py_data = sio.loadmat('py_data.mat')
        print(py_data)
        data_stripped = {data_list[0]: 0.0,
                         data_list[1]: float(py_data[data_list[1]][0,0]),
                         data_list[2]: float(py_data[data_list[2]][0,0]),
                         data_list[3]: float(py_data[data_list[3]][0,0])}
        #py_data['self_distance'][0,0] = 0.0
        print(data_stripped)
        sio.savemat('py_data.mat',data_stripped)
        break
    except Exception:
        time.sleep(0.01)
time.sleep(6)
while True:
    try:
        py_data = sio.loadmat('py_data.mat')
        print(py_data)
        data_stripped = {data_list[0]: 1.0,
                         data_list[1]: float(py_data[data_list[1]][0,0]),
                         data_list[2]: float(py_data[data_list[2]][0,0]),
                         data_list[3]: float(py_data[data_list[3]][0,0])}
        #py_data['self_distance'][0,0] = 1.0
        print("Updating self_distance = ", 1.0)
        sio.savemat('py_data.mat',data_stripped)
        break
    except Exception:
        time.sleep(0.01)
time.sleep(10)
while True:
    try:
        py_data = sio.loadmat('py_data.mat')
        print(py_data)
        data_stripped = {data_list[0]: 2.0,
                         data_list[1]: float(py_data[data_list[1]][0,0]),
                         data_list[2]: float(py_data[data_list[2]][0,0]),
                         data_list[3]: float(py_data[data_list[3]][0,0])}
        #py_data['self_distance'][0,0] = 2.0
        #print(data_stripped)
        sio.savemat('py_data.mat',data_stripped)
        break
    except Exception:
        time.sleep(0.01)
time.sleep(2)
flag = 0
while flag == 0:
    while True:
        try:
            py_data = sio.loadmat('py_data.mat')
            #print(py_data)
            if (py_data[data_list[3]][0,0] == 0.0):
                flag = 1
            break
        except Exception:
            time.sleep(0.01)
    time.sleep(1)

time.sleep(10)
while True:
    try:
        py_data = sio.loadmat('py_data.mat')
        print(py_data)
        data_stripped = {data_list[0]: 3.0,
                         data_list[1]: float(py_data[data_list[1]][0,0]),
                         data_list[2]: float(py_data[data_list[2]][0,0]),
                         data_list[3]: float(py_data[data_list[3]][0,0])}
        #py_data['self_distance'][0,0] = 3.0
        #print(data_stripped)
        sio.savemat('py_data.mat',data_stripped)
        break
    except Exception:
        time.sleep(0.1)
        
time.sleep(10)                
while True:
    try:
        py_data = sio.loadmat('py_data.mat')
        print(py_data)
        data_stripped = {data_list[0]: 4.0,
                         data_list[1]: float(py_data[data_list[1]][0,0]),
                         data_list[2]: float(py_data[data_list[2]][0,0]),
                         data_list[3]: float(py_data[data_list[3]][0,0])}
        #py_data['self_distance'][0,0] = 4.0
        #print(data_stripped)
        sio.savemat('py_data.mat',data_stripped)
        break
    except Exception:
        time.sleep(0.1)
                


