#-*- coding: utf-8 -*-
from ctypes import *
# Let's map the Microsoft types to ctypes for clarity
WORD = c_ushort
DWORD = c_ulong
DWORD64 = c_ulonglong
LONG = c_long
LPBYTE = POINTER(c_ubyte)
LPTSTR = POINTER(c_char)
HANDLE = c_void_p
# Constants
STANDARD_RIGHTS_REQUIRED = 0x000F0000L
SYNCHRONIZE = 0x00100000L

DEBUG_PROCESS = 0x00000001
CREATE_NEW_CONSOLE = 0x00000010
PROCESS_ALL_ACCESS = 0x001F0FFF
THREAD_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED or SYNCHRONIZE or 0xFFFF)
DBG_CONTINUE = 0x00010002L
INFINITE = 0x1
TH32CS_SNAPTHREAD = 0x00000004 #表示我们要搜集快照 snapshot中所有已经注册了的线程

#define CONTEXT_CONTROL             0x00000001L // SS:SP, CS:IP, FLAGS, BP
#define CONTEXT_INTEGER             0x00000002L // AX, BX, CX, DX, SI, DI
#define CONTEXT_SEGMENTS            0x00000004L // DS, ES, FS, GS
#define CONTEXT_FLOATING_POINT      0x00000008L // 387 state
#define CONTEXT_DEBUG_REGISTERS     0x00000010L // DB 0-3,6,7
#define CONTEXT_EXTENDED_REGISTERS  0x00000020L // cpu specific extensions
#define CONTEXT_FULL (CONTEXT_CONTROL | CONTEXT_INTEGER | CONTEXT_SEGMENTS)
#define CONTEXT_ALL (CONTEXT_FULL | CONTEXT_FLOATING_POINT | CONTEXT_DEBUG_REGISTERS | CONTEXT_EXTENDED_REGISTERS)
CONTEXT_AMD64 = 0x100000
CONTEXT_SEGMENTS  = (CONTEXT_AMD64 or 0x4L)
CONTEXT_CONTROL  = (CONTEXT_AMD64 or 0x1L)
CONTEXT_INTEGER   = (CONTEXT_AMD64 or 0x2L)
CONTEXT_FLOATING_POINT = (CONTEXT_AMD64 or 0x8L)
CONTEXT_FULL = (CONTEXT_CONTROL | CONTEXT_INTEGER | CONTEXT_FLOATING_POINT)
CONTEXT_DEBUG_REGISTERS = (CONTEXT_AMD64 | 0x10L)
# Structures for CreateProcessA() function
class STARTUPINFO(Structure):
    _fields_ = [
        ("cb", DWORD),
        ("lpReserved", LPTSTR),
        ("lpDesktop", LPTSTR),
        ("lpTitle", LPTSTR),
        ("dwX", DWORD),
        ("dwY", DWORD),
        ("dwXSize", DWORD),
        ("dwYSize", DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAttribute",DWORD),
        ("dwFlags", DWORD),
        ("wShowWindow", WORD),
        ("cbReserved2", WORD),
        ("lpReserved2", LPBYTE),
        ("hStdInput", HANDLE),
        ("hStdOutput", HANDLE),
        ("hStdError", HANDLE),
    ]
class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD),
    ]

class LUID_AND_ATTRIBUTES(Structure):
    _fields_=[
        ("Luid",DWORD),
        ("Attributes",DWORD),
    ]

class TOKEN_PRIVILEGES(Structure):
    _fields_=[
        ("PrivilegeCount",DWORD),
        ("Privileges",LUID_AND_ATTRIBUTES*10),
    ]

######################DEBUG_EVENT structure begin#############################
class EXCEPTION_RECORD(Structure):
    _fields_ = [
        ("ExceptionCode",DWORD),
        ("ExceptionFlags",DWORD),
        ("ExceptionRecord",DWORD),
        ("ExceptionAddress",DWORD),
        ("NumberParameters",DWORD),
        ("ExceptionInformation",LPTSTR),
    ]
class EXCEPTION_DEBUG_INFO(Structure):
    _fields_ = [
        ("ExceptionRecord",EXCEPTION_RECORD),
        ("dwFirstChance",DWORD),
    ]
class CREATE_PROCESS_DEBUG_INFO(Structure):
    _fields_ = [
        ("hFile", HANDLE),
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("lpBaseOfImage", DWORD),
        ("dwDebugInfoFileOffset", DWORD),
        ("nDebugInfoSize", DWORD),
        ("lpThreadLocalBase", DWORD),
        ("lpStartAddress", DWORD),
        ("lpImageName", DWORD),
        ("fUnicode", DWORD),
    ]

class CREATE_THREAD_DEBUG_INFO(Structure):
    _fields_=[
        ("hThread",HANDLE),
        ("lpThreadLocalBase",DWORD),
        ("lpStartAddress",DWORD),
    ]
class EXIT_THREAD_DEBUG_INFO(Structure):
    _fields_=[
        ("dwExitCode",DWORD)
    ]
class EXIT_PROCESS_DEBUG_INFO(Structure):
    _fields_=[
        ("dwExitCode",DWORD)
    ]
class LOAD_DLL_DEBUG_INFO(Structure):
    _fields_=[
        ("hFile",HANDLE),
        ("lpBaseOfDll",DWORD),
        ("dwDebugInfoFileOffset",DWORD),
        ("nDebugInfoSize",DWORD),
        ("lpImageName",DWORD),
        ("fUnicode",WORD),
    ]
class UNLOAD_DLL_DEBUG_INFO(Structure):
    _fields_=[
        ("lpBaseOfDll",DWORD)
    ]
class OUTPUT_DEBUG_STRING_INFO(Structure):
    _fields_=[
        ("lpDebugStringData",LPTSTR),
        ("fUnicode",WORD),
        ("nDebugStringLength",WORD),
    ]
class RIP_INFO(Structure):
    _fields_=[
        ("dwError",DWORD),
        ("dwType",DWORD)
    ]

class DEBUG_EVENT_UNION(Union):
    _fields_=[
        ("Exception",EXCEPTION_DEBUG_INFO),
        ("CreateThread",CREATE_THREAD_DEBUG_INFO),
        ("CreateProcessInfo",CREATE_PROCESS_DEBUG_INFO),
        ("ExitThread",EXIT_THREAD_DEBUG_INFO),
        ("ExitProcess",EXIT_PROCESS_DEBUG_INFO),
        ("LoadDll",LOAD_DLL_DEBUG_INFO),
        ("UnloadDll",UNLOAD_DLL_DEBUG_INFO),
        ("DebugString",OUTPUT_DEBUG_STRING_INFO),
        ("RipInfo",RIP_INFO),
    ]

class DEBUG_EVENT(Structure):
    _fields_=[
        ("dwDebugEventCode",DWORD),
        ("dwProcessId",DWORD),
        ("dwThreadId",DWORD),
        ("u",DEBUG_EVENT_UNION),
    ]
######################DEBUG_EVENT structure end#############################
class THREADENTRY32(Structure):
    _fields_=[
        ("dwSize",DWORD),
        ("cntUsage",DWORD),
        ("th32ThreadID",DWORD),
        ("th32OwnerProcessID",DWORD),
        ("tpBasePri",LONG),
        ("tpDeltaPri",LONG),
        ("dwFlags",DWORD),
    ]

# typedef struct _FLOATING_SAVE_AREA
# {
#      ULONG ControlWord;
#      ULONG StatusWord;
#      ULONG TagWord;
#      ULONG ErrorOffset;
#      ULONG ErrorSelector;
#      ULONG DataOffset;
#      ULONG DataSelector;
#      UCHAR RegisterArea[80];
#      ULONG Cr0NpxState;
# } FLOATING_SAVE_AREA, *PFLOATING_SAVE_AREA;
class FLOATING_SAVE_AREA(Structure):
    _fields_=[
        ("ControlWord",DWORD),
        ("StatusWord",DWORD),
        ("TagWord",DWORD),
        ("ErrorOffset",DWORD),
        ("ErrorSelector",DWORD),
        ("DataOffset",DWORD),
        ("DataSelector",DWORD),
        ("RegisterArea",c_char*80),
        ("Cr0NpxState",DWORD),
    ]

class CONTEXT(Structure):
    _fields_=[
        ("ContextFlags",DWORD),
        ("Dr0",DWORD),
        ("Dr1",DWORD),
        ("Dr2",DWORD),
        ("Dr3",DWORD),
        ("Dr6",DWORD),
        ("Dr7",DWORD),
        ("FloatSave",FLOATING_SAVE_AREA),
        ("SegGs",DWORD),
        ("SegFs",DWORD),
        ("SegEs",DWORD),
        ("SegDs",DWORD),
        ("Edi",DWORD),
        ("Esi",DWORD),
        ("Ebx",DWORD),
        ("Edx",DWORD),
        ("Ecx",DWORD),
        ("Eax",DWORD),
        ("Ebp",DWORD),
        ("Eip",DWORD),
        ("SegCs",DWORD),
        ("EFlags",DWORD),
        ("Esp",DWORD),
        ("SegSs",DWORD),
        ("ExtendedRegisters",c_byte*512)
    ]
class CONTEXT64(Structure):
    _fields_=[
        ("P1Home",DWORD64),
        ("P2Home",DWORD64),
        ("P3Home",DWORD64),
        ("P4Home",DWORD64),
        ("P5Home",DWORD64),
        ("P6Home",DWORD64),
        ("ContextFlags",DWORD),
        ("MxCsr",DWORD),
        ("SegCs",WORD),
        ("SegDs",WORD),
        ("SegEs",WORD),
        ("SegFs",WORD),
        ("SegGs",WORD),
        ("SegSs",WORD),
        ("EFlags",DWORD),

        ("Dr0",DWORD64),
        ("Dr1",DWORD64),
        ("Dr2",DWORD64),
        ("Dr3",DWORD64),
        ("Dr6",DWORD64),
        ("Dr7",DWORD64),

        ("Rax",DWORD64),
        ("Rcx",DWORD64),
        ("Rdx",DWORD64),
        ("Rbx",DWORD64),
        ("Rsp",DWORD64),
        ("Rbp",DWORD64),
        ("Rsi",DWORD64),
        ("Rdi",DWORD64),
        ("R8",DWORD64),
        ("R9",DWORD64),
        ("R10",DWORD64),
        ("R11",DWORD64),
        ("R12",DWORD64),
        ("R13",DWORD64),
        ("R14",DWORD64),
        ("R15",DWORD64),
        ("Rip",DWORD64)
    ]
# typedef struct DECLSPEC_ALIGN(16) _CONTEXT {
#
#     //
#     // Register parameter home addresses.
#     //
#     // N.B. These fields are for convience - they could be used to extend the
#     //      context record in the future.
#     //
#
#     DWORD64 P1Home;
#     DWORD64 P2Home;
#     DWORD64 P3Home;
#     DWORD64 P4Home;
#     DWORD64 P5Home;
#     DWORD64 P6Home;
#
#     //
#     // Control flags.
#     //
#
#     DWORD ContextFlags;
#     DWORD MxCsr;
#
#     //
#     // Segment Registers and processor flags.
#     //
#
#     WORD   SegCs;
#     WORD   SegDs;
#     WORD   SegEs;
#     WORD   SegFs;
#     WORD   SegGs;
#     WORD   SegSs;
#     DWORD EFlags;
#
#     //
#     // Debug registers
#     //
#
#     DWORD64 Dr0;
#     DWORD64 Dr1;
#     DWORD64 Dr2;
#     DWORD64 Dr3;
#     DWORD64 Dr6;
#     DWORD64 Dr7;
#
#     //
#     // Integer registers.
#     //
#
#     DWORD64 Rax;
#     DWORD64 Rcx;
#     DWORD64 Rdx;
#     DWORD64 Rbx;
#     DWORD64 Rsp;
#     DWORD64 Rbp;
#     DWORD64 Rsi;
#     DWORD64 Rdi;
#     DWORD64 R8;
#     DWORD64 R9;
#     DWORD64 R10;
#     DWORD64 R11;
#     DWORD64 R12;
#     DWORD64 R13;
#     DWORD64 R14;
#     DWORD64 R15;
#
#     //
#     // Program counter.
#     //
#
#     DWORD64 Rip;
#
#     //
#     // Floating point state.
#     //
#
#     union {
#         XMM_SAVE_AREA32 FltSave;
#         struct {
#             M128A Header[2];
#             M128A Legacy[8];
#             M128A Xmm0;
#             M128A Xmm1;
#             M128A Xmm2;
#             M128A Xmm3;
#             M128A Xmm4;
#             M128A Xmm5;
#             M128A Xmm6;
#             M128A Xmm7;
#             M128A Xmm8;
#             M128A Xmm9;
#             M128A Xmm10;
#             M128A Xmm11;
#             M128A Xmm12;
#             M128A Xmm13;
#             M128A Xmm14;
#             M128A Xmm15;
#         } DUMMYSTRUCTNAME;
#     } DUMMYUNIONNAME;
#
#     //
#     // Vector registers.
#     //
#
#     M128A VectorRegister[26];
#     DWORD64 VectorControl;
#
#     //
#     // Special debug control registers.
#     //
#
#     DWORD64 DebugControl;
#     DWORD64 LastBranchToRip;
#     DWORD64 LastBranchFromRip;
#     DWORD64 LastExceptionToRip;
#     DWORD64 LastExceptionFromRip;
# } CONTEXT, *PCONTEXT;