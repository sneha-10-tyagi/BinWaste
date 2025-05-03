import serial
import csv
import time


arduino_port = "/dev/tty.usbserial-1120"  // use your system's port
baud_rate = 9600  

ser = serial.Serial(arduino_port, baud_rate)
print("Connected to Arduino...")

with open('dustbin_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Distance (cm)', 'Fill (%)', 'Alert/Warning'])  # Write the header row
    
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            
            # Example parsing from serial data:
            if "Distance" in line and "Fill" in line:
                data = line.split(',')
                distance = data[0].split(":")[1].strip()
                fill = data[1].split(":")[1].strip()
                
                # Check for alerts/warnings
                alert_warning = ""
                if "ALERT" in line:
                    alert_warning = "ALERT"
                elif "WARNING" in line:
                    alert_warning = "WARNING"
                
                writer.writerow([distance, fill, alert_warning])
                print(f"Logged: Distance={distance} cm, Fill={fill}%, Alert={alert_warning}")
                
                time.sleep(1)  
