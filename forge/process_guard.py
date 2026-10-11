"""Own the process tree so timeout and parent exit cannot leave background workers."""

from __future__ import annotations

import os
import signal
import subprocess


class ProcessGuard:
    def __init__(self):
        self.process = None
        self.handle = None
        if os.name == "nt":
            import ctypes
            from ctypes import wintypes as w

            class Basic(ctypes.Structure):
                _fields_ = [
                    ("process_time", ctypes.c_int64),
                    ("job_time", ctypes.c_int64),
                    ("flags", w.DWORD),
                    ("min_ws", ctypes.c_size_t),
                    ("max_ws", ctypes.c_size_t),
                    ("active", w.DWORD),
                    ("affinity", ctypes.c_size_t),
                    ("priority", w.DWORD),
                    ("scheduling", w.DWORD),
                ]

            class Limits(ctypes.Structure):
                _fields_ = [
                    ("basic", Basic),
                    ("io", ctypes.c_uint64 * 6),
                    ("process_memory", ctypes.c_size_t),
                    ("job_memory", ctypes.c_size_t),
                    ("peak_process", ctypes.c_size_t),
                    ("peak_job", ctypes.c_size_t),
                ]

            self.api = ctypes.WinDLL("kernel32", use_last_error=True)
            signatures = {
                "CreateJobObjectW": ([ctypes.c_void_p, w.LPCWSTR], w.HANDLE),
                "SetInformationJobObject": (
                    [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD],
                    w.BOOL,
                ),
                "AssignProcessToJobObject": ([w.HANDLE, w.HANDLE], w.BOOL),
                "TerminateJobObject": ([w.HANDLE, w.UINT], w.BOOL),
                "CloseHandle": ([w.HANDLE], w.BOOL),
            }
            for name, (arguments, result) in signatures.items():
                function = getattr(self.api, name)
                function.argtypes, function.restype = arguments, result
            self.handle = self.api.CreateJobObjectW(None, None)
            if not self.handle:
                raise ctypes.WinError(ctypes.get_last_error())
            limits = Limits()
            limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            if not self.api.SetInformationJobObject(
                self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)
            ):
                self.api.CloseHandle(self.handle)
                self.handle = None
                raise ctypes.WinError(ctypes.get_last_error())

    def __enter__(self):
        return self

    def attach(self, process: subprocess.Popen) -> None:
        self.process = process
        if self.handle and not self.api.AssignProcessToJobObject(self.handle, process._handle):
            process.kill()
            process.wait(timeout=10)
            raise OSError("Cannot establish process-tree ownership.")
        if self.handle:
            import ctypes
            from ctypes import wintypes

            resume = ctypes.WinDLL("ntdll").NtResumeProcess
            resume.argtypes = [wintypes.HANDLE]
            resume.restype = wintypes.LONG
            if resume(process._handle) != 0:
                self.stop()
                process.wait(timeout=10)
                raise OSError("Cannot resume owned process.")

    def stop(self):
        if self.handle:
            if not self.api.TerminateJobObject(self.handle, 1):
                raise OSError("Cannot terminate process job.")
        elif self.process:
            try:
                os.killpg(self.process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

    def __exit__(self, *args):
        try:
            self.stop()
        finally:
            if self.handle:
                self.api.CloseHandle(self.handle)
                self.handle = None
