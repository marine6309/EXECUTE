import wmi

def get_cpu_temperature():
    try:
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        temperature_info = w.Sensor()
        for sensor in temperature_info:
            if sensor.SensorType == u'Temperature' and 'CPU' in sensor.Name:
                return sensor.Value
    except Exception as e:
        print(f"Could not read CPU temperature: {e}")
        return None

cpu_temp = get_cpu_temperature()
if cpu_temp is not None:
    print(f"CPU Temperature: {cpu_temp}°C")
else:
    print("Could not read CPU temperature.")
