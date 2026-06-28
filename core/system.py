import os
import psutil
from datetime import datetime
from rich.table import Table
from rich.panel import Panel
from rich import box
from utils.cache import sys_cache

def generate_system_panel():
    table = Table(box=box.SIMPLE, show_header=False, expand=True)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("System", f"{sys_cache.uname.system} {sys_cache.uname.release} ({sys_cache.uname.machine})")
    table.add_row("Node", sys_cache.uname.node)
    
    uptime = datetime.now() - sys_cache.boot_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    table.add_row("Uptime", f"{days}d {hours}h {minutes}m")
    
    try:
        load = os.getloadavg()
        table.add_row("Load Avg", f"{load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}")
    except AttributeError:
        table.add_row("Load Avg", "N/A (Windows)")
        
    users = psutil.users()
    user_list = ", ".join(list(set([u.name for u in users])))
    table.add_row("Users", user_list)

    return Panel(table, title="[bold blue]System Info", border_style="blue")
