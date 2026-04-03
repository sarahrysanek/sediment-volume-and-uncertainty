# sediment-volume-and-uncertainty
Python workflow for calculating sediment thickness, volume, accumulation rates, and uncertainties from seismic TWT data, developed for active margin systems and adaptable to similar datasets.

# Sediment Volume and Accumulation Rate Calculations

## Overview

This repository contains a Python workflow for calculating sediment thickness, total sediment volume, accumulation rates, and associated uncertainties from gridded seismic two-way travel time (TWT) data.

The code was developed as part of a dissertation focused on sediment routing and accumulation at active margins, with application to the Baranof Fan system and adjacent regions. The grids used in the initial study were created based on 2D seismic profile interpretations, that were gridded in Kingdom and exported as .xyz files. They were then clipped to the areas of interest, and anamolous values were removed using GMT.

## Method Summary

Sediment thickness is derived from two-way travel time (TWT) using a constant seismic velocity. Thickness is then converted to volumetric estimates based on grid cell dimensions. Sediment accumulation rates are calculated using sequence duration constraints.

Uncertainty propagation follows the methodology of Gulick et al. (2015), adapted from spreadsheet-based calculations into a fully reproducible Python workflow.

### Key Steps

1. **Input TWT data**

   * Gridded seismic two-way travel time (seconds)
   * Associated latitude and longitude

2. **Thickness conversion**

   * One-way travel time (OWTT) = TWT / 2
   * Sediment thickness = OWTT × seismic velocity

3. **Volume calculation**

   * Grid cell area assumed to be 500 m × 500 m based on gridding resolution
   * Volume per cell = thickness × cell area
   * Total sediment volume = sum of all grid cells

4. **Uncertainty estimation**

   * Area uncertainty derived from mapping resolution and perimeter
   * Velocity uncertainty assumed at 7%
   * Vertical resolution based on seismic wavelength limits
   * Thickness and volume uncertainties propagated using standard error propagation

5. **Sediment accumulation rates**

   * Thickness converted to cm
   * Rates calculated over user-defined time intervals based on known age-dated horizons 
   * Statistics reported (min, max, mean), including seperate statistics for depocenters

## Inputs

* Tab-delimited text file containing:

  * Longitude
  * Latitude
  * Two-way travel time (TWT)

Example header format:

```
lon    lat    twt
```

## Outputs

* Total sediment volume
* Maximum and mean sediment thickness
* Sediment accumulation rates (cm/kyr and cm/yr)
* CSV file for mapping (longitude, latitude, sedimentation rate), outputs are ready to be plotted in any mapping software 

## How to Run

### Requirements

* Python 3
* numpy
* pandas

### Execution

Update file paths in the script to point to your local data, then run:

```
python error_calculation.py
```

## Notes on Parameters

Key parameters are defined within the script and should be modified based on your grid parameters:

* Seismic velocity (default: 2 km/s)
* Grid spacing (default: 500 m)
* Sequence duration (Myr)
* Uncertainty terms (velocity, resolution, area)

These values are currently based on published constraints and are study-specific assumptions.

## Reproducibility

This script represents a direct translation of previously spreadsheet-based calculations into Python to improve transparency and reproducibility. All processing steps are explicitly defined and can be adapted for other study areas with similar seismic datasets.

## Author

Sarah Rysanek
PhD Dissertation Research – Sediment Routing at Active Margins
Rysanek et al., 2026 (in prep)

## References

Rysanek, S., Worthington, L. L. T., Walton, M., Gulick, S., Brandl, C.C., Adedeji, O., & Roland, E. (in prep).
Seismic reflection imaging provides integrated records of tectonic and glacial
sedimentary processes in the eastern Gulf of Alaska. Geology. 

Gulick, S.P.S. et al., 2015, Mid-Pleistocene climate transition drives net mass loss from rapidly uplifting St. Elias Mountains, Alaska: Proceedings of the National Academy of Sciences of the United States of America, v. 112, p. 15042–15047, doi:10.1073/pnas.1512549112.

Walton, M.A.L., Gulick, S.P.S., Reece, R., Barth, G.A., Ginger A. Barth, Christeson, G.L., and Van Avendonk, H.J.A., 2014, Dynamic response to strike-slip tectonic control on the deposition and evolution of the Baranof Fan, Gulf of Alaska: Geosphere, v. 10, p. 680–691, doi:10.1130/ges01034.1.
