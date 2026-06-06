# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.9",
#     "polars==1.41.2",
# ]
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import polars as pl
    from pathlib import Path

    return Path, pl


@app.cell
def _(Path):
    src1793 = (Path("1793-census") / "kolin-city.cex").resolve()
    return (src1793,)


@app.cell
def _(Path):
    src1783 = (Path("1783") / "Kolin-cols.cex").resolve()
    return (src1783,)


@app.cell
def _(pl, src1783):
    df1783 = pl.read_csv(
        src1783,
        separator="|",
        has_header=True,
        infer_schema_length=1000,
        truncate_ragged_lines=True
    )
    return (df1783,)


@app.cell
def _(pl, src1793):
    df1793 = pl.read_csv(
        src1793,
        separator="|",
        has_header=True,
        infer_schema_length=1000,
        truncate_ragged_lines=True
    ).drop_nulls(subset=["District Number"])

    return (df1793,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 1793
    """)
    return


@app.cell
def _(df1793):
    df1793
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 1783
    """)
    return


@app.cell
def _(df1783):
    df1783
    return


if __name__ == "__main__":
    app.run()
