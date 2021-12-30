import numpy as np
import pandas as pd
import cleaning
import featEng as fe

# Get the data
data = pd.read_csv('big_dataset.csv')
print(data.info())

# clean the data
data = cleaning.clean(data)

# feature engineering
data = fe.get_brand(data)
data = fe.get_brand_num(data)
data = fe.getModel(data)
data = fe.get_model_num(data)
data = fe.getSpecialScore(data)
data = fe.conv_conditions(data)
data = fe.getDiscount(data)
data = fe.getCountry(data)
data['length'] = data.Listing_title.map(lambda x: len(x))#
data['log_current_price'] = data.current_price.map(lambda x: np.log(x))
data['log_original_price'] = data.original_price.map(lambda x: np.log(x))
data = fe.binPrices(data, 30) # 30 bins

data.to_csv('cleanedEngineeredData.csv', index=False)
