from __future__ import annotations

import typer
from gatesmith.cli import renderer

from gatesmith.core.parser import ParseError
from gatesmith.core.pipeline import synthesize as run_pipeline
from gatesmith.io.reader import read_input
from gatesmith.io.writer import write_output

app = typer.Typer(help="Gatesmith")


@app.command()
def synthesize(
    input: str = typer.Argument(
        ..., help="Single Verilog assign statement or a file path"
    ),
    output: str = typer.Option("out.v", help="Destination Verilog file"),
    verbose: bool = typer.Option(False, help="Print synthesis diagnostics"),
) -> None:
    try:
        source = read_input(input)
        result = run_pipeline(source)
    except (ParseError, ValueError) as exc:
        renderer.render_error(str(exc))
        raise typer.Exit(code=1) from exc
    except Exception as exc:
        renderer.render_error("Unexpected synthesis failure")
        raise typer.Exit(code=1) from exc

    if verbose:
        vars_ = result.variables

        renderer.render_input_verilog(source)
        renderer.render_ast(result.assignment.expr)
        renderer.render_truth_table_rows(result.truth_table, vars_)
        renderer.render_minterms(result.minterms, vars_)
        renderer.render_qmc_rounds(result.trace.rounds, vars_)
        renderer.render_prime_implicants(result.trace.prime_implicants, vars_)
        if result.trace.prime_implicants:
            renderer.render_prime_coverage(
                result.trace.prime_implicants, result.minterms, vars_
            )
        renderer.render_summary(result)
        renderer.render_verilog(result.verilog)

    write_output(output, result.verilog)
    typer.echo(output)


if __name__ == "__main__":
    app()
