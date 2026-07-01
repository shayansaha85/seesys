import asciichartpy
from rich.panel import Panel
from rich.text import Text
from rich import box
from utils.cache import sys_cache

def generate_cpu_graph_panel():
    data = list(sys_cache.cpu_history)
    if not data or all(v == 0.0 for v in data):
        # asciichartpy needs at least some variation or handles all-zeros poorly sometimes,
        # but latest versions handle it okay.
        pass
        
    try:
        chart = asciichartpy.plot(data, {'height': 6, 'min': 0, 'max': 100})
        # asciichartpy outputs ANSI codes by default? No, it outputs plain text.
        # We can colorize it with rich Text
        text = Text(chart, style="bold green")
    except Exception as e:
        text = Text(f"Graph Error: {e}", style="red")
        
    return Panel(text, title="[bold green]CPU Usage History (%)", border_style="green", box=box.SIMPLE)

def generate_mem_graph_panel():
    data = list(sys_cache.mem_history)
        
    try:
        chart = asciichartpy.plot(data, {'height': 6, 'min': 0, 'max': 100})
        text = Text(chart, style="bold magenta")
    except Exception as e:
        text = Text(f"Graph Error: {e}", style="red")
        
    return Panel(text, title="[bold magenta]Memory Usage History (%)", border_style="magenta", box=box.SIMPLE)
