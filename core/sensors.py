import psutil
from rich.table import Table
from rich.panel import Panel
from rich import box

def generate_sensors_panel():
    table = Table(box=box.SIMPLE, show_header=False, expand=True)
    table.add_column("Sensor", style="cyan")
    table.add_column("Value", style="white")
    
    has_sensors = False
    
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        if temps:
            has_sensors = True
            for name, entries in temps.items():
                for entry in entries:
                    label = entry.label or name
                    temp_color = "green" if entry.current < 60 else "yellow" if entry.current < 80 else "red"
                    table.add_row(f"Temp ({label})", f"[{temp_color}]{entry.current}°C[/{temp_color}]")
                    
    if hasattr(psutil, "sensors_fans"):
        fans = psutil.sensors_fans()
        if fans:
            has_sensors = True
            for name, entries in fans.items():
                for entry in entries:
                    label = entry.label or name
                    table.add_row(f"Fan ({label})", f"{entry.current} RPM")
                    
    if hasattr(psutil, "sensors_battery"):
        batt = psutil.sensors_battery()
        if batt:
            has_sensors = True
            batt_color = "green" if batt.percent > 30 else "red"
            plugged = " (Plugged In)" if batt.power_plugged else ""
            table.add_row("Battery", f"[{batt_color}]{batt.percent}%{plugged}[/{batt_color}]")
            
    if not has_sensors:
        table.add_row("No sensors detected", "N/A")
        
    return Panel(table, title="[bold red]Sensors", border_style="red")
