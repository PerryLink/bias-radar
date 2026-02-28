import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
from .scanner import BiasScanner
from .visualizer import BiasVisualizer

app = typer.Typer()
console = Console()


@app.command()
def run(
    model: str = typer.Option("bert-base-uncased", "--model", "-m", help="HuggingFace model name or local path"),
    output: str = typer.Option(None, "--output", "-o", help="Output path for radar chart PNG")
):
    """Scan a language model for gender bias and generate a radar chart"""

    console.print(f"\n[cyan]🔍 Scanning model:[/cyan] {model}")
    console.print("[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]\n")

    try:
        scanner = BiasScanner(model_name=model)
        console.print("[yellow]Loading model...[/yellow]")
        scanner.load_model()

        console.print("[yellow]Scanning professions...[/yellow]\n")
        results = scanner.scan_all()

        # Display results table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Profession", style="cyan", width=15)
        table.add_column("He%", justify="right", style="blue")
        table.add_column("She%", justify="right", style="red")
        table.add_column("Bias Score", justify="right", style="yellow")
        table.add_column("", justify="center", width=3)

        for profession, bias_score in results.items():
            he_pct = f"{bias_score * 100:.0f}%"
            she_pct = f"{(1 - bias_score) * 100:.0f}%"
            score_str = f"{bias_score:.2f}"

            # Add indicator
            if bias_score > 0.6:
                indicator = "🔴"
            elif bias_score < 0.4:
                indicator = "🔵"
            else:
                indicator = "🟢"

            table.add_row(profession, he_pct, she_pct, score_str, indicator)

        console.print(table)
        console.print("\n[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]")

        # Generate visualization
        if output is None:
            model_name = model.split('/')[-1]
            output = f"bias_report_{model_name}.png"

        visualizer = BiasVisualizer(results)
        visualizer.create_radar_chart(output)

        console.print(f"\n[green]📸 Radar chart saved to:[/green] {output}\n")

    except Exception as e:
        console.print(f"\n[red]❌ Error:[/red] {str(e)}\n")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
