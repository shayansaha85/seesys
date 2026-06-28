import time
import psutil
from rich.live import Live
from rich.layout import Layout
from rich.console import Console

from utils.cache import sys_cache
from core.system import generate_system_panel
from core.cpu import generate_cpu_panel
from core.memory import generate_memory_panel
from core.disk import generate_disk_panel
from core.network import generate_network_panel
from core.sensors import generate_sensors_panel
from core.process import generate_process_panel

def make_layout(dt):
    layout = Layout()
    
    layout.split_column(
        Layout(name="upper", ratio=1),
        Layout(name="middle", ratio=1),
        Layout(name="lower", ratio=2)
    )
    
    layout["upper"].split_row(
        Layout(name="sys"),
        Layout(name="cpu"),
        Layout(name="mem")
    )
    
    layout["middle"].split_row(
        Layout(name="disk"),
        Layout(name="net"),
        Layout(name="sens")
    )
    
    # Update panels
    layout["sys"].update(generate_system_panel())
    layout["cpu"].update(generate_cpu_panel())
    layout["mem"].update(generate_memory_panel())
    layout["disk"].update(generate_disk_panel(dt))
    layout["net"].update(generate_network_panel(dt))
    layout["sens"].update(generate_sensors_panel())
    layout["lower"].update(generate_process_panel())
    
    return layout

def main():
    console = Console()
    console.clear()
    
    # Initialize CPU times for percentage calculation
    psutil.cpu_percent(interval=None)
    psutil.cpu_percent(interval=None, percpu=True)
    
    try:
        with Live(console=console, refresh_per_second=1, screen=True) as live:
            while True:
                # Calculate dt for network/disk stats
                current_time = time.time()
                dt = current_time - sys_cache.last_time
                
                # Generate layout and render
                layout = make_layout(dt)
                live.update(layout)
                
                # Update cache times after rendering so the next frame diffs correctly
                sys_cache.update_io_time()
                
                time.sleep(1)
    except KeyboardInterrupt:
        console.print("[bold red]Monitor stopped.[/bold red]")

if __name__ == "__main__":
    main()
