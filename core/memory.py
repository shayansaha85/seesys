import psutil
from rich.table import Table
from rich.panel import Panel
from rich import box
from utils.cache import sys_cache
from utils.formatters import bytes_to_human

def generate_memory_panel():
    table = Table(box=box.SIMPLE, show_header=False, expand=True)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    svmem = psutil.virtual_memory()
    mem_color = "green" if svmem.percent < 70 else "yellow" if svmem.percent < 90 else "red"
    
    table.add_row("RAM Total", bytes_to_human(sys_cache.mem_total))
    table.add_row("RAM Used", f"[{mem_color}]{bytes_to_human(svmem.used)} ({svmem.percent}%)[/{mem_color}]")
    table.add_row("RAM Free", bytes_to_human(svmem.available))
    
    swap = psutil.swap_memory()
    swap_color = "green" if swap.percent < 50 else "yellow" if swap.percent < 80 else "red"
    
    table.add_row("Swap Total", bytes_to_human(sys_cache.swap_total))
    table.add_row("Swap Used", f"[{swap_color}]{bytes_to_human(swap.used)} ({swap.percent}%)[/{swap_color}]")
    table.add_row("Swap Free", bytes_to_human(swap.free))

    return Panel(table, title="[bold magenta]Memory Metrics", border_style="magenta")
