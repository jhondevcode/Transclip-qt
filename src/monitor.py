"""
"""

from PyQt6.QtCore import QThread
from impl import AbstractMonitor


class Monitor(QThread, AbstractMonitor):
    
    def __init__(self):
        QThread.__init__(self)
        AbstractMonitor.__init__(self)

    def start_monitoring(self):
        pass

    def stop_monitoring(self):
        pass
