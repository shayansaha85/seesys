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
from core.graphs import generate_cpu_graph_panel, generate_mem_graph_panel

def make_layout(dt):
    from core.gpu import HAS_NVML, generate_gpu_panel
    
    layout = Layout()
    
    rows = [
        Layout(name="upper", ratio=1), 
        Layout(name="graphs", ratio=1),
        Layout(name="middle", ratio=1)
    ]
    if HAS_NVML:
        rows.append(Layout(name="middle2", ratio=1))
    rows.append(Layout(name="lower", ratio=2))
    
    layout.split_column(*rows)
    
    layout["upper"].split_row(
        Layout(name="sys"),
        Layout(name="cpu"),
        Layout(name="mem")
    )
    
    layout["graphs"].split_row(
        Layout(name="cpu_graph"),
        Layout(name="mem_graph")
    )
    
    layout["middle"].split_row(
        Layout(name="disk"),
        Layout(name="net"),
        Layout(name="sens")
    )
    
    if HAS_NVML:
        layout["middle2"].split_row(Layout(name="gpu"))
    
    # Update panels
    layout["sys"].update(generate_system_panel())
    layout["cpu"].update(generate_cpu_panel())
    layout["mem"].update(generate_memory_panel())
    
    layout["cpu_graph"].update(generate_cpu_graph_panel())
    layout["mem_graph"].update(generate_mem_graph_panel())
    
    layout["disk"].update(generate_disk_panel(dt))
    layout["net"].update(generate_network_panel(dt))
    layout["sens"].update(generate_sensors_panel())
    
    if HAS_NVML:
        layout["gpu"].update(generate_gpu_panel())
        
    layout["lower"].update(generate_process_panel())
    
    return layout

def main():
    console = Console()
    console.clear()
    
    # Initialize CPU times for percentage calculation
    psutil.cpu_percent(interval=None)
    psutil.cpu_percent(interval=None, percpu=True)
    
    try:
        with Live(console=console, refresh_per_second=2, screen=True) as live:
            while True:
                # Calculate dt for network/disk stats
                current_time = time.time()
                dt = current_time - sys_cache.last_time
                
                # Generate layout and render
                layout = make_layout(dt)
                live.update(layout)
                
                # Update cache times after rendering so the next frame diffs correctly
                sys_cache.update_io_time()
                
                time.sleep(0.5)
    except KeyboardInterrupt:
        console.print("[bold red]Monitor stopped.[/bold red]")

if __name__ == "__main__":
    main()
