import requests
import pandas as pd
import matplotlib.pyplot as plt
import json

# More Documentation on https://bber.unm.edu/apidoc

def setParameters(dataFilters):
    '''
    param : dataFilters

    this function expects a python dictionary where the key can be one of :
        "stfips", "areaType", "area", "source", "periodType", "periodYear", "indcode", "ownership", "adjusted"
    The values must be a value present in the BBER_dataDictionary.json for it to do a lookup of parameter codes.
    '''
    dataDictionary = json.load(open('./BBER_dataDictionary.json'))

    stfips = dataDictionary['stfips'][dataFilters['stfips']]
    areaType = dataDictionary['areaTypes'][dataFilters['areaType']]
    area = dataFilters['area']
    table = dataDictionary['dataSource'][dataFilters['source']]
    periodType = dataDictionary['periodTypes'][dataFilters['periodType']]
    periodYear = dataFilters['periodYear']
    indcode = dataDictionary['industryCodes'][dataFilters['indcode']]
    ownership = dataDictionary['ownership'][dataFilters['ownership']]
    adjusted = dataFilters['adjusted']

    API_URL = f'https://api.bber.unm.edu/api/data/rest/bbertable?table={table}&stfips={stfips}&areatype={areaType}&area={area}&periodtype={periodType}&periodyear={periodYear}&indcode={indcode}&ownership={ownership}&adjusted={adjusted}'

    return API_URL


def getData(apiUrl):
    '''
    param : apiUrl Eg: https://api.bber.unm.edu/api/data/rest/bbertable?table=covid19&stfips=35

    this function expects a string that follows BBER API specs. Refer to https://bber.unm.edu/apidoc for more information.
    '''

    response = requests.get(apiUrl)
    data = response.json()

    # Table MetaData. such as tablename, title, description, release, schedule... etc.
    table_metadata = data['metadata']['table']
    print(table_metadata)

    print('\n\n\n\n')

    # Columns MetaData. such as columnname, title, description... etc. for each column in the data
    columns_metadata_df = pd.DataFrame(data['metadata']['columns'])
    print(columns_metadata_df.head())

    print('\n\n\n\n')

    # Data is represented as row and column on a dataframe. Refer to column metadata to get information about each column
    data_df = pd.DataFrame(data['data'])
    print(f'there are {len(data_df)} entries')
    print(data_df.head())

    return data_df


def main():

    # we'll use the same parameters to title the graphs and give parameters to API call.
    dataFilters = {
        "stfips": 'New Mexico',
        "areaType": 'State',
        "area": '',  # empty string denotes this filter won't be applied. so all area in areatype above are returned
        "source": "Gross Receipt Collections RP80's",
        "periodType": 'Monthly',
        "periodYear": '2020',
        "indcode": 'Agriculture, Forestry, Fishing and Hunting',
        "ownership": 'Private',
        "adjusted": '',  # 1 for seasonally adjusted and 0 for not seasonally adjusted
    }

    API_URL = setParameters(dataFilters)
    print(API_URL)
    data_df = getData(API_URL)

    graphTitle = f"{dataFilters['source']} for {dataFilters['stfips']} : {dataFilters['areaType']} on {dataFilters['periodYear']} : {dataFilters['periodType']} for {dataFilters['indcode']} : {dataFilters['ownership']} Industry "
    sorted_data_df = data_df.sort_values(by='period')
    sorted_data_df.plot(x="period", y="grosrcpt", kind="bar", title=graphTitle)

    plt.show()


if __name__ == '__main__':
    main()
