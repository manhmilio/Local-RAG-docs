#!/usr/bin/env python3
"""
Script hỗ trợ quản lý Ollama models
"""
import ollama
import sys
from rich.console import Console
from rich.table import Table
from config import settings

console = Console()


def list_models():
    """List tất cả models đã pull"""
    console.print("\n[bold cyan]📦 Ollama Models:[/bold cyan]\n")
    
    try:
        client = ollama.Client(host=settings.OLLAMA_BASE_URL)
        response = client.list()
        models = response.get('models', [])
        
        if not models:
            console.print("[yellow]No models found. Pull a model first![/yellow]")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Model Name", style="cyan")
        table.add_column("Size", justify="right")
        table.add_column("Modified", style="green")
        
        for model in models:
            name = model.get('name', 'Unknown')
            size = f"{model.get('size', 0) / 1e9:.2f} GB"
            modified = model.get('modified_at', 'Unknown')[:10]
            table.add_row(name, size, modified)
        
        console.print(table)
        
        # Show current model
        console.print(f"\n[bold]Current configured model:[/bold] [green]{settings.OLLAMA_MODEL}[/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")


def pull_model(model_name: str):
    """Pull một model mới"""
    console.print(f"\n[cyan]Pulling model:[/cyan] [bold]{model_name}[/bold]")
    console.print("[yellow]This may take several minutes...[/yellow]\n")
    
    try:
        client = ollama.Client(host=settings.OLLAMA_BASE_URL)
        
        # Pull with progress
        current_digest = None
        for progress in client.pull(model_name, stream=True):
            digest = progress.get('digest', '')
            if digest != current_digest:
                current_digest = digest
                status = progress.get('status', '')
                console.print(f"  {status}")
        
        console.print(f"\n[green]✅ Successfully pulled {model_name}[/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error pulling model: {str(e)}[/red]")


def delete_model(model_name: str):
    """Xóa một model"""
    console.print(f"\n[yellow]Deleting model:[/yellow] [bold]{model_name}[/bold]")
    
    try:
        client = ollama.Client(host=settings.OLLAMA_BASE_URL)
        client.delete(model_name)
        console.print(f"[green]✅ Successfully deleted {model_name}[/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error deleting model: {str(e)}[/red]")


def recommend_models():
    """Hiển thị models được recommend"""
    console.print("\n[bold cyan]🎯 Recommended Models for Medical Chatbot:[/bold cyan]\n")
    
    recommendations = [
        {
            "name": "mistral:7b",
            "size": "~4.1 GB",
            "pros": "Fast, good quality, multilingual support",
            "best_for": "General medical Q&A"
        },
        {
            "name": "llama3.1:8b",
            "size": "~4.7 GB",
            "pros": "Latest Llama, excellent performance",
            "best_for": "Complex medical reasoning"
        },
        {
            "name": "gemma2:9b",
            "size": "~5.4 GB",
            "pros": "Google's model, good at following instructions",
            "best_for": "Structured medical responses"
        },
        {
            "name": "qwen2:7b",
            "size": "~4.4 GB",
            "pros": "Excellent multilingual, good Vietnamese",
            "best_for": "Vietnamese medical content"
        },
    ]
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Model", style="cyan", width=15)
    table.add_column("Size", justify="right", width=10)
    table.add_column("Pros", width=30)
    table.add_column("Best For", style="green", width=25)
    
    for rec in recommendations:
        table.add_row(rec["name"], rec["size"], rec["pros"], rec["best_for"])
    
    console.print(table)
    
    console.print("\n[bold]To pull a model:[/bold]")
    console.print("[cyan]  ollama pull <model_name>[/cyan]")
    console.print("\n[bold]Example:[/bold]")
    console.print("[cyan]  ollama pull mistral:7b[/cyan]")


def main():
    """Main CLI"""
    console.print("\n[bold magenta]🦙 Ollama Model Manager[/bold magenta]")
    
    if len(sys.argv) < 2:
        console.print("\n[bold]Usage:[/bold]")
        console.print("  python ollama_manager.py [command] [args]")
        console.print("\n[bold]Commands:[/bold]")
        console.print("  list              - List all installed models")
        console.print("  pull <model>      - Pull a new model")
        console.print("  delete <model>    - Delete a model")
        console.print("  recommend         - Show recommended models")
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_models()
    
    elif command == "pull":
        if len(sys.argv) < 3:
            console.print("[red]Error: Model name required[/red]")
            console.print("Usage: python ollama_manager.py pull <model_name>")
            return
        pull_model(sys.argv[2])
    
    elif command == "delete":
        if len(sys.argv) < 3:
            console.print("[red]Error: Model name required[/red]")
            console.print("Usage: python ollama_manager.py delete <model_name>")
            return
        
        # Confirm
        console.print(f"\n[yellow]⚠️  Are you sure you want to delete {sys.argv[2]}?[/yellow]")
        confirm = input("Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            delete_model(sys.argv[2])
        else:
            console.print("[cyan]Cancelled[/cyan]")
    
    elif command == "recommend":
        recommend_models()
    
    else:
        console.print(f"[red]Unknown command: {command}[/red]")


if __name__ == "__main__":
    main()
