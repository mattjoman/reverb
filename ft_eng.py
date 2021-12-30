import numpy as np
import pandas as pd
import re
from re import search
from scipy import stats


def clean(data):
	# Dropping rows with 'None' (there aren't many)
	indexes = data[ data['listing_title'] == 'None'].index
	data.drop(indexes , inplace=True)

	# Getting floats from the price strings
	data['original_price'] = data.original_price.map(lambda x: float(x.replace('£', '').replace('GBP', '').replace(',', '')))
	data['current_price'] = data.current_price.map(lambda x: float(x.replace('£', '').replace('GBP', '').replace(',', '')))

	return data





brands = ['squier', 'fender', 'epiphone', 'gibson', 'ibanez', 'danelectro', 'schecter', 'jackson', 'esp', 'sterling', 'ernie ball', 'music man', 'yamaha', 'paul reed smith', 'prs', 'charvel', 'suhr', 'g&l', 'peavey', 'gretsch', 'washburn', 'godin', 'carvin', 'tokai', 'kramer', 'tiesco', 'warmoth', 'line 6', 'mayones', 'fernandez', 'evh', 'hagstrom', 'dean', 'greco', 'tom anderson', 'chapman', 'knaggs', 'rickenbacker']


# Getting the brand of guitar (improve on this)
def get_brand(data):

    brand_name = []
    brand_num = []
    titles = data.listing_title.values

    for i in np.arange(len(data.listing_title)):
        x = titles[i]

        match = False
        for j, brand in enumerate(brands):
            if search(brand, x, flags=re.IGNORECASE):
                match = True
                brand_name.append(brand)
                brand_num.append(j+1)
                break

        if not match:
            brand_name.append('other')
            brand_num.append(0)

    data['brand_name'] = brand_name
    data['brand_num'] = brand_num

    return data






models = ['strat', 'tele', 'jaguar', 'jazzmaster', 'les paul', 'firebird', 'sg', 'flying v', 'jem']


# Get the model of guitar (strat, tele, les paul, sg, ...)
# include more models and alternative spellings
def getModel(data):

    model_name = []
    model_num = []
    titles = data.listing_title.values

    for i in np.arange(len(data.listing_title)):
        x = titles[i]

        match = False
        for j, model in enumerate(models):
            if search(model, x, flags=re.IGNORECASE):
                match = True
                model_name.append(model)
                model_num.append(j+1)
                break

        if not match:
            model_name.append('other')
            model_num.append(0)

    data['model_name'] = model_name
    data['model_num'] = model_num

    return data






condition_labels = ['Mint', 'Excellent', 'Very Good', 'Good', 'Fair']

# convert the conditions to numerical values
def conv_conditions(data):

    condition_num = []
    conditions = data.condition.values

    for i in np.arange(len(data.listing_title)):
        x = conditions[i]

        match = False
        for j, label in enumerate(condition_labels):
            if search(label, x, flags=re.IGNORECASE):
                match = True
                condition_num.append(j+1)
                break

        if not match:
            condition_num.append(0)

    data['condition_num'] = condition_num

    return data







# Calculate the discount
def getDiscount(data):

	import numpy as np
	import pandas as pd

	discount = data.original_price.values - data.current_price.values
	data['discount'] = discount

	# was there a discount?
	cur_p = data.current_price.values
	ori_p = data.original_price.values
	is_discounted = np.empty(len(ori_p))
	for i in np.arange(len(data.current_price.values)):
		if cur_p[i] < ori_p[i]:
			is_discounted[i] = 1
		else:
			is_discounted[i] = 0

	data['is_discounted'] = is_discounted
	return data





# Get the country it was made in
def getCountry(data):

	country = []
	country_num = np.empty(len(data.current_price.values))
	for i in np.arange(len(data.current_price.values)):
		title = data.listing_title.values[i]
		if search('mim', title, flags=re.IGNORECASE):
			country.append('mexico')
			country_num[i] = 1
		elif search('American', title, flags=re.IGNORECASE):
			country.append('usa')
			country_num[i] = 2
		elif search('Japanese', title, flags=re.IGNORECASE):
			country.append('japan')
			country_num[i] = 3
		elif search('korean', title) or search('korea', title, flags=re.IGNORECASE):
			country.append('korea')
			country_num[i] = 4
		else:
			country.append('other')
			country_num[i] = 0

	data['country'] = country
	data['country_num'] = country_num
	return data






"""

# Putting the prices into bins for classification models
def binPrices(_data, _bins):


	# Get the log prices
	prices = _data.log_current_price.values

	# Fit a normal PDF to the logged prices
	loc, scale = stats.norm.fit(prices)

	# Put prices into categorical bins using a PPF

	# Creating bin edges
	bins = _bins
	edges = np.empty(bins-1)
	for b in np.arange(bins-1):
		edges[b] = stats.norm.ppf(((b+1)/bins), loc=loc, scale=scale)

	# Creating bin centres
	centres = np.empty(bins)
	for c in np.arange(bins):
		centres[c] = stats.norm.ppf(((2*c+1)/2)/bins, loc=loc, scale=scale)

	cen = pd.DataFrame(centres)
	cen.to_csv('bin_centres.csv', index=False)

	# Binning the prices
	i = 0
	which_bin = np.empty(len(prices))
	centre_val = np.empty(len(prices))
	for p in prices:
		if p < edges[0]:
			bin_ = 0
			centre = np.exp(centres[0])
		elif p > edges[-1]:
			bin_ = bins-1
			centre = np.exp(bins-1)
		else:
			for e in np.arange(len(edges)):
				if p > edges[e]:
					bin_ = e+1
					centre = np.exp(centres[e+1])
				else:
					bin_ = bin_
					centre = centre

		which_bin[i] = bin_
		centre_val[i] = centre

		i += 1

	_data['binned_prices'] = which_bin
	_data['bin_centres'] = centre_val
	return _data

"""



if __name__=='__main__':
    # Get the data
    data = pd.read_csv('raw_data.csv')
    print('\n\nRaw data:')
    print(data.info())
    print('\n\n')

    # clean the data
    data = clean(data)

    # feature engineering
    data = get_brand(data)
    #data = get_brand_num(data)
    data = getModel(data)
    #data = get_model_num(data)
    #data = getSpecialScore(data)
    data = conv_conditions(data)
    data = getDiscount(data)
    data = getCountry(data)
    data['length'] = data.listing_title.map(lambda x: len(x))
    data['log_current_price'] = data.current_price.map(lambda x: np.log(x))
    data['log_original_price'] = data.original_price.map(lambda x: np.log(x))
    #data = binPrices(data, 30) # 30 bins

    print('Processed data:')
    print(data.info())
    print('\n\n')

    data.to_csv('processed_data.csv', index=False)

