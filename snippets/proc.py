import subprocess as sp
import sys
import platform
from typing import Optional

class Proc:
    """
    DESCRIPTION:
        CREDIT: https://gist.github.com/HarmonicHemispheres/2ab991476e37ae20796a70de3d43c90a
    
    EXAMPLE USAGE:
        ```
        import proc
        proc.Proc(
            win=f"cmd.exe /C start .\\docs\\build\\html\\index.html",
            mac=f"open docs/build/html/index.html",
            linux="xdg-open docs/build/html/index.html",
        ).run()
        ```
    
    TABLE CREDIT: 
        https://stackoverflow.com/questions/446209/possible-values-from-sys-platform
    ┍━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━┑
    │ System              │ Value               │
    ┝━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━┥
    │ Linux               │ linux or linux2 (*) │
    │ Windows             │ win32               │
    │ Windows/Cygwin      │ cygwin              │
    │ Windows/MSYS2       │ msys                │
    │ Mac OS X            │ darwin              │
    │ OS/2                │ os2                 │
    │ OS/2 EMX            │ os2emx              │
    │ RiscOS              │ riscos              │
    │ AtheOS              │ atheos              │
    │ FreeBSD 7           │ freebsd7            │
    │ FreeBSD 8           │ freebsd8            │
    │ FreeBSD N           │ freebsdN            │
    │ OpenBSD 6           │ openbsd6            │
    ┕━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━┙
    """

    def __init__(self, all=None, win=None, mac=None, linux=None, cwd=None, show=True):
        # -- Commands
        self.cmd_all: Optional[str] = all
        self.cmd_win: Optional[str] = win
        self.cmd_mac: Optional[str] = mac
        self.cmd_linux: Optional[str] = linux

        # -- Parameters
        self.cwd = cwd
        self.show = show

    def run(self, shell=True):
        output = ""

        # -- WIN
        if sys.platform == "win32":
            if self.cmd_win:
                res = sp.Popen(self.cmd_win, shell=shell, cwd=self.cwd, stdout=sp.PIPE)
                output = res.communicate()[0]
            elif self.cmd_all:
                res = sp.Popen(self.cmd_all, shell=shell, cwd=self.cwd, stdout=sp.PIPE)
                output = res.communicate()[0]

        # -- MAC
        elif sys.platform == "darwin":

            if self.cmd_mac:
                res = sp.Popen(self.cmd_mac, shell=shell, cwd=self.cwd, stdout=sp.PIPE)
                output = res.communicate()[0]
            elif self.cmd_all:
                res = sp.Popen(self.cmd_all, shell=shell, cwd=self.cwd, stdout=sp.PIPE)
                output = res.communicate()[0]

        # -- LINUX
        elif sys.platform == "linux":
            if self.cmd_linux:
                res = sp.Popen(self.cmd_linux, shell=shell, cwd=self.cwd, stdout=sp.PIPE)
                output = res.communicate()[0]
            elif self.cmd_all:
                res = sp.Popen(self.cmd_all, shell=shell, cwd=self.cwd, stdout=sp.PIPE)
                output = res.communicate()[0]

        # -- Anything else
        else:
            if self.cmd_linux:
                res = sp.Popen(self.cmd_linux, shell=shell, cwd=self.cwd, stdout=sp.PIPE)
                output = res.communicate()[0]
            elif self.cmd_all:
                res = sp.Popen(self.cmd_all, shell=shell, cwd=self.cwd, stdout=sp.PIPE)
                output = res.communicate()[0]
        
        if self.show:
            print(output.decode("utf-8"))
        
        return output.decode("utf-8")