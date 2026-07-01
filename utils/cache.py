import time
import platform
import psutil
from datetime import datetime
from collections import deque

class SystemCache:
    def __init__(self):
        # Global IO tracking
        self.last_net_io = psutil.net_io_counters(pernic=True)
        self.last_disk_io = psutil.disk_io_counters()
        self.last_time = time.time()
        
        # Static system info
        self.uname = platform.uname()
        self.boot_time = datetime.fromtimestamp(psutil.boot_time())
        self.cores_phy = psutil.cpu_count(logical=False)
        self.cores_log = psutil.cpu_count(logical=True)
        self.mem_total = psutil.virtual_memory().total
        self.swap_total = psutil.swap_memory().total
        
        # History for sparklines (60 ticks)
        self.cpu_history = deque([0.0] * 40, maxlen=40)
        self.mem_history = deque([0.0] * 40, maxlen=40)
        
        # Interactive state
        self.process_sort_by = 'cpu_percent'
        self.process_selected_idx = 0
        self.kill_msg = ""
        
        # Static partitions
        self.partitions = []
        try:
            self.partitions = psutil.disk_partitions(all=False)
        except Exception:
            pass

    def update_io_time(self):
        self.last_time = time.time()
        try:
            self.last_net_io = psutil.net_io_counters(pernic=True)
            self.last_disk_io = psutil.disk_io_counters()
        except Exception:
            pass
            
        try:
            self.cpu_history.append(psutil.cpu_percent(interval=None))
            self.mem_history.append(psutil.virtual_memory().percent)
        except Exception:
            pass

# Create a global instance
sys_cache = SystemCache()
