import psutil
from rich.table import Table
from rich.panel import Panel
from rich import box
from utils.cache import sys_cache

def generate_cpu_panel():
    table = Table(box=box.SIMPLE, show_header=False, expand=True)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    cpu_freq = psutil.cpu_freq()
    freq_str = f"{cpu_freq.current:.0f}Mhz" if cpu_freq else "N/A"
    
    table.add_row("Cores (Phy/Log)", f"{sys_cache.cores_phy} / {sys_cache.cores_log}")
    table.add_row("Frequency", freq_str)
    
    cpu_percent = sys_cache.cpu_history[-1] if sys_cache.cpu_history else 0.0
    color = "green" if cpu_percent < 60 else "yellow" if cpu_percent < 85 else "red"
    table.add_row("Overall Usage", f"[{color}]{cpu_percent:.1f}%[/{color}]")

    per_cpu = psutil.cpu_percent(interval=None, percpu=True)
    per_cpu_strs = []
    for i, p in enumerate(per_cpu):
        c = "green" if p < 60 else "yellow" if p < 85 else "red"
        per_cpu_strs.append(f"C{i}: [{c}]{p}%[/{c}]")
    
    for i in range(0, len(per_cpu_strs), 4):
        table.add_row("", "  ".join(per_cpu_strs[i:i+4]))

    return Panel(table, title="[bold green]CPU Metrics", border_style="green")
