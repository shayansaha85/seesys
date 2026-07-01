from rich.table import Table
from rich.panel import Panel
from rich import box
from utils.formatters import bytes_to_human

try:
    import pynvml
    HAS_NVML = True
    try:
        pynvml.nvmlInit()
    except Exception:
        HAS_NVML = False
except ImportError:
    HAS_NVML = False

def generate_gpu_panel():
    table = Table(box=box.SIMPLE, show_header=False, expand=True)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")

    if not HAS_NVML:
        table.add_row("Status", "N/A (pynvml not installed or no GPU)")
        return Panel(table, title="[bold cyan]GPU Metrics", border_style="cyan")

    try:
        device_count = pynvml.nvmlDeviceGetCount()
        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(name, bytes):
                name = name.decode('utf-8')
                
            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
            temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            
            mem_used_human = bytes_to_human(memory.used)
            mem_total_human = bytes_to_human(memory.total)
            mem_percent = (memory.used / memory.total) * 100 if memory.total > 0 else 0
            
            util_color = "green" if utilization.gpu < 60 else "yellow" if utilization.gpu < 85 else "red"
            mem_color = "green" if mem_percent < 60 else "yellow" if mem_percent < 85 else "red"
            temp_color = "green" if temp < 60 else "yellow" if temp < 80 else "red"
            
            table.add_row(f"GPU {i}", f"{name}")
            table.add_row("Usage", f"[{util_color}]{utilization.gpu}%[/{util_color}]")
            table.add_row("Memory", f"[{mem_color}]{mem_used_human} / {mem_total_human} ({mem_percent:.1f}%)[/{mem_color}]")
            table.add_row("Temp", f"[{temp_color}]{temp}°C[/{temp_color}]")
            
            if i < device_count - 1:
                table.add_row("", "")
                
    except Exception as e:
        table.add_row("Error", str(e))
        
    return Panel(table, title="[bold cyan]GPU Metrics", border_style="cyan")
