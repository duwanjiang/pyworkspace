# _*_ encoding:utf-8 _*_
from ctypes import *
import my_debugger_defines

kernel32 = windll.kernel32
advapi32 = windll.advapi32

TOKEN_ADJUST_PRIVILEGES = 0x00032


class enabledebugprivilege():
    def upPrivilege(self):
        hToken = my_debugger_defines.HANDLE()
        fOk = False
        currentHandle = kernel32.GetCurrentProcess()
        print "当前进程句柄:%d" % currentHandle
        isOpenProcess = advapi32.OpenProcessToken(currentHandle, TOKEN_ADJUST_PRIVILEGES, byref(hToken))
        print "打开进程结果:%d" % isOpenProcess
        if (isOpenProcess):
            tp = my_debugger_defines.TOKEN_PRIVILEGES()
            tp.PrivilegeCount = 1
            print advapi32
            advapi32.LookupPrivilegeValue(None, SE_DEBUG_NAME, byref(tp.Privileges[0].Luid))
            tp.Privileges[0].Attributes = advapi32.SE_PRIVILEGE_ENABLED
            advapi32.AdjustTokenPrivileges(hToken, False, byref(tp), sizeof(tp), None, None)
            result = kernel32.GetLastError()
            print "查看权限提升结果%d" % result
            fOk = (result == 0x0)
            kernel32.CloseHandle(hToken)
        else:
            print "打开进程失败！Error:%d" % kernel32.GetLastError()
        return fOk
