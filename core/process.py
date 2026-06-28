import psutil
from rich.table import Table
from rich.panel import Panel
from rich import box

def generate_process_panel():
    table = Table(box=box.SIMPLE, expand=True)
    table.add_column("PID", style="cyan", justify="right")
    table.add_column("Name", style="white")
    table.add_column("User", style="blue")
    table.add_column("CPU %", style="green", justify="right")
    table.add_column("MEM %", style="yellow", justify="right")
    table.add_column("Status", style="magenta")
    table.add_column("Command", style="dim")
    
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    processes = sorted(processes, key=lambda p: p.get('cpu_percent') or 0.0, reverse=True)
    
    for p in processes[:15]: 
        username = ""
        cmd = p['name']
        
        try:
            proc = psutil.Process(p['pid'])
            username = proc.username()
            cmdline = proc.cmdline()
            if cmdline:
                cmd = " ".join(cmdline)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

        if len(cmd) > 50:
            cmd = cmd[:47] + "..."
            
        table.add_row(
            str(p['pid']),
            p['name'][:20],
            username[:12],
            f"{p['cpu_percent']:.1f}%" if p['cpu_percent'] is not None else "0.0%",
            f"{p['memory_percent']:.1f}%" if p['memory_percent'] is not None else "0.0%",
            p['status'],
            cmd
        )
        
    return Panel(table, title="[bold white]Top Processes", border_style="white")
