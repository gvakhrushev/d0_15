"""Bounded single-row Lean pilot. Opt-in; caller must coordinate all builds."""
import ctypes
from ctypes import wintypes
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

class Basic(ctypes.Structure):
    _fields_ = [("process_time", ctypes.c_longlong), ("job_time", ctypes.c_longlong),
                ("flags", wintypes.DWORD), ("min_ws", ctypes.c_size_t), ("max_ws", ctypes.c_size_t),
                ("active_limit", wintypes.DWORD), ("affinity", ctypes.c_size_t),
                ("priority", wintypes.DWORD), ("scheduling", wintypes.DWORD)]
class IOCounts(ctypes.Structure):
    _fields_ = [(name, ctypes.c_ulonglong) for name in ("read_op", "write_op", "other_op", "read_bytes", "write_bytes", "other_bytes")]
class Extended(ctypes.Structure):
    _fields_ = [("basic", Basic), ("io", IOCounts), ("process_memory", ctypes.c_size_t),
                ("job_memory", ctypes.c_size_t), ("peak_process", ctypes.c_size_t), ("peak_job", ctypes.c_size_t)]
class Memory(ctypes.Structure):
    _fields_ = [("length",wintypes.DWORD),("load",wintypes.DWORD), ("total_phys",ctypes.c_ulonglong),
                ("free_phys",ctypes.c_ulonglong),("total_page",ctypes.c_ulonglong),("free_page",ctypes.c_ulonglong),
                ("total_virtual",ctypes.c_ulonglong),("free_virtual",ctypes.c_ulonglong),("free_ext",ctypes.c_ulonglong)]
K = ctypes.WinDLL("kernel32", use_last_error=True)
K.DefineDosDeviceW.argtypes = [wintypes.DWORD,wintypes.LPCWSTR,wintypes.LPCWSTR]
K.DefineDosDeviceW.restype = wintypes.BOOL
K.CreateJobObjectW.argtypes = [ctypes.c_void_p,wintypes.LPCWSTR]
K.CreateJobObjectW.restype = wintypes.HANDLE
K.SetInformationJobObject.argtypes = [wintypes.HANDLE,ctypes.c_int,ctypes.c_void_p,wintypes.DWORD]
K.SetInformationJobObject.restype = wintypes.BOOL
K.AssignProcessToJobObject.argtypes = [wintypes.HANDLE,wintypes.HANDLE]
K.AssignProcessToJobObject.restype = wintypes.BOOL
K.TerminateJobObject.argtypes = [wintypes.HANDLE,wintypes.UINT]
K.TerminateJobObject.restype = wintypes.BOOL
K.CloseHandle.argtypes=[wintypes.HANDLE]; K.CloseHandle.restype=wintypes.BOOL
K.GetProcessAffinityMask.argtypes=[wintypes.HANDLE,ctypes.POINTER(ctypes.c_size_t),ctypes.POINTER(ctypes.c_size_t)]
K.GetProcessAffinityMask.restype=wintypes.BOOL
K.GetCurrentProcess.restype=wintypes.HANDLE
K.SetProcessAffinityMask.argtypes=[wintypes.HANDLE,ctypes.c_size_t]; K.SetProcessAffinityMask.restype=wintypes.BOOL
K.GlobalMemoryStatusEx.argtypes=[ctypes.POINTER(Memory)]; K.GlobalMemoryStatusEx.restype=wintypes.BOOL

def check(value):
    if not value: raise ctypes.WinError(ctypes.get_last_error())
    return value

def available():
    s=Memory(); s.length=ctypes.sizeof(s); check(K.GlobalMemoryStatusEx(ctypes.byref(s))); return s.free_phys

import argparse, hashlib, json, msvcrt
import extract_original_future_witness as guard

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--pilot',type=Path,required=True);parser.add_argument('--formal',type=Path,required=True);parser.add_argument('--build-lock',type=Path,required=True);parser.add_argument('--log',type=Path,required=True);args=parser.parse_args()
    if os.name != 'nt': raise RuntimeError('Windows required')
    expected='353879d776b8275e2bdf9244b621373c882bc27af0b1c6548349c5c80ddef5d0'
    if digest(args.pilot)!=expected: raise RuntimeError('pilot digest mismatch')
    if args.log.exists(): raise RuntimeError('log must not exist')
    if args.build_lock.name!='d0-task-build.lock': raise RuntimeError('unexpected lock')
    if available()<4*1024**3: raise RuntimeError('insufficient initial memory')
    if guard.lean_build_running(): raise RuntimeError('existing Lean process')
    with args.build_lock.open('r+b') as lock:
        if os.fstat(lock.fileno()).st_size<1: raise RuntimeError('empty lock')
        lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        job=None;gate=None
        try:
            if guard.lean_build_running(): raise RuntimeError('existing Lean process')
            job=check(K.CreateJobObjectW(None,None))
            limits=Extended();limits.basic.flags=0x200|0x2000;limits.job_memory=3*1024**3
            check(K.SetInformationJobObject(job,9,ctypes.byref(limits),ctypes.sizeof(limits)))
            gate_code="import subprocess,sys; ready=sys.stdin.readline(); sys.exit(subprocess.call(['lake','env','lean',sys.argv[1]]) if ready=='go\\n' else 99)"
            # Gate waits for parent assignment before starting Lean.
            with args.log.open('xb') as output:
                gate=subprocess.Popen([sys.executable,'-X','utf8','-B','-u','-c',gate_code,str(args.pilot)],cwd=args.formal,stdin=subprocess.PIPE,stdout=output,stderr=subprocess.STDOUT,creationflags=subprocess.BELOW_NORMAL_PRIORITY_CLASS)
                check(K.AssignProcessToJobObject(job,wintypes.HANDLE(gate._handle)))
                gate.stdin.write(b'go\n');gate.stdin.flush();gate.stdin.close()
                start=time.monotonic(); reason='completed'
                while gate.poll() is None:
                    time.sleep(2)
                    if available()<1024**3: reason='low_memory';check(K.TerminateJobObject(job,75));break
                    if time.monotonic()-start>180: reason='timeout';check(K.TerminateJobObject(job,76));break
                code=gate.wait();elapsed=time.monotonic()-start
            if digest(args.pilot)!=expected: raise RuntimeError('pilot changed during run')
            print(json.dumps({'status':reason,'exit_code':code,'elapsed_seconds':elapsed,'pilot_sha256':expected,'job_memory_limit_bytes':3*1024**3,'scope':'all 128 finite rows, cached Lean environment; no source bridge'}))
            return 0 if reason=='completed' and code==0 else 1
        finally:
            if job: K.CloseHandle(job)
            if gate and gate.poll() is None: gate.kill();gate.wait()
            lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_UNLCK,1)

if __name__=='__main__': raise SystemExit(main())
