import psutil
from rich.table import Table
from rich.panel import Panel
from rich import box
from utils.cache import sys_cache
from utils.formatters import bytes_to_human

def generate_network_panel(dt):
    table = Table(box=box.SIMPLE, expand=True)
    table.add_column("Interface", style="cyan")
    table.add_column("Up/Down Speed", style="green")
    
    if_stats = psutil.net_if_stats()
    curr_io = psutil.net_io_counters(pernic=True)
    
    for interface_name, stats in if_stats.items():
        if interface_name == 'lo' or not stats.isup:
            continue 
                
        rx_speed = 0
        tx_speed = 0
        
        if curr_io and sys_cache.last_net_io and interface_name in curr_io and interface_name in sys_cache.last_net_io and dt > 0:
            rx_speed = (curr_io[interface_name].bytes_recv - sys_cache.last_net_io[interface_name].bytes_recv) / dt
            tx_speed = (curr_io[interface_name].bytes_sent - sys_cache.last_net_io[interface_name].bytes_sent) / dt
            
        if rx_speed > 0 or tx_speed > 0:
            table.add_row(
                interface_name[:15], 
                f"↑ {bytes_to_human(tx_speed)}/s ↓ {bytes_to_human(rx_speed)}/s"
            )
            
    return Panel(table, title="[bold cyan]Network Metrics", border_style="cyan")
