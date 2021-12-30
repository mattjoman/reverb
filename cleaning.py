
def clean(_data):
	import numpy as np
	import pandas as pd
	# Dropping rows with 'None' (there aren't many)
	indexes = _data[ _data['Listing_title'] == 'None'].index
	_data.drop(indexes , inplace=True)

	# Getting floats from the price strings
	_data['original_price'] = _data.Original_price.map(lambda x: float(x.replace('£', '').replace('GBP', '').replace(',', '')))
	_data['current_price'] = _data.Current_price.map(lambda x: float(x.replace('£', '').replace('GBP', '').replace(',', '')))

	return _data
