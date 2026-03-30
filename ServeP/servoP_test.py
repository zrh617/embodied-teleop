import csv
import time
from CPS import CPSClient


cps = CPSClient()
cps.HRIF_Connect(0, "10.20.200.46", 10003)

with open('E05_ServoP_data.csv', 'r') as readCSV:
    teach = [row for row in csv.reader(readCSV)]

joints = teach[0]  # start joints for the servo motion
points = [0, 0, 0, 0, 0, 0]
result = []
cps.HRIF_GetInverseKin(0, 0, joints[0:6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                             result)  # Invert the first pose positions into a joint position for joint motion.This is done to reduce the collision
nRet = cps.HRIF_MoveJ(0, 0, points, result, "TCP", "Base", 50, 360, 50, 1, 0, 0, 0, "0")  # move to the start
if nRet != 0:
    raise ValueError(f"MoveJ返回错误:{nRet}")
time.sleep(0.05)
result = []
cps.HRIF_IsMotionDone(0, 0, result)
# wait for the robot move to the start
while not result[0]:
    cps.HRIF_IsMotionDone(0, 0, result)

giff = 8000
servoTime = 0.02  # parameter for servo interval, 20ms,no less than 15ms
# to set the look-ahead time. The larger the look-ahead time, the smoother the actual motion trajectory, but the phase lag will also increase accordingly.
lookaheadTime = 0.2  # parameter for servo lookahead time, 200ms.Suggest between 50ms and 200ms
nRet = cps.HRIF_StartServo(0, 0, servoTime, lookaheadTime)  # start servoP task
if nRet != 0:
    raise ValueError(f"StartServoP返回错误:{nRet}")

# time.sleep(0.01)
# invoke "PushServoP" intervally to drive robot move
startTime = time.perf_counter()
count = 0
for i, point in enumerate(teach):
    nRet = cps.HRIF_PushServoP(0, 0, point, ['0'] * 6, ['0'] * 6)
    if nRet != 0:
        raise ValueError(f"PushServoP返回错误:{nRet}")
    count += 1

    # 等待 servoTime 时间间隔
    while True:
        currentTime = time.perf_counter()
        if (currentTime - startTime) > (servoTime * (i + 1)):
            break
        time.sleep(0.0001)

end = time.perf_counter()
print(f"runtime: {end - startTime:.4f}")
print("ServoP 运动结束")
