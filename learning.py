import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

from datetime import datetime

from cognite.config import configure_session

from cognite.v05.assets import get_assets
from cognite.v05.assets import get_asset
from cognite.v05.assets import get_asset_subtree

from cognite.v05.files import list_files
from cognite.v05.files import get_file_info
from cognite.v05.files import download_file

from cognite.v05.timeseries import get_datapoints_frame
from cognite.v05.timeseries import get_timeseries

from cognite.v05.tagmatching import tag_matching

configure_session(os.environ['COGNITE_API_KEY'], 'publicdata')

# Get the assets and print memory location
assets = get_assets()
# print(assets)

# View the assets in a table
assets_df = assets.to_pandas()
# print(assets_df)

# Print single asset
scrubber_file_name = 'PH-ME-P-0152-001'
# print(list_files(name=scrubber_file_name).to_pandas())

# Print url to download the file using the file id
# print(download_file(list_files(name=scrubber_file_name).to_pandas().id[0]))

scrubber_level_working_setpoint = 'VAL_23-LIC-92521:Control Module:YR'
scrubber_level_measured_value  = 'VAL_23-LIC-92521:Z.X.Value'
scrubber_level_output  = 'VAL_23-LIC-92521:Z.Y.Value'
all_ts_names = [scrubber_level_working_setpoint, scrubber_level_measured_value, scrubber_level_output]
start = datetime(2018, 7, 1)
end = '1d-ago'
data = get_datapoints_frame(all_ts_names, start=start, end=end, granularity='1h', aggregates=['average', 'min', 'max'])
data = data.fillna(method='ffill')

T = pd.to_datetime(data.timestamp, unit='ms')
plt.figure(figsize=(10, 5))
plt.plot(T, data[scrubber_level_working_setpoint+'|average'].values, label='setpoint')
plt.plot(T, data[scrubber_level_measured_value+'|average'].values, label='measured value')
plt.plot(T, data[scrubber_level_output+'|average'].values, label='level output')
plt.legend()
plt.show()
