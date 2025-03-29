import socket
import urllib.parse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print
from rich.progress import track
import time


console = Console()

def http_to_ip(url):
    try:
        
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc

        
        domain = domain.split(':')[0] if ':' in domain else domain
        
        
        for _ in track(range(2), description="Resolving IP..."):
            time.sleep(0.5)  
        
        
        ip_address = socket.gethostbyname(domain)

       
        table = Table(title="[bold green]DNS Resolution Results[/]", show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="bright_yellow")
        
        
        table.add_row("Original URL", url)
        table.add_row("Domain", domain)
        table.add_row("IP Address", ip_address)
        table.add_row("Full IP URL", f"{parsed.scheme}://{ip_address}{parsed.path}")

        console.print(table)

        
        console.print(Panel.fit(
            "[bold]Tip:[/] Some websites may not work when accessed via IP\n"
            "due to [yellow]SSL certificates[/] or [yellow]virtual hosting[/].",
            title="[blue]Note[/]",
            border_style="blue"
        ))

    except socket.gaierror:
        console.print("[bold red]Error:[/] Unable to resolve the domain. Check the URL and try again.")
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/] {str(e)}")

if __name__ == "__main__":
    console.print(Panel.fit(
        "[bold green]HTTP to IP Converter[/]\n"
        "Enter a URL (e.g. [yellow]google.com[/] or [yellow]https://example.com[/])",
        subtitle="Press Ctrl+C to exit"
    ))
    
    while True:
        try:
            url = console.input("\n[bold cyan]>> [/] Enter URL: ").strip()
            if url.lower() in ('exit', 'quit'):
                console.print("[bold green]Goodbye![/]")
                break
            if not url:
                continue  
            
            http_to_ip(url)
            
        except KeyboardInterrupt:
            console.print("\n[red]Exiting...[/] See you next time!")
            break
