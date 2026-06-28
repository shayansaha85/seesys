import psutil
from rich.table import Table
from rich.panel import Panel
from rich import box
from utils.cache import sys_cache
from utils.formatters import bytes_to_human

def generate_disk_panel(dt):
    table = Table(box=box.SIMPLE, expand=True)
    table.add_column("Device", style="cyan")
    table.add_column("Mount", style="white")
    table.add_column("Size", justify="right", style="green")
    table.add_column("Use %", justify="right")
    
    for partition in sys_cache.partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            color = "green" if usage.percent < 75 else "yellow" if usage.percent < 90 else "red"
            table.add_row(
                partition.device,
                partition.mountpoint,
                bytes_to_human(usage.total),
                f"[{color}]{usage.percent}%[/{color}]"
            )
        except PermissionError:
            continue
            
    curr_io = psutil.disk_io_counters()
    
    if curr_io and sys_cache.last_disk_io and dt > 0:
        read_bps = (curr_io.read_bytes - sys_cache.last_disk_io.read_bytes) / dt
        write_bps = (curr_io.write_bytes - sys_cache.last_disk_io.write_bytes) / dt
        table.add_section()
        table.add_row("Disk I/O", "", f"R: {bytes_to_human(read_bps)}/s", f"W: {bytes_to_human(write_bps)}/s")
        
    return Panel(table, title="[bold yellow]Disk Metrics", border_style="yellow")
