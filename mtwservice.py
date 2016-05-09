# Mininal Windows Service to run mtwserver.py JOS 2016-05-04
# Requirements: Python 3.4, pywin32. Do this to install pywin32...
# c:\python34\scripts\pip install pypiwin32
# With thanks to Chris Umbel for the original impl here...
# http://www.chrisumbel.com/article/windows_services_in_python
# I've adapted Chris's code to spawn a child process.
# To install the service run this at the cmd line...
# c:\python34\python mtwservice.py install  --startup auto
# ...or just this for more command line options...
# c:\python34\python mtwservice.py
import win32service
import win32serviceutil
import win32event
import subprocess
import os
import logging
import servicemanager

class MTWService( win32serviceutil.ServiceFramework):
    # At cmd line you can "net start mtwservice" or "net stop mtwservice"
    # Or "sc start mtwservice" "sc stop mtwservice"
    _svc_name_ = "MTWService"
    # Service name in the Service Control Manager (SCM)
    _svc_display_name_ = "Minimal Tornado WebServer"
    # SCM description
    _svc_description_ = "A very simple web server"

    def __init__( self, args):
        win32serviceutil.ServiceFramework.__init__( self, args)
        self.popn = None
        self.env = os.environ
        self.env['SSROOT'] = r'c:\ss'
        self.env['SSROOTX'] = r'c:/ss'

    def SvcDoRun( self):
        # NB this function does not return, it blocks in self.popn.communicate( )
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        args = [r'c:\python34\python.exe', r'c:\osullivj\src\py\mtwserver.py']
        self.popn = subprocess.Popen( args, cwd=r'c:\osullivj\src\py', env=self.env)
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        sstdout, sstderr = self.popn.communicate( )

    # called when we're being shut down
    def SvcStop( self):
        # tell the SCM we're shutting down
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.popn.terminate( )
        self.ReportServiceStatus( win32service.SERVICE_STOPPED)


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine( MTWService)