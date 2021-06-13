# On mass conservation and extrapolation of long short-term memory networks
Code and models for the HESS paper on mass conservation and extrapolation with deep learning

Contents:
- **neuralhydrology**: deep learning codebase (https://neuralhydrology.readthedocs.io/en/latest/) that includes both the LSTM and MC-LSTM used in this paper
- **data**
    - **b17-out**: output of the return periods calculations from the Bulletin 17b procedure.
    - **usgs-peak**: Annual peak flows from the USGS National Water Information System (https://nwis.waterdata.usgs.gov/usa/nwis/peak; accessed 10 June 2021)
- **split-data**: code and output to split the CAMELS data by years according to their annual peak flow return period.
- **b17**: Matlab code from Mathworks File Exchange to fit the peak annual flow events to the distribution to obtain returnperiod estimates for each basin (Burkey, 2009). 
- **results**: Python code (in Jupyter notebooks) for processing the model results
    - paper_figures.ipynb
    - paper_table.ipynb
    - results_analysis.ipynb
