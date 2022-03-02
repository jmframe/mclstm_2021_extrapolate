# Deep learning rainfall-runoff predictions of extreme events
Code and models for the HESS paper on mass conservation and extrapolation to low probability runoff events with deep learning

Contents:
- **neuralhydrology**: deep learning codebase (https://neuralhydrology.readthedocs.io/en/latest/) that includes both the LSTM and MC-LSTM used in this paper
- **data**
    - **b17-out**: output of the return periods calculations from the Bulletin 17b procedure.
    - **usgs-peak**: Annual peak flows from the USGS National Water Information System (https://nwis.waterdata.usgs.gov/usa/nwis/peak; accessed 10 June 2021)
- **split-data**: code and output to split the CAMELS data by years according to their annual peak flow return period.
- **b17**: Matlab code from Mathworks File Exchange to fit the peak annual flow events to the distribution to obtain returnperiod estimates for each basin (Burkey, 2009). 
- **results**: Python code (in Jupyter notebooks) for processing the model results
    - **model_output_for_analysis** This directory has the output of each model saved in a pickle file (.p)
    - **paper_table.ipynb** This notebook takes the run outputs and calculates the performance metrics for the three different training periods, two time splits and one split by peak annual flow return period.
    - **results_analysis.ipynb** This notebook takes the run outputs and calculates the performance metrics for each individual year, and associates those metrics with the peak annual return periods, and saves these values in pickle files (.pkl), one for each training type.
    - **paper_figures.ipynb** This notebook reads the pickle files saved by the results analysis notebook and makes the plots that are shown in the paper. 

# Notes about this repository
- The Pickle files were generated using XArray 0.16.1
