#_*_ encoding:utf-8 _*_
import my_debugger
import my_enabledebugprivilege
debugger = my_debugger.debugger()
# enabledebugprivilege = my_enabledebugprivilege.enabledebugprivilege()
# #提升当前进程权限
# if enabledebugprivilege.upPrivilege():
#     print "当前进程权限提升成功！"
# else:
#     print "权限提升失败！"
debugger.load("E:\\notepad++\\notepad++.exe")
pid = raw_input("Enter the PID of the process to attach to: ")
debugger.attach(int(pid))
list = debugger.enumerate_threads()
for thread in list:
    thread_context = debugger.get_thread_context(thread)
    if thread_context:
        # Now let's output the contents of some of the registers
        print "[*] Dumping registers for thread ID: 0x%08x" % thread
        print "[**] EIP: 0x%08x" % thread_context.Eip
        print "[**] ESP: 0x%08x" % thread_context.Esp
        print "[**] EBP: 0x%08x" % thread_context.Ebp
        print "[**] EAX: 0x%08x" % thread_context.Eax
        print "[**] EBX: 0x%08x" % thread_context.Ebx
        print "[**] ECX: 0x%08x" % thread_context.Ecx
        print "[**] EDX: 0x%08x" % thread_context.Edx
        print "[*] END DUMP"
debugger.detach()