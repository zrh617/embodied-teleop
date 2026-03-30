#!/usr/bin/env python
# _*_ coding:utf-8 _*_
'''
*	Copyright(c) 2020-2025 Huayan Robotics
*   All rights reserved.
*	
*	FileName:CPS.py
*	Descriptio:Python SDK
*   version:1.1.0.0
*	Modification Records:
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*   SDK Version                    Date                                                      Add                                                            Modify                                                       Delete
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*   V1.0.0.0                       2022.05.12                                                Create a file
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*   V1.0.0.1                       2022.07.07                                                Create a interface
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*   V1.0.0.2                       2022.08.05                                                Create a interface
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*   V1.0.0.3                       2022.08.28                                                HRIF_SetToolMotion
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*   V1.0.0.4                       2023.02.13                                                HRIF_ReadOverride
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*   V1.0.0.5                       2023.02.13                                                HRIF_ReadPointByName
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*   V1.0.1.0                       2023.02.23                                                HRIF_GetErrorCodeStr
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*   V1.0.2.0                       2023.02.23                                                HRIF_SetPoseTrackingMaxMotionLimit
                                                                                             HRIF_SetPoseTrackingPIDParams
                                                                                             HRIF_SetPoseTrackingTargetPos
                                                                                             HRIF_SetPoseTrackingState
                                                                                             HRIF_SetUpdateTrackingPose
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*   V1.0.2.1                       2023.03.21                                                                                                               HRIF_IsBlendingDone
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*   V1.0.2.2                       2023.08.22                                                                                                               HRIF_ReadHoldingRegisters
                                                                                                                                                            HRIF_WriteHoldingregisters  
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*   V1.0.3.0                       2024.04.15                                                HRIF_SetSimulation
                                                                                             HRIF_OpenBrake
                                                                                             HRIF_CloseBrake
                                                                                             HRIF_ReadBrakeStatus
                                                                                             HRIF_MoveToSS
                                                                                             HRIF_SetCollideLevel
                                                                                             HRIF_ReadMaxPayload
                                                                                             HRIF_ReadPayload
                                                                                             HRIF_CalUcsPlane
                                                                                             HRIF_CalUcsLine
                                                                                             HRIF_CalTcp3P
                                                                                             HRIF_CalTcp4P
                                                                                             HRIF_ConfigTCP
                                                                                             HRIF_ConfigUCS
                                                                                             HRIF_HRSetMaxSearchDistance
                                                                                                                                                             HRIF_HRApp      
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*   V1.0.4.0                       2024.08.27                                                HRIF_EnableEndBTN
                                                                                             HRIF_ReadPointList
                                                                                             HRIF_ReadTCPList
                                                                                             HRIF_ReadUSCList
                                                                                             HRIF_SetFTFreeDriveSpeedMode
                                                                                             HRIF_ReadtFTFreeDriveSpeedMode
                                                                                             HRIF_ReadFTCabData
                                                                                             HRIF_SetFreeDriveMotionFreedom
                                                                                             HRIF_SetFTFreeFactor
                                                                                             HRIF_SetFreeDriveCompensateForce
                                                                                             HRIF_ReadFTMotionFreedom
                                                                                             HRIF_SetSteadyContactDeviationRange
                                                                                             HRIF_InitPath
                                                                                             HRIF_PushPathPoints
                                                                                             HRIF_EndPushPathPoints
                                                                                             HRIF_DelPath
                                                                                             HRIF_ReadPathList
                                                                                             HRIF_ReadPathInfo
                                                                                             HRIF_UpdataPathName
                                                                                             HRIF_ReadPathState
                                                                                             HRIF_MoveLinearWeave
                                                                                             HRIF_MoveCircularWeave
                                                                                             HRIF_ReadServoEsJState
                                                                                                                                                              HRIF_WayPoint2
                                                                                                                                                              HRIF_SetScriptForceControlState
                                                                                                                                                              HRIF_MoveS                                                                                                  
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
* V1.0.5.0                          2024.09.02                                               HRIF_MovePathJOL
                                                                                             HRIF_GetMovePathJOLIndex
                                                                                             HRIF_cdsSetIO
                                                                                             HRIF_SetPoseTrackingStopTimeOut
                                                                                             HRIF_EnterSafeGuard
                                                                                             HRIF_AddSafePlane
                                                                                             HRIF_DelSafePlane
                                                                                             HRIF_ReadSafePlaneList
                                                                                             HRIF_ReadSafePlane
                                                                                             HRIF_UpdateSafePlane
                                                                                             HRIF_SetDepthThresholdForDampingArea
                                                                                             HRIF_SpeedJ
                                                                                             HRIF_SpeedL
                                                                                             HRIF_ReadTriStageSwicth
                                                                                             HRIF_SetTriStageSwicth                                                                          
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
* V1.0.5.1                          2024.10.10                                                                                                                HRIF_ReadCurFSM
                                                                                                                                                              HRIF_MoveLinearWeave
                                                                                                                                                              HRIF_MoveCircularWeave                                                                       
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
* V1.0.6.0                          2024.10.11                                               HRIF_SwitchScript
                                                                                             HRIF_ReadDefaultScript                                                                                                                                                                                                                                                                                                                  HRIF_InitPathJ(Delete)                                                                          
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
* V1.0.7.0                          2024.12.27                                               HRIF_MoveAlignToZ
                                                                                             HRIF_SetBaseInstallingAngle
                                                                                             HRIF_GetBaseInstallingAngle                                                                    
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
* V1.0.8.0                          2024.02.05                                               HRIF_SetLastCalibParams
                                                                                             HRIF_GetLastCalibParams                                                       
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
* V1.0.9.0                          2025.03.05                                               HRIF_GetLoadIdentifyResult
                                                                                             HRIF_LoadIdentify
                                                                                             HRIF_SetFTCalibration
                                                                                             HRIF_ReadForceData
                                                                                             HRIF_SetInitializeForceSensor
                                                                                             HRIF_GetLastCalibParams  
* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
* V1.0.10.0                          2025.03.25                                              HRIF_ShortJogJ
                                                                                             HRIF_ShortJogL
                                                                                             HRIF_LongJogJ
                                                                                             HRIF_LongJogL
                                                                                             HRIF_LongMoveEvent     
* V1.0.11.0                          2025.07.30                                              HRIF_GetInverseDynamics
                                                                                             HRIF_SetFTUCS
                                                                                             HRIF_ReadFTUCS                                                                                                                                                                                                                                                        
 * ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
 *V1.0.12.0                          2025.08.13                                              HRIF_ReadAllBoxCI
                                                                                             HRIF_ReadAllBoxCO
                                                                                             HRIF_ReadAllBoxDI
                                                                                             HRIF_ReadAllBoxDO
                                                                                             HRIF_ReadActCoord
                                                                                             HRIF_ReadActCoord_nJ
                                                                                             HRIF_CalTCPOrt
                                                                                             HRIF_SetDftTCP
                                                                                             HRIF_SetPathRefJoints
 * ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 *V1.1.0.0                          2025.09.12                                                                                                                Modify connection
 * ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 '''


import time
from tokenize import Double
import socket
import os
import struct
from enum import IntEnum


# from yaml import compose_all


class RbtFSM(IntEnum):
    enCPSState_PreInitialize = 0  # PreInitialize / 未初始化
    enCPSState_Initialize = 1  # 1 Initialize / 初始化
    # ElectricBox FSM / 电箱状态机   
    enCPSState_ElectricBoxDisconnect = 2  # 2 ElectricBoxDisconnect  / 与电箱控制板断开
    enCPSState_ElectricBoxConnecting = 3  # 3 ElectricBoxConnecting  / 连接电箱控制板
    enCPSState_EmergencyStopHandling = 4  # 4 EmergencyStopHandling  / 急停处理
    enCPSState_EmergencyStop = 5  # 5 EmergencyStop  / 急停
    enCPSState_Blackouting48V = 6  # 6 Blackouting48V  / 正在切断本体供电
    enCPSState_Blackout48V = 7  # 7 Blackout48V / 本体供电已切断
    enCPSState_Electrifying48V = 8  # 8 Electrifying48V  / 正在准备给本体供电
    enCPSState_SafetyGuardErrorHandling = 9  # 9 SafetyGuardErrorHandling / 安全光幕错误处理中
    enCPSState_SafetyGuardError = 10  # 10 SafetyGuardError / 安全光幕错误
    enCPSState_SafetyGuardHandling = 11  # 11 SafetyGuardHandling  / 安全光幕处理
    enCPSState_SafetyGuard = 12  # 12 SafetyGuard  / 安全光幕
    # controller FSM  / 控制器状态机
    enCPSState_ControllerDisconnecting = 13  # 13 ControllerDisconnecting  / 正在反初始化控制器
    enCPSState_ControllerDisconnect = 14  # 14 ControllerDisconnect / 控制器已处于未初始化状态
    enCPSState_ControllerConnecting = 15  # 15 ControllerConnecting / 正在初始化控制器
    enCPSState_ControllerVersionError = 16  # 16 ControllerVersionError  / 控制器版本过低错误
    enCPSState_EtherCATError = 17  # 17 EtherCATError / EtherCAT错误
    enCPSState_ControllerChecking = 18  # 18 ControllerChecking / 控制器初始化后检查状态
    # Robot FSM / 机器人状态机
    enCPSState_Reseting = 19  # 19 Reseting / 复位机器人
    enCPSState_RobotOutofSafeSpace = 20  # 20 RobotOutofSafeSpace / 机器人超出安全空间
    enCPSState_RobotCollisionStop = 21  # 21 RobotCollisionStop / 机器人安全碰撞停车
    enCPSState_Error = 22  # 22 Error / 机器人错误
    enCPSState_Enabling = 23  # 23 Enabling / 机器人使能中
    enCPSState_Disable = 24  # 24 Disable / 机器人去使能
    enCPSState_Moving = 25  # 25 Moving / 机器人运动中
    enCPSState_LongJogMoving = 26  # 26 LongJogMoving / 机器人长点动运动中
    enCPSState_RobotStopping = 27  # 27 RobotStopping / 机器人停止运动中
    enCPSState_Disabling = 28  # 28 Disabling / 机器人去使能中
    enCPSState_RobotOpeningFreeDriver = 29  # 29 RobotOpeningFreeDriver / 机器人正在开启零力示教
    enCPSState_RobotClosingFreeDriver = 30  # 30 RobotClosingFreeDriver / 机器人正在关闭零力示教
    enCPSState_FreeDriver = 31  # 31 FreeDriver / 机器人处于零力示教
    enCPSState_RobotHolding = 32  # 32 RobotHolding / 机器人暂停
    enCPSState_StandBy = 33  # 33 StandBy / 机器人就绪
    # script FSM / 脚本状态机
    enCPSState_ScriptRunning = 34  # 34 ScriptRunning / 脚本运行中
    enCPSState_ScriptHoldHandling = 35  # 35 ScriptHoldHandling / 脚本暂停处理中
    enCPSState_ScriptHolding = 36  # 36 ScriptHolding / 脚本暂停
    enCPSState_ScriptStopping = 37  # 37 ScriptStopping / 脚本停止中
    enCPSState_ScriptStopped = 38  # 38 ScriptStopped / 脚本已停止
    # HRApp / 插件
    enCPSState_HRAppDisconnected = 39  # 39 HRAppDisconnected / HRApp部件断开
    enCPSState_HRAppError = 40  # 40 HRAppError / HRApp部件错误
    # RobotLoadIdentify / 负载辨识
    enCPSState_RobotLoadIdentify = 41  # 41 RobotLoadIdentify / 负载辨识
    # brake / 抱闸
    enCPSState_Braking = 42  # 42 Braking / 开关抱闸中
    enCPSState_TemperatureTooLow = 43  # 43 TemperatureTooLow / 温度过低
    # FT / 力控
    enCPSState_FTOpeningFreeDriver = 44  # 44 FTOpeningFreeDriver / 机器人正在开启力控零力示教
    enCPSState_FTClosingFreeDriver = 45  # 45 FTClosingFreeDriver / 机器人正在关闭力控零力示教
    enCPSState_FTFreeDriver = 46  # 46 FTFreeDriver / 机器人处于力控零力示教


dic_ErrorCode = {
    39500: "NotConnected / 跟机器人连接未建立",
    39501: "ParamErrorInCommand / 命令输入参数错误",
    39502: "ParamErrorInResponse / 命令响应中参数错误",
    39503: "SocketCommError / Socket通讯错误(超时、接收异常等)",
    39504: "Connect2CPSFailed / 跟机器人连接错误",
    39505: "CmdErrorInResponse / 命令接收错误",
    20018: ""
}

import threading

lock = threading.Lock()
lock_fast = threading.Lock()


class RbtClient(object):
    clientIP = '127.0.0.1'
    clientPort = 10003
    output_log = False

    def __init__(self):
        self.fast_cmd_list = []
        self.hb_thread = None
        self.tcp = None
        self.tcp_fast = None
        self.fast_port = None
        self.lock = threading.Lock()
        self.lock_fast = threading.Lock()
        self.stop_heartbeat = False

    def _send_and_recv(self, tcp_socket, cmd, timeout=10):
        """General send and receive methods for handling data transmission, including timeout control."""
        """通用的发送和接收方法，处理数据的发送和接收，包含超时控制。"""
        tcp_socket.send(cmd.encode())
        count = 0
        ret = ""
        tcp_socket.settimeout(timeout)
        while count < 5:
            count += 1
            try:
                data = tcp_socket.recv(4096).decode("utf-8", "ignore")
                if self.output_log:
                    print(data)
                if data:
                    ret += data
                    if ret.endswith(';'):
                        break
            except socket.timeout:
                continue  # Time Retry / 超时重试
        else:
            # data recceive timeout / 接收数据超时
            raise TimeoutError("data recceive timeout.")
        return ret

    def heartbeat_thread(self):
        """Heartbeat thread, regularly check connection status"""
        """心跳线程，定期检查连接状态。"""
        result = []
        while not self.stop_heartbeat:
            nRet = self.sendAndRecv('IsSimulation,;', result)
            if nRet != 0:
                self.DisconnectFromCPS()
                break
            time.sleep(1)

    def Connect2CPS(self, hostName, nPort):
        """Connect to CPS and start the heartbeat thread, set the connection parameters."""
        """连接到CPS并启动心跳线程，设置连接参数。"""
        self.clientIP = hostName
        self.clientPort = nPort

        # create TCP connection / 创建 TCP 连接
        self.tcp = socket.socket()
        self.tcp.settimeout(5)
        ret = self.tcp.connect_ex((self.clientIP, self.clientPort))

        if ret != 0:
            self.tcp.close()
            print(f"connect error [error is {ret}.msg:{os.strerror(ret)}]")
            return ret

        # Start heartbeat thread (if not start) / 启动心跳线程（如果未启动）
        if not self.hb_thread:
            self.stop_heartbeat = False
            self.hb_thread = threading.Thread(target=self.heartbeat_thread, daemon=True)
            self.hb_thread.start()

        # Get fastport / 获取快速端口
        result = []
        nRet = self.sendAndRecv('ReadFastCmdPort,0,;', result)
        if nRet != 0:
            return ret

        self.fast_port = int(result[0])
        # Is the current connection a fastport / 当前连接的是否是快速端口
        if self.fast_port == self.clientPort:  
            return 0

        # Connect to fastport / 连接到快速端口
        self.tcp_fast = socket.socket()
        self.tcp_fast.settimeout(5)
        ret = self.tcp_fast.connect_ex((self.clientIP, self.fast_port))

        self.sendAndRecv_fast('ReadCmdList,0,;', self.fast_cmd_list)

        return ret

    def DisconnectFromCPS(self):
        """Disconnect and stop the heartbeat thread."""
        """断开连接，停止心跳线程。"""
        # End heartbeat thread using flag bit / 使用标志位结束心跳线程
        self.stop_heartbeat = True  

        if self.tcp:
            self.tcp.close()
            self.tcp = None

        if self.tcp_fast:
            self.tcp_fast.close()
            self.tcp_fast = None

        return 0

    def sendScriptFinish(self, errorCode):
        """"Send script completion information."""
        """发送脚本完成信息。"""
        command = f'SendScriptFinish,0,{errorCode},;'
        self.tcp.send(command.encode())
        self.tcp.recv(self.clientPort).decode("utf-8", "ignore")

    def setOutputLog(self, output):
        """"Set output log flag """
        """设置输出日志标志。"""
        self.output_log = output

    def sendAndRecv_fast(self, cmd, result):
        """Send and Receive(via fast port)."""
        """发送并接收数据（通过快速端口）。"""
        with self.lock_fast:
            try:
                ret = self._send_and_recv(self.tcp_fast, cmd)
                retData_fast = ret.split(',')
                if len(retData_fast) < 3 or retData_fast[0] == "errorcmd":
                    return 39503

                if retData_fast[1] == "Fail":
                    errorData = int(retData_fast[2])
                    return errorData

                if cmd.split(",")[0] != retData_fast[0]:
                    return 39505

                result.clear()
                result.extend(retData_fast[2:-1])  # Ignore the first two elements and the last element / 忽略前两个元素和最后一个元素
            except Exception as e:
                print(f"Exception:{e}")
                return 39503
        return 0

    def sendAndRecv(self, cmd, result):
        """Send and Recevie(via standard port)"""
        """发送并接收数据（通过标准端口）。"""
        if cmd.split(",")[0] in self.fast_cmd_list:
            return self.sendAndRecv_fast(cmd,result)
        with self.lock:
            try:
                ret = self._send_and_recv(self.tcp, cmd)
                retData = ret.split(',')
                if len(retData) < 3 or retData[0] == "errorcmd":
                    return 39503

                if retData[1] == "Fail":
                    errorData = int(retData[2])
                    return errorData

                if cmd.split(",")[0] != retData[0]:
                    return 39505

                result.clear()
                result.extend(retData[2:-1])  # Ignore the first two elements and the last element / 忽略前两个元素和最后一个元素
            except Exception as e:
                print(f"Exception: {e}")
                return 39503
        return 0

class PluginClient(object):
    # for v8 plugin
    clientIP = '127.0.0.1'
    clientPort = 40005
    plugin_lock = threading.Lock()

    def __init__(self):
        self.tcp = None

    def Connect2Plugin(self, hostName):
        self.clientIP = hostName
        self.tcp = socket.socket()
        self.tcp.settimeout(2)
        ret = self.tcp.connect_ex((self.clientIP, self.clientPort))

        if ret != 0:
            self.tcp.close()
            print("connect error [error is {0}.msg:{1}]".format(ret, os.strerror(ret)))
            return ret

        return ret

    def DisconnectFromPlugin(self):
        self.tcp.close()
        self.tcp = None
        return 0

    def sendAndRecv(self, cmd, result):
        try:
            with self.plugin_lock:
                self.tcp.send(cmd.encode())
                count = 0
                ret = ""
                self.tcp.settimeout(10)  # Set the receive timeout to 10 seconds and attempt to receive 6 times / 设置接收超时时间为 10 秒，尝试接收 6 次
                while count < 6:
                    count += 1
                    try:
                        data = self.tcp.recv(4096).decode("utf-8", "ignore")
                        if data:
                            ret += data
                            if ret.endswith(';'):
                                break
                    except socket.timeout:
                        continue  # Time Retry / 超时重试
                else:
                    raise TimeoutError("receive data timeout")

            retData = ret.split(',')

            if retData[1] == "Fail":
                errorData = int(retData[2])
                return errorData

            # ensure result is a list / 确保 result 是一个列表
            if not isinstance(result, list):
                raise TypeError("result should a list")

            if cmd.split(",")[0] != retData[0]:
                return 39505

            # Process returned data / 处理返回数据
            result.clear()
            result.extend(retData[2:-1])  # Ignore the first two elements and the last element / 忽略前两个元素和最后一个元素

        except Exception as e:
            print("Exception:", e)
            return 39503
        return 0

class CPSClient(object):
    clientIP = '127.0.0.1'
    clientPort = 10003
    g_clients = []
    g_plugin_clients = []
    MaxBox = 5
    g_client_state = [False, False, False, False, False]
    g_plugin_client_state = [False, False, False, False, False]
    isV8CPS = False
    g_lock = threading.Lock()

    dic_FSM = {
        0: "PreInitialize / 未初始化",
        1: "Initialize / 初始化",
        2: "ElectricBoxDisconnect / 与电箱控制板断开",
        3: "ElectricBoxConnecting / 连接电箱控制板",
        4: "EmergencyStopHandling / 急停处理中",
        5: "EmergencyStop / 急停",
        6: "Blackouting48V / 正在切断本体供电",
        7: "Blackout48V / 本体供电已切断",
        8: "Electrifying48V / 正在准备给本体供电",
        9: "SafetyGuardErrorHandling / 安全光幕错误处理中",
        10: "SafetyGuardError / 安全光幕错误",
        11: "SafetyGuardHandling / 安全光幕处理中",
        12: "SafetyGuard / 安全光幕",
        13: "ControllerDisconnecting / 正在反初始化控制器",
        14: "ControllerDisconnect / 控制器已处于未初始化状态",
        15: "ControllerConnecting / 正在初始化控制器",
        16: "ControllerVersionError / 控制器版本过低错误",
        17: "EtherCATError / EtherCAT错误",
        18: "ControllerChecking / 控制器初始化后检查",
        19: "Reseting / 正在复位机器人",
        20: "RobotOutofSafeSpace / 机器人超出安全空间",
        21: "RobotCollisionStop / 机器人安全碰撞停车",
        22: "Error / 机器人错误",
        23: "Enabling / 机器人使能中",
        24: "Disable / 机器人去使能",
        25: "Moving / 机器人运动中",
        26: "LongJogMoving / 机器人长点动运动中",
        27: "RobotStopping / 机器人停止运动中",
        28: "Disabling / 机器人去使能中",
        29: "RobotOpeningFreeDriver / 机器人正在开启零力示教",
        30: "RobotClosingFreeDriver / 机器人正在关闭零力示教",
        31: "FreeDriver / 机器人处于零力示教",
        32: "RobotHolding / 机器人暂停",
        33: "StandBy / 机器人准备就绪",
        34: "ScriptRunning / 脚本运行中",
        35: "ScriptHoldHandling / 脚本暂停处理中",
        36: "ScriptHolding / 脚本暂停",
        37: "ScriptStopping / 脚本停止中",
        38: "ScriptStopped / 脚本已停止",
        39: "HRAppDisconnected / HRApp部件断开",
        40: "HRAppError / HRApp部件错误",
        41: "RobotLoadIdentify / 负载辨识",
        42: "Braking / 开关抱闸中",
        43: "TemperatureTooLow / 温度过低",
        44: "FTOpeningFreeDriver / 机器人正在开启力控零力示教",
        45: "FTClosingFreeDriver / 机器人正在关闭力控零力示教",
        46: "FTFreeDriver / 机器人处于力控零力示教"
    }

    def __init__(self):
        with self.g_lock:
            if len(self.g_clients) == self.MaxBox:
                return
            for i in range(self.MaxBox):
                self.g_clients.append(RbtClient())
                self.g_plugin_clients.append(PluginClient())
            return

    def _waitMotion(self, isblending):
        motionIndex = 0
        doneFlag = '0'
        movingFlag = '1'
        if isblending:
            motionIndex = 11
            doneFlag = '1'
            movingFlag = '0'

        time.sleep(0.02)
        nDisableCNT = 0
        while True:
            if nDisableCNT >= 5:
                time.sleep(0.01)
                os._exit(0)
            ret = []
            self.HRIF_ReadRobotState(0, 0, ret)
            if ret[1] == '0':
                nDisableCNT += 1
                log = ('[script]EnableState[' + ret[2] + '],count[' + str(nDisableCNT) + '] error')
                continue
            else:
                nDisableCNT = 0

            if ret[2] == '1' or ret[7] == '1' or ret[9] == '0' or ret[10] == '0':
                log = ('[script]errorState[' + ret[2] + '],emergency[' + ret[7] + '],Electfify[' + ret[9] + ']')
                # print(log)
                time.sleep(0.1)
                os._exit(0)
            elif ret[8] == '1':
                time.sleep(0.01)
                continue

            elif ret[6] == '1':
                time.sleep(0.01)
                continue

            elif ret[motionIndex] == doneFlag:
                log = ('[script]ret[' + str(motionIndex) + ']==' + ret[motionIndex])
                # print(log)
                break

            elif ret[motionIndex] == movingFlag:
                log = ('ret[' + str(motionIndex) + ']==' + ret[motionIndex])
                time.sleep(0.01)
                continue

            else:
                log = '[script]waitBlendingDone unknow status exit'
                # print(log)
                os._exit(0)
        return

    def waitMoveDone(self, boxID, rbtID):
        self._waitMotion(False)

    def waitBlendingDone(self, boxID, rbtID):
        self._waitMotion(True)

    def waitFSM(self, targetFSM, wait_timeout):
        result = []
        self.HRIF_ReadCurFSM(0, 0, result)
        start = time.perf_counter()
        end = time.perf_counter()
        if not result:
            return -1
        while int(result[0]) != targetFSM:
            end = time.perf_counter()
            if (end - start) >= wait_timeout:
                break
            time.sleep(0.1)
            self.HRIF_ReadCurFSM(0, 0, result)
        return int(result[0])

    def HRIF_FinishInitialize(self):
        result = []
        command = 'FinishInitialize,;'
        return self.g_clients[0].sendAndRecv(command, result)

    def HRIF_SetOutputLog(self, output):
        self.g_clients[0].setOutputLog(output)

    def HRIF_ReadFastCmdPort(self, result):
        command = 'ReadFastCmdPort,0,;'
        return self.g_clients[0].sendAndRecv(command, result)

    def HRIF_ReadCmdList(self, result):
        command = 'ReadCmdList,0,;'
        return self.g_clients[0].sendAndRecv_fast(command, result)

    def IsHRAppCmdExist(self):
        result = []
        command = 'IsHRAppCmdExist,0,;'
        return self.g_clients[0].sendAndRecv(command, result)

    #
    # part 1 Interfaces for initialization / 初始化函数接口
    #

    '''
    *	@index : 1
    *	@param brief: Connect to the robot server / 连接机器人服务器
    *	@param boxID: Control box ID / 电箱ID号
    *   @param hostName : IP address of CPS / 控制器IP地址，根据实际设置的IP地址定义
    *	@param nPort : Port number / 控制器端口号
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_Connect(self, boxID, hostName, nPort):
        if boxID >= self.MaxBox:
            return 39501
        try:
            ret = self.g_clients[boxID].Connect2CPS(hostName, nPort)
            if ret != 0:
                return 39504
            self.g_client_state[boxID] = True

            ret = self.IsHRAppCmdExist()
            if ret != 0:
                return 0
            self.isV8CPS = True
            plugin_ret = self.g_plugin_clients[boxID].Connect2Plugin(hostName)

            if plugin_ret == 0:
                self.g_plugin_client_state[boxID] = True
            else:
                print("Connect to plugin server failed!")
            return 0
        except:
            return 39504

    '''
    *	@index : 2
    *	@param brief:Disconnet from robot server / 断开连接机器人服务器
    *	@param boxID: Control box ID / 电箱ID号
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_DisConnect(self, boxID):
        if boxID >= self.MaxBox:
            return 39501
        try:
            self.g_clients[boxID].DisconnectFromCPS()
            self.g_client_state[boxID] = False
            if self.isV8CPS:
                self.g_plugin_clients[boxID].DisconnectFromPlugin()
                self.g_plugin_client_state[boxID] = False
            return 0
        except:
            return 39504

    '''
    *	@index : 3
    *	@param brief: Check the connection status to CPS / 检查控制器连接状态
    *	@param boxID: Control box ID / 电箱ID号
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_IsConnected(self, boxID):
        return self.g_client_state[boxID]

    '''
    *	@index : 4
    *	@param brief: Power off the robot and shut down the system / 控制器断电(断开机器人供电，系统关机)
    *	@param boxID: Control box ID / 电箱ID号
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ShutdownRobot(self, boxID):
        result = []
        command = 'OSCmd,1,;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 5
    *	@param brief: Connect to control box / 连接控制器电箱
    *	@param boxID: Control box ID / 电箱ID号
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_Connect2Box(self, boxID):
        result = []
        command = 'ConnectToBox,;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 6
    *	@param brief: Power on the robot / 机器人上电
    *	@param boxID: Control box ID / 电箱ID号
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_Electrify(self, boxID):
        result = []
        command = 'Electrify,;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 7
    *	@param brief: Power off the robot / 机器人断电
    *	@param boxID: Control box ID / 电箱ID号
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_BlackOut(self, boxID):
        result = []
        command = 'BlackOut,;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 8
    *	@param brief: Connect to the controller, start master, initialize slave, configure and check paramters, finally switch to DISABLE state / 连接控制器，连接过程中会启动主站，初始化从站，配置参数，检查配置，完成后跳转到去使能状态
    *	@param boxID: Control box ID / 电箱ID号
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_Connect2Controller(self, boxID):
        result = []
        command = 'StartMaster,'
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 9
    *	@param brief: Check the simulation status / 设置机器人的模拟状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param state: status / 是否为模拟机器人
    *                     0:real mode / 真实机器人
    *                     1:simulated mode / 模拟机器人
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetSimulation(self, boxID, state):
        result = []
        command = 'SetSimulation,0,'
        command += str(state)
        command += ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 10
    *	@param brief: Check the simulation status / 是否为模拟机器人
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]: status / 是否为模拟机器人
    *                        0:real mode / 真实机器人
    *                        1:simulated mode / 模拟机器人
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_IsSimulateRobot(self, boxID, result):
        command = 'IsSimulation,;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 11
    *	@param brief: Check the controller's state / 控制器是否启动完成
    *	@param boxID: Control box ID / 电箱ID号
    *	@param result[0]: Start status/ 是否启动
    *	                     0 : not started / 未启动
    *                        1 : started / 启动
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_IsControllerStarted(self, boxID, result):
        command = 'ReadControllerState,'
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 12
    *	@param brief: Get explanation of error code / 获取错误码解释
    *	@param boxID: Control box ID / 电箱ID号
    *	@param nErrorCode: Error code / 错误码
    *	@param result[0]: Error code explanation / 错误码解释
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码解释
    '''
    def HRIF_GetErrorCodeStr(self, boxID, nErrorCode, result):
        command = 'GetErrorCodeStr,'
        command += str(nErrorCode) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 13
    *	@param brief: Read the version of robot / 读取控制器版本号
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]: Whole version / 整体版本号
    *	@param result[1]: CPS version / CPS版本 
    *	@param result[2]: Controller version / 控制器版本
    *	@param result[3]: Control box version / 电箱版本 
    *	@param result[4]: Firmware version of control board / 控制板固件版本
    *	@param result[5]: Firmware version of control board / 控制板固件版本
    *	@param result[6]: Algorithm version / 算法版本 
    *	@param result[7]: Firmware version / 固件版本 
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadVersion(self, boxID, rbtID, result):
        command = 'ReadVersion,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 14
    *	@param brief: Read the robot model / 读取机器人类型
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]: Robot model / 机器人类型
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadRobotModel(self, boxID, rbtID, result):
        command = 'ReadRobotModel,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    #
    # part 2 Interfaces for axis group control command / 轴组控制指令函数接口
    #

    '''
    *	@index : 1
    *	@param brief:  Enable the robot / 机器人使能
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GrpEnable(self, boxID, rbtID):
        result = []
        command = 'GrpPowerOn,'
        command += str(rbtID) + ',;'
        ret = self.g_clients[boxID].sendAndRecv(command, result)
        if ret == 20005:
            command = 'GrpEnable,'
            command += str(rbtID) + ',;'
            ret = self.g_clients[boxID].sendAndRecv(command, result)
        return ret


    '''
    *	@index : 2
    *	@param brief: Disable the robot / 机器人去使能
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GrpDisable(self, boxID, rbtID):
        result = []
        command = 'GrpPowerOff,'
        command += str(rbtID) + ',;'
        ret = self.g_clients[boxID].sendAndRecv(command, result)
        if ret == 20005:
            command = 'GrpDisable,'
            command += str(rbtID) + ',;'
            ret = self.g_clients[boxID].sendAndRecv(command, result)
        return ret

    '''
    *	@index : 3
    *	@param brief: Reset the robot / 机器人复位
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_GrpReset(self, boxID, rbtID):
        result = []
        command = 'GrpReset,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 4
    *	@param brief: Stop robot moving / 停止运动命令
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GrpStop(self, boxID, rbtID):
        result = []
        command = 'GrpStop,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 5
    *	@param brief: Pause robot moving / 暂停运动命令
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GrpInterrupt(self, boxID, rbtID):
        result = []
        command = 'GrpInterrupt,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 6
    *	@param brief: Continue robot moving after pause / 继续运动命令
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GrpContinue(self, boxID, rbtID):
        result = []
        command = 'GrpContinue,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 7
    *	@param brief: Close free driver / 关闭零力示教
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_GrpCloseFreeDriver(self, boxID, rbtID):
        result = []
        command = 'GrpCloseFreeDriver,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 8
    *	@param brief: Open free driver / 开启零力示教
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GrpOpenFreeDriver(self, boxID, rbtID):
        result = []
        command = 'GrpOpenFreeDriver,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 9
    *	@param brief: Open the brake / 松闸
    *	@param boxID: Control box ID / 电箱ID号
    *	@param nAxisID : Robot Axis ID, 0-5 / 轴ID
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    *	@param nAxisID[0]: Axis id / 轴ID
    '''
    def HRIF_OpenBrake(self, boxID, nAxisID):
        result = []
        command = 'OpenBrake,0,'
        command += str(nAxisID)
        command += ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 10
    *	@param brief: Close the brake / 抱闸
    *	@param boxID: Control box ID / 电箱ID号
    *	@param nAxisID : Robot Axis ID, 0-5 / 轴ID
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    *	@param nAxisID[0]: 轴ID
    '''
    def HRIF_CloseBrake(self, boxID, nAxisID):
        result = []
        command = 'CloseBrake,0,'
        command += str(nAxisID)
        command += ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 11
    *	@param brief: Read the brake status of each Axis / 读取各关节松/抱闸状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param result[0]~result[5] : Robot Axis status / 各关节轴状态，1：松闸，0：抱闸
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadBrakeStatus(self, boxID, result):
        command = 'ReadBrakeStatus,0,;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 12
    *	@param brief: Move to safe space / 移动到安全空间
    *	@param boxID: Control box ID / 电箱ID号
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_MoveToSS(self, boxID):
        result = []
        command = 'MoveToSS,0,;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 13
    *	@param brief:Enter or exit safeguard status by force to realize soft EStop(emergency stop). Move will be stopped. System can be reset after EStop is canceled. / 强制进入或者取消进入安全光幕状态，以此方式实现软件急停，以及软急停后的恢复。强制进入安全光幕状态后，当前的运动会被停止掉。需要先取消强制，然后才能复位系统。
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID : Robot ID / 机器人ID号
    *	@param flag: 1 to enter, 0 to cancel / 1: 强制进入安全光幕状态；0: 取消强制进入安全光幕状态  
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_EnterSafeGuard(self, boxID, rbtID, flag):
        result = []
        command = 'EnterSafetyGuard,'
        command += str(rbtID) + ','
        command += str(flag) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 14
    *	@param brief: Read whether the three-stage switch is turned on and the mode / 读取三段式开关是否开启以及模式
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID : Robot ID / 机器人ID号
    *	@param result[0]: Three stage switch  / 三段式按钮
    *                                                        0：colse/关闭
    *                                                        1：open/开启
    *	@param result[0]: Mode / 模式
    *                                                        0：FreeDrive/零力示教
    *                                                        1：Enable/使能
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadTriStageSwitch(self, boxID, rbtID, result):
        command = 'ReadTriStageSwitch,'
        command += str(rbtID) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 15
    *	@param brief: Set three-stage switch and mode / 设置三段式开关以及模式
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID : Robot ID / 机器人ID号
    *	@param enable : Three stage switch  / 三段式按钮
    *                                                              0：colse/关闭
    *                                                              1：open/开启
    *   @param mode : Mode / 模式
    *                                                              0：FreeDrive/零力示教
    *                                                              1：Enable/使能 
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetTriStageSwitch(self, boxID, rbtID, enable, mode):
        result = []
        command = 'SetTriStageSwitch,'
        command += str(rbtID) + ','
        command += str(enable) + ','
        command += str(mode) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 16
    *	@param brief: Z-axis alignment / Z轴对齐 
    *	@param boxID : Control box ID / 电箱ID号
    *	@param rbtID : Robot ID / 机器人ID号
    *	@param tcp : Tcp Name  / 工具坐标系的名称
    *   @param ucs : Ucs Name / 用户坐标系的名称
    *   @param result[0] : Is the Z-axis aligned  / Z轴是否已经对齐
    *   @param result[1]-result[6] : J1-J6 Joint Position / J1到J6轴的关节位置 
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_MoveAlignToZ(self, boxID, rbtID, tcp, ucs, result):
        command = 'MoveAlignToZ,'
        command += str(rbtID) + ','
        command += str(tcp) + ','
        command += str(ucs) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 17
    *	@param brief: Start Load Identification. / 开始负载识别
    *	@param boxID : Control box ID / 电箱ID号
    *	@param rbtID : Robot ID / 机器人ID号
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_LoadIdentify(self, boxID, rbtID):
        result = []
        command = 'LoadIdentify,'
        command += str(rbtID) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 18
    *	@param brief: Get the load identification result / 获取负载辨识结果
    *	@param boxID : Control box ID / 电箱ID号
    *	@param rbtID : Robot ID / 机器人ID号
    *   @param result[0] : Load identification status: / 负载辨识状态
    *                    - 0: Success / 成功
    *                    - 1: First trajectory error / 第一条轨迹错误
    *                    - 2: Second trajectory error / 第二条轨迹错误
    *                    - 3: Third trajectory error / 第三条轨迹错误
    *                    - 4: Load identification in progress / 负载辨识运行中
    *                    - 5: Unexpected stop / 意外停止
    *                    - 6: Unexpected exit / 意外退出
    *                    - 7: Initialization, load identification not started / 初始化，负载辨识未开始
    *   @param result[1]: Progress status (0~100)(Current load identification progress)/ 进度状态 - 当前负载识别进度
    *                 
    *   @param result[2] : Identified load mass (unit: kg) / 负载质量,Kg
    *   @param result[3] :Load center of mass X coordinate / 质心X坐标
    *   @param result[4] :Load center of mass Y coordinate / 质心Y坐标
    *   @param result[5] : Load center of mass Z coordinate / 质心Z坐标
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GetLoadIdentifyResult(self, boxID, rbtID, result):
        command = 'GetLoadIdentifyResult,'
        command += str(rbtID) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    #
    # part 3 Interfaces for script / 脚本控制函数接口
    #

    '''
    *	@index : 1
    *	@param brief: Run the specified function / 运行指定脚本函数
    *	@param boxID: Control box ID / 电箱ID号
    *	@param strFuncName : The specified function name composed in the teaching pendant / 指定脚本函数名称，对应示教器界面的函数
    *	@param param : Parameters / 参数
    *	@param result[0] : Function Name / 函数名
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_RunFunc(self, boxID, funcName, params, result):
        command = 'RunFunc,'
        command += funcName + ','
        for param in params:
            command += str(param) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 2
    *	@param brief: Run the main function to start the script execution composed and compiled in the teaching pendant / 执行脚本Main函数，调用后执行示教器页面编译好的脚本文件
    *	@param boxID: Control box ID / 电箱ID号
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_StartScript(self, boxID):
        result = []
        command = 'StartScript,;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 3
    *	@param brief: Stop the script execution running in teaching pendant / 停止脚本，调用后停止示教器页面正在执行脚本文件
    *	@param boxID: Control box ID / 电箱ID号
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_StopScript(self, boxID):
        result = []
        command = 'StopScript,;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 4
    *	@param brief: Pause the script execution running in teaching pendant / 暂停脚本，调用后暂停示教器页面正在执行脚本文件
    *	@param boxID: Control box ID / 电箱ID号
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_PauseScript(self, boxID):
        result = []
        command = 'PauseScript,;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 5
    *	@param brief: Continue the script execution paused int the teaching pendant / 继续脚本，调用后继续运行示教器页面正在暂停的脚本文件，不处于暂停状态则返回20018错误
    *	@param boxID: Control box ID / 电箱ID号
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ContinueScript(self, boxID):
        result = []
        command = 'ContinueScript,;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 6
    *	@param brief: Applies the specified script file / 应用指定的脚本文件
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID号
    *	@param name: ScriptName / 脚本的名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SwitchScript(self, boxID, rbtID, name):
        result = []
        command = 'SwitchScript,'
        command += str(rbtID) + ','
        command += name +',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 7
    *	@param brief: Read the current application script file / 读取当前应用脚本文件
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID号
    *	@param result[0]: ScriptName / 当前应用的脚本名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadDefaultScript(self, boxID, rbtID, result):
        command = 'ReadDefaultScript,'
        command += str(rbtID) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    #
    # part 4  Interfaces for control box / 电箱控制函数接口
    #

    '''
    *	@index : 1
    *	@param brief: Read box message / 读取电箱信息
    *	@param boxID: Control box ID / 电箱ID号
    *	@param result[0] : Control box connection status / 电箱连接状态
    *	@param result[1] : Voltage value with 48V / 48V电压值
    *	@param result[2] : 48V output voltage / 48V输出电压值
    *	@param result[3] : 48V output current / 48V输出电流值
    *	@param result[4] : Remote emergency stop status / 远程急停状态
    *	@param result[5] : Three stage status / 三段按钮状态
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadBoxInfo(self, boxID, result):
        command = 'ReadBoxInfo,;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index: 2  Read box control input / 读取电箱控制数字输入状态读取电箱控制数字输入状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param bit: CI bit / 控制数字输入位
    *	@param result[0]: CI value / 数字输入状态
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadBoxCI(self, boxID, bit, result):
        command = 'ReadBoxCI,' + str(bit) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 3
    *	@param brief: Read box digital input / 读取电箱通用数字输入状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param bit : DI bit / 通用数字输入位
    *	@param result[0]: DI value / 通用数字输入状态
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码 
    '''
    def HRIF_ReadBoxDI(self, boxID, bit, result):
        command = 'ReadBoxDI,' + str(bit) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 4
    *	@param brief: Read box control output / 读取电箱控制器数字输出状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param bit : CO bit / 控制器数字输出位
    *	@param result[0]: CO valur / 数字输出状态
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadBoxCO(self, boxID, bit, result):
        command = 'ReadBoxCO,' + str(bit) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 5
    *	@param brief: Read box digital output / 读取电箱通用数字输出状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param bit : DO bit / 通用数字输出位
    *	@param result[0]: DO value / 通用数字输出状态
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadBoxDO(self, boxID, bit, result):
        command = 'ReadBoxDO,' + str(bit) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 6
    *	@param brief: Read all control box config digital input statuses / 读取电箱所有的控制数字输入状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param result[0]-result[5]: Vector storing all config input (CI) values / 存储所有可配置数字输入(CI)状态的向量
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadAllBoxCI(self, boxID,result):
        command = 'ReadBoxCI,'
        for i in range(8):
            command += str(i) +','
        command += ';'
        print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 7
    *	@param brief: Read all control box config digital input statuses / 读取电箱所有的控制数字输入状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param result[0]-result[5]: Vector storing all digital input (DI) values / 存储所有通用数字输入(DI)状态的向量
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''  
    def HRIF_ReadAllBoxDI(self, boxID,result):
        command = 'ReadBoxDI,'
        for i in range(8):
            command += str(i) +','
        command += ';'
        print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 8
    *	@param brief: Read all control box config digital output statuses / 读取电箱所有的可配置数字输出状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param result[0]-result[5]: Vector storing all config output (CO) values / 存储所有可配置数字输出(CO)状态的向量
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadAllBoxCO(self, boxID,result):
        command = 'ReadBoxCO,'
        for i in range(8):
            command += str(i) +','
        command += ';'
        print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 9
    *	@param brief: Read all control box general digital output statuses / 读取电箱所有的通用数字输出状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param result[0]-result[5]: Vector storing all digital output (DO) values / 存储所有通用数字输出(DO)状态的向量
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadAllBoxDO(self, boxID,result):
        command = 'ReadBoxDO,'
        for i in range(8):
            command += str(i) +','
        command += ';'
        print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 10
    *	@param brief: Read box analog input / 读取电箱模拟量输入值
    *	@param boxID: Control box ID / 电箱ID号
    *	@param bit : AI bit / 模拟量输入位
    *	@param result[0] : Current (4~20mA) or voltage (0~10V) / 电流模式:4-20mA,电压模式:0-10V
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadBoxAI(self, boxID, bit, result):
        command = 'ReadBoxAI,' + str(bit) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 11
    *	@param brief: Read box analog output / 读取电箱模拟量输出模式和值
    *	@param boxID: Control box ID / 电箱ID号
    *	@param bit : AO bit / 模拟量输出位
    *	@param result[0] : Current or voltage mode / 对应位模拟量通道模式 1:电压 2:电流
    *	@param result[1] :  Current value (4~20mA) or voltage value (0~10V) / 电流模式:4-20mA,电压模式:0-10V
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadBoxAO(self, boxID, bit, result):
        command = 'ReadBoxAO,' + str(bit) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 12
    *	@param brief: Set Box control output / 设置控制数字输出状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param bit : CO bit / 控制数字输出位
    *	@param state : CO value / 控制器数字输出目标状态
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetBoxCO(self, boxID, bit, state):
        result = []
        command = 'SetBoxCO,' + str(bit) + ',' + str(state) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 13
    *	@param brief: Set Box digital output / 设置电箱通用数字输出状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param bit : DO / 通用数字输出位
    *	@param state :  DO value / 通用数字输出目标状态
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetBoxDO(self, boxID, bit, state):
        result = []
        command = 'SetBoxDO,' + str(bit) + ',' + str(state) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 14
    *	@param brief: Set Box analog output mode / 设置电箱模拟量输出模式
    *	@param boxID: Control box ID / 电箱ID号
    *	@param bit : AO bit / 模拟量输出模式通道
    *	@param pattern : AO Mode / 模拟量输出模式,1:电压,2:电流
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetBoxAOMode(self, boxID, index, pattern):
        result = []
        command = 'SetBoxAOMode,' + str(index) + ',' + str(pattern) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 15
    *	@param brief:Set Box analog output and mode / 设置电箱模拟量输出值和模式
    *	@param boxID: Control box ID / 电箱ID号
    *	@param bit : AO bit / 模拟量输出位
    *	@param value : AO value / 模拟量输出值
    *	@param pattern : AO mode / 模拟量输出模式,1:电压,2:电流
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetBoxAOVal(self, boxID, index, value, pattern):
        result = []
        command = 'SetBoxAO,' + str(index) + ',' + str(value) + ',' + str(pattern) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 16
    *	@param brief: Set End digital output / 设置末端数字输出状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param bit : End DO bit / 末端数字输出位
    *	@param state : End DO value / 末端数字输出值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetEndDO(self, boxID, rbtID, bit, state):
        result = []
        command = 'SetEndDO,'
        command += str(rbtID) + ','
        command += str(bit) + ','
        command += str(state) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 17
    *	@param brief: Set welding analog output voltage / 设置焊接模拟量输出电压
    *	@param boxID: Control box ID / 电箱ID号
    *	@param nState : Channel switch status / 通道开关状态 0：关闭 1：开启
    *	@param nIndex : Voltage analog channel / 电压模拟量通道，AO0和AO1
    *	@param dInitAO : Initial voltage / 初始化电压
    *	@param dWeldingAO : Welding voltage / 焊接电压，单位：V
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetMoveParamsAO(self, boxID, nState, nIndex, dInitAO, dWeldingAO):
        result = []
        command = 'SetMoveParamsAO,0,'
        command += str(nState) + ','
        command += str(nIndex) + ','
        command += str(dInitAO) + ','
        command += str(dWeldingAO) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 18
    *	@param brief: Read End digital input / 读取末端数字输入状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param bit :  End DI bit/ 末端输入位
    *	@param result[0] : End DI value / 末端输入值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadEndDI(self, boxID, rbtID, bit, result):
        command = 'ReadEI,'
        command += str(rbtID) + ','
        command += str(bit) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 19
    *	@param brief: Read End digital output / 读取末端数字输出状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param bit : End DO bit / 末端数字输出位
    *	@param result[0] : End DO value / 末端数字输出值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadEndDO(self, boxID, rbtID, bit, result):
        command = 'ReadEO,'
        command += str(rbtID) + ','
        command += str(bit) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 20
    *	@param brief: Read End analog input / 读取末端模拟量输入状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param bit : End AI bit / 末端模拟量输入位
    *	@param result[0] : End AI value / 末端模拟量输入值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadEndAI(self, boxID, rbtID, bit, result):
        command = 'ReadEAI,'
        command += str(rbtID) + ','
        command += str(bit) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 21
    *	@param brief: Read End Button / 读取末端按键状态，根据搭载的末端类型，各状态表示含义会有区别
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0] : End button 1 / 末端按键1状态
    *	@param result[1] : End button 2 / 末端按键2状态
    *	@param result[2] : End button 3 / 末端按键3状态
    *	@param result[3] : End button 4 / 末端按键4状态
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadEndBTN(self, boxID, rbtID, result):
        command = 'ReadEndBTN,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 22
    *	@param brief: Set End Button / 设置末端按键状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param state : End button status, 1 for enabled, 0 for enabled / 末端按键启用开关, 1: 启用, 0: 禁用
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_EnableEndBTN(self, boxID, rbtID, state):
        result = []
        command = 'EnableEndBTN,'
        command += str(rbtID) + ','
        command += str(state) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    #
    # part 5  Interfaces for read state and set command / 读取与设置函数接口
    #

    '''
    *	@index : 1
    *	@param brief: Set Override / 设置速度比
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param vel: Override value (0.01~1.00) / 需要设置的速度比(0.01-1)
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetOverride(self, boxID, rbtID, vel):
        result = []
        command = 'SetOverride,'
        command += str(rbtID) + ','
        command += str(vel) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 2
    *	@param brief: Set Tool motion / 开启或关闭 Tool 坐标系运动模式
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param state: 0 for closed, 1 for open / 0(关闭)/1(开启)
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetToolMotion(self, boxID, rbtID, state):
        result = []
        command = 'SetToolMotion,'
        command += str(rbtID) + ','
        command += str(state) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 3
    *	@param brief: Set payload / 设置当前负载参数
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param Mass:Mass / 质量
    *	@param Center_X: Gravity-CX / 质心X方向偏移
    *	@param Center_Y: Gravity-CY / 质心Y方向偏移
    *	@param Center_Z: Gravity-CZ / 质心Z方向偏移
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    ''' 
    def HRIF_SetPayload(self, boxID, rbtID, Mass, Center_X, Center_Y, Center_Z):
        result = []
        command = 'SetPayload,'
        command += str(rbtID) + ','
        command += str(Mass) + ','
        command += str(Center_X) + ','
        command += str(Center_Y) + ','
        command += str(Center_Z) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 4
    *	@param brief: Set joint max velocity / 设置关节最大运动速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param Joint[0]-Joint[5]: Joint1~6 max velocity / J1-J6轴最大速度，单位[°/ s]
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetJointMaxVel(self, boxID, rbtID, Joint):
        result = []
        command = 'SetJointMaxVel,'
        command += str(rbtID) + ','
        for i in range(len(Joint)):
            command += str(Joint[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 5
    *	@param brief: Set joint max velocity / 设置关节最大运动速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param Joint[0]-Joint[n-1]: Joint1~n max velocity / J1-Jn轴最大速度，单位[°/ s]
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetJointMaxVel_nJ(self, boxID, rbtID, Joint):
        result = []
        command = 'SetJointMaxVel,'
        command += str(rbtID) + ','
        for i in range(len(Joint)):
            command += str(Joint[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 6
    *	@param brief: Set joint max acceleration / 设置关节最大运动加速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param Joint[0]-Joint[5]: Joint1~6 max acceleration /J1-J6轴轴最大加速度，单位[°/ s^2]
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetJointMaxAcc(self, boxID, rbtID, Joint):
        result = []
        command = 'SetJointMaxAcc,'
        command += str(rbtID) + ','
        for i in range(len(Joint)):
            command += str(Joint[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 7
    *	@param brief: Set joint max acceleration / 设置关节最大运动加速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param Joint[0]-Joint[n-1]: Joint1~n max acceleration /J1-Jn轴轴最大加速度，单位[°/ s^2]
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetJointMaxAcc_nJ(self, boxID, rbtID, Joint):
        result = []
        command = 'SetJointMaxAcc,'
        command += str(rbtID) + ','
        for i in range(len(Joint)):
            command += str(Joint[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 8
    *	@param brief: Set linear max velocity / 设置直线运动最大速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param MaxVel: Linear max velocity / 直线运动最大速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetLinearMaxVel(self, boxID, rbtID, MaxVel):
        result = []
        command = 'SetLinearMaxVel,'
        command += str(rbtID) + ','
        command += str(MaxVel) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 9
    *	@param brief:Set linear max acceleration / 设置直线运动最大加速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param MaxAcc: Linear max acceleration / 直线运动最大加速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetLinearMaxAcc(self, boxID, rbtID, MaxAcc):
        result = []
        command = 'SetLinearMaxAcc,'
        command += str(rbtID) + ','
        command += str(MaxAcc) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 10
    *	@param brief: Set max range of joint motion / 设置最大关节运动范围
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param pMax[0]-pMax[5]: Max joint angle / 最大关节角度
    *	@param pMin[0]-pMin[5]: Min joint angle /最小关节角度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetMaxAcsRange(self, boxID, rbtID, pMax, pMin):
        result = []
        command = 'SetMaxAcsRange,'
        command += str(rbtID) + ','
        for i in range(len(pMax)):
            command += str(pMax[i]) + ','
        for i in range(len(pMin)):
            command += str(pMin[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 11
    *	@param brief: Set max range of joint motion / 设置最大关节运动范围
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param pMax[0]-pMax[n-1]: Max joint angle / 最大关节角度
    *	@param pMin[0]-pMin[n-1]: Min joint angle /最小关节角度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetMaxAcsRange_nJ(self, boxID, rbtID, pMax, pMin):
        result = []
        command = 'SetMaxAcsRange,'
        command += str(rbtID) + ','
        for i in range(len(pMax)):
            command += str(pMax[i]) + ','
        for i in range(len(pMin)):
            command += str(pMin[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 12
    *	@param brief: Set max range of linear motion / 设置空间最大运动范围
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param pMax:  Max range of XYZ / X,Y,Z最大范围
    *	@param pMin:  Min range of XYZ / X,Y,Z最小范围
    *	@param pUcs:  UCS pose / 基于用户坐标
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetMaxPcsRange(self, boxID, rbtID, pMax, pMin, pUcs):
        result = []
        command = 'SetMaxPcsRange,'
        command += str(rbtID) + ','
        for i in range(3):
            command += str(pMax[i]) + ','
        command += str(180)
        command += ','
        command += str(180)
        command += ','
        command += str(180)
        command += ','
        for i in range(3):
            command += str(pMin[i]) + ','
        command += str(-180)
        command += ','
        command += str(-180)
        command += ','
        command += str(-180)
        command += ','
        for i in range(0, 6):
            command += str(pUcs[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 13
    *	@param brief: Read joint range and linear range / 读取关节范围和空间范围
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5]: Max joint angle / 最大关节角度
    *	@param result[6]-result[11]: Min joint angle /最小关节角度
    *	@param result[12]-result[17]: Max range of XYZRXRYRZ / XYZ、RXRYRZ最大范围
    *	@param result[18]-result[23]: Min range of XYZRXRYRZ / XYZ、RXRYRZ最小范围
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadMaxRange(self,  boxID, rbtID, result):
        command = 'ReadMaxRange,'
        command += str(rbtID) +','
        command += ';'
        print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 14
    *	@param brief: Read joint range and linear range / 读取关节范围和空间范围
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[n-1]: Max joint angle / 最大关节角度
    *	@param result[n]-result[2n-1]: Min joint angle /最小关节角度
    *	@param result[2n]-result[3n-1]: Max linear range / 最大空间范围
    *	@param result[3n]-result[4n-1]: Min linear range / 最小空间范围
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadMaxRange_nJ(self,  boxID, rbtID, result):
        command = 'ReadMaxRange,'
        command += str(rbtID) +','
        command += ';'
        print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 15
    *	@param brief: set the collision sensitivity level / 设置碰撞安全等级
    *	@param boxID: Control box ID / 电箱ID号
    *	@param nSafeLevel : sensitivity level, 0-5, 0 for the highest, 5 for the lowest / 安全等级(0-5) 0：高限制，安全系数高  5：低限制，高风险
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetCollideLevel(self, boxID, nSafeLevel):
        result = []
        command = 'SetCollideLevel,0,' + str(nSafeLevel) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 16
    *	@param brief: Read the maximum payload / 读取末端最大负载
    *	@param boxID: Control box ID / 电箱ID号
    *	@param result : maximum payload at the end (kg) / 末端最大负载，单位：kg
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadMaxPayload(self, boxID, result):
        command = 'ReadMaxPayload,0,;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 17
    *	@param brief: Read payload / 读取当前负载参数
    *	@param boxID: Control box ID / 电箱ID号
    *	@param result[0]: Mass / 质量
    *	@param result[1]: Gravity-CX / 质心X方向偏移
    *	@param result[2]: Gravity-CY / 质心Y方向偏移
    *	@param result[3]: Gravity-CZ / 质心Z方向偏移
       *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadPayload(self, boxID, result):
        command = 'ReadPayload,0,;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 18
    *	@param brief: Read Override / 读取当前速度比
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]: Override value  / 读取到的速度比(0.01~1)
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadOverride(self, boxID, rbtID, result):
        command = 'ReadOverride,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 19
    *	@param brief: Read joint max velocity / 读取关节最大运动速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5]: Max velocity of J1~J6 / J1-J6轴最大运动速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadJointMaxVel(self, boxID, rbtID, result):
        command = 'ReadJointMaxVel,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 20
    *	@param brief: Read joint max velocity / 读取关节最大运动速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[n-1]: Max velocity of J1~Jn / J1-Jn轴最大运动速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *   
    '''
    def HRIF_ReadJointMaxVel_nJ(self, boxID, rbtID, result):
        command = 'ReadJointMaxVel,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 21
    *	@param brief: Read joint max acceleration / 读取关节最大运动加速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5] : Max acceleration of J1~J6 / J1-J6轴最大加速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadJointMaxAcc(self, boxID, rbtID, result):
        command = 'ReadJointMaxAcc,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 22
    *	@param brief: Read joint max acceleration / 读取关节最大运动加速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[n-1] : Max acceleration of J1~Jn / J1-Jn轴最大加速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadJointMaxAcc_nJ(self, boxID, rbtID, result):
        command = 'ReadJointMaxAcc,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 23
    *	@param brief: Read joint max jerk / 读取关节最大运动加加速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5] : Max jerk of J1~J6 / J1-J6轴最大加加速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadJointMaxJerk(self, boxID, rbtID, result):
        command = 'ReadJointMaxJerk,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 24
    *	@param brief: Read joint max jerk / 读取关节最大运动加加速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[n-1] : Max jerk of J1~Jn / J1-Jn轴最大加加速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadJointMaxJerk_nJ(self, boxID, rbtID, result):
        command = 'ReadJointMaxJerk,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 25
    *	@param brief: Read linear motion parameters /读取直线运动最大速度、加速度和加加速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0] : Linear motion velocity / 直线运动速度(单位[mm/ s])
    *	@param result[1] : Linear motion acceleration / 最大直线加速度(单位[mm/ s2])
    *	@param result[2] : Linear motion jerk / 最大直线加加速度(单位[mm/ s3])
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_ReadLinearMaxSpeed(self, boxID, rbtID, result):
        command = 'ReadLinearMaxVel,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 26
    *	@param brief:Read Emergency stop information / 读取急停信息
    *	@param boxID: Control box ID / 电箱ID号
    *	@param result[0] : Error occurs when the two emergency signals are different / 急停回路有两路，当两路信号不相同时，则认为急停回路有错误，这个则为1
    *	@param result[1] : Cut off 48V output to the robot when an emergency stop occurs / 急停信号，发生急停时，会断48V输出到本体的供电，但是不会断220V到48V的供电
    *	@param result[2] : Error occurs when the two safeguard signals are different / 安全光幕回路有两路，当两路信号不相同时，则认为安全光幕回路有错误，这个则为1
    *	@param result[3] : Stop the motion but never cutt off power supply when safeguard occurs / 安全光幕信号，发生安全光幕时，会停止机器人运动，并且不再接受运动指令，不会断本体供电
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_ReadEmergencyInfo(self, boxID, result):
        command = 'ReadEmergencyInfo,'
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 27
    *	@param brief: Read robot state / 读取当前机器人状态标志
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0] : Moving state / 运动状态
    *   @param result[1] : Enable state / 使能状态
    *   @param result[2] : Error state / 错误状态
    *   @param result[3] : Error code / 错误码
    *   @param result[4] : Error axis ID / 错误轴ID
    *   @param result[5] : Breaking status / 抱闸是否打开状态
    *   @param result[6] : Pause state /暂停状态
    *   @param result[7] : Emergency stop state /急停状态
    *   @param result[8] : Safty guard state / 安全光幕状态
    *   @param result[9] : Electrify state / 上电状态
    *   @param result[10] : Connection of control box state / 连接电箱状态
    *   @param result[11] : Moving blending done state / WayPoint运动完成状态
    *   @param result[12] : In actual pose state / 运动命令位置与实际位置是否到位
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_ReadRobotState(self, boxID, rbtID, result):
        command = 'ReadRobotState,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 28
    *	@param brief: Read current waypoint ID / 读取WayPoint当前运动ID号
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]: Current ID / 当前 ID
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadCurWaypointID(self, boxID, rbtID, result):
        command = 'ReadCurWayPointID,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 29
    *	@param brief: Read axis error code / 读取错误码
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *   @param result[0]: Error code / 错误码
    *	@param result[1]-result[5] : The error code of J1~J6, 0 if no error / 每个轴(J1~J6)的错误码，如果没有错误则为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadAxisErrorCode(self, boxID, rbtID, result):
        command = 'ReadAxisErrorCode,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 30
    *	@param brief: Read axis error code / 读取错误码
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *   @param result[0]: Error code / 错误码
    *	@param result[1]-result[n] : The error code of J1~Jn, 0 if no error / 每个轴(J1~Jn)的错误码，如果没有错误则为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadAxisErrorCode_nJ(self, boxID, rbtID, result):
        command = 'ReadAxisErrorCode,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 31
    *	@param brief: Read current FSM / 读取状态机状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0] : Current FSM / 当前状态机状态,具体描述见接口说明文档
    *	@param result[1] : FSM description / 状态机描述
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadCurFSM(self, boxID, rbtID, result):
        command = 'ReadCurFSM,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
      *	@index : 32
      *	@param brief: Read point pose, joint positions, UCS and TCP by point name / 根据点位名称读取点位信息
      *	@param boxID: Control box ID / 电箱ID号
      *	@param rbtID: Robot ID / 机器人ID,一般为0
      *	@param pointName: Point name / 点位名称
      *	@param result[0]-result[5] : joint positions / 关节坐标
      *	@param result[6]-result[11] : pose / 笛卡尔坐标
      *	@param result[12]-result[17] : TCP pose / 当前工具坐标
      *	@param result[18]-result[23] : UCS pose / 当前用户坐标
      *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadPointByName(self, boxID, rbtID, pointName, result):
        command = 'ReadPointByName,'
        command += str(rbtID) + ','
        command += pointName + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
      *	@index : 33
      *	@param brief: Read point pose, joint positions, UCS and TCP by point name / 根据点位名称读取点位信息
      *	@param boxID: Control box ID / 电箱ID号
      *	@param rbtID: Robot ID / 机器人ID,一般为0
      *	@param pointName: Point name / 点位名称
      *	@param result[0]-result[n-1]: joint positions / 关节坐标
      *	@param result[n]-result[2n-1]: pose / 笛卡尔坐标
      *	@param result[2n]-result[3n-1]: TCP pose / 当前工具坐标
      *	@param result[3n]-result[4n-1]: UCS pose / 当前用户坐标
      *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadPointByName_nJ(self, boxID, rbtID, pointName, result):
        command = 'ReadPointByName,'
        command += str(rbtID) + ','
        command += pointName + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
      *	@index : 34
      *	@param brief: Read FSM from CPS / 读取当前状态机
      *	@param boxID: Control box ID / 电箱ID号
      *	@param rbtID: Robot ID / 机器人ID,一般为0
      *	@param result[0]: Current FSM / 当前状态机状态
      *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_ReadCurFSMFromCPS(self, boxID, rbtID, result):
        command = 'ReadCurFSM,'
        command += str(rbtID) + ','
        command += ';'
        nRet = self.g_clients[boxID].sendAndRecv(command, result)
        if len(result) < 1:
            return nRet
        strRes = self.dic_FSM.get(int(result[0]))
        result.append(strRes)
        return nRet

    '''
    *	@index : 35
    *	@param brief:  Read robot state / 读取当前机器人状态标志
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]: Moving state / 运动状态
    *   @param result[1]: Enable state / 使能状态
    *   @param result[2]: Error state / 错误状态
    *   @param result[3]: Error code / 错误码
    *   @param result[4]: Error axis ID / 错误轴ID
    *   @param result[5]: Breaking status / 抱闸是否打开状态
    *   @param result[6]: Pause state / 暂停状态
    *   @param result[7]: Moving blending done state / WayPoint运动完成状态
        '''
    def HRIF_ReadRobotFlags(self, boxID, rbtID, result):
        result2 = []
        command = 'ReadRobotState,'
        command += str(rbtID) + ','
        command += ';'
        DataRet = self.g_clients[boxID].sendAndRecv(command, result2)
        for i in range(8):
            result += str(result2[i])
        return DataRet

    '''
      *	@index : 36
      *	@param brief: Read point list as name / 读取系统中保存的点位名称列表
      *	@param boxID: Control box ID / 电箱ID号
      *	@param rbtID: Robot ID / 机器人ID,一般为0
      *	@param result: Point list / 点位列表
      *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_ReadPointList(self, boxID, rbtID, result):
        command = 'ReadPointList,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    #
    # part 6 Interfaces for position, velocity and current reading / 位置,速度,电流读取函数接口
    #

    '''
    *	@index : 1
    *	@param brief: Read actual pose and joint positions / 读取当前位置信息
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5]: joint positions / 关节坐标
    *	@param result[6]-result[11]: pose / 笛卡尔坐标
    *	@param result[12]-result[17]: TCP pose / TCP坐标
    *	@param result[18]-result[23]: UCS pose / 用户坐标
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadActPos(self, boxID, rbtID, result):
        command = 'ReadActPos,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 1
    *	@param brief: Read actual pose and joint positions / 读取当前位置信息
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[n-1]: joint positions / 关节坐标
    *	@param result[n]-result[2n-1]: pose / 笛卡尔坐标
    *	@param result[2n]-result[3n-1]: TCP pose / TCP坐标
    *	@param result[3n]-result[4n-1]: UCS pose / 用户坐标
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadActPos_nJ(self, boxID, rbtID, result):
        command = 'ReadActPos,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 3
    *	@param brief: Read command joint positions / 读取关节命令位置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5]: Joint command positions / 关节命令位置
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadCmdJointPos(self, boxID, rbtID, result):
        command = 'ReadCmdPos,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 4
    *	@param brief: Read command joint positions / 读取关节命令位置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[n-1]: Joint command positions / 关节命令位置
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadCmdJointPos_nJ(self, boxID, rbtID, result):
        command = 'ReadCmdPos,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 5
    *	@param brief: Read actual joint positions / 读取关节实际位置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5]: Joint actual positions / 关节实际位置
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadActJointPos(self, boxID, rbtID, result):
        command = 'ReadActACS,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 6
    *	@param brief: Read actual joint positions / 读取关节实际位置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[n-1]: Joint actual positions / 关节实际位置
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadActJointPos_nJ(self, boxID, rbtID, result):
        command = 'ReadActACS,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 7
    *	@param brief: Read command pose of TCP / 读取命令 TCP 位置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5]: TCP command pose / 命令TCP位置
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_ReadCmdTcpPos(self, boxID, rbtID, result):
        command = 'ReadCmdPos,'
        command += str(rbtID) + ','
        command += ';'
        errorCode = self.g_clients[boxID].sendAndRecv(command, result)
        if errorCode != 0:
            return errorCode
        del result[6]
        del result[6]
        del result[6]
        del result[6]
        del result[6]
        del result[6]
        return errorCode

    '''
    *	@index : 8
    *	@param brief: Read actual pose of TCP / 读取实际 TCP 位置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5]: TCP actual pose / 实际TCP位置
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadActTcpPos(self, boxID, rbtID, result):
        retData = []
        errorCode = self.HRIF_ReadActPos(boxID, rbtID, retData)
        if errorCode != 0:
            return errorCode
        for i in range(6, 12):
            result.append(retData[i])
        return errorCode

    '''
    *	@index : 9
    *	@param brief: Read command velocity of joint / 读取关节命令速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5]:Joint command velocity / 关节命令速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadCmdJointVel(self, boxID, rbtID, result):
        command = 'ReadCmdJointVel,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 10
    *	@param brief: Read command velocity of joint / 读取关节命令速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[n-1]:Joint command velocity / 关节命令速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadCmdJointVel_nJ(self, boxID, rbtID, result):
        command = 'ReadCmdJointVel,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 11
    *	@param brief: Read actual velocity of joint / 读取关节实际速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5]: Joint actual velocity / 关节实际速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadActJointVel(self, boxID, rbtID, result):
        command = 'ReadActJointVel,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 12
    *	@param brief: Read actual velocity of joint / 读取关节实际速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[n-1]: Joint actual velocity / 关节实际速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadActJointVel_nJ(self, boxID, rbtID, result):
        command = 'ReadActJointVel,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 13
    *	@param brief: Read command velocity of TCP / 读取命令 TCP 速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5] : TCP command velocity / TCP命令速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadCmdTcpVel(self, boxID, rbtID, result):
        command = 'ReadCmdTcpVel,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 14
    *	@param brief: Read actual velocity of TCP / 读取实际 TCP 速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5]: TCP actual velocity / TCP实际速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadActTcpVel(self, boxID, rbtID, result):
        command = 'ReadActTcpVel,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 15
    *	@param brief: Read command current of joint / 读取关节命令电流
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5]: Joint command current / 关节命令电流 
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadCmdJointCur(self, boxID, rbtID, result):
        command = 'ReadCmdJointCur,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 16
    *	@param brief: Read command current of joint / 读取关节命令电流
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[n-1]: Joint command current / 关节命令电流 
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadCmdJointCur_nJ(self, boxID, rbtID, result):
        command = 'ReadCmdJointCur,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 17
    *	@param brief: Read actual current of joint / 读取关节实际电流
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5]: Joint actual current / 关节实际电流
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadActJointCur(self, boxID, rbtID, result):
        command = 'ReadActJointCur,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 18
    *	@param brief: Read actual current of joint / 读取关节实际电流
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[n-1]: Joint actual current / 关节实际电流
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadActJointCur_nJ(self, boxID, rbtID, result):
        command = 'ReadActJointCur,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 19
    *	@param brief:  Read End velocity of TCP / 读取 TCP 末端速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0] : TCP command velocity / 命令速度mm/s
    *	@param result[1] : TCP actual velocity / 实际速度mm/s
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadTcpVelocity(self, boxID, rbtID, result):
        command = 'ReadTcpVelocity,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    #
    # part 7 Interfaces for calculation / 计算类函数接口
    #

    '''
    *	@index : 1
    *	@param brief: Quaternion to Euler angle / 四元素转欧拉角
    *	@param boxID: Control box ID / 电箱ID号
    *	@param dQuaW : Quaternion W / 四元素W
    *	@param dQuaX : Quaternion X / 四元素X
    *	@param dQuaY : Quaternion Y / 四元素Y
    *	@param dQuaZ : Quaternion Z / 四元素Z
    *	@param result[0] : Euler angle RX / 欧拉角rx
    *	@param result[1] : Euler angle RY / 欧拉角ry
    *	@param result[2] : Euler angle RZ /欧拉角rz
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_Quaternion2RPY(self, boxID, dQuaW, dQuaX, dQuaY, dQuaZ, result):
        command = 'Quaternion2RPY,0,'
        command += str(dQuaW) + ','
        command += str(dQuaX) + ','
        command += str(dQuaY) + ','
        command += str(dQuaZ) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 2
    *	@param brief: Euler angle to Quaternion / 欧拉角转四元素
    *	@param boxID: Control box ID / 电箱ID号
    *	@param Rx : Euler angle RX / 欧拉角rx
    *	@param Ry : Euler angle RY / 欧拉角ry
    *	@param Rz :Euler angle RZ /欧拉角rz
    *	@param result[0] : Quaternion W / 四元素W
    *	@param result[1] : Quaternion X / 四元素X
    *	@param result[2] : Quaternion Y / 四元素Y
    *	@param result[3] : Quaternion Z / 四元素Z
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_RPY2Quaternion(self, boxID, Rx, Ry, Rz, result):
        command = 'RPY2Quaternion,0,'
        command += str(Rx) + ','
        command += str(Ry) + ','
        command += str(Rz) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 3
    *	@param brief: Inverse kinematics transformation from pose to joint positions / 逆解,由指定用户坐标系位置和工具坐标系下的迪卡尔坐标计算对应的关节坐标位置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param rawPCS : pose in specified UCS and TCP / 指定用户坐标系和工具坐标系下的迪卡尔坐标位置(需要逆解的迪卡尔坐标位置)
    *	@param rawACS : Reference joint coordinates / 参考关节坐标,逆解出现多个解时需要根据参考关节坐标选取最终解
    *	@param tcp : TCP pose / dCoord所在的工具坐标
    *	@param ucs : UCS pose / dCoord所在的用户坐标
    *	@return result[0]-result[5] : Inverse solution of J1~J6 / 逆解
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GetInverseKin(self, boxID, rbtID, rawPCS, rawACS, tcp, ucs, result):
        command = 'PCS2ACS,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(rawPCS[i]) + ','
        for i in range(0, 6):
            command += str(rawACS[i]) + ','
        for i in range(0, 6):
            command += str(tcp[i]) + ','
        for i in range(0, 6):
            command += str(ucs[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    '''
    *	@index : 4
    *	@param brief: Inverse kinematics transformation from pose to joint positions / 逆解,由指定用户坐标系位置和工具坐标系下的迪卡尔坐标计算对应的关节坐标位置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param rawPCS : pose in specified UCS and TCP / 指定用户坐标系和工具坐标系下的迪卡尔坐标位置(需要逆解的迪卡尔坐标位置)
    *	@param rawACS : Reference joint coordinates / 参考关节坐标,逆解出现多个解时需要根据参考关节坐标选取最终解
    *	@param tcp : TCP pose / dCoord所在的工具坐标
    *	@param ucs : UCS pose / dCoord所在的用户坐标
    *	@return result[0]-result[n-1] : Inverse solution of J1~J6 / 逆解
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GetInverseKin_nJ(self, boxID, rbtID, rawPCS, rawACS, tcp, ucs, result):
        command = 'PCS2ACS,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(rawPCS[i]) + ','
        for i in range(0, len(rawACS)):
            command += str(rawACS[i]) + ','
        for i in range(0, 6):
            command += str(tcp[i]) + ','
        for i in range(0, 6):
            command += str(ucs[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 5
    *	@param brief: Forward kinematics transformation from joint positions to pose / 正解，由关节坐标位置计算指定用户坐标系和工具坐标系下的迪卡尔坐标位置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param rawACS : joint positions / 需要计算正解的关节坐标
    *	@param tcp : TCP pose for the target / Target所对应的工具坐标
    *	@param ucs : UCS pose for the target / Target所对应的用户坐标
    *	@return result[0]-result[5] : pose in specified UCS and TCP / 指定用户坐标系和工具坐标系下的迪卡尔坐标位置
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GetForwardKin(self, boxID, rbtID, rawACS, tcp, ucs, result):
        command = 'ACS2PCS,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(rawACS[i]) + ','
        for i in range(0, 6):
            command += str(tcp[i]) + ','
        for i in range(0, 6):
            command += str(ucs[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 6
    *	@param brief: Forward kinematics transformation from joint positions to pose / 正解，由关节坐标位置计算指定用户坐标系和工具坐标系下的迪卡尔坐标位置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param rawACS : joint positions / 需要计算正解的关节坐标
    *	@param tcp : TCP pose for the target / Target所对应的工具坐标
    *	@param ucs : UCS pose for the target / Target所对应的用户坐标
    *	@return result[0]-result[5] : pose in specified UCS and TCP / 指定用户坐标系和工具坐标系下的迪卡尔坐标位置
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GetForwardKin_nJ(self, boxID, rbtID, rawACS, tcp, ucs, result):
        command = 'ACS2PCS,'
        command += str(rbtID) + ','
        for i in range(0, len(rawACS)):
            command += str(rawACS[i]) + ','
        for i in range(0, 6):
            command += str(tcp[i]) + ','
        for i in range(0, 6):
            command += str(ucs[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 7
    *	@param brief: Pose transformation from Base to UCS&TCP / 由基座坐标系下的坐标位置计算指定用户坐标系和工具坐标系下的迪卡尔坐标位置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param Base : Pose in Base coordinate system / 基座坐标系下的迪卡尔坐标位置
    *	@param TCP : TCP pose for the target / dTarget所对应的工具坐标
    *	@param UCS : UCS pose for the target / dTarget所对应的用户坐标
    *	@return result[0-5] : Pose in the specified UCS and TCP / 指定用户坐标系和工具坐标系下的迪卡尔坐标
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_Base2UcsTcp(self, boxID, Base, TCP, UCS, result):
        command = 'Base2UcsTcp,0,'
        for i in range(0, 6):
            command += str(Base[i]) + ','
        for i in range(0, 6):
            command += str(TCP[i]) + ','
        for i in range(0, 6):
            command += str(UCS[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 8
    *	@param brief: Pose transformation from UCS&TCP to Base / 由指定用户坐标系和工具坐标系下的迪卡尔坐标位置计算基座坐标系下的坐标位置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param UcsTcp : Pose in speicified UCS and TCP / 指定用户坐标系和工具坐标系下的迪卡尔坐标
    *	@param TCP : TCP pose for dCoord / dCoord所对应的工具坐标
    *	@param UCS : UCS pose for dCoord / dCoord所对应的用户坐标
    *	@return result[0]-result[5] : pose in Base coordinate system / 基座坐标系下的迪卡尔坐标位置
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_UcsTcp2Base(self, boxID, UcsTcp, TCP, UCS, result):
        command = 'UcsTcp2Base,0,'
        for i in range(0, 6):
            command += str(UcsTcp[i]) + ','
        for i in range(0, 6):
            command += str(TCP[i]) + ','
        for i in range(0, 6):
            command += str(UCS[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 9
    *	@param brief: Pose addition calculation / 点位加法计算
    *	@param boxID: Control box ID / 电箱ID号
    *	@param pos1 : Pose of point 1 / 空间坐标 1 
    *	@param pos2 : Pose of point 2 / 空间坐标 2 
    *	@return result[0-5] : Calculation result / 计算结果
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_PoseAdd(self, boxID, pos1, pos2, result):
        command = 'PoseAdd,0,'
        for i in range(0, 6):
            command += str(pos1[i]) + ','
        for i in range(0, 6):
            command += str(pos2[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 10
    *	@param brief: Pose subtraction calculation / 点位减法计算
    *	@param boxID: Control box ID / 电箱ID号
    *	@param pos1 : Pose of point 1 / 空间坐标 1 
    *	@param pos2 : Pose of point 2 / 空间坐标 2 
    *	@return result[0]-result[5] : Calculation result / 计算结果
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_PoseSub(self, boxID, pos1, pos2, result):
        command = 'PoseSub,0,'
        for i in range(0, 6):
            command += str(pos1[i]) + ','
        for i in range(0, 6):
            command += str(pos2[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 11
    *	@param brief: Pose transformation through combined caculations, from P1 based on Base coordinate system to P3 based on UCS with P2 / 坐标变换,组合运算P3=HRIF_PoseTrans(P1,HRIF_PoseInverse(P2))，得到的就是基坐标系下的P1,在用户坐标系P2下的位置P3组合运算 HRIF_PoseTrans(p1,HRIF_PoseInverse(p2))，得到的就是基坐标系下的 p1,在用户坐标系 p2 下的位置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param pos1 : Pose of point 1 / 空间坐标 1 
    *	@param pos2 : Pose of point 2 / 空间坐标 2 
    *	@return result[0-5] : Calculation result, P3 / 计算结果
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_PoseTrans(self, boxID, pos1, pos2, result):
        command = 'PoseTrans,0,'
        for i in range(0, 6):
            command += str(pos1[i]) + ','
        for i in range(0, 6):
            command += str(pos2[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 12
    *	@param brief: Inverse kinematics transformation for pose / 坐标运动学逆变换
    *	@param boxID: Control box ID / 电箱ID号
    *	@param pos1 : Pose of point 1 / 空间坐标 1 
    *	@return result[0]-result[5] : Pose of calculation result / 逆运算后的空间坐标
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_PoseInverse(self, boxID, pos1, result):
        command = 'PoseInverse,0,'
        for i in range(0, 6):
            command += str(pos1[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 13
    *	@param brief: Calculate points distance / 计算点位距离
    *	@param boxID: Control box ID / 电箱ID号
    *	@param pos1 : Pose of point 1 / 空间坐标 1 
    *	@param pos1 : Pose of point 2 / 空间坐标 2 
    *	@return result[0] : Points distance (mm) / 点位距离，单位(mm) 
    *	@return result[1] : Angle between poses / 姿态距离，单位(°) 
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_PoseDist(self, boxID, pos1, pos2, result):
        command = 'CalPointDistance,0,'
        for i in range(0, 6):
            command += str(pos1[i]) + ','
        for i in range(0, 6):
            command += str(pos2[i]) + ','
        command += ';'
        ret = self.g_clients[boxID].sendAndRecv(command, result)
        if ret == 20005:
            command = 'PoseDist,0,'
            for i in range(0, 6):
                command += str(pos1[i]) + ','
            for i in range(0, 6):
                command += str(pos2[i]) + ','
            command += ';'
            ret = self.g_clients[boxID].sendAndRecv(command, result)
        # 检查result是否包含字符串，并将其转换为float
        for i in range(len(result)):
            if isinstance(result[i], str):
                try:
                    result[i] = float(result[i])
                except ValueError:
                    # 如果转换失败（例如，字符串不能转换为float），保持原值或进行错误处理
                    pass

        return ret

    '''
    *	@index : 14
    *	@param brief: Linear interpolation calculation for pose / 空间位置直线插补计算
    *	@param boxID: Control box ID / 电箱ID号
    *	@param pos1 : Pose of point 1 / 空间坐标 1
    *	@param pos2 : Pose of point 2 / 空间坐标 2
    *	@param alpha: Interpolation scale / 插补比例 
    *	@return result[0]-result[5] : Calculation result, pose of point 3 / 计算结果
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_PoseInterpolate(self, boxID, pos1, pos2, alpha, result):
        command = 'PoseInterpolate,0,'
        for i in range(0, 6):
            command += str(pos1[i]) + ','
        for i in range(0, 6):
            command += str(pos2[i]) + ','
        command += str(alpha) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 15
    *	@param brief: Calculate the rotation center. P1,P2,P3 are the points before rotation and P4,P5,P6 are the points after rotation / 轨迹旋转中心计算，p1,p2,p3为旋转前轨迹的特征点，p4,p5,p6为旋转后的轨迹的特征点
    *	@param boxID: Control box ID / 电箱ID号
    *	@param pose1 : Pose of point 1 / 坐标1(X-Z)
    *	@param pose2 : Pose of point 2 / 坐标2(X-Z)
    *	@param pose3 : Pose of point 3 / 坐标3(X-Z)
    *	@param pose4 : Pose of point 4 / 坐标4(X-Z)
    *	@param pose5 : Pose of point 5 / 坐标5(X-Z)
    *	@param pose6 : Pose of point 6 / 坐标6(X-Z)
    *	@return result[0]-result[5] : Calculation result, UCS / 计算结果
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_PoseDefdFrame(self, boxID, pos1, pos2, pos3, pos4, pos5, pos6, result):
        command = 'PoseDefdFrame,0,'
        for i in range(0, 3):
            command += str(pos1[i]) + ','
        for i in range(0, 3):
            command += str(pos2[i]) + ','
        for i in range(0, 3):
            command += str(pos3[i]) + ','
        for i in range(0, 3):
            command += str(pos4[i]) + ','
        for i in range(0, 3):
            command += str(pos5[i]) + ','
        for i in range(0, 3):
            command += str(pos6[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 16
    *	@param brief:  Calculate UCS through 3-point plane / 通过三点平面法计算UCS
    *	@param boxID: Control box ID / 电箱ID号
    *	@param pos1 : Position of point 1 in Base and specified TCP / 点1在Base坐标系下系统默认TCP的位置
    *	@param pos2 : Position of point 2 in Base and specified TCP / 点2在Base坐标系下系统默认TCP的位置
    *	@param pos3 : Position of point 3 in Base and specified TCP / 点3在Base坐标系下系统默认TCP的位置
    *	@return result[0]-result[5] :  Pose of UCS / 计算得出的UCS位姿
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_CalUcsPlane(self, boxID, pos1, pos2, pos3, result):
        command = 'CalUcsPlane,0,'
        for i in range(0, 3):
            command += str(pos1[i]) + ','
        for i in range(0, 3):
            command += str(pos2[i]) + ','
        for i in range(0, 3):
            command += str(pos3[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 17
    *	@param brief: Calculate UCS through 2-point linee / 通过两点直线法计算UCS
    *	@param boxID: Control box ID / 电箱ID号
    *	@param pos1: Pose of point 1 in Base and specified TCP / 点1在Base坐标系下系统默认TCP的位置
    *	@param pos2: Pose of point 2 in Base and specified TCP / 点2在Base坐标系下系统默认TCP的位置
    *	@return result[0]-result[5]: Pose of UCS / 计算得出的UCS
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_CalUcsLine(self, boxID, pos1, pos2, result):
        command = 'CalUcsLine,0,'
        for i in range(0, 6):
            command += str(pos1[i]) + ','
        for i in range(0, 6):
            command += str(pos2[i]) + ','

        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 18
    *	@param brief: Calculate TCP through 3-point / 通过三点平面法计算TCP
    *	@param boxID: Control box ID / 电箱ID号
    *	@param pos1 : Pose of point 1 in Base and system default TCP / 点1在Base坐标系下系统默认TCP的位姿
    *	@param pos2 : Pose of point 2 in Base and system default TCP / 点2在Base坐标系下系统默认TCP的位姿
    *	@param pos3 : Pose of point 3 in Base and system default TCP / 点3在Base坐标系下系统默认TCP的位姿
    *	@return result[0]-result[2]: Position of TCP / 计算得出的TCP的位置
    *	@return result[3]-result[5]: Orientation of TCP, usually 0 / 计算得出的TCP的姿态, 结果一般为0
    *	@return result[6]: quality of the result, 0 for good, 1 for poor, 2 for abnormal / 计算结果的质量，0：良好；1：差（最好不用）；2：异常
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_CalTcp3P(self, boxID, pos1, pos2, pos3, result):
        command = 'CalTcp3P,0,'
        for i in range(0, 6):
            command += str(pos1[i]) + ','
        for i in range(0, 6):
            command += str(pos2[i]) + ','
        for i in range(0, 6):
            command += str(pos3[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 19
    *	@param brief: Calculate TCP through 4-point / 通过四点平面法计算TCP
    *	@param boxID: Control box ID / 电箱ID号
    *	@param pos1 : Pose of point 1 in Base and system default TCP / 点1在Base坐标系下系统默认TCP的位姿
    *	@param pos2 : Pose of point 2 in Base and system default TCP / 点2在Base坐标系下系统默认TCP的位姿
    *	@param pos3 : Pose of point 3 in Base and system default TCP / 点3在Base坐标系下系统默认TCP的位姿
    *	@param pos4 : Pose of point 4 in Base and system default TCP / 点4在Base坐标系下系统默认TCP的位姿
    *	@return result[0]-result[2]: Position of TCP / 计算得出的TCP的位置
    *	@return result[3]-result[5]: Orientation of TCP, usually 0 / 计算得出的TCP的姿态, 结果一般为0
    *	@return result[6] : quality of the result, 0 for good, 1 for poor, 2 for abnormal / 计算结果的质量，0：良好；1：差（最好不用）；2：异常
    *	@return result[7-10] : error index for the 4 source points, 0 for abnormal, 1 for normal / 各个源点的错误指示，0：异常；1：正常
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_CalTcp4P(self, boxID, pos1, pos2, pos3, pos4, result):
        command = 'CalTcp4P,0,'
        for i in range(0, 6):
            command += str(pos1[i]) + ','
        for i in range(0, 6):
            command += str(pos2[i]) + ','
        for i in range(0, 6):
            command += str(pos3[i]) + ','
        for i in range(0, 6):
            command += str(pos4[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    
    '''
    *	@index : 20
    *	@param brief: Calculate TCP orientation / 计算TCP姿态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID : Robot ID / 机器人ID号
    *	@param dUcs : Coordinates and rotation angles in user coordinate system / 用户坐标系下的坐标和旋转角
    *	@param dPcs : Coordinates and rotation angles of TCP / TCP的坐标和旋转角
    *	@param result[0]-result[2]: Calculated rotation angles  / 计算得到的TCP姿态
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_CalTCPOrt(self, boxID, rbtID, dUcs, dPcs, result ):
        command = 'CalTCPOrt,'
        command += str(rbtID) +','
        for i in range(6):
            command += str(dUcs[i]) + ','
        for i in range(6):
            command += str(dPcs[i]) + ','
        command += ';'
        print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 21
    *	@param brief: Calculate inverse dynamics results / 计算动力学逆解结果
    *	@param boxID: Control box ID / 电箱ID号
    *	@param dPose_J1~6 : Joint position / 各关节位置,单位(°)
    *	@param dVel_J1~6 : Joint velocities / 各关节速度,单位(°/s)
    *	@param dAcc_J1~6 : Joint accelerations / 各关节加速度,单位(°/s²）
    *	@param result[0]-result[5]: Joint torques calculated by inverse dynamics (Nm) / 通过逆动力学计算得到的各关节扭矩（牛・米）
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GetInverseDynamics(self, boxID, pose, vel, acc, result):
        command = 'GetInverseDynamics,0,'
        for i in range(0, 6):
            command += str(pose[i]) + ','
        for i in range(0, 6):
            command += str(vel[i]) + ','
        for i in range(0, 6):
            command += str(acc[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)


    #
    # part 8 Interfaces for TCP and UCS / TCP和UCS设置
    #

    '''
    *	@index : 1
    *	@param brief: Set current UCS / 设置当前用户坐标-不写入配置文件，重启后失效
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param TCP: Pose of UCS / 需设置的用户坐标值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_SetTCP(self, boxID, rbtID, TCP):
        result = []
        command = 'SetCurTCP,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(TCP[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 2
    *	@param brief:Set current UCS / 设置当前用户坐标-不写入配置文件，重启后失效
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param UCS: Pose of UCS / 需设置的用户坐标值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetUCS(self, boxID, rbtID, UCS):
        result = []
        command = 'SetCurUCS,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(UCS[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 3
    *	@param brief: Read current TCP / 读取当前设置的工具坐标值
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@return result[0]-result[5] : Pose of TCP / 读取的工具坐标值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadCurTCP(self, boxID, rbtID, result):
        command = 'ReadCurTCP,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 4
    *	@param brief: Read current UCS / 读取当前设置的用户坐标值
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@return result[0]-result[5] : Pose of UCS / 读取的用户坐标值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadCurUCS(self, boxID, rbtID, result):
        command = 'ReadCurUCS,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 5
    *	@param brief: Set current TCP By Name / 通过名称设置工具坐标列表中的值为当前工具坐标，对应名称为示教器配置页面 TCP 示教的工具名称
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param TcpName: TCP name / TCP坐标名称用户坐标名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetTCPByName(self, boxID, rbtID, TcpName):
        result = []
        command = 'SetTCPByName,'
        command += str(rbtID) + ','
        command += str(TcpName) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 6
    *	@param brief:Set current UCS By Name / 通过名称设置用户坐标列表中的值为当前用户坐标，对应名称为示教器配置页面用户坐标示教的名称
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param UcsName: UCS name / UCS坐标名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetUCSByName(self, boxID, rbtID, UcsName):
        result = []
        command = 'SetUCSByName,'
        command += str(rbtID) + ','
        command += str(UcsName) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 7
    *	@param brief: Read TCP By Name / 通过名称读取指定 TCP 坐标，对应名称为示教器配置页面 TCP 示教的工具名称
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param TCP: TCP name / TCP名称，和示教器页面的TCP对应
    *	@return result[0]-result[5] : Pose of TCP / 读取到的对应TCP值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadTCPByName(self, boxID, rbtID, TCP, result):
        command = 'ReadTCPByName,'
        command += str(rbtID) + ','
        command += str(TCP) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 8
    *	@param brief: Read UCS By Name / 通过名称读取指定 UCS 坐标，对应名称为示教器配置页面用户坐标示教的用户坐标名称
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param UCS: UCS name / UCS名称，和示教器页面的UCS对应
    *	@return result[0-5] : Pose of UCS / 读取到的对应UCS值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadUCSByName(self, boxID, rbtID, UCS, result):
        command = 'ReadUCSByName,'
        command += str(rbtID) + ','
        command += str(UCS) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 9
    *	@param brief: Confige TCP / 新建指定名称的TCP和值
    *	@param boxID: Control box ID / 电箱ID号
    *	@param sTcpName: TCP name / 工具坐标名称
    *	@param dTcp_X-dTcp_Rz : Pose of TCP / 工具坐标
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ConfigTCP(self, boxID, name, pos):
        result = []
        command = 'ConfigTCP,0,'
        command += name + ','
        for i in range(0, 6):
            command += str(pos[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 10
    *	@param brief: Confige UCS / 新建指定名称的UCS和值
    *	@param boxID: Control box ID / 电箱ID号
    *	@param sUcsName: UCS name / 用户坐标名称
    *	@param dTcp_X-dTcp_Rz : Pose of UCS / 用户坐标
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ConfigUCS(self, boxID, name, pos):
        result = []
        command = 'ConfigUCS,0,'
        command += name + ','
        for i in range(0, 6):
            command += str(pos[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 11
    *	@param brief: Read TCP list / 读取系统中保存的工具坐标名称列表
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result: vector of TCP list / 工具坐标称列表
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadTCPList(self, boxID, rbtID, result):
        command = 'ReadTCPList,'
        command += str(rbtID) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 12
    *	@param brief: Read UCS list / 读取系统中保存的用户坐标名称列表
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result: vector of UCS list / 用户坐标名称列表
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadUCSList(self, boxID, rbtID, result):
        command = 'ReadUCSList,'
        command += str(rbtID) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 13
    *	@param brief: Set the current base mounting angle / 设定当前机座安装角度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param rotation: Set base rotation angle / 设置机座在水平面上的旋转
    *	@param tilt: Set base tilt angle / 设置机座在垂直方向上的倾斜
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetBaseInstallingAngle(self, boxID, rbtID, rotation, tilt):
        result = []
        command = 'SetBaseInstallingAngle,'
        command += str(rbtID) + ','
        command += str(rotation) + ','
        command += str(tilt) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 14
    *	@param brief: Get the current base mounting angle / 获取当前机座安装角度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]: Get base rotation angle /获取机座在水平面上的旋转角度
    *	@param result[1]: Get base tilt angle /获取机座在垂直方向上的倾斜角度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GetBaseInstallingAngle(self, boxID, rbtID, result):
        command = 'GetBaseInstallingAngle,'
        command += str(rbtID) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 15
    *	@param brief: Set default TCP (Tool Center Point) / 设置默认的工具中心点(TCP)
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param TCP: Name of the TCP to be set as default / 要设置为默认的TCP名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetDftTCP(self, boxID, rbtID, TCP):
        command = 'SetDftTCP,'
        command += str(rbtID) +','
        command += str(TCP) + ','
        command += ';'
        print(command)
        result = []
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 16
    *	@param brief: Read current coordinates of the robot arm / 读取机械臂当前坐标
    *   @details: Get joint coordinates and user coordinates of the robot arm in current state by inputting TCP and UCS names / 通过输入TCP和UCS名称，获取机械臂当前状态下的关节坐标和用户坐标
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param TCP : Name of the tool center point / 工具中心点(TCP)名称
    *	@param UCS : Name of the user coordinate system / 用户坐标系名称
    *	@param result[0]-result[5]: Current joint coordinates /当前关节坐标值
    *	@param result[6]-result[11]: Current user coordinates / 当前用户坐标值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadActCoord(self, boxID, rbtID, TCP, UCS, result):
        command = 'ReadActCoord,'
        command += str(rbtID) + ','
        command += TCP + ','
        command += UCS + ','
        command += ";"
        print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 17
    *	@param brief: Read current coordinates of the robot arm / 读取机械臂当前坐标
    *   @details: Get joint coordinates and user coordinates of the robot arm in current state by inputting TCP and UCS names / 通过输入TCP和UCS名称，获取机械臂当前状态下的关节坐标和用户坐标
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param TCP : Name of the tool center point / 工具中心点(TCP)名称
    *	@param UCS : Name of the user coordinate system / 用户坐标系名称
    *	@param result[0]-result[n-1]: Current joint coordinates /当前关节坐标值
    *	@param result[n]-result[2n-1]: Current user coordinates / 当前用户坐标值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadActCoord_nJ(self,boxID, rbtID,TCP,UCS, result):
        command = 'ReadActCoord,'
        command += str(rbtID) + ','
        command += TCP + ','
        command += UCS + ','
        command += ";"
        print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)


    #
    # part 9 Interfaces for force control / 力控类函数接口
    #

    '''
    *	@index : 1
    *	@param brief: Set force control status / 设置力控状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param state : 0 for closed, 1 for open / 0:关闭力控运动/1:开启力控运动
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetForceControlState(self, boxID, rbtID, state):
        result = []
        command = 'SetForceControlState,'
        command += str(rbtID) + ','
        command += str(state) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 2
    *	@param brief: Read force control status /读取力控状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]:  0 for closed, 1 for seeking, 2 for seeking completed, 3 for free drive / 力控状态 0:关闭状态,1:力控探寻状态,2:力控探寻完成状态,3:力控自由驱动状态
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadForceControlState(self, boxID, rbtID, result):
        command = 'ReadFTControlState,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 3
    *	@param brief: Set force sensor direction align with TCP / 设置力传感器方向为tool坐标方向
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param mode : 0 for not align with TCP, 1 for align with TCP / 0(力传感器方向不为tool坐标方向)/1(力传感器方向为tool坐标方向)
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetForceToolCoordinateMotion(self, boxID, rbtID, mode):
        result = []
        command = 'SetForceToolCoordinateMotion,'
        command += str(rbtID) + ','
        command += str(mode)
        command += ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 4
    *	@param brief: Disable force control / 暂停力控运动，仅暂停力控功能，不暂停运动和脚本
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ForceControlInterrupt(self, boxID, rbtID):
        result = []
        command = 'GrpFCInterrupt,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 5
    *	@param brief: Enable force control / 继续力控运动，仅继续力控运动功能，不继续运动和脚本
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ForceControlContinue(self, boxID, rbtID):
        result = []
        command = 'GrpFCContinue,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 6
    *	@param brief: Reset force sensor to zero / 力控清零，在原有数据的基础上重新标定力传感器
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetForceZero(self, boxID, rbtID):
        result = []
        command = 'SetForceZero,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 7
    *	@param brief: Set max velocity of force seeking / 设置力控探寻的最大速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param MaxLinearVelocity : Max linear velocity / 直线探寻最大速度
    *	@param MaxAngularVelocity : Max angular velocity / 姿态探寻最大速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetMaxSearchVelocities(self, boxID, rbtID, MaxLinearVelocity, MaxAngularVelocity):
        result = []
        command = 'HRSetMaxSearchVelocities,'
        command += str(rbtID) + ','
        command += str(MaxLinearVelocity) + ','
        command += str(MaxAngularVelocity) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 8
    *	@param brief: Set control freedom / 设置力控探寻自由度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param freedom[0]-freedom[5]: 0 for closed / 1 for open / 各方向力控自由度状态 0：关闭  1：开启
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetControlFreedom(self, boxID, rbtID, freedom):
        result = []
        command = 'HRSetControlFreedom,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(freedom[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 9
    *	@param brief: Set force control strategy / 设置控制策略
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param strategy: 0 for Compliant force and 1 for Constant force / 控制策略 0：柔顺模式 1：恒力模式
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetForceControlStrategy(self, boxID, rbtID, strategy):
        result = []
        command = 'HRSetForceControlStrategy,'
        command += str(rbtID) + ','
        command += str(strategy)
        command += ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 10
    *	@param brief: Set force sensor pose / 设置力传感器中心相对于法兰盘的安装位置和姿态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param position[0]-position[5]: Pose / 力传感器中心相对于法兰盘的安装位置和姿态
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetFreeDrivePositionAndOrientation(self, boxID, rbtID, position):
        result = []
        command = 'SetFTPosition,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(position[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 11
    *	@param brief: Set PID for force seeking / 设置力控探寻 PID 参数
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param fP: PID / PID 参数 
    *	@param fI: PID / PID 参数 
    *	@param fD: PID / PID 参数 
    *	@param tP: PID / PID 参数 
    *	@param tI: PID / PID 参数 
    *	@param tD: PID / PID 参数
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetPIDControlParams(self, boxID, rbtID, fP, fI, fD, tP, tI, tD):
        result = []
        command = 'HRSetPIDControlParams,'
        command += str(rbtID) + ','
        command += str(fP)
        command += ','
        command += str(fI)
        command += ','
        command += str(fD)
        command += ','
        command += str(tP)
        command += ','
        command += str(tI)
        command += ','
        command += str(tD)
        command += ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 12
    *	@param brief: Set mass parameters / 设置惯量控制参数
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param mass:  Mass parameters / 惯量控制参数
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetMassParams(self, boxID, rbtID, mass):
        result = []
        command = 'HRSetMassParams,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(mass[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 13
    *	@param brief: Set damp parameters / 设置阻尼控制参数
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param damp:  Damp parameters / 阻尼控制参数
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetDampParams(self, boxID, rbtID, damp):
        result = []
        command = 'HRSetDampParams,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(damp[i]) + ','
        command += ';'
        retData = self.g_clients[boxID].sendAndRecv(command, result)
        return retData

    '''
    *	@index : 14
    *	@param brief: Set stiffness parameters / 设置刚度(k)控制参数
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param stiff: Stiffness parameters / 刚度控制参数
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetStiffParams(self, boxID, rbtID, stiff):
        result = []
        command = 'HRSetStiffParams,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(stiff[i]) + ','
        command += ';'
        retData = self.g_clients[boxID].sendAndRecv(command, result)
        return retData

    '''
    *	@index : 15
    *	@param brief: Set force control goal / 设置力控目标力
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param force_goal: Goal values / 力控目标力
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetForceControlGoal(self, boxID, rbtID, force_goal):
        result = []
        command = 'HRSetControlGoal,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(force_goal[i]) + ','
        for i in range(0, 6):
            command += str(0) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 16
    *	@param brief:  Set control seeking goal / 设置力控目标力和目标距离(力控目标距离暂未启用)
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param forcegoal: Seeking force / 各方向探寻目标力
    *	@param distance: Seeking distance / 各方向探寻距离(暂未启用，可全部设置为0)
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetControlGoal(self, boxID, rbtID, forcegoal, distance):
        result = []
        command = 'HRSetControlGoal,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(forcegoal[i]) + ','
        for i in range(0, 6):
            command += str(distance[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 17
    *	@param brief: Set force data limit / 设置力控限制范围-力传感器超过此范围后控制器断电
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param max: Max limit / 各方向传感器限制最大值
    *	@param min: Min limit / 各方向传感器限制最小值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetForceDataLimit(self, boxID, rbtID, max, min):
        result = []
        command = 'HRSetForceDataLimit,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(max[i]) + ','
        for i in range(0, 6):
            command += str(min[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 18
    *	@param brief: Set force distance limit / 设置力控形变范围
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param allowDistance: Allowed seeking distance / 允许的探寻距离
    *	@param strengthLevel: Power term for the deviation from boundary. 2 for square, 3 for cubic / 位置与边界设置偏离距离的幂次项，设成2，就表示阻力与偏离边界的平方项成比例；设成3，就表示阻力与偏离边界的立方项成比例
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetForceDistanceLimit(self, boxID, rbtID, allowDistance, strengthLevel):
        result = []
        command = 'HRSetForceDistanceLimit,'
        command += str(rbtID) + ','
        command += str(allowDistance) + ','
        command += str(strengthLevel) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 19
    *	@param brief: Set force free drive mode / 设置开启或者关闭力控自由驱动模式
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param state: 0 for closed, 1 for open /  0(关闭)/1(开启)
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetForceFreeDriveMode(self, boxID, rbtID, state):
        result = []
        command = 'SetFTFreeDriveState,'
        command += str(rbtID) + ','
        command += str(state) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 20
    *	@param brief: Set speed mode for force free drive / 设置自由驱动的速度模式
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param nMode: Speed mode, 0 as normal mode, 1 as slow mode, 2 as fast mode, 3 as Welding mode / 速度模式，0:正常模式，1:慢速精准模式，2:快速流畅模式, 3:焊接模式
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetFTFreeDriveSpeedMode(self, boxID, rbtID, mode):
        result = []
        command = 'SetFTFreeDriveSpeedMode,'
        command += str(rbtID) + ','
        command += str(mode) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 21
    *	@param brief: Read force control calibration data / 读取设定后的自由驱动速度模式
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]: speed mode, 0 as normal mode, 1 as slowmode, 2 as fast mode, 3 as Welding mode / 速度模式，0:正常模式，1:慢速精准模式，2:快速流畅模式, 3:焊接模式
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadFTFreeDriveSpeedMode(self, boxID, rbtID, result):
        command = 'ReadFTFreeDriveSpeedMode,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 22
    *	@param brief: Read force control calibration data / 读取力控标定后数据
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5]:  Calibration data /需读取到的对应力传感器值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadFTCabData(self, boxID, rbtID, result):
        command = 'ReadFTCabData,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 23
    *	@param brief: ead  force data from the force sensor / 读取力控原始数据
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]: Force data in the X direction / x方向的原始力数据
    *	@param result[1]: Force data in the Y direction / y方向的原始力数据
    *	@param result[2]: Force data in the Z direction / z方向的原始力数据
    *	@param result[3]: Force data in the RX direction / RX方向的原始力数据
    *	@param result[4]: Force data in the RY direction / RY方向的原始力数据
    *	@param result[5]: Force data in the RZ direction / RZ方向的原始力数据
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadFTData(self, boxID, rbtID, result):
        command = 'ReadForceData,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 24
    *	@param brief: Set the end freedom in free drive / 设置力控自由驱动末端自由度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param df[0]-df[5]: The available freedom parameters in free drive / 设置力控拖动下可开放的自由度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetFreeDriveMotionFreedom(self, boxID, df):
        result = []
        command = 'SetFTMotionFreedom,0,'
        for i in range(0, 6):
            command += str(df[i]) + ','
        command += ';'
        # print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 25
    *	@param brief: Set force free drive translation compliance and rotation compliance / 设置平移柔顺度和旋转柔顺度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param dLinear: translation compliance / 平移柔顺度
    *	@param dAngular: rotation compliance / 旋转柔顺度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetFTFreeFactor(self, boxID, dLinear, dAngular):
        result = []
        command = 'SetFTFreeFactor,0,'
        command += str(dLinear) + ','
        command += str(dAngular) + ',;'

        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 26
    *	@param brief: Set the maximum value, minimum value of the tangential force in the x/y direction and the maximum speed of lifting / 设置x/y方向切向力最大值、最小值和上抬最大速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param Max: Max tangential force (N) / 切向力最大值，单位：N
    *	@param Min: Min tangential force (N) / 切向力最小值，单位：N
    *	@param Vel: Max lifting Velocity (mm/s) /越障上抬最大速度，单位：mm/s
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetTangentForceBounds(self, boxID, rbtID, Max, Min, Vel):
        result = []
        command = 'SetTangentForceBounds,'
        command += str(rbtID) + ','
        command += str(Max) + ','
        command += str(Min) + ','
        command += str(Vel) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 27
    *	@param brief: Set the orientation compensation force size and vector direction [x,y,z] in FreeDrive mode / 设置FreeDrive模式下的定向补偿力大小及矢量方向
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param dForce: Compensation force size(N) / 补偿力大小，单位：N
    *	@param x-z: The vactor direction of compensation force based Base / 补偿力在基坐标系下的矢量方向
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetFreeDriveCompensateForce(self, boxID, rbtID, force, x, y, z):
        result = []
        command = 'SetFreeDriveCompensateForce,'
        command += str(rbtID) + ','
        command += str(force) + ','
        command += str(x) + ','
        command += str(y) + ','
        command += str(z) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 28
    *	@param brief: Set the six-dimensional force activation threshold (force and torque) / 设置六维力启动阈值（力与扭矩）
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param ForceThreshold: Force activation threshold(N) / 自由驱动力启动阈值，单位：N
    *	@param TorqueThreshold: Torque activation threshold (Nm) / 自由驱动力矩启动阈值，单位：N.m
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetFTWrenchThresholds(self, boxID, rbtID, force, torque):
        result = []
        command = 'SetFTWrenchThresholds,'
        command += str(rbtID) + ','
        command += str(force) + ','
        command += str(torque) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 29
    *	@param brief: Set the maximum linear speed and attitude angular speed of force free drive / 设置力控自由驱动最大直线速度及姿态角速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param vel: Max linear speed (mm/s) / 自由驱动最大直线速度，单位：mm/s
    *	@param angular_vel: Max attitude angular speed (°/s) / 自由驱动最大姿态角速度，单位：°/s
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetMaxFreeDriveVel(self, boxID, rbtID, vel, angular_vel):
        result = []
        command = 'SetMaxFreeDriveVel,'
        command += str(rbtID) + ','
        command += str(vel) + ','
        command += str(angular_vel) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 30
    *	@param brief: Read the end degrees of freedom of the force free drive / 读取力控自由驱动的末端自由度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0-5]: The available freedom parameters in free drive / 设置力控拖动下可开放的自由度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadFTMotionFreedom(self, boxID, rbtID, result):
        command = 'ReadFTMotionFreedom,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 31
    *	@param brief: Set each degree of freedom (X/Y/Z/RX/RY/RZ) to force control the maximum distance of exploration / 设置各自由度（X/Y/Z/RX/RY/RZ）力控探寻最大距离
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param AllowDistance1-AllowDistance6: Max distance of exploration in all directions(mm) / 各方向探寻最大距离，单位：mm
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetMaxSearchDistance(self, boxID, rbtID, AllowDistance1, AllowDistance2, AllowDistance3, AllowDistance4,
                                  AllowDistance5, AllowDistance6):
        result = []
        command = 'HRSetMaxSearchDistance,'
        command += str(rbtID) + ','
        command += str(AllowDistance1) + ','
        command += str(AllowDistance2) + ','
        command += str(AllowDistance3) + ','
        command += str(AllowDistance4) + ','
        command += str(AllowDistance5) + ','
        command += str(AllowDistance6) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 32
    *	@param brief: Set the mean filter for force and torque / 设置力与力矩数据的均值滤波器
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param ForceState: Force data mean filtering switch, 0 as close, 1 as open / 力数据均值滤波开关 0：关闭 1：开启
    *	@param TorqueState: Torque data mean filtering switch, 0 as close, 1 as open / 力矩数据均值滤波开关 0：关闭 1：开启
    *	@param ForceLength: Mean filtering length for force data / 力值均值滤波长度
    *	@param TorqueLength: Mean filtering length for torque data / 力矩均值滤波长度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_SetFTMovingAvgFilterParams(self, boxID, rbtID, ForceState, TorqueState, ForceLength, TorqueLength):
        result = []
        command = 'HRSetFTMovingAvgFilterParams,'
        command += str(rbtID) + ','
        command += str(ForceState) + ','
        command += str(TorqueState) + ','
        command += str(ForceLength) + ','
        command += str(TorqueLength) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 33
    *	@param brief: Turn on/off force sensor _ Script with configuration / 开启关闭力传感器_脚本带配置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param state: Set state for force senser / 设置力传感器状态
    *	@param FTMode: 0 for Compliant force and 1 for Constant force / 控制策略 0：柔顺模式 1：恒力模式
    *	@param UCS: Tool / 用户坐标
    *	@param vel[0]: Linear speed / 线速度
    *	@param vel[1]: Angular speed / 角度速度
    *	@param forces : Target exploration force for all directions / 目标探寻力x、y、z、Rx、Ry、Rz
    *	@param freedom : Freedom parameters for free drive exploration / 力控探寻自由度X,Y,Z,Rx,Ry,Rz
    *	@param PID : fP,fI,fD,tP,tI,tD /PID参数
    *	@param Mass : Mass / 惯量控制参数
    *	@param Damp : Damp / 阻尼控制参数
    *	@param Stiff : Stiffness / 刚度参数x、y、z、Rx、Ry、Rz
    *	@param return: open  force control, 0 as success, 1 as fail / 是否开启力控成功(0成功，1失败)
    '''

    def HRIF_SetScriptForceControlState(self, boxID, rbtID, state, FTMode, UCS, TCP, vel, forces, freedom, PID, Mass,
                                        Damp, Stiff):
        result = []
        command = 'SetScriptForceControlState,'
        command += str(rbtID) + ','
        command += str(state) + ','
        command += str(FTMode) + ','
        command += str(UCS) + ','
        command += str(TCP) + ','
        for i in range(0, 2):
            command += str(vel[i]) + ','
        for i in range(0, 6):
            command += str(forces[i]) + ','
        for i in range(0, 6):
            command += str(freedom[i]) + ','
        for i in range(0, 6):
            command += str(PID[i]) + ','
        for i in range(0, 6):
            command += str(Mass[i]) + ','
        for i in range(0, 6):
            command += str(Damp[i]) + ','
        for i in range(0, 6):
            command += str(Stiff[i]) + ','
        command += ';'
        retData = self.g_clients[boxID].sendAndRecv(command, result)
        if retData == 0:
            while True:
                command = 'ReadFTControlState,'
                command += str(rbtID) + ','
                command += ';'
                retData = self.g_clients[boxID].sendAndRecv(command, result)
                if state == 1:
                    if int(result[0]) == 2:
                        break
                elif state == 0:
                    if int(result[0]) != 2:
                        time.sleep(0.2)
                        break
                time.sleep(0.2)
        return retData

    '''
    *	@index : 34
    *	@param brief: Set constant force control stability phase boundary / 设置恒力控稳定阶段边界
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param x-rz: Max distance of positive (mm) / 正方向(与探寻方向一致)最大距离，单位：mm
    *	@param nx-nrz: Max distance of negative (mm) / 负方向(与探寻方向相反)最大距离，单位：mm
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetSteadyContactDeviationRange(self, boxID, rbtID, x, y, z, rx, ry, rz, nx, ny, nz, nrx, nry, nrz):
        result = []
        command = 'HRSetSteadyContactDeviationRange,'
        command += str(rbtID) + ','
        command += str(x) + ','
        command += str(y) + ','
        command += str(z) + ','
        command += str(rx) + ','
        command += str(ry) + ','
        command += str(rz) + ','
        command += str(nx) + ','
        command += str(ny) + ','
        command += str(nz) + ','
        command += str(nrx) + ','
        command += str(nry) + ','
        command += str(nrz) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 35
    *	@param brief: Set the distance threshold when the virtual wall begins to generate damping / 设置虚拟墙开始产生阻尼时的距离阈值
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *   @param depth: Threshold size / 阈值大小
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetDepthThresholdForDampingArea(self, boxID, rbtID, depth):
        result = []
        command = 'SetDepthThresholdForDampingArea,'
        command += str(rbtID) + ','
        command += str(depth) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 36
    *	@param brief: Add a new safe plane / 新增安全平面
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *   @param name: plane name / 平面名称
    *   @param UcsName: UCS Name/ 用户坐标系名称
    *   @param mode: Mode / 安全模式
    *   @param display: display / 是否显示安全平面
    *   @param switch: switch / 是否启用安全平面
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_AddSafePlane(self, boxID, rbtID, name, UcsName, mode, display, switch):
        result = []
        command = 'AddSafePlane,'
        command += str(rbtID) + ','
        command += str(name) + ','
        command += str(UcsName) + ','
        command += str(mode) + ','
        command += str(display) + ','
        command += str(switch) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 37
    *	@param brief: Update SafePlane Info / 更新安全平面
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *   @param name: plane name / 平面名称
    *   @param UcsName: UCS Name/ 用户坐标系名称
    *   @param mode: Mode / 安全模式
    *   @param display: display / 是否显示安全平面
    *   @param switch: switch / 是否启用安全平面
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_UpdateSafePlane(self, boxID, rbtID, name, UcsName, mode, display, switch):
        result = []
        command = 'UpdateSafePlane,'
        command += str(rbtID) + ','
        command += name + ','
        command += UcsName + ','
        command += str(mode) + ','
        command += str(display) + ','
        command += str(switch) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 38
    *	@param brief: Delete Safe Plane / 删除安全平面
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *   @param name: plane name / 平面名称
    *   @param UcsName: UCS Name/ 用户坐标系名称
    *   @param mode: Mode / 安全模式
    *   @param display: display / 是否显示安全平面
    *   @param switch: switch / 是否启用安全平面
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_DelSafePlane(self, boxID, rbtID, name):
        result = []
        command = 'DelSafePlane,'
        command += str(rbtID) + ','
        command += name + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 39
    *	@param brief: Get SafePlane List / 获取安全平面列表
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *   @param result: SafePlane List / 安全平面列表
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadSafePlaneList(self, boxID, rbtID, result):
        command = 'ReadSafePlane,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 40
    *	@param brief: Read SafePlane Info / 读取安全平面信息
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *   @param name: plane name / 平面名称
    *   @param result[0]: UCS Name/ 用户坐标系名称
    *   @param result[1]: Mode / 安全模式
    *   @param result[2]: display / 是否显示安全平面
    *   @param result[3]: switch / 是否启用安全平面
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadSafePlane(self, boxID, rbtID, name, result):
        command = 'ReadSafePlane,'
        command += str(rbtID) + ','
        command += name + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 41
    *	@param brief: Set calibration parameters / 设置标定参数
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *   @param calibrationForce: Set calibration force in XYZ / 设置XYZ方向标定力
    *   @param torque: Set calibration moment in XYZ / 设置XYZ方向标定力矩
    *   @param gravity: Get gravity / 重力（G）
    *   @param cmOffset: Set center of gravity offset in XYZ / 设置XYZ方向重心偏移
    *   @param installRotationAngel: Set current base mounting Installation angle / 设置当前基座安装角度（InstallRotationAngle）
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetInitializeForceSensor(self, boxID, rbtID, calibrationForce, torque, gravity, cmOffset, installRotationAngel):
        result = []
        command = 'SetInitializeForceSensor,'
        command += str(rbtID) + ','
        for i in range(len(calibrationForce)):
            command += str(calibrationForce[i]) + ','
        for i in range(len(torque)):
            command += str(torque[i]) + ','
        command += str(gravity) + ','
        for i in range(len(cmOffset)):
            command += str(cmOffset[i]) + ','
        command += str(installRotationAngel) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 42
    *	@param brief: Get calibration parameters / 获取标定参数
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *   @param result[0]-result[2]: Get calibration force in XYZ / 获取XYZ方向标定力
    *   @param result[3]-result[5]: Get calibration moment in XYZ / 获取XYZ方向标定力矩
    *   @param result[6]: Get gravity / 重力（G）
    *   @param result[7]-result[9]: Get center of gravity offset in XYZ / 获取XYZ方向重心偏移
    *   @param result[10]: Get current base mounting Installation angle / 获取当前基座安装角度（InstallRotationAngle）
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GetLastCalibParams(self, boxID, rbtID, result):
        command = 'GetLastCalibParams,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 43
    *	@param brief: Set the calibration data for the force sensor / 设置力传感器的标定数据
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *   @param num: Number of calibration points / 标定点位的数量
    *   @param Point: Point data for force control calibration / 用于力控标定的点位数据
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *    
    '''
    def HRIF_SetFTCalibration(self, boxID, rbtID, num, Point):
        result = []
        command = 'SetFTCalibration,'
        command += str(rbtID) + ','
        for row in Point:  # 遍历每一行
            for value in row:
                command += str(value) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 44
    *	@param brief: Read  force data from the force sensor / 读取力控原始数据
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]: Force data in the X direction / x方向的原始力数据
    *	@param result[1]: Force data in the Y direction / y方向的原始力数据
    *	@param result[2]: Force data in the Z direction / z方向的原始力数据
    *	@param result[3]: Force data in the RX direction / RX方向的原始力数据
    *	@param result[4]: Force data in the RY direction / RY方向的原始力数据
    *	@param result[5]: Force data in the RZ direction / RZ方向的原始力数据
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadForceData(self, boxID, rbtID, result):
        command = 'ReadForceData,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 45
    *	@param brief: Set current UCS / 设置力控用户坐标系
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *   @param ucs:  Pose of UCS / 需设置的用户坐标值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *    
    '''
    def HRIF_SetFTUCS(self, boxID, rbtID, ucs):
        result = []
        command = 'SetFTUCS,'
        command += str(rbtID) + ','
        for item in ucs:
            command += str(item) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 46
    *	@param brief: Read current UCS / 读取力控用户坐标系
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]-result[5]: Pose of UCS / 读取的用户坐标值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadFTUCS(self, boxID, rbtID, result):
        command = 'ReadFTUCS,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)



    #
    # part 10 Interfaces for moving / 运动类函数接口
    #

    '''
    *	@index : 1
    *	@param brief: Start joint short jog / 关节短点动 运动距离 2°，最大速度<10°/s
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param axisId: Axis ID, 0~5 / 需要运动的关节索引0-5
    *	@param direction: Moving direction, 0 for negative and 1 for positive / 需要运动的关节运动方向：0(负方向)/1(正方向)
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ShortJogJ(self, boxID, rbtID, axisId, direction):
        result = []
        command = 'ShortJogJ,'
        command += str(rbtID) + ','
        command += str(axisId) + ','
        command += str(direction) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 2
    *	@param brief: Cartesian short jog / 迪卡尔坐标短点动 运动距离2mm，最大速度<10mm/s
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param pcsId: Axis ID, 0~5 / 需要运动的关节索引0-5
    *	@param direction:  Moving direction, 0 for negative and 1 for positive / 需要运动的关节运动方向：0(负方向)/1(正方向)
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ShortJogL(self, boxID, rbtID, pcsId, direction):
        result = []
        command = 'ShortJogL,'
        command += str(rbtID) + ','
        command += str(pcsId) + ','
        command += str(direction) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 3
    *	@param brief: Start joint long jog / 关节长点动，最大运动速度<10°/s
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param axisId: Axis ID, 0~5 / 指定运动的关节索引0-5
    *	@param direction: Moving direction, 0 for negative and 1 for positive / 指定运动的关节方向：0(负方向)/1(正方向)
    *	@param state: 0 for closed and 1 for open / 0(关闭)/1(开启)
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_LongJogJ(self, boxID, rbtID, axisId, direction, state):
        result = []
        command = 'LongJogJ,'
        command += str(rbtID) + ','
        command += str(axisId) + ','
        command += str(direction) + ','
        command += str(state) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 4
    *	@param brief: Start cartesian long jog / 迪卡尔坐标长点动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param pcsId:  Axis ID, 0~5 /指定运动的迪卡尔坐标索引0-5
    *	@param direction: Moving direction, 0 for negative and 1 for positive / 指定运动的迪卡尔坐标方向：0(负方向)/1(正方向)
    *	@param state: 0 for closed and 1 for open / 0(关闭)/1(开启)
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_LongJogL(self, boxID, rbtID, pcsId, direction, state):
        result = []
        command = 'LongJogL,'
        command += str(rbtID) + ','
        command += str(pcsId) + ','
        command += str(direction) + ','
        command += str(state) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)


    '''
    *	@index : 5
    *	@param brief: Continue long jog. Successively call this function after HRIF_ShortJogL or HRIF_LongJogJ with less than 500 ms interval to keep continuous moving / 长点动继续指令，当开始长点动之后，要按 500 毫秒或更短时间为时间周期发送一次该指令，否则长点动会停止
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_LongMoveEvent(self, boxID, rbtID):
        result = []
        command = 'LongMoveEvent,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    ''' 
    *	@index : 6
    *	@param brief: Check if the motion is done / 判断运动是否停止
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]: 1 as done, 0 for as done / 1: 运动完成； 0: 运动未完成
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_IsMotionDone(self, boxID, rbtID, result):
        result.clear()
        ret = []
        errorCode = self.HRIF_ReadRobotState(boxID, rbtID, ret)
        if errorCode != 0:
            return errorCode
        result.append(ret[11] == "1" and ret[0] == "0")
        return errorCode

    ''' 
    *	@index : 7
    *	@param brief: Check if the waypoint blending is done / 判断路点是否运动完成
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]: 1 as done, 0 as not done / 1:运动完成;0：运动未完成
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_IsBlendingDone(self, boxID, rbtID, result):
        ret = []
        command = 'ReadRobotState,'
        command += str(rbtID) + ','
        command += ';'
        net = self.g_clients[boxID].sendAndRecv(command, ret)
        if net != 0:
            return net
        if (ret[1] == 0 and ret[2] == 1 and ret[7] == 1 and ret[8] == 1 and ret[9] == 0 and ret[10] == 0):
            return 20018
        if (int(ret[11]) == 1):
            result.append(True)
        else:
            result.append(False)
        return net

    '''
    *	@index : 8
    *	@param brief: Start waypoint move / 执行路点运动(HRIF_WayPointEx 与 HRIF_WayPoint 区别在于 HRIF_WayPointEx 需要设置工具坐标与用户坐标具体的值，而HRIF_WayPoint 使用示教器示教的对应工具坐标与用户坐标名称)
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param type : Move type, 0 for MoveJ, 1 for MoveL / 运动类型，0：MoveJ；1：MoveL
    *	@param points : Target pose, invalid when IsUseJoint equals 1. Target joint positions is obtained through inversely solving from this pose when IsUseJoint equals 0 / 目标迪卡尔位置-当nIsUseJoint=1时无效，nIsUseJoint=0时，用此迪卡尔坐标作为目标位置，通过逆解计算得到关节坐标为目标关节坐标
    *	@param RawACSpoints : Target joint positions when IsUseJoint equals 1; Reference joint positions for the inversely solving when IsUseJoint equals 0. / 目标关节位置-当nIsUseJoint=1时，使用此关节坐标作为目标关节坐标，nIsUseJoint=0时，此关节坐标仅作为计算逆解时选解的参考关节坐标
    *	@param tcp : Target TCP name, invalid when IsUseJoint equals 1, "TCP" is valid as default / 目标迪卡尔坐标所处的工具坐标系名称，与示教器页面的名称对应，当nIsUseJoint=1时无效，可使用默认名称”TCP”
    *	@param ucs : Target UCS name, invalid when IsUseJoint equals 1, "Base" is valid as default / 目标迪卡尔坐标所处的用户坐标系名称，与示教器页面的名称对应-当nIsUseJoint=1时无效，可使用默认名称”Base”
    *	@param speed : Motion speed, mm/s or °/s / 运动速度，速度单位是毫米每秒，度每秒
    *	@param acc : Motion acceleration, mm/(s^2) or °/(s^2) / 运动加速度，毫米每秒平方，度每秒平方
    *	@param radius : Blending radius, mm / 过渡半径，单位毫米
    *	@param isJoint : Using joint or not, usable when MoveType equals 0, 0 for not using joint, 1 for using joint / 是否使用关节角度，是否使用关节角度作为目标点，仅当nMoveType=0时本参数有效。0：不使用关节角度1：使用关节角度
    *	@param isSeek,bit,state: Seeking or not, 1 for seeking; Motion stops when DO-nIOBit equals nIoState / 探寻参数，当nIsSeek为1，则开启探寻，这时电箱的DO nIOBit位为nIOState时，就停止运动，否则运动到目标点再停止
    *	@param cmdID: Command ID, waypoint ID also, customized or set to 1, 2, 3 in order / 当前路点ID，可以自定义，也可以按顺序设置为“1”，“2”，“3”
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_WayPointEx(self, boxID, rbtID, type, points, RawACSpoints, tcp, ucs, speed, acc, radius, isJoint, isSeek,
                        bit, state, cmdID):
        result = []
        command = 'WayPointEx,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(points[i]) + ','
        for i in range(0, 6):
            command += str(RawACSpoints[i]) + ','
        for i in range(0, 6):
            command += str(ucs[i]) + ','
        for i in range(0, 6):
            command += str(tcp[i]) + ','
        command += str(speed) + ','
        command += str(acc) + ','
        command += str(radius) + ','
        command += str(type) + ','
        command += str(isJoint) + ','
        command += str(isSeek) + ','
        command += str(bit) + ','
        command += str(state) + ','
        command += cmdID + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 9
    *	@param brief: Start waypoint move / 执行路点运动(HRIF_WayPointEx 与 HRIF_WayPoint 区别在于 HRIF_WayPointEx 需要设置工具坐标与用户坐标具体的值，而HRIF_WayPoint 使用示教器示教的对应工具坐标与用户坐标名称)
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param type : Move type, 0 for MoveJ, 1 for MoveL / 运动类型，0：MoveJ；1：MoveL
    *	@param points : Target pose, invalid when IsUseJoint equals 1. Target joint positions is obtained through inversely solving from this pose when IsUseJoint equals 0 / 目标迪卡尔位置-当nIsUseJoint=1时无效，nIsUseJoint=0时，用此迪卡尔坐标作为目标位置，通过逆解计算得到关节坐标为目标关节坐标
    *	@param RawACSpoints : Target joint positions when IsUseJoint equals 1; Reference joint positions for the inversely solving when IsUseJoint equals 0. / 目标关节位置-当nIsUseJoint=1时，使用此关节坐标作为目标关节坐标，nIsUseJoint=0时，此关节坐标仅作为计算逆解时选解的参考关节坐标
    *	@param tcp : Target TCP name, invalid when IsUseJoint equals 1, "TCP" is valid as default / 目标迪卡尔坐标所处的工具坐标系名称，与示教器页面的名称对应，当nIsUseJoint=1时无效，可使用默认名称”TCP”
    *	@param ucs : Target UCS name, invalid when IsUseJoint equals 1, "Base" is valid as default / 目标迪卡尔坐标所处的用户坐标系名称，与示教器页面的名称对应-当nIsUseJoint=1时无效，可使用默认名称”Base”
    *	@param speed : Motion speed, mm/s or °/s / 运动速度，速度单位是毫米每秒，度每秒
    *	@param acc : Motion acceleration, mm/(s^2) or °/(s^2) / 运动加速度，毫米每秒平方，度每秒平方
    *	@param radius : Blending radius, mm / 过渡半径，单位毫米
    *	@param isJoint : Using joint or not, usable when MoveType equals 0, 0 for not using joint, 1 for using joint / 是否使用关节角度，是否使用关节角度作为目标点，仅当nMoveType=0时本参数有效。0：不使用关节角度1：使用关节角度
    *	@param isSeek,bit,state: Seeking or not, 1 for seeking; Motion stops when DO-nIOBit equals nIoState / 探寻参数，当nIsSeek为1，则开启探寻，这时电箱的DO nIOBit位为nIOState时，就停止运动，否则运动到目标点再停止
    *	@param cmdID: Command ID, waypoint ID also, customized or set to 1, 2, 3 in order / 当前路点ID，可以自定义，也可以按顺序设置为“1”，“2”，“3”
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_WayPointEx_nJ(self, boxID, rbtID, type, points, RawACSpoints, tcp, ucs, speed, acc, radius, isJoint, isSeek,
                        bit, state, cmdID):
        result = []
        command = 'WayPointEx,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(points[i]) + ','
        for i in range(0, len(RawACSpoints)):
            command += str(RawACSpoints[i]) + ','
        for i in range(0, 6):
            command += str(ucs[i]) + ','
        for i in range(0, 6):
            command += str(tcp[i]) + ','
        command += str(speed) + ','
        command += str(acc) + ','
        command += str(radius) + ','
        command += str(type) + ','
        command += str(isJoint) + ','
        command += str(isSeek) + ','
        command += str(bit) + ','
        command += str(state) + ','
        command += cmdID + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 10
    *	@param brief: Start waypoint move. / 执行路点运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param type : Move type, 0 for MoveJ, 1 for MoveL / 运动类型，0：MoveJ；1：MoveL
    *	@param points : Target pose, invalid when IsUseJoint equals 1. Target joint positions is obtained through inversely solving from this pose when IsUseJoint equals 0 / 目标迪卡尔位置-当nIsUseJoint=1时无效，nIsUseJoint=0时，用此迪卡尔坐标作为目标位置，通过逆解计算得到关节坐标为目标关节坐标
    *	@param RawACSpoints : Target joint positions when IsUseJoint equals 1; Reference joint positions for the inversely solving when IsUseJoint equals 0. / 目标关节位置-当nIsUseJoint=1时，使用此关节坐标作为目标关节坐标，nIsUseJoint=0时，此关节坐标仅作为计算逆解时选解的参考关节坐标
    *	@param tcp : Target TCP name, invalid when IsUseJoint equals 1, "TCP" is valid as default / 目标迪卡尔坐标所处的工具坐标系名称，与示教器页面的名称对应，当nIsUseJoint=1时无效，可使用默认名称”TCP”
    *	@param ucs : Target UCS name, invalid when IsUseJoint equals 1, "Base" is valid as default / 目标迪卡尔坐标所处的用户坐标系名称，与示教器页面的名称对应-当nIsUseJoint=1时无效，可使用默认名称”Base”
    *	@param speed : Motion speed, mm/s or °/s / 运动速度，速度单位是毫米每秒，度每秒
    *	@param Acc : Motion acceleration, mm/(s^2) or °/(s^2) / 运动加速度，毫米每秒平方，度每秒平方
    *	@param radius : Blending radius, mm / 过渡半径，单位毫米
    *	@param isJoint : Using joint or not, usable when MoveType equals 0, 0 for not using joint, 1 for using joint / 是否使用关节角度，是否使用关节角度作为目标点，仅当nMoveType=0时本参数有效。0：不使用关节角度1：使用关节角度
    *	@param isSeek,bit,state: Seeking or not, 1 for seeking; Motion stops when DO-nIOBit equals nIoState / 探寻参数，当nIsSeek为1，则开启探寻，这时电箱的DO nIOBit位为nIOState时，就停止运动，否则运动到目标点再停止
    *	@param cmdID: Command ID, waypoint ID also, customized or set to 1, 2, 3 in order / 当前路点ID，可以自定义，也可以按顺序设置为“1”，“2”，“3”
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_WayPoint(self, boxID, rbtID, type, points, RawACSpoints, tcp, ucs, speed, Acc, radius, isJoint, isSeek,
                      bit, state, cmdID):
        result = []
        command = 'WayPoint,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(points[i]) + ','
        for i in range(0, 6):
            command += str(RawACSpoints[i]) + ','
        command += str(tcp) + ','
        command += str(ucs) + ','
        command += str(speed) + ','
        command += str(Acc) + ','
        command += str(radius) + ','
        command += str(type) + ','
        command += str(isJoint) + ','
        command += str(isSeek) + ','
        command += str(bit) + ','
        command += str(state) + ','
        command += str(cmdID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 11
    *	@param brief: Start waypoint move. / 执行路点运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param type : Move type, 0 for MoveJ, 1 for MoveL / 运动类型，0：MoveJ；1：MoveL
    *	@param points : Target pose, invalid when IsUseJoint equals 1. Target joint positions is obtained through inversely solving from this pose when IsUseJoint equals 0 / 目标迪卡尔位置-当nIsUseJoint=1时无效，nIsUseJoint=0时，用此迪卡尔坐标作为目标位置，通过逆解计算得到关节坐标为目标关节坐标
    *	@param RawACSpoints : Target joint positions when IsUseJoint equals 1; Reference joint positions for the inversely solving when IsUseJoint equals 0. / 目标关节位置-当nIsUseJoint=1时，使用此关节坐标作为目标关节坐标，nIsUseJoint=0时，此关节坐标仅作为计算逆解时选解的参考关节坐标
    *	@param tcp : Target TCP name, invalid when IsUseJoint equals 1, "TCP" is valid as default / 目标迪卡尔坐标所处的工具坐标系名称，与示教器页面的名称对应，当nIsUseJoint=1时无效，可使用默认名称”TCP”
    *	@param ucs : Target UCS name, invalid when IsUseJoint equals 1, "Base" is valid as default / 目标迪卡尔坐标所处的用户坐标系名称，与示教器页面的名称对应-当nIsUseJoint=1时无效，可使用默认名称”Base”
    *	@param speed : Motion speed, mm/s or °/s / 运动速度，速度单位是毫米每秒，度每秒
    *	@param Acc : Motion acceleration, mm/(s^2) or °/(s^2) / 运动加速度，毫米每秒平方，度每秒平方
    *	@param radius : Blending radius, mm / 过渡半径，单位毫米
    *	@param isJoint : Using joint or not, usable when MoveType equals 0, 0 for not using joint, 1 for using joint / 是否使用关节角度，是否使用关节角度作为目标点，仅当nMoveType=0时本参数有效。0：不使用关节角度1：使用关节角度
    *	@param isSeek,bit,state: Seeking or not, 1 for seeking; Motion stops when DO-nIOBit equals nIoState / 探寻参数，当nIsSeek为1，则开启探寻，这时电箱的DO nIOBit位为nIOState时，就停止运动，否则运动到目标点再停止
    *	@param cmdID: Command ID, waypoint ID also, customized or set to 1, 2, 3 in order / 当前路点ID，可以自定义，也可以按顺序设置为“1”，“2”，“3”
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_WayPoint_nJ(self, boxID, rbtID, type, points, RawACSpoints, tcp, ucs, speed, Acc, radius, isJoint, isSeek,
                      bit, state, cmdID):
        result = []
        command = 'WayPoint,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(points[i]) + ','
        for i in range(0, len(RawACSpoints)):
            command += str(RawACSpoints[i]) + ','
        command += str(tcp) + ','
        command += str(ucs) + ','
        command += str(speed) + ','
        command += str(Acc) + ','
        command += str(radius) + ','
        command += str(type) + ','
        command += str(isJoint) + ','
        command += str(isSeek) + ','
        command += str(bit) + ','
        command += str(state) + ','
        command += str(cmdID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 12
    *	@param brief: Start waypoint move / 执行路点运动(HRIF_WayPoint2 新增直线与圆弧过渡不减速功能，HRIF_WayPoint 只有直线与直线之间有过渡)
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param type : Move type, 0 for MoveJ, 1 for MoveL, 2 for MoveC / 运动类型，0：MoveJ；1：MoveL；2：MoveC
    *	@param EndPos : Target pose, invalid when IsUseJoint equals 1. Target pose is obtained through inverse kinematics from this pose when IsUseJoint equals 0 / 目标迪卡尔位置-当nIsUseJoint=1时无效，nIsUseJoint=0时，用此迪卡尔坐标作为目标位置，通过逆解计算得到关节坐标为目标关节坐标
    *	@param AuxPos : Target auxiliary pose invalid when IsUseJoint equals 1, used as the middle point when nMoveType equals 2. Target pose is obtained through inverse kinematics from this pose when IsUseJoint equals 0 / 目标迪卡尔位置-当nIsUseJoint=1时无效，nIsUseJoint=0时，用此迪卡尔坐标作为目标位置，通过逆解计算得到关节坐标为目标关节坐标
    *	@param AcsPos : Target joint positions when IsUseJoint equals 1; Reference joint positions for the inverse kinematics when IsUseJoint equals 0. / 目标关节位置-当nIsUseJoint=1时，使用此关节坐标作为目标关节坐标，nIsUseJoint=0时，此关节坐标仅作为计算逆解时选解的参考关节坐标
    *	@param Tcp : Target TCP name, invalid when IsUseJoint equals 1, "TCP" is valid as default / 目标迪卡尔坐标所处的工具坐标系名称，与示教器页面的名称对应，当nIsUseJoint=1时无效，可使用默认名称”TCP”
    *	@param Ucs : Target UCS name, invalid when IsUseJoint equals 1, "Base" is valid as default / 目标迪卡尔坐标所处的用户坐标系名称，与示教器页面的名称对应-当nIsUseJoint=1时无效，可使用默认名称”Base”
    *	@param Vel : Motion speed, mm/s or °/s / 运动速度，速度单位是毫米每秒，度每秒
    *	@param Acc : Motion acceleration, mm/(s^2) or °/(s^2) / 运动加速度，毫米每秒平方，度每秒平方
    *	@param Radius : Blending radius, mm / 过渡半径，单位毫米
    *	@param isJoint : Using joint or not, usable when MoveType equals 0, 0 for not using joint, 1 for using joint / 是否使用关节角度，是否使用关节角度作为目标点，仅当nMoveType=0时本参数有效。0：不使用关节角度1：使用关节角度
    *	@param isSeek,bit,state: Seeking or not, 1 for seeking; Motion stops when DO-nIOBit equals nIoState / 探寻参数，当nIsSeek为1，则开启探寻，这时电箱的DO nIOBit位为nIOState时，就停止运动，否则运动到目标点再停止
    *	@param cmdID: Command ID, waypoint ID also, customized or set to 1, 2, 3 in order / 当前路点ID，可以自定义，也可以按顺序设置为“1”，“2”，“3”
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_WayPoint2(self, boxID, rbtID, type, EndPos, AuxPos, AcsPos, Tcp, Ucs, Vel, Acc, Radius, isJoint, isSeek,
                       bit, state, cmdID):
        result = []
        command = 'WayPoint2,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(EndPos[i]) + ','
        for i in range(0, 6):
            command += str(AcsPos[i]) + ','
        command += Tcp + ','
        command += Ucs + ','
        command += str(Vel) + ','
        command += str(Acc) + ','
        command += str(Radius) + ','
        command += str(type) + ','
        command += str(isJoint) + ','
        command += str(isSeek) + ','
        command += str(bit) + ','
        command += str(state) + ','
        for i in range(0, 6):
            command += str(AuxPos[i]) + ','
        command += cmdID + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 13
    *	@param brief: Start waypoint move / 执行路点运动(HRIF_WayPoint2 新增直线与圆弧过渡不减速功能，HRIF_WayPoint 只有直线与直线之间有过渡)
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param type : Move type, 0 for MoveJ, 1 for MoveL, 2 for MoveC / 运动类型，0：MoveJ；1：MoveL；2：MoveC
    *	@param EndPos : Target pose, invalid when IsUseJoint equals 1. Target pose is obtained through inverse kinematics from this pose when IsUseJoint equals 0 / 目标迪卡尔位置-当nIsUseJoint=1时无效，nIsUseJoint=0时，用此迪卡尔坐标作为目标位置，通过逆解计算得到关节坐标为目标关节坐标
    *	@param AuxPos : Target auxiliary pose invalid when IsUseJoint equals 1, used as the middle point when nMoveType equals 2. Target pose is obtained through inverse kinematics from this pose when IsUseJoint equals 0 / 目标迪卡尔位置-当nIsUseJoint=1时无效，nIsUseJoint=0时，用此迪卡尔坐标作为目标位置，通过逆解计算得到关节坐标为目标关节坐标
    *	@param AcsPos : Target joint positions when IsUseJoint equals 1; Reference joint positions for the inverse kinematics when IsUseJoint equals 0. / 目标关节位置-当nIsUseJoint=1时，使用此关节坐标作为目标关节坐标，nIsUseJoint=0时，此关节坐标仅作为计算逆解时选解的参考关节坐标
    *	@param Tcp : Target TCP name, invalid when IsUseJoint equals 1, "TCP" is valid as default / 目标迪卡尔坐标所处的工具坐标系名称，与示教器页面的名称对应，当nIsUseJoint=1时无效，可使用默认名称”TCP”
    *	@param Ucs : Target UCS name, invalid when IsUseJoint equals 1, "Base" is valid as default / 目标迪卡尔坐标所处的用户坐标系名称，与示教器页面的名称对应-当nIsUseJoint=1时无效，可使用默认名称”Base”
    *	@param Vel : Motion speed, mm/s or °/s / 运动速度，速度单位是毫米每秒，度每秒
    *	@param Acc : Motion acceleration, mm/(s^2) or °/(s^2) / 运动加速度，毫米每秒平方，度每秒平方
    *	@param Radius : Blending radius, mm / 过渡半径，单位毫米
    *	@param isJoint : Using joint or not, usable when MoveType equals 0, 0 for not using joint, 1 for using joint / 是否使用关节角度，是否使用关节角度作为目标点，仅当nMoveType=0时本参数有效。0：不使用关节角度1：使用关节角度
    *	@param isSeek,bit,state: Seeking or not, 1 for seeking; Motion stops when DO-nIOBit equals nIoState / 探寻参数，当nIsSeek为1，则开启探寻，这时电箱的DO nIOBit位为nIOState时，就停止运动，否则运动到目标点再停止
    *	@param cmdID: Command ID, waypoint ID also, customized or set to 1, 2, 3 in order / 当前路点ID，可以自定义，也可以按顺序设置为“1”，“2”，“3”
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_WayPoint2_nJ(self, boxID, rbtID, type, EndPos, AuxPos, AcsPos, Tcp, Ucs, Vel, Acc, Radius, isJoint, isSeek,
                       bit, state, cmdID):
        result = []
        command = 'WayPoint2,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(EndPos[i]) + ','
        for i in range(0, len(AcsPos)):
            command += str(AcsPos[i]) + ','
        command += Tcp + ','
        command += Ucs + ','
        command += str(Vel) + ','
        command += str(Acc) + ','
        command += str(Radius) + ','
        command += str(type) + ','
        command += str(isJoint) + ','
        command += str(isSeek) + ','
        command += str(bit) + ','
        command += str(state) + ','
        for i in range(0, 6):
            command += str(AuxPos[i]) + ','
        command += cmdID + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 14
    *	@param brief: Start joint move. HRIF_WayPoint is more recommended yet / 机器人运动到指定的角度坐标位置, 建议使用HRIF_WayPoint
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param points : Target pose, invalid when IsUseJoint equals 1. Target joint positions is obtained through inversely solving from this pose when IsUseJoint equals 0 / 目标迪卡尔位置-当nIsUseJoint=1时无效，nIsUseJoint=0时，用此迪卡尔坐标作为目标位置，通过逆解计算得到关节坐标为目标关节坐标
    *	@param RawACSpoints : Target joint positions when IsUseJoint equals 1; Reference joint positions for the inversely solving when IsUseJoint equals 0. / 目标关节位置-当nIsUseJoint=1时，使用此关节坐标作为目标关节坐标，nIsUseJoint=0时，此关节坐标仅作为计算逆解时选解的参考关节坐标
    *	@param tcp : Target TCP name, invalid when IsUseJoint equals 1, "TCP" is valid as default / 目标迪卡尔坐标所处的工具坐标系名称，与示教器页面的名称对应，当nIsUseJoint=1时无效，可使用默认名称”TCP”
    *	@param ucs :Target UCS name, invalid when IsUseJoint equals 1, "Base" is valid as default / 目标迪卡尔坐标所处的用户坐标系名称，与示教器页面的名称对应-当nIsUseJoint=1时无效，可使用默认名称”Base”
    *	@param speed : Motion speed, mm/s or °/s / 运动速度，速度单位是毫米每秒，度每秒
    *	@param Acc : Motion acceleration, mm/(s^2) or °/(s^2) / 运动加速度，毫米每秒平方，度每秒平方
    *	@param radius : Blending radius, mm / 过渡半径，单位毫米
    *	@param isJoint : Using joint or not, usable when MoveType equals 0, 0 for not using joint, 1 for using joint / 是否使用关节角度，是否使用关节角度作为目标点，仅当nMoveType=0时本参数有效。0：不使用关节角度1：使用关节角度
    *	@param isSeek,bit,state: Seeking or not, 1 for seeking; Motion stops when DO-nIOBit equals nIoState / 探寻参数，当nIsSeek为1，则开启探寻，这时电箱的DO nIOBit位为nIOState时，就停止运动，否则运动到目标点再停止
    *	@param cmdID: Command ID, waypoint ID also, customized or set to 1, 2, 3 in order / 当前路点ID，可以自定义，也可以按顺序设置为“1”，“2”，“3”
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_MoveJ(self, boxID, rbtID, points, RawACSpoints, tcp, ucs, speed, Acc, radius, isJoint, isSeek, bit, state,
                   cmdID):
        result = []
        command = 'WayPoint,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(points[i]) + ','
        for i in range(0, 6):
            command += str(RawACSpoints[i]) + ','
        command += str(tcp) + ','
        command += str(ucs) + ','
        command += str(speed) + ','
        command += str(Acc) + ','
        command += str(radius) + ','
        command += '0,'
        command += str(isJoint) + ','
        command += str(isSeek) + ','
        command += str(bit) + ','
        command += str(state) + ','
        command += str(cmdID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 14
    *	@param brief: Start joint move. HRIF_WayPoint is more recommended yet / 机器人运动到指定的角度坐标位置, 建议使用HRIF_WayPoint
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param points : Target pose, invalid when IsUseJoint equals 1. Target joint positions is obtained through inversely solving from this pose when IsUseJoint equals 0 / 目标迪卡尔位置-当nIsUseJoint=1时无效，nIsUseJoint=0时，用此迪卡尔坐标作为目标位置，通过逆解计算得到关节坐标为目标关节坐标
    *	@param RawACSpoints : Target joint positions when IsUseJoint equals 1; Reference joint positions for the inversely solving when IsUseJoint equals 0. / 目标关节位置-当nIsUseJoint=1时，使用此关节坐标作为目标关节坐标，nIsUseJoint=0时，此关节坐标仅作为计算逆解时选解的参考关节坐标
    *	@param tcp : Target TCP name, invalid when IsUseJoint equals 1, "TCP" is valid as default / 目标迪卡尔坐标所处的工具坐标系名称，与示教器页面的名称对应，当nIsUseJoint=1时无效，可使用默认名称”TCP”
    *	@param ucs :Target UCS name, invalid when IsUseJoint equals 1, "Base" is valid as default / 目标迪卡尔坐标所处的用户坐标系名称，与示教器页面的名称对应-当nIsUseJoint=1时无效，可使用默认名称”Base”
    *	@param speed : Motion speed, mm/s or °/s / 运动速度，速度单位是毫米每秒，度每秒
    *	@param Acc : Motion acceleration, mm/(s^2) or °/(s^2) / 运动加速度，毫米每秒平方，度每秒平方
    *	@param radius : Blending radius, mm / 过渡半径，单位毫米
    *	@param isJoint : Using joint or not, usable when MoveType equals 0, 0 for not using joint, 1 for using joint / 是否使用关节角度，是否使用关节角度作为目标点，仅当nMoveType=0时本参数有效。0：不使用关节角度1：使用关节角度
    *	@param isSeek,bit,state: Seeking or not, 1 for seeking; Motion stops when DO-nIOBit equals nIoState / 探寻参数，当nIsSeek为1，则开启探寻，这时电箱的DO nIOBit位为nIOState时，就停止运动，否则运动到目标点再停止
    *	@param cmdID: Command ID, waypoint ID also, customized or set to 1, 2, 3 in order / 当前路点ID，可以自定义，也可以按顺序设置为“1”，“2”，“3”
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_MoveJ_nJ(self, boxID, rbtID, points, RawACSpoints, tcp, ucs, speed, Acc, radius, isJoint, isSeek, bit, state,
                   cmdID):
        result = []
        command = 'WayPoint,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(points[i]) + ','
        for i in range(0, len(RawACSpoints)):
            command += str(RawACSpoints[i]) + ','
        command += str(tcp) + ','
        command += str(ucs) + ','
        command += str(speed) + ','
        command += str(Acc) + ','
        command += str(radius) + ','
        command += '0,'
        command += str(isJoint) + ','
        command += str(isSeek) + ','
        command += str(bit) + ','
        command += str(state) + ','
        command += str(cmdID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 15
    *	@param brief: Start linear move. HRIF_WayPoint is more recommended yet / 机器人直线运动到指定的空间坐标位置, 建议使用HRIF_WayPoint
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param points : Target pose / 目标迪卡尔位置
    *	@param RawACSpoints : Reference joint positions near to the target pose / 关节位置-建议使用目标迪卡尔坐标附近的关节坐标值
    *	@param tcp : TCP name / 目标迪卡尔坐标所处的工具坐标系名称
    *	@param ucs : UCS name / 目标迪卡尔坐标所处的用户坐标系名称
    *	@param speed : Motion speed, mm/s or °/s / 运动速度，速度单位是毫米每秒，度每秒
    *	@param Acc : Motion acceleration, mm/(s^2) or °/(s^2) / 运动加速度，毫米每秒平方，度每秒平方
    *	@param radius : Blending radius, mm / 过渡半径，单位毫米
    *	@param isJoint : Using joint or not, usable when MoveType equals 0, 0 for not using joint, 1 for using joint / 是否使用关节角度，是否使用关节角度作为目标点，仅当nMoveType=0时本参数有效。0：不使用关节角度1：使用关节角度
    *	@param isSeek,bit,state: Seeking or not, 1 for seeking; Motion stops when DO-nIOBit equals nIoState / 探寻参数，当nIsSeek为1，则开启探寻，这时电箱的DO nIOBit位为nIOState时，就停止运动，否则运动到目标点再停止
    *	@param cmdID: Command ID, waypoint ID also, customized or set to 1, 2, 3 in order / 当前路点ID，可以自定义，也可以按顺序设置为“1”，“2”，“3”
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_MoveL(self, boxID, rbtID, points, RawACSpoints, tcp, ucs, speed, Acc, radius, isSeek, bit, state, cmdID):
        result = []
        command = 'WayPoint,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(points[i]) + ','
        for i in range(0, 6):
            command += str(RawACSpoints[i]) + ','
        command += str(tcp) + ','
        command += str(ucs) + ','
        command += str(speed) + ','
        command += str(Acc) + ','
        command += str(radius) + ','
        command += '1,'
        command += '0,'
        command += str(isSeek) + ','
        command += str(bit) + ','
        command += str(state) + ','
        command += str(cmdID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 16
    *	@param brief: Start linear move. HRIF_WayPoint is more recommended yet / 机器人直线运动到指定的空间坐标位置, 建议使用HRIF_WayPoint
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param points : Target pose / 目标迪卡尔位置
    *	@param RawACSpoints : Reference joint positions near to the target pose / 关节位置-建议使用目标迪卡尔坐标附近的关节坐标值
    *	@param tcp : TCP name / 目标迪卡尔坐标所处的工具坐标系名称
    *	@param ucs : UCS name / 目标迪卡尔坐标所处的用户坐标系名称
    *	@param speed : Motion speed, mm/s or °/s / 运动速度，速度单位是毫米每秒，度每秒
    *	@param Acc : Motion acceleration, mm/(s^2) or °/(s^2) / 运动加速度，毫米每秒平方，度每秒平方
    *	@param radius : Blending radius, mm / 过渡半径，单位毫米
    *	@param isJoint : Using joint or not, usable when MoveType equals 0, 0 for not using joint, 1 for using joint / 是否使用关节角度，是否使用关节角度作为目标点，仅当nMoveType=0时本参数有效。0：不使用关节角度1：使用关节角度
    *	@param isSeek,bit,state: Seeking or not, 1 for seeking; Motion stops when DO-nIOBit equals nIoState / 探寻参数，当nIsSeek为1，则开启探寻，这时电箱的DO nIOBit位为nIOState时，就停止运动，否则运动到目标点再停止
    *	@param cmdID: Command ID, waypoint ID also, customized or set to 1, 2, 3 in order / 当前路点ID，可以自定义，也可以按顺序设置为“1”，“2”，“3”
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_MoveL_nJ(self, boxID, rbtID, points, RawACSpoints, tcp, ucs, speed, Acc, radius, isSeek, bit, state, cmdID):
        result = []
        command = 'WayPoint,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(points[i]) + ','
        for i in range(0, len(RawACSpoints)):
            command += str(RawACSpoints[i]) + ','
        command += str(tcp) + ','
        command += str(ucs) + ','
        command += str(speed) + ','
        command += str(Acc) + ','
        command += str(radius) + ','
        command += '1,'
        command += '0,'
        command += str(isSeek) + ','
        command += str(bit) + ','
        command += str(state) + ','
        command += str(cmdID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 17
    *	@param brief: Start round move / 开始圆弧轨迹运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param StartPoint : Start pose / 圆弧开始位置
    *	@param AuxPoint : Via pose / 圆弧经过位置
    *	@param EndPoint : End pose / 圆弧结束位置
    *	@param fixedPosure : 0 for unfixed orientation, 1 for fixed orientation, 2 for newly added gradual orientation arc motion.  
    *                    / 0:渐变姿态圆弧运动，1:固定姿态圆弧运动，2:新增的渐变姿态圆弧运动
    *	@param nMoveCType : 1 for arc, 0 for circle / 1:圆弧轨迹，0:整圆轨迹
    *	@param nRadLen : Invalid when nMoveCType equals 1; Circles when nMoveCType equals 0. / 当nMoveCType=1时参数无效，由三个点确定圆弧轨迹
    *			         当nMoveCType=0时，参数为整圆的圈数,通过三个点位确定圆弧路径，当使用整圆运动时表示整圆的圈数，小数部分无效
    *	@param speed : Motion speed, mm/s / 运动速度，单位是毫米每秒
    *	@param Acc : Motion acceleration, mm/(s^2) / 运动加速度，毫米每秒平方
    *	@param radius : Blending radius, mm / 过渡半径，单位毫米
    *	@param tcp : TCP name / 工具坐标名称
    *	@param ucs : UCS name / 用户坐标名称
    *	@param cmdID : Command ID / 命令ID
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_MoveC(self, boxID, rbtID, StartPoint, AuxPoint, EndPoint, fixedPosure, nMoveCType, nRadLen, speed, Acc,
                   radius, tcp, ucs, cmdID):
        result = []
        command = 'MoveC,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(StartPoint[i]) + ','
        for i in range(0, 6):
            command += str(AuxPoint[i]) + ','
        for i in range(0, 6):
            command += str(EndPoint[i]) + ','
        command += str(fixedPosure) + ','
        command += str(nMoveCType) + ','
        command += str(nRadLen) + ','
        command += str(speed) + ','
        command += str(Acc) + ','
        command += str(radius) + ','
        command += str(tcp) + ','
        command += str(ucs) + ','
        command += str(cmdID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 17
    *	@param brief: Start round move / 开始圆弧轨迹运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param StartPoint : Start pose / 圆弧开始位置
    *	@param AuxPoint : Via pose / 圆弧经过位置
    *	@param EndPoint : End pose / 圆弧结束位置
    *	@param joint : expand axis pose / 拓展轴位置
    *	@param fixedPosure : 0 for unfixed orientation, 1 for fixed orientation, 2 for newly added gradual orientation arc motion.  
    *                    / 0:渐变姿态圆弧运动，1:固定姿态圆弧运动，2:新增的渐变姿态圆弧运动
    *	@param nMoveCType : 1 for arc, 0 for circle / 1:圆弧轨迹，0:整圆轨迹
    *	@param nRadLen : Invalid when nMoveCType equals 1; Circles when nMoveCType equals 0. / 当nMoveCType=1时参数无效，由三个点确定圆弧轨迹
    *			         当nMoveCType=0时，参数为整圆的圈数,通过三个点位确定圆弧路径，当使用整圆运动时表示整圆的圈数，小数部分无效
    *	@param speed : Motion speed, mm/s / 运动速度，单位是毫米每秒
    *	@param Acc : Motion acceleration, mm/(s^2) / 运动加速度，毫米每秒平方
    *	@param radius : Blending radius, mm / 过渡半径，单位毫米
    *	@param tcp : UCS name / 用户坐标名称
    *	@param ucs : TCP name / 工具坐标名称
    *	@param cmdID: Command ID / 命令ID
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_MoveC_nJ(self, boxID, rbtID, StartPoint, AuxPoint, EndPoint, joint, IsUseCurRefAC, fixedPosure, nMoveCType,
                      nRadLen, speed, Acc, radius, tcp, ucs, cmdID):
        result = []
        command = 'MoveC,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(StartPoint[i]) + ','
        for i in range(0, 6):
            command += str(AuxPoint[i]) + ','
        for i in range(0, 6):
            command += str(EndPoint[i]) + ','
        for i in range(0, len(joint)):
            command += str(joint[i]) + ','
        command += str(IsUseCurRefAC) + ','
        command += str(fixedPosure) + ','
        command += str(nMoveCType) + ','
        command += str(nRadLen) + ','
        command += str(speed) + ','
        command += str(Acc) + ','
        command += str(radius) + ','
        command += str(tcp) + ','
        command += str(ucs) + ','
        command += str(cmdID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 18
    *	@brief: Start zigzag move / 开始Z型轨迹运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param StartPoint : Start pose / 开始位置
    *	@param EndPoint : End pose / 结束位置
    *	@param PlanePoint : Plane pose / 确定平面点位置
    *	@param Speed : Motion speed, mm/s / 运动速度，单位是毫米每秒
    *	@param Acc : Motion acceleration, mm/(s^2) / 运动加速度，毫米每秒平方
    *	@param WIdth : Width / 宽度
    *	@param Density : Density, mm / 密度，毫米
    *	@param EnableDensity : 0 is disable density and 1 for enable density / 是否使用密度(0:不使用，1:使用)
    *	@param EnablePlane : Use plane pose or not; UCS is automatically used if plane pose is not used / 是否使用平面点，不使用时根据选择的用户坐标确定XYZ平面
    *	@param EnableWaiTime : 0 for disable waiting time, 1 for enable waiting time / 是否开启转折点等待时间(0:不使用，1:使用)
    *	@param PosiTime : Waiting time (ms) for Positive turning point / 正向转折点等待时间ms
    *	@param NegaTime : Waiting time (ms) for Negative turning point / 负向转折点等待时间ms
    *	@param Radius : Blending radius, mm / 过渡半径，单位毫米
    *	@param tcp : TCP name / 工具坐标名称
    *	@param ucs : UCS name / 用户坐标名称
    *	@param cmdID : Command ID / 命令ID
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_MoveZ(self, boxID, rbtID, StartPoint, EndPoint, PlanePoint, Speed, Acc, WIdth, Density, EnableDensity,
                   EnablePlane, EnableWaiTime, PosiTime, NegaTime, Radius, tcp, ucs, cmdID):
        result = []
        command = 'MoveZ,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(StartPoint[i]) + ','
        for i in range(0, 6):
            command += str(EndPoint[i]) + ','
        for i in range(0, 6):
            command += str(PlanePoint[i]) + ','
        command += str(Speed) + ','
        command += str(Acc) + ','
        command += str(WIdth) + ','
        command += str(Density) + ','
        command += str(EnableDensity) + ','
        command += str(EnablePlane) + ','
        command += str(EnableWaiTime) + ','
        command += str(PosiTime) + ','
        command += str(NegaTime) + ','
        command += str(Radius) + ','
        command += str(tcp) + ','
        command += str(ucs) + ','
        command += str(cmdID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 19
    *	@brief: Start elliptical move / 开始椭圆轨迹运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param dP1 : Teaching p1 (p1~p5 should be listed as sequence in arc)/ 示教点1,示教点位必须按照轨迹顺序排列
    *	@param dP2 : Teaching p2 / 示教位置2
    *	@param dP3 : Teaching p3 / 示教位置3
    *	@param dP4 : Teaching p4 / 示教位置4
    *	@param dP5 : Teaching p5 / 示教位置5
    *	@param nOrientMode : 0 is for arc, 1 is for circle / 弧运动类型：0：圆弧，1：整圆
    *	@param nMoveType : 0 for unfixed orientation , 1 for fixed orientation  / 0:不使用固定姿态，1:使用固定姿态
    *	@param dArcLength : Arc length (mm) / 弧长
    *	@param dVelocity : Motion speed, mm/s / 运动速度，单位是毫米每秒
    *	@param dAcc : Motion acceleration, mm/(s^2) / 运动加速度，毫米每秒平方
    *	@param Radius : Blending radius, mm / 过渡半径，单位毫米
    *	@param tcp : TCP name / 工具坐标名称
    *	@param ucs : UCS name / 用户坐标名称
    *	@param cmdID : Command ID / 命令ID
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_MoveE(self, boxID, rbtID, dP1, dP2, dP3, dP4, dP5, nOrientMode, nMoveType, dArcLength, dVelocity, dAcc,
                   Radius, tcp, ucs, cmdID):
        result = []
        command = 'MoveE,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(dP1[i]) + ','
        for i in range(0, 6):
            command += str(dP2[i]) + ','
        for i in range(0, 6):
            command += str(dP3[i]) + ','
        for i in range(0, 6):
            command += str(dP4[i]) + ','
        for i in range(0, 6):
            command += str(dP5[i]) + ','
        command += str(nOrientMode) + ','
        command += str(nMoveType) + ','
        command += str(dArcLength) + ','
        command += str(dVelocity) + ','
        command += str(dAcc) + ','
        command += str(Radius) + ','
        command += str(tcp) + ','
        command += str(ucs) + ','
        command += str(cmdID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 20
    *	@brief: Start spiral move / 开始螺旋运动轨迹运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param dSpiralIncrement : Spiral Increment radius /  螺旋运动每圈增量半径
    *	@param dSpiralDiameter : Spiral end radius / 螺旋运动结束半径，单位[mm]
    *	@param dVelocity : Motion speed, mm/s / 运动速度，单位是毫米每秒
    *	@param dAcc : Motion acceleration, mm/(s^2) / 运动加速度，毫米每秒平方
    *	@param dRadius : Blending radius, mm / 过渡半径，单位毫米
    *	@param sTcpName : TCP name / 工具坐标名称
    *	@param sUcsName : UCS name / 用户坐标名称
    *	@param cmdID : Command ID / 命令ID
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_MoveS(self, boxID, rbtID, dSpiralIncrement, dSpiralDiameter, dVelocity, dAcc, dRadius, sTcpName, sUcsName,
                   cmdID):
        result = []
        command = 'MoveS,'
        command += str(rbtID) + ','
        command += str(dSpiralIncrement) + ','
        command += str(dSpiralDiameter) + ','
        command += str(dVelocity) + ','
        command += str(dAcc) + ','
        command += str(dRadius) + ','
        command += str(sTcpName) + ','
        command += str(sUcsName) + ','
        command += str(cmdID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 21
    *	@brief: Start relative joint move / 关节相对运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param nAxis: Axis ID , 0~5 for jonit 1 ~6 / 关节编号
    *	@param nDirection: Move direction, 0 for negative，1 for positive / 运动方向，1为正方向，0为负方向
    *	@param dDistance: Move distance (°) / 运动距离(°)
    '''
    def HRIF_MoveRelJ(self, boxID, rbtID, nAxis, nDirection, dDistance):
        result = []
        command = 'MoveRelJ,'
        command += str(rbtID) + ','
        command += str(nAxis) + ','
        command += str(nDirection) + ','
        command += str(dDistance) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 22
    *	@brief: Start relative linear move / 空间相对运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param nAxis: Pose ID, 0~5 for X, Y, Z, Rx, Ry, Rz / 空间坐标维度编号
    *	@param nDirection: Move direction, 0 for negative, 1 for positive / 运动方向，1为正方向，0为负方向
    *	@param dDistance: Move distance (mm or °) / 运动距离(mm或者°)
    *   @param nToolMotion: Tool motion, 0 for UCS based move, 1 for TCP based move / 运动坐标类型，0为按当前UCS，1为当前TCP
    '''
    def HRIF_MoveRelL(self, boxID, rbtID, nAxis, nDirection, dDistance, nToolMotion):
        result = []
        command = 'MoveRelL,'
        command += str(rbtID) + ','
        command += str(nAxis) + ','
        command += str(nDirection) + ','
        command += str(dDistance) + ','
        command += str(nToolMotion) + ','
        command += ';'
        # print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 23
    *	@brief: Start relative wayPoint / 路点相对运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param nType : Move type, 0 for joint, 1 for linear / 运动类型，0为关节运动，1为直线运动
    *	@param nPointList : Using point saved in points list or not, 0 for not using,  1 for using / 是否使用点位列表的点位，0为不使用，1为使用
    *	@param Pos : Target pose / 空间目标位置
    *   @param rawACT : Target joint positions / 关节目标位置
    *   @param nrelMoveType : Relative move type, 0 for absolute value, 1 for superimposed value / 相对运动类型，0为绝对值，1为叠加值
    *   @param nAxisMask : Is Axis/Direction Moving, 0 for not moving, 1 for moving / 各轴\各方向是否运动，0为不运动，1为运动
    *   @param dTarget : Moving distance; invalid when nAxisMask equals 0; joint move an absolute or superimposed distance when nAxisMask equals 1 and nType equals 0; Pose move an absolute or superimposed distance when nAxisMask equals 1 and nType equals 1 / 运动距离，nType=0 并 nAxisMask=1：该关节运动绝对距离或叠加距离；nType=1 并 nAxisMask=1：该坐标运动绝对距离或叠加距离；nAxisMask=0：本参数无效
    *   @param sTcpName : Target TCP name / 工具坐标系名称
    *   @param sUcsName : Target UCS name / 用户坐标系名称
    *   @param dVelocity : Velocity (mm/s) or (°/s) / 运动速度，关节运动时单位(°/s)，空间运动时 X，Y，Z 单位(mm/s)，Rx，Ry，Rz 单位(°/s)
    *   @param dAcc : Acceleration (mm/s^2) or (°/s^2) / 运动加速度，关节运动时单位(°/s^2)，空间运动时 X，Y，Z 单位(mm/s^2)，Rx，Ry，Rz 单位(°/s^2)
    *   @param dRadius : Blending radius, mm / 过渡半径，单位毫米
    *	@param isJoint : Using joint or not, usable when MoveType equals 0, 0 for not using joint, 1 for using joint / 是否使用关节角度，是否使用关节角度作为目标点，仅当nMoveType=0时本参数有效。0：不使用关节角度1：使用关节角度
    *	@param isSeek,bit,state: Seeking or not, 1 for seeking; Motion stops when DO-nIOBit equals nIoState / 探寻参数，当nIsSeek为1，则开启探寻，这时电箱的DO nIOBit位为nIOState时，就停止运动，否则运动到目标点再停止
    *	@param cmdID: Command ID, waypoint ID also, customized or set to 1, 2, 3 in order / 当前路点ID，可以自定义，也可以按顺序设置为“1”，“2”，“3”
    '''
    def HRIF_WayPointRel(self, boxID, rbtID, nType, nPointList, Pos, rawACT, nrelMoveType, nAxisMask, dTarget, sTcpName,
                         sUcsName, dVelocity, dAcc, dRadius, nIsUseJoint, nIsSeek, nIOBit, nIOState, strcmdID):
        result = []
        command = 'WayPointRel,'
        command += str(rbtID) + ','
        command += str(nType) + ','
        command += str(nPointList) + ','

        for i in range(0, 6):
            command += str(Pos[i]) + ','

        for i in range(0, 6):
            command += str(rawACT[i]) + ','

        command += str(nrelMoveType) + ','

        for i in range(0, 6):
            command += str(nAxisMask[i]) + ','

        for i in range(0, 6):
            command += str(dTarget[i]) + ','

        command += str(sTcpName) + ','
        command += str(sUcsName) + ','
        command += str(dVelocity) + ','
        command += str(dAcc) + ','
        command += str(dRadius) + ','
        command += str(nIsUseJoint) + ','
        command += str(nIsSeek) + ','
        command += str(nIOBit) + ','
        command += str(nIOState) + ','
        command += str(strcmdID) + ',;'
        # print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 24
    *	@brief: Start relative wayPoint / 路点相对运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param nType : Move type, 0 for joint, 1 for linear / 运动类型，0为关节运动，1为直线运动
    *	@param nPointList : Using point saved in points list or not, 0 for not using,  1 for using / 是否使用点位列表的点位，0为不使用，1为使用
    *	@param Pos : Target pose / 空间目标位置
    *   @param rawACT : Target joint positions / 关节目标位置
    *   @param nrelMoveType : Relative move type, 0 for absolute value, 1 for superimposed value / 相对运动类型，0为绝对值，1为叠加值
    *   @param nAxisMask : Is Axis/Direction Moving, 0 for not moving, 1 for moving / 各轴\各方向是否运动，0为不运动，1为运动
    *   @param dTarget : Moving distance; invalid when nAxisMask equals 0; joint move an absolute or superimposed distance when nAxisMask equals 1 and nType equals 0; Pose move an absolute or superimposed distance when nAxisMask equals 1 and nType equals 1 / 运动距离，nType=0 并 nAxisMask=1：该关节运动绝对距离或叠加距离；nType=1 并 nAxisMask=1：该坐标运动绝对距离或叠加距离；nAxisMask=0：本参数无效
    *   @param sTcpName : Target TCP name / 工具坐标系名称
    *   @param sUcsName : Target UCS name / 用户坐标系名称
    *   @param dVelocity : Velocity (mm/s) or (°/s) / 运动速度，关节运动时单位(°/s)，空间运动时 X，Y，Z 单位(mm/s)，Rx，Ry，Rz 单位(°/s)
    *   @param dAcc : Acceleration (mm/s^2) or (°/s^2) / 运动加速度，关节运动时单位(°/s^2)，空间运动时 X，Y，Z 单位(mm/s^2)，Rx，Ry，Rz 单位(°/s^2)
    *   @param dRadius : Blending radius, mm / 过渡半径，单位毫米
    *	@param isJoint : Using joint or not, usable when MoveType equals 0, 0 for not using joint, 1 for using joint / 是否使用关节角度，是否使用关节角度作为目标点，仅当nMoveType=0时本参数有效。0：不使用关节角度1：使用关节角度
    *	@param isSeek,bit,state: Seeking or not, 1 for seeking; Motion stops when DO-nIOBit equals nIoState / 探寻参数，当nIsSeek为1，则开启探寻，这时电箱的DO nIOBit位为nIOState时，就停止运动，否则运动到目标点再停止
    *	@param cmdID: Command ID, waypoint ID also, customized or set to 1, 2, 3 in order / 当前路点ID，可以自定义，也可以按顺序设置为“1”，“2”，“3”
    '''
    def HRIF_WayPointRel_nJ(self, boxID, rbtID, nType, nPointList, Pos, rawACT, nrelMoveType, nAxisMask, dTarget, sTcpName,
                         sUcsName, dVelocity, dAcc, dRadius, nIsUseJoint, nIsSeek, nIOBit, nIOState, strcmdID):
        result = []
        command = 'WayPointRel,'
        command += str(rbtID) + ','
        command += str(nType) + ','
        command += str(nPointList) + ','

        for i in range(0, 6):
            command += str(Pos[i]) + ','

        for i in range(0, len(rawACT)):
            command += str(rawACT[i]) + ','

        command += str(nrelMoveType) + ','

        for i in range(0, 6):
            command += str(nAxisMask[i]) + ','

        for i in range(0, 6):
            command += str(dTarget[i]) + ','

        command += str(sTcpName) + ','
        command += str(sUcsName) + ','
        command += str(dVelocity) + ','
        command += str(dAcc) + ','
        command += str(dRadius) + ','
        command += str(nIsUseJoint) + ','
        command += str(nIsSeek) + ','
        command += str(nIOBit) + ','
        command += str(nIOState) + ','
        command += str(strcmdID) + ',;'
        # print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 25
    *	@brief: Check temperature under low / 检查温度是否低于低温阈值
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0]: 1 as under low, 0 as not under low / 1:低于低温阈值，0不低于低温阈值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_CheckTemperatureUnderLow(self, boxID, rbtID, result):
        command = 'CheckTemperatureUnderLow,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 26
    *	@brief: Start linear weave move / 开始直线摆焊运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param StartPoint : Start pose / 开始点位置
    *	@param EndPoint : End pose / 结束点位置
    *	@param dVelocity : Motion speed, mm/s / 运动速度，单位是毫米每秒
    *	@param Acc : Motion acceleration, mm/(s^2) / 运动加速度，毫米每秒平方
    *	@param dRadius : Blending radius, mm / 过渡半径，单位毫米
    *	@param dAmplitude : Weaving amplitude, mm / 宽度，摆焊的幅值，单位:mm
    *	@param dIntervalDistance : Referenced weaving interval, robot will rectify it slightly to ensure the StartPos and EndPos be passed through after some weaving cycles, mm 
    *                            / 摆焊的间距，此值仅供参考，机器人系统会自动微调该值以确保运动轨迹经过若干个完整周期的摆动后能通过起始点和结束点，单位:mm
    *	@param nWeaveFrameType : the way to determine the weaving plane and weaving direction / 用于决定摆焊平面和摆焊方向的选择方式
    *                            0: The +X of weaving plane is from StartPos to EndPos. The +Z(normal direction) of weaving plane is along TCP +Z. The +Y of weaving plane is determined by +X and +Z. The start direction of weaving move is toward the +Y side
    *                            1: The +X of weaving plane is from StartPos to EndPos. The Z of weaving plane is parallel with TCP Z. The +Y of weaving plane is along TCP +Y. The start direction of weaving move is toward the +Y side                            
    *                            / 0：摆焊平面的+X方向为从StartPos到EndPos，+Z方向（即摆焊平面的法线方向）为跟工具坐标系的+Z相同的方向，+Y方向由右手定则确定。摆焊启动时的运动方向跟+Y方向同侧
    *                            / 1：摆焊平面的+X方向为从StartPos到EndPos，Z方向跟刀具坐标系的Z方向平行，+Y方向跟工具坐标系的+Y方向同侧。摆焊启动时的运动方向跟+Y方向同侧    
    *	@param dElevation : The elevation of the weave, degree / 摆焊的仰角，单位:度
    *	@param dAzimuth : The azimuth of the weave, degree / 摆焊的方向角，即绕摆焊平面法向量的旋转角，单位:度
    *	@param dCentreRise : The bulge height of the welding torch at the weaving weld center, mm / 摆焊的中心隆起量，即摆焊中心处焊炬的隆起量，单位:mm
    *   @param nEnableWaiTime : 0 to disable waiting time, 1 to enable waiting time / 是否开启转折点等待时间(0:不使用，1:使用)
    *	@param nPosiTime : Waiting time (ms) at Positive turning point / 正向转折点等待时间ms
    *	@param nNegaTime : Waiting time (ms) at Negative turning point / 负向转折点等待时间ms
    *	@param sTcpName : TCP name / 工具坐标名称
    *	@param sUcsName : UCS name / 用户坐标名称
    *	@param sCmdID : Command ID / 命令ID
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_MoveLinearWeave(self, boxID, rbtID, StartPoint, EndPoint, dVelocity, Acc, dRadius, dAmplitude,
                             dIntervalDistance, nWeaveFrameType,
                             dElevation, dAzimuth, dCentreRise, nEnableWaiTime, nPosiTime, nNegaTime, sTcpName,
                             sUcsName, sCmdID, result):
        command = 'MoveLinearWeave,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(StartPoint[i]) + ','
        for i in range(0, 6):
            command += str(EndPoint[i]) + ','
        command += str(dVelocity) + ','
        command += str(Acc) + ','
        command += str(dRadius) + ','
        command += str(dAmplitude) + ','
        command += str(dIntervalDistance) + ','
        command += str(nWeaveFrameType) + ','
        command += str(dElevation) + ','
        command += str(dAzimuth) + ','
        command += str(dCentreRise) + ','
        command += str(nEnableWaiTime) + ','
        command += str(nPosiTime) + ','
        command += str(nNegaTime) + ','
        command += str(sTcpName) + ','
        command += str(sUcsName) + ','
        command += str(sCmdID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 27
    *	@brief: circular weave move / 圆弧摆焊运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param StartPoint : Start pose / 开始点位置
    *	@param AuxPoint : Via pose / 经过点位置    
    *	@param EndPoint : End pose / 结束点位置
    *	@param dVelocity : Motion speed, mm/s / 运动速度，单位是毫米每秒
    *	@param Acc : Motion acceleration, mm/(s^2) / 运动加速度，毫米每秒平方
    *	@param dRadius : Blending radius, mm / 过渡半径，单位毫米
    *	@param nOrientMode : 0 for unfixed orientation, 1 for fixed orientation  / 0:不使用固定姿态，1:使用固定姿态
    *	@param nMoveWhole : 0: 0 for circle, 1 for arc / 整圆轨迹，1:圆弧轨迹，
    *	@param dMoveWholeLen :Invalid when nMoveCType equals 1; Circles when nMoveCType equals 0. / 当使用圆弧运动时该参数无效，通过计算三个点位来确定圆弧路径及弧度；当使用整圆运动时表示整圆的圈数
    *	@param dAmplitude : Amplitude, mm / 宽度，摆焊的幅值，单位:mm
    *	@param dIntervalDistance :Referenced weaving interval, robot will rectify it slightly to ensure the StartPos and EndPos be passed through after some weaving cycles, mm 
    *                             / 摆焊的间距，此值仅供参考，机器人系统会自动微调该值以确保运动轨迹经过若干个完整周期的摆动后能通过起始点和结束点，单位:mm
    *	@param nWeaveFrameType : the way to determine the weaving plane and weaving direction / 用于决定摆焊平面和摆焊方向的选择方式
    *                            0: The +X of weaving plane is from StartPos to EndPos. The +Z(normal direction) of weaving plane is along TCP +Z. The +Y of weaving plane is determined by +X and +Z. The start direction of weaving move is toward the +Y side
    *                            1: The +X of weaving plane is from StartPos to EndPos. The Z of weaving plane is parallel with TCP Z. The +Y of weaving plane is along TCP +Y. The start direction of weaving move is toward the +Y side                            
    *                            / 0：摆焊平面的+X方向为从StartPos到EndPos，+Z方向（即摆焊平面的法线方向）为跟工具坐标系的+Z相同的方向，+Y方向由右手定则确定。摆焊启动时的运动方向跟+Y方向同侧
    *                            / 1：摆焊平面的+X方向为从StartPos到EndPos，Z方向跟刀具坐标系的Z方向平行，+Y方向跟工具坐标系的+Y方向同侧。摆焊启动时的运动方向跟+Y方向同侧   。    
    *	@param dElevation : The elevation of the weave, degree / 摆焊的仰角，单位:度
    *	@param dAzimuth : The azimuth of the weave, degree /摆焊的方向角，即绕摆焊平面法向量的旋转角，单位:度
    *	@param dCentreRise : The bulge height of the welding torch at the weaving weld center, mm / 摆焊的中心隆起量，即摆焊中心处焊炬的隆起量，单位:mm
    *   @param nEnableWaiTime : 0 to disable waiting time, 1 to enable waiting time / 是否开启转折点等待时间(0:不使用，1:使用)
    *	@param nPosiTime : Waiting time (ms) at Positive turning point / 正向转折点等待时间ms
    *	@param nNegaTime : Waiting time (ms) at Negative turning point / 负向转折点等待时间ms
    *	@param sTcpName : TCP name / 工具坐标名称
    *	@param sUcsName : UCS name / 用户坐标名称
    *	@param sCmdID : Command ID / 命令ID
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_MoveCircularWeave(self, boxID, rbtID, StartPoint, AuxPoint, EndPoint, dVelocity, Acc, dRadius, nOrientMode,
                               nMoveWhole, dMoveWholeLen, dAmplitude, dIntervalDistance, nWeaveFrameType,
                               dElevation, dAzimuth, dCentreRise, nEnableWaiTime, nPosiTime, nNegaTime, sTcpName,
                               sUcsName, sCmdID, result):
        command = 'MoveCircularWeave,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(StartPoint[i]) + ','
        for i in range(0, 6):
            command += str(AuxPoint[i]) + ','
        for i in range(0, 6):
            command += str(EndPoint[i]) + ','
        command += str(dVelocity) + ','
        command += str(Acc) + ','
        command += str(dRadius) + ','
        command += str(nOrientMode) + ','
        command += str(nMoveWhole) + ','
        command += str(dMoveWholeLen) + ','
        command += str(dAmplitude) + ','
        command += str(dIntervalDistance) + ','
        command += str(nWeaveFrameType) + ','
        command += str(dElevation) + ','
        command += str(dAzimuth) + ','
        command += str(dCentreRise) + ','
        command += str(nEnableWaiTime) + ','
        command += str(nPosiTime) + ','
        command += str(nNegaTime) + ','
        command += str(sTcpName) + ','
        command += str(sUcsName) + ','
        command += str(sCmdID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    #
    # part 11 Interface of Trajectory Motion Control / 连续轨迹运动类控制指令
    #
    '''
    *	@index : 1
    *	@param brief: Start to push ACS points for MovePathJ / 初始化关节连续轨迹运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param trackName : MovePathJ name / 轨迹名称
    *	@param speedRatio : Speed override / 运动速度
    *	@param radius : Blending radius, mm / 过渡半径，单位毫米
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_StartPushMovePathJ(self, boxID, rbtID, trackName, speedRatio, radius):
        result = []
        command = 'StartPushMovePath,'
        command += str(rbtID) + ','
        command += trackName + ','
        command += str(speedRatio) + ','
        command += str(radius) + ','
        command += ';'
        # print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 2
    *	@param brief: Push an ACS raw point to MovePathJ. 4 points at lease are needed. / 添加运动轨迹点，可多次调用此函数，一般情况下点位数量需要>=4
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param trackName : MovePathJ name / 轨迹名称
    *	@param paramsJ[0]-paramsJ[5] : joint positions / 关节位置
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_PushMovePathJ(self, boxID, rbtID, trackName, paramsJ):
        result = []
        command = 'PushMovePathJ,'
        command += str(rbtID) + ','
        command += trackName
        command += ','
        for i in range(0, 6):
            command += str(paramsJ[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 3
    *	@param brief: End pushing ACS raw point to MovePathJ and start calculating the path / 结束向轨迹中推送点位，并开始计算轨迹
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param trackName : MovePathJ name / 轨迹名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_EndPushMovePathJ(self, boxID, rbtID, trackName):
        result = []
        command = 'EndPushMovePath,'
        command += str(rbtID) + ','
        command += trackName + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 4
    *	@param brief: End pushing PCS raw point to MovePathL and start calculating the path / 结束向轨迹中推送点位，并开始计算轨迹
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param trackName : MovePathL name / 轨迹名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_EndPushMovePath(self, boxID, rbtID, trackName):
        result = []
        command = 'EndPushMovePath,'
        command += str(rbtID) + ','
        command += trackName + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    # '''
    # *	@index : 5
    # *	@param brief:执行轨迹运动
    # *	@param boxID: Control box ID / 电箱ID号
    # *	@param rbtID: Robot ID / 机器人ID,一般为0
    # *	@param trackName : 轨迹名称
    # *	
    # *	@return : nRet=0 : Function call succeeded / 函数调用成功
    # *             nRet>0 : Error code of function call / 函数调用失败的错误码
    # '''
    # def HRIF_MovePath(self,boxID,rbtID,trajectName):
    #     result = []
    #     command = 'MovePath,'
    #     command += str(rbtID) + ','
    #     command += str(trajectName) + ','
    #     command += ';'
    #     return self.g_clients[boxID].sendAndRecv(command,result)

    '''
    *	@index : 5
    *	@param brief: Run PathJ / 以关节运动的方式运行指定的轨迹
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param sPathName : Path name / 轨迹名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_MovePathJ(self, boxID, rbtID, sPathName):
        result = []
        command = 'MovePathJ,'
        command += str(rbtID) + ','
        command += str(sPathName) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 6
    *	@param brief: Read the status of the path / 读取当前的轨迹状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param trackName : Path name / 轨迹名称
    *	@param result[0] : State of path / 轨迹状态  
    *               0: Not taught / 0: 轨迹未示教
    *               1: Teaching in progress / 1: 轨迹示教中
    *               2: Calculating / 2: 轨迹计算中
    *               3: Calculation completed / 3: 轨迹完成计算
    *               4: Teaching completed / 4: 轨迹完成示教
    *               5:Calculation error / 5: 轨迹计算错误
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadMovePathJState(self, boxID, rbtID, trackName, result):
        command = 'ReadMovePathState,'
        command += str(rbtID) + ','
        command += trackName + ','
        command += ';'
        retData = self.g_clients[boxID].sendAndRecv(command, result)
        return retData

    '''
    *	@index : 7
    *	@param brief: Update MovePathJ name / 更新指定轨迹名称
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param trackName : MovePathJ name / 轨迹名称
    *	@param newName : New MovePathJ name / 新轨迹名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_UpdateMovePathJName(self, boxID, rbtID, trackName, newName):
        result = []
        command = 'UpdateMovePathName,'
        command += str(rbtID) + ','
        command += trackName + ','
        command += newName + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 8
    *	@param brief: Delete a MovepathJ / 删除指定轨迹
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param trackName : MovePathJ name / 需要删除的轨迹名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_DelMovePathJ(self, boxID, rbtID, trackName):
        result = []
        command = 'DelMovePath,'
        command += str(rbtID) + ','
        command += trackName + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 9
    *	@param brief: Read process and point index of a path move / 读取轨迹运动进度，仅对MovePathL生效，建议读取频率保持在20ms上下
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *   @param result[0] : Current path process, 0~1, more than 0.999999 for move done / 当前运动进度(0-1),>0.999999表示运动完成
    *   @param result[1] : Point index finished / 当前轨迹运动到的点位索引
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadTrackProcess(self, boxID, rbtID, result):
        command = 'ReadSoftMotionProgress,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 10
    *	@param brief: Initialize MovePathL / 初始化MovePathL
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param trackName : MovePathL name / 轨迹名称
    *	@param vel : Velocity / 运动速度
    *	@param acc : Acceleration / 运动加速度
    *	@param jerk : Jerk / 运动加加速度
    *	@param ucs : UCS name / 指定轨迹所在的用户坐标系名称
    *	@param tcp : TCP name / 指定轨迹所在的工具坐标值名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_InitMovePathL(self, boxID, rbtID, trackName, vel, acc, jerk, ucs, tcp):
        result = []
        command = 'InitMovePathL,'
        command += str(rbtID) + ','
        command += trackName + ','
        command += str(vel) + ','
        command += str(acc) + ','
        command += str(jerk) + ','
        command += ucs + ','
        command += tcp + ','
        command += ';'
        # print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 11
    *	@param brief: Push an PCS point to MovePathL / 下发MovePathL点位-调用一次下发一个目标点位
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param trackName : MovePathL name / 轨迹名称
    *	@param paramPcs : Raw point pose / 空间点位
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_PushMovePathL(self, boxID, rbtID, trackName, paramPcs):
        result = []
        command = 'PushMovePathL,'
        command += str(rbtID) + ','
        command += trackName + ','
        for i in range(0, 6):
            command += str(paramPcs[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 12
    *	@param brief: Push an list of ACS or PCS points to MovePathJ or MovePathL / 批量下发MovePathJ/MovePathL点位-调用一次可下发多个点位数据
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param trackName : MovePathJ or MovePathL name / 轨迹名称
    *	@param moveType : Move type, 0 for MovePathJ, 1 for MovePathL / 运动类型-0(MovePathJ)/1(MovePathL)
    *	@param pointsSize : Points number / 轨迹点位数量
    *	@param points : Points list / 轨迹点列表
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_PushMovePaths(self, boxID, rbtID, trackName, moveType, pointsSize, points):
        result = []
        command = 'PushMovePaths,'
        command += str(rbtID) + ','
        command += trackName
        command += ','
        command += str(moveType)
        command += ','
        command += str(pointsSize)
        command += ','
        for pos in points:
            command += str(pos) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 13
    *	@param brief: Run PathL / 运行PathL
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param sPathName : Path name / 轨迹名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_MovePathL(self, boxID, rbtID, sPathName):
        result = []
        command = 'MovePathL,'
        command += str(rbtID) + ','
        command += str(sPathName) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 14
    *	@param brief: Set Override for MovePathL / 设置轨迹运动速度比，轨迹运动中设置有效。仅对MovePathL生效
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param MovePathOverride : Set Override / 设置速度比
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetMovePathOverride(self, boxID, rbtID, MovePathOverride):
        result = []
        command = 'SetMovePathOverride,'
        command += str(rbtID) + ','
        command += str(MovePathOverride)
        command += ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 15
    *	@param brief: Initialize path / 初始化轨迹
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *   @param nRawDataType: Raw points data type, 0 for ACS, 1 for PCS / 原始点位数据类型 0：关节点位 1：空间点位
    *	@param sPathName : Path name / 轨迹名称
    *	@param vel : Velocity for PathL calculation / 运动速度
    *	@param acc : Acceleration for PathL calculation / 运动加速度
    *	@param jerk : Jerk for PathL calculation / 运动加加速度
    *	@param ucs : UCS name / 指定轨迹所在的用户坐标系名称
    *	@param tcp : TCP name / 指定轨迹所在的工具坐标值名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_InitPath(self, boxID, rbtID, nRawDataType, sPathName, dSpeedRatio, dRadius, vel, acc, jerk, ucs, tcp):
        result = []
        command = 'InitPath,'
        command += str(rbtID) + ','
        command += str(nRawDataType) + ','
        command += sPathName + ','
        command += str(dSpeedRatio) + ','
        command += str(dRadius) + ','
        command += str(vel) + ','
        command += str(acc) + ','
        command += str(jerk) + ','
        command += ucs + ','
        command += tcp + ','
        command += ';'
        # print(command)
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 16
    *	@param brief: Push raw points to path / 向轨迹中批量推送原始点位（可多次调用）(MovePathJ/MovePathL均有效)
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param sPathName : Path name / 轨迹名称
    *	@param sPoints : Points data / 点位数据
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_PushPathPoints(self, boxID, rbtID, sPathName, sPoints):
        result = []
        command = 'PushPathPoints,'
        command += str(rbtID) + ','
        command += sPathName
        command += ','
        for pos in sPoints:
            command += str(pos) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 17
    *	@param brief: End pushing points to the path and start calculating the pathJ/L / 结束向轨迹中推送点位，并开始计算轨迹(MovePathJ/MovePathL均有效)
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param sPathName : Path name / 轨迹名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_EndPushPathPoints(self, boxID, rbtID, sPathName):
        result = []
        command = 'EndPushPathPoints,'
        command += str(rbtID) + ','
        command += sPathName + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 18
    *	@param brief: Delete the Path with the specified name / 删除指定轨迹(MovePathJ/MovePathL均有效)
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param sPathName : Path name / 轨迹名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_DelPath(self, boxID, rbtID, sPathName):
        result = []
        command = 'DelPath,'
        command += str(rbtID) + ','
        command += sPathName + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 19
    *	@param brief: Read all path lists / 读取所有轨迹列表
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result: path name list / 轨迹列表   
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadPathList(self, boxID, rbtID, result):
        command = 'ReadPath,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 20
    *	@param brief: Read the information of the specified name path / 读取指定名称轨迹的信息
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param sPathName : Path name / 轨迹名称
    *	@param result[0] : Raw point type, 0 for ACS, 1 for PCS / 原始点位类型 0：关节点位 1：空间点位
    *	@param result[1] : PathJ status: / PathJ的状态 
    *                       0: Not taught, 1: Teaching in progress, 4: Teaching completed, 2: Calculating, 5: Calculation error, 3: Calculation completed, 9: Imported, 10: Post-import processing 
    *                       /0: 未示教 1: 示教中 4：示教完 2：计算中 5：计算出错 3：计算完成 9：已导入 10：导入后处理
    *	@param result[2] : PathJ error code / PathJ的错误码
    *	@param result[3] : The state of PathL, the same as stateJ / PathL的状态，同stateJ
    *	@param result[4] : PathL error code / PathL的错误码
    *	@param result[5] : Path speed ratio / 轨迹运动速度比
    *	@param result[6] : Blending radius, mm / 过渡半径，单位：mm
    *	@param result[7] : Velocity for Path / 轨迹运动速度，单位：mm/s
    *	@param result[8] : Acceleration for Path / 轨迹运动加速度，单位：mm/s^2
    *	@param result[9] : Jerk for Path / 轨迹运动加加速度，单位：mm/s^3
    *	@param result[10] : User coordinates / 用户坐标
    *	@param result[11] : Tool coordinates / 工具坐标
    *	@param result[12] : Raw points count / 原始点位个数
    *	@param result[13] : The first raw point coordinates (J1/J2/J3/J4/J5/J6 or X/Y/Z/RX/RY/RZ) / 第一个原始点位坐标(J1/J2/J3/J4/J5/J6 或 X/Y/Z/RX/RY/RZ)
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadPathInfo(self, boxID, rbtID, sPathName, result):
        command = 'ReadPath,'
        command += str(rbtID) + ','
        command += sPathName + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 21
    *	@param brief: Update the name of the specified path / 更新指定轨迹的名称(MovePathJ/MovePathL均有效)
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param sPathName : Path name / 轨迹名称
    *	@param sPathNewName : New path name / 新轨迹名称
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_UpdatePathName(self, boxID, rbtID, sPathName, sPathNewName):
        result = []
        command = 'UpdatePathName,'
        command += str(rbtID) + ','
        command += sPathName + ','
        command += sPathNewName + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 22
    *	@param brief: Read the status of the path / 读取轨迹的状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param sPathName : Path name / 轨迹名称
    *	@param result[0] : State of MovePathJ refer to HRIF_ReadPathInfo / PathJ的状态， 参见HRIF_ReadPathInfo
    *	@param result[1] : nErrorCodeJ / PathJ的错误码
    *	@param result[2] : State of MovePathL refer to HRIF_ReadPathInfo / PathL的状态， 参见HRIF_ReadPathInfo
    *	@param result[3] : nErrorCodeL / PathL的错误码
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadPathState(self, boxID, rbtID, sPathName, result):
        command = 'ReadPathState,'
        command += str(rbtID) + ','
        command += sPathName + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 23
    *	@param brief: Set the reference joint coordinates for space point trajectory/ 设置空间点位轨迹参考关节坐标
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param sPathName : Path name / 轨迹名称
    *	@param dAcs : Reference joint coordinates / 参考关节坐标
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetPathRefJoints(self, boxID, rbtID, sPathName,dAcs):
        command = 'SetPathRefJoints,'
        command += str(rbtID) + ','
        command += sPathName + ','
        for i in range(6):
            command += str(dAcs[i]) + ','
        command += ';'
        print(command)
        result = []
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 24
    *	@param brief: Start MovePathJ for online implementation planning / 启动在线实施规划的MovePathJ
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param dVel : Joint velocitie / 关节速度
    *   @param dAcc : Joint acceleration / 关节加速度
    *   @param dTol : Filter parameter / 过渡参数
    *	@param RawACSpoints : Target joint pose / 目标关节位置
    *	@param nIsSetIO : Is set IO, 0 as set, 1 as not set / 各点是否设置IO，0：该点位运动结束时要设置IO，1：该点位运动结束时不设置IO
    *	@param nEndDOMask : The EndDO to be modified is identified by bit / 需要更改的EndDO按bit标识
    *	@param nEndDOVal : The target state of each EndDO to be modified./ 各个需要更改的EndDO的目标状态
    *	@param nBoxDOMask : The BoxDO to be modified is identified by bit. / 需要更改的BoxDO按bit标识
    *	@param nBoxDOVal : The target state of each BoxDO to be modified. / 各个需要更改的BoxDO的目标状态
    *	@param nBoxCOMask : The BoxCO to be modified is identified by bit / 需要更改的BoxCO按bit标识
    *	@param nBoxCOVal : The target state of each BoxCO to be modified / 各个需要更改的BoxCO的目标状态
    *	@param nBoxAOCH0_Mask : Indicator of whether BoxAOCH0 needs to be modified. / BoxAOCH0是否需要更改的标识
    *	@param nBoxAOCH0_Mode : Mode / 模式
    *	@param nBoxAOCH1_Mask : Indicator of whether BoxAOCH1 needs to be modified. / BoxAOCH1是否需要更改的标识
    *	@param nBoxAOCH1_Mode : Mode / 模式
    *	@param dbBoxAOCH0_Val : Corresponding analog value / 对应模拟量值
    *	@param dbBoxAOCH1_Val : Corresponding analog value / 对应模拟量值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_MovePathJOL(self, boxID, rbtID, dVel, dAcc, dTol, RawACSpoints, nIsSetIO, nEndDOMask, nEndDOVal,
                         nBoxDOMask, nBoxDOVal, nBoxCOMask, nBoxCOVal, nBoxAOCH0_Mask, nBoxAOCH0_Mode, nBoxAOCH1_Mask,
                         nBoxAOCH1_Mode, dbBoxAOCH0_Val, dbBoxAOCH1_Val):
        result = []
        command = 'MovePathJOL,'
        command += str(rbtID) + ','
        command += str(dVel) + ','
        command += str(dAcc) + ','
        command += str(dTol) + ','
        for i in range(0, len(nIsSetIO)):
            for j in range(6*i, 6*i+6):
                command += str(RawACSpoints[j]) + ','
            command += str(nIsSetIO[i]) + ','
            command += str(nEndDOMask[i]) + ','
            command += str(nEndDOVal[i]) + ','
            command += str(nBoxDOMask[i]) + ','
            command += str(nBoxDOVal[i]) + ','
            command += str(nBoxCOMask[i]) + ','
            command += str(nBoxCOVal[i]) + ','
            command += str(nBoxAOCH0_Mask[i]) + ','
            command += str(nBoxAOCH0_Mode[i]) + ','
            command += str(nBoxAOCH1_Mask[i]) + ','
            command += str(nBoxAOCH1_Mode[i]) + ','
            command += str(dbBoxAOCH0_Val[i]) + ','
            command += str(dbBoxAOCH1_Val[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    '''
    *	@index : 25
    *	@param brief: Obtain the index number of the current point position of MovePathJOL motion and the total number of points in the trajectory motion / 获取MovePathJOL运动当前的点位索引号及轨迹运动所有点总数
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param dVel : Joint velocitie / 关节速度
    *   @param dAcc : Joint acceleration / 关节加速度
    *   @param dTol : Filter parameter / 过渡参数
    *	@param RawACSpoints : Target joint pose / 目标关节位置
    *	@param nIsSetIO : Is set IO, 0 as set, 1 as not set / 各点是否设置IO，0：该点位运动结束时要设置IO，1：该点位运动结束时不设置IO
    *	@param nEndDOMask : The EndDO to be modified is identified by bit / 需要更改的EndDO按bit标识
    *	@param nEndDOVal : The target state of each EndDO to be modified./ 各个需要更改的EndDO的目标状态
    *	@param nBoxDOMask : The BoxDO to be modified is identified by bit. / 需要更改的BoxDO按bit标识
    *	@param nBoxDOVal : The target state of each BoxDO to be modified. / 各个需要更改的BoxDO的目标状态
    *	@param nBoxCOMask : The BoxCO to be modified is identified by bit / 需要更改的BoxCO按bit标识
    *	@param nBoxCOVal : The target state of each BoxCO to be modified / 各个需要更改的BoxCO的目标状态
    *	@param nBoxAOCH0_Mask : Indicator of whether BoxAOCH0 needs to be modified. / BoxAOCH0是否需要更改的标识
    *	@param nBoxAOCH0_Mode : Mode / 模式
    *	@param nBoxAOCH1_Mask : Indicator of whether BoxAOCH1 needs to be modified. / BoxAOCH1是否需要更改的标识
    *	@param nBoxAOCH1_Mode : Mode / 模式
    *	@param dbBoxAOCH0_Val : Corresponding analog value / 对应模拟量值
    *	@param dbBoxAOCH1_Val : Corresponding analog value / 对应模拟量值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_GetMovePathJOLIndex(self, rbtID, boxID, result):
        command = 'GetMovePathJOLIndex,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
    #
    # part 12 Interfaces for Servo / 伺服控制类函数接口
    #

    '''
    *	@index : 1
    *	@param brief:  Start Servo J/P with the specified ServoTime of update and LookaheadTime. This function is a member of the suite including HRIF_StartServo, HRIF_PushServoJ and HRIF_PushServoP / 启动机器人在线控制(servoJ 或 servoP)时,设定位置固定更新的周期和前瞻时间
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param servoTime : interval of update (s) / 固定更新的周期 s
    *	@param lookaheadTime : LookaheadTime (s) / 前瞻时间 s
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_StartServo(self, boxID, rbtID, servoTime, lookaheadTime):
        result = []
        command = 'StartServo,'
        command += str(rbtID) + ','
        command += str(servoTime) + ',' + str(lookaheadTime) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 2
    *	@param brief: Push point of joint positions to robot with the ServoTime and LookaheadTime specified in HRIF_StartServo function, and the robot will track the joint positions in real time. This function is a member of the suite including HRIF_StartServo, HRIF_PushServoJ and HRIF_PushServoP / 在线关节位置命令控制，以 StartServo 设定的固定更新时间发送关节位置，机器人将实时的跟踪关节位置指令
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param dACSd : Joint positions / 关节点位
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_PushServoJ(self, boxID, rbtID, dACS):
        result = []
        command = 'PushServoJ,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(dACS[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 3
    *	@param brief: Push pose point to robot with the ServoTime and LookaheadTime specified in HRIF_StartServo function, and the robot will track the pose in real time. This function is a member of the suite including HRIF_StartServo, HRIF_PushServoJ and HRIF_PushServoP / 在线末端TCP位置命令控制,以 StartServo 设定的固定更新时间发送 TCP 位置，机器人将实时的跟踪目标 TCP 位置逆运算转换后的关节位置指令
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param pose : Pose coordinates / 更新的目标迪卡尔坐标位置
    *	@param ucs : UCS coordinates / 用户坐标
    *	@param tcp : TCP coordinates / 工具坐标
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_PushServoP(self, boxID, rbtID, pose, ucs, tcp):
        result = []
        command = 'PushServoP,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(pose[i]) + ','
        for i in range(0, 6):
            command += str(ucs[i]) + ','
        for i in range(0, 6):
            command += str(tcp[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 4
    *	@param brief: In SpeedJ mode,Push joint command velocity / 在SpeedJ模式下，下发关节命令速度指令
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param cmdVel : Joint speed / 更新的各关节命令关节速度，单位：°/s
    *	@param acc : Joint Acc / 关节设定加速度，单位：°/s^2
    *	@param runtime : Command execution exceeds this time, the movement will stop / 指令运行超过该时间，运动将会停止。单位：s
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SpeedJ(self, boxID, rbtID, cmdVel, acc, runtime):
        result = []
        command = 'SpeedJ,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(cmdVel[i]) + ','
        command += str(acc) + ','
        command += str(runtime) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 5
    *	@param brief: In SpeedL mode,Push position command velocity / 在SpeedL模式下，下发关节命令速度指令
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param cmdVel : Position velocity / 更新的空间运动速度，单位：mm/s
    *	@param linearAcc :  Linear Acc / 直线设定加速度
    *	@param acc : Angular Acc / 角度设定加速度，单位：°/s^2
    *	@param runtime : Command execution exceeds this time, the movement will stop / 指令运行超过该时间，运动将会停止。单位：s
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SpeedL(self, boxID, rbtID, cmdVel, linearAcc, acc, runtime):
        result = []
        command = 'SpeedL,'
        command += str(rbtID) + ','
        for i in range(0, 6):
            command += str(cmdVel[i]) + ','
        command += str(linearAcc) + ','
        command += str(acc) + ','
        command += str(runtime) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 6
    *	@param brief: Initialize servoEsJ, truncating points / 初始化在线控制模式，清空缓存点位,ServoEsJ
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_InitServoEsJ(self, boxID, rbtID):
        result = []
        command = 'InitServoEsJ,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 7
    *	@param brief: Start move for servoEsJ /启动在线控制模式，设定位置固定更新的周期和前瞻时间，开始运动
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param dServoTime : interval of update (s) / 更新周期
    *	@param dLookaheadTime : LookaheadTime (s) / 前瞻时间
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_StartServoEsJ(self, boxID, rbtID, dServoTime, dLookaheadTime):
        result = []
        command = 'StartServoEsJ,'
        command += str(rbtID) + ','
        command += str(dServoTime) + ','
        command += str(dLookaheadTime) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 8
    *	@param brief: Push points list for servoEsJ / 批量下发在线控制点位,每个点位下发频率由固定更新的周期确定
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param nPointSize : Point size, maximum 500 / 点位数量
    *	@param sPoints : Points list / 点位信息
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_PushServoEsJ(self, boxID, rbtID, nPointSize, sPoints):
        result = []
        command = 'PushServoEsJ,'
        command += str(rbtID) + ','
        command += str(nPointSize) + ','
        for i in range(len(sPoints)):
            command += str(sPoints[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 9
    *	@param brief: Read servoEsJ state with call interval more than 20 ms / 读取当前是否可以继续下发点位信息，循环读取间隔>20ms
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param result[0] : Pushing point is allowed or not; 0 for allowed, 1 for not allowed /  0：允许下发点位; 1：不允许下发点位
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''

    def HRIF_ReadServoEsJState(self, boxID, rbtID, result):
        command = 'ReadServoEsJState,'
        command += str(rbtID) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    #
    # part 13 Interface of relative tracking motion / 相对跟踪运动类控制接口
    #

    '''
    *	@index : 1
    *	@param brief: Set motion parameters of tracking motion / 启动机器人在线控制(servoJ 或 servoP)时,设定位置固定更新的周期和前瞻时间
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param state : 0 to disable tracking, 1 to enable trackin / 跟踪状态(0:关闭相对跟踪运动 1:开启相对跟踪运动)
    *	@param distance : Relative distance of tracking / 相对跟踪运动保持的相对距离
    *	@param dAwayVelocity: Away velocity of tracking / 相对跟踪的运动的远离速度
    *	@param dGobackVelocity: Back velocity of tracking / 相对跟踪的运动的返回速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetMoveTraceParams(self, boxID, rbtID, state, distance, dAwayVelocity, dGobackVelocity):
        result = []
        command = 'SetMoveTraceParams,'
        command += str(rbtID) + ','
        command += str(state) + ','
        command += str(distance) + ','
        command += str(dAwayVelocity) + ','
        command += str(dGobackVelocity) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 2
    *	@param brief: Set initial parameters of tracking motion / 设置相对跟踪运动初始化参数
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param dK,dB: parameters in equation as y = dK * x + dB / 计算公式y = dK * x + dB
    *	@param maxLimit: Max distance detected by laser sensor / 激光传感器检测距离最大值
    *	@param minLinit: Min distance detected by laser sensor / 激光传感器检测距离最小值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetMoveTraceInitParams(self, boxID, rbtID, dK, dB, maxLimit, minLimit):
        result = []
        command = 'SetMoveTraceInitParams,'
        command += str(rbtID) + ','
        command += str(dK) + ','
        command += str(dB) + ','
        command += str(maxLimit) + ','
        command += str(minLimit) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 3
    *	@param brief:  Set end orientation in tracking motion / 设置相对跟踪运动的跟踪探寻方向
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param direction: Tracking and exploration direction (x, y, z invalid, can be set to 0) (Rx, Ry, Rz units [°]) / 跟踪探寻方向(x,y,z无效,可设置0)(Rx,Ry,Rz单位[°])
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetMoveTraceUcs(self, boxID, rbtID, direction):
        result = []
        command = 'SetMoveTraceUcs,'
        command += str(rbtID) + ','
        for i in range(len(direction)):
            command += str(direction[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 4
    *	@param brief: Set tracking motion state / 设置传送带跟踪运动状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param state: 0 to disable tracking, 1 to enable tracking / 0:关闭传送带跟踪，1:开启传送带跟踪
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetTrackingState(self, boxID, rbtID, state):
        result = []
        command = 'SetTrackingState,'
        command += str(rbtID) + ','
        command += str(state) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    #
    # part 14 interfaces for tracking position / 位置跟随类指令
    #
    '''
    *	@index : 1
    *	@param brief: Set max velocity of tracking position / 设置位置跟随的最大跟随速度
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param dMaxLineVel: Max follow position velocity / 直线最大速度
    *	@param dMaxOriVel: Max follow angular velocity / 姿态最大速度
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetPoseTrackingMaxMotionLimit(self, boxID, rbtID, dMaxLineVel, dMaxOriVel):
        result = []
        command = 'SetPoseTrackingMaxMotionLimit,'
        command += str(rbtID) + ','
        command += str(dMaxLineVel) + ','
        command += str(dMaxOriVel) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 2
    *	@param brief: Set location tracking timeout stop time / 设置位置跟踪超时停止时间
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param dTime: time out / 超时停止时间，单位：秒[s]
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetPoseTrackingStopTimeOut(self, boxID, rbtID, dTime):
        result = []
        command = 'SetPoseTrackingStopTimeOut,'
        command += str(rbtID) + ','
        command += str(dTime) + ',;'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 3
    *	@param brief: Set PID of tracking position / 设置PID参数
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param dPosPID1: Follow position PID / 位置跟随PID
    *	@param dPosPID2: Follow position PID / 位置跟随PID
    *	@param dPosPID3: Follow position PID / 位置跟随PID
    *	@param dOriPID1: Follow angular PID / 姿态跟随PID
    *	@param dOriPID2: Follow angular PID / 姿态跟随PID
    *	@param dOriPID3: Follow angular PID / 姿态跟随PID
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetPoseTrackingPIDParams(self, boxID, rbtID, dPosPID1, dPosPID2, dPosPID3, dOriPID1, dOriPID2, dOriPID3):
        result = []
        command = 'SetPoseTrackingPIDParams,'
        command += str(rbtID) + ','
        command += str(dPosPID1) + ','
        command += str(dPosPID2) + ','
        command += str(dPosPID3) + ','
        command += str(dOriPID1) + ','
        command += str(dOriPID2) + ','
        command += str(dOriPID3) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 4
    *	@param brief: Set target of tracking position / 设置位置跟随的目标位置
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param dX: Distance maintained in the X direction / X方向保持的距离
    *	@param dY: Distance maintained in the Y direction / Y方向保持的距离
    *	@param dZ: Distance maintained in the Z direction / Z方向保持的距离
    *	@param dRx: Distance maintained in the Rx direction / Rx方向保持的距离
    *	@param dRy: Distance maintained in the Ry direction / Ry方向保持的距离
    *	@param dRz: Distance maintained in the Rz direction / Rz方向保持的距离
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetPoseTrackingTargetPos(self, boxID, rbtID, dX, dY, dZ, dRx, dRy, dRz):
        result = []
        command = 'SetPoseTrackingTargetPos,'
        command += str(rbtID) + ','
        command += str(dX) + ','
        command += str(dY) + ','
        command += str(dZ) + ','
        command += str(dRx) + ','
        command += str(dRy) + ','
        command += str(dRz) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 5
    *	@param brief: Set state of tracking position / 设置位置跟随状态
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param nState: Tracking state / 跟随的状态
    *                              0: Disable tracking position / 0：关闭位置跟随
    *                              1: Enable tracking position / 1：开启位置跟随
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetPoseTrackingState(self, boxID, rbtID, nState):
        result = []
        command = 'SetPoseTrackingState,'
        command += str(rbtID) + ','
        command += str(nState) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 6
    *	@param brief: Set real time position update of tracking position / 设置实时更新传感器位置信息
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param dX: Checking distance for X / 检测到的X方向保持的距离
    *	@param dY: Checking distance for Y / 检测到的Y方向保持的距离
    *	@param dZ: Checking distance for Z / 检测到的Z方向保持的距离
    *	@param dRx: Checking distance for Rx / 检测到的Rx方向保持的距离
    *	@param dRy: Checking distance for Ry / 检测到的Ry方向保持的距离
    *	@param dRz: Checking distance for Rz / 检测到的Rz方向保持的距离
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_SetUpdateTrackingPose(self, boxID, rbtID, dX, dY, dZ, dRx, dRy, dRz):
        result = []
        command = 'SetUpdateTrackingPose,'
        command += str(rbtID) + ','
        command += str(dX) + ','
        command += str(dY) + ','
        command += str(dZ) + ','
        command += str(dRx) + ','
        command += str(dRy) + ','
        command += str(dRz) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    #
    # part 15 Interforces for other / 其他函数接口
    #

    '''
    *	@index : 1
    *	@param brief: Excute HRApp command / 执行插件 app 命令
    *	@param boxID: Control box ID / 电箱ID号
    *	@param name : HRAppName / 插件名称
    *	@param param: Command name and paramters / 命令名称及参数
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_HRAppCmd(self, boxID, name, cmd, param, result):
        command = 'HRAppCmd,'
        command += str(name) + ','
        command += str(cmd) + ','
        for i in range(len(param)):
            command += str(param[i]) + ','
        command += ';'
        if self.isV8CPS and self.g_plugin_client_state[boxID]:
            return self.g_plugin_clients[boxID].sendAndRecv(command, result)
        elif self.isV8CPS and not self.g_plugin_client_state[boxID]:
            print("Unable to connect to plugin service")
            return 39504
        else:
            return self.g_clients[boxID].sendAndRecv(command, result)
    
    def HRIF_HRApp(self, boxID, name, cmd, param, result):
        self.HRIF_HRAppCmd(boxID, name, cmd, param, result)

    '''
    *	@index : 2
    *	@param brief: Write End holding registers of Modbus slave / 写末端连接的 modbus 从站寄存器
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param nSlaveID: Modbus Slave ID / 从站ID
    *	@param nFunction: Function code / 功能码
    *	@param nRegAddr: Register beginning address / 寄存器起始地址
    *	@param nRegCount: Registers number, maximum 11 / 寄存器数量，最大11个
    *	@param data : Registers value, with the registers size of nRegCount / 需要写的寄存器值，vector的大小与寄存器数量一致
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_WriteEndHoldingRegisters(self, boxID, rbtID, nSlaveID, nFunction, nRegAddr, nRegCount, data):
        result = []
        command = 'WriteHoldingRegisters,'
        command += str(rbtID) + ','
        command += str(nSlaveID) + ','
        command += str(nFunction) + ','
        command += str(nRegAddr) + ','
        command += str(nRegCount) + ','
        if nRegCount != len(data):
            return ['-1']
        for i in range(nRegCount):
            command += str(data[i]) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)

    '''
    *	@index : 3
    *	@param brief: Read End holding registers of Modbus slave / 读取末端Modbus寄存器
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param nSlaveID: Modbus slave ID / 从站ID
    *	@param nFunction: Function code / 功能码
    *                            0x01-Read coil register / 读线圈寄存器
    *                            0x02-Read line discrete input register / 读线离散输入寄存器
    *                            0x03-Read holding register / 读保持寄存器
    *                            0x04-Read input register / 读输入寄存器
    *                            0x05-Write signle coil register / 写单个线圈寄存器
    *                            0x06-Write signle holding register / 写单个保持寄存器
    *                            0x0f-Write multiple coil register / 写多个线圈寄存器
    *                            0x10-Write multiple holding register / 写多个保持寄存器
    *	@param nRegAddr: Register beginning address / 寄存器起始地址
    *	@param nRegCount: Registers number, maximum 12 / 寄存器数量，最大12个
    *	@param retData[1-n]: obtained registers value, with the registers size of nRegCount / 返回读取的寄存器值，vector的大小与寄存器数量一致
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_ReadEndHoldingRegisters(self, boxID, rbtID, nSlaveID, nFunction, nRegAddr, nRegCount, result):
        command = 'ReadHoldingRegisters,'
        command += str(rbtID) + ','
        command += str(nSlaveID) + ','
        command += str(nFunction) + ','
        command += str(nRegAddr) + ','
        command += str(nRegCount) + ',;'
        retData = self.g_clients[boxID].sendAndRecv(command, result)
        return retData

    '''
    *	@index : 4
    *	@param brief: Wait for robot stop moving / 等待机器人运动停止
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def waitMovementDone(self, boxID, rbtID, result):
        while True:
            command = 'ReadCurFSM,'
            command += str(rbtID) + ','
            command += ';'
            retData = self.g_clients[boxID].sendAndRecv(command, result)
            if retData != 0:
                return retData
            if not result:
                return 39505
            if int(result[0]) == 25:
                time.sleep(0.1)
                continue
            else:
                break
        return 0
    
    '''
    *	@index : 5
    *	@param brief: Set IO before the motion command reaches the target point / 在运动指令到达目标点位前设置IO
    *	@param boxID: Control box ID / 电箱ID号
    *	@param rbtID: Robot ID / 机器人ID,一般为0
    *	@param nEndDOMask : The EndDO to be modified is identified by bit/ 需要更改的EndDO按bit标识
    *   @param nEndDOVal :  The target state of each EndDO to be modified./ 各个需要更改的EndDO的目标状态
    *   @param nBoxDOMask : The BoxDO to be modified is identified by bit. / 需要更改的BoxDO按bit标识
    *   @param nBoxDOVal : The target state of each BoxDO to be modified. / 各个需要更改的BoxDO的目标状态
    *   @param nBoxCOMask : The BoxCO to be modified is identified by bit / 需要更改的BoxCO按bit标识
    *   @param nBoxCOVal : The target state of each BoxCO to be modified / 各个需要更改的BoxCO的目标状态
    *   @param nBoxAOCH0_Mask : Indicator of whether BoxAOCH0 needs to be modified. / BoxAOCH0是否需要更改的标识
    *   @param nBoxAOCH0_Mode :  Mode / 模式
    *   @param nBoxAOCH1_Mask :  Indicator of whether BoxAOCH1 needs to be modified. / BoxAOCH1是否需要更改的标识
    *   @param nBoxAOCH1_Mode : Mode / 模式
    *   @param dbBoxAOCH0_Val :  Corresponding analog value / 对应模拟量值
    *   @param dbBoxAOCH1_Val :  Corresponding analog value / 对应模拟量值
    *	
    *	@return : nRet=0 : Function call succeeded / 函数调用成功
    *             nRet>0 : Error code of function call / 函数调用失败的错误码
    '''
    def HRIF_cdsSetIO(self, boxID, rbtID, nEndDOMask, nEndDOVal, nBoxDOMask, nBoxDOVal, nBoxCOMask, nBoxCOVal, nBoxAOCH0_Mask,
                nBoxAOCH0_Mode, nBoxAOCH1_Mask, nBoxAOCH1_Mode, dbBoxAOCH0_Val, dbBoxAOCH1_Val):
        result = []
        command = 'cdsSetIO,'
        command += str(nEndDOMask) + ','
        command += str(nEndDOVal) + ','
        command += str(nBoxDOMask) + ','
        command += str(nBoxDOVal) + ','
        command += str(nBoxCOMask) + ','
        command += str(nBoxCOVal) + ','
        command += str(nBoxAOCH0_Mask) + ','
        command += str(nBoxAOCH0_Mode) + ','
        command += str(nBoxAOCH1_Mask) + ','
        command += str(nBoxAOCH1_Mode) + ','
        command += str(dbBoxAOCH0_Val) + ','
        command += str(dbBoxAOCH1_Val) + ','
        command += ';'
        return self.g_clients[boxID].sendAndRecv(command, result)
    
# sendVarValue
# No output

def ReadFloat(*args, reverse=False):
    for n, m in args:
        n, m = '%04x' % n, '%04x' % m
    if reverse:
        v = n + m
    else:
        v = m + n
    y_bytes = bytes.fromhex(v)
    y = struct.unpack('!f', y_bytes)[0]
    y = round(y, 6)
    return y


def WriteFloat(value, reverse=False):
    print(WriteFloat)
    y_bytes = struct.pack('!f', value)
    print(y_bytes)
    y_hex = ''.join(['%02x' % i for i in y_bytes])
    print(y_hex)
    n, m = y_hex[:-4], y_hex[-4:]
    n, m = int(n, 16), int(m, 16)
    if reverse:
        v = [n, m]
    else:
        v = [m, n]
    return v


def ReadDint(*args, reverse=False, result):
    for n, m in args:
        n, m = '%04x' % n, '%04x' % m
    if reverse:
        v = n + m
    else:
        v = m + n
    y_bytes = bytes.fromhex(v)
    y = struct.unpack('!i', y_bytes)[0]
    return y


def WriteDint(value, reverse=False):
    y_bytes = struct.pack('!i', value)
    # y_hex = bytes.hex(y_bytes)
    y_hex = ''.join(['%02x' % i for i in y_bytes])
    n, m = y_hex[:-4], y_hex[-4:]
    n, m = int(n, 16), int(m, 16)
    if reverse:
        v = [n, m]
    else:
        v = [m, n]
    return v
