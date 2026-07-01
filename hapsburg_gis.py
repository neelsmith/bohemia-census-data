# /// script
# dependencies = [
#     "geopandas==1.1.3",
#     "leafmap==0.62.0",
#     "marimo",
# ]
# requires-python = ">=3.12"
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import geopandas as gpd
    import leafmap
    import os

    return gpd, leafmap, os


@app.cell(hide_code=True)
def _(mo):
    # File path input
    file_path = mo.ui.text(
        value="osmfiles/stredocesky-260607.osm.pbf", 
        label="Path to Local OSM File:"
    )

    # GDAL OSM Layer selector
    layer_type = mo.ui.dropdown(
        options={
            "Points (Cafes, Trees, Knots)": "points",
            "Lines (Roads, Rivers, Railways)": "lines",
            "Multilines (Complex Linear Features)": "multilines",
            "Multipolygons (Buildings, Boundaries, Forests)": "multipolygons"
        },
   
        label="GDAL OSM Layer:"
    )

    # Tag filtering inputs
    tag_key = mo.ui.text(value="highway", label="Filter Key:")
    tag_val = mo.ui.text(value="primary", label="Filter Value ('any' for all):")

    # Arrange the UI neatly
    mo.vstack([
        file_path,
        mo.hstack([layer_type, tag_key, tag_val])
    ])
    return file_path, layer_type, tag_key, tag_val


@app.cell
def _(file_path):
    file_path.value
    return


@app.cell
def _(mo):
    mo.notebook_dir()
    return


@app.cell
def _(os, path_val):
    os.path.exists(path_val)
    return


@app.cell
def _(tag_key):
    tag_key.value
    return


@app.cell
def _(tag_val):
    tag_val.value
    return


@app.cell
def _(gdf_raw):
    gdf_raw.columns
    return


@app.cell
def _(gdf_raw, tag_key, tag_val):
    gdf_raw[gdf_raw[tag_key.value] == tag_val.value]
    return


@app.cell
def _(file_path):
    path_val = file_path.value
    return (path_val,)


@app.cell
def _(layer_type):
    chosen_layer = layer_type.value
    return (chosen_layer,)


@app.cell
def _(tag_key):
    k = tag_key.value
    return (k,)


@app.cell
def _(tag_val):
    v = tag_val.value
    return (v,)


@app.cell
def _(chosen_layer):
    chosen_layer
    return


@app.cell
def _(chosen_layer, gpd, k, mo, os, path_val, v):
    if os.path.exists(path_val):
        try:
            # Load ONLY the specific layer chosen in the dropdown
            # GDAL optimizes this by scanning the file for just this geometry type
            gdf_raw = gpd.read_file(path_val, layer=chosen_layer)
        
            # Apply reactive column filtering
            if k in gdf_raw.columns:
                if v and v.lower() != 'any':
                    gdf_selected = gdf_raw[gdf_raw[k] == v]
                else:
                    gdf_selected = gdf_raw[gdf_raw[k].notnull()]
                status = mo.md(f"✅ Loaded **{len(gdf_selected)}** features from layer **'{chosen_layer}'**.")
            else:
                gdf_selected = gdf_raw
                status = mo.md(f"⚠️ Column `{k}` not found in **'{chosen_layer}'**. Showing all {len(gdf_raw)} elements.")
            
        except Exception as e:
            gdf_selected = gpd.GeoDataFrame()
            status = mo.md(f"❌ Error loading layer '{chosen_layer}': {e}")
    else:
        gdf_selected = gpd.GeoDataFrame()
        status = mo.md(f"📁 File not found.")

    status
    return gdf_raw, gdf_selected


@app.cell
def _(chosen_layer, gdf_selected, leafmap):
    m = leafmap.Map()
    m.add_gdf(gdf_selected, layer_name=f"OSM {chosen_layer}")
    m.zoom_to_bounds(gdf_selected.total_bounds)

    m
    return


if __name__ == "__main__":
    app.run()
