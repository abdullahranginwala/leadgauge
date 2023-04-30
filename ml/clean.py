# Supress Warnings
import warnings
warnings.filterwarnings('ignore')

# Importing libraries
import numpy as np
import pandas as pd
# Data display coustomization
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)

# this was reached after a thorough analysis
determining_cols = []
training_cols = []


data = pd.read_csv('Leads.csv')
data = data.replace('Select', np.nan)
data = data.drop(data.loc[:,list(round(100*(data.isnull().sum()/len(data.index)), 2)>70)].columns, 1)

data['Lead Quality'] = data['Lead Quality'].replace(np.nan, 'Not Sure')
# By analysis, these values seem to have more than 45% null values and also have a lot of variation. As a result, they need to be removed
data = data.drop(['Asymmetrique Activity Index','Asymmetrique Activity Score','Asymmetrique Profile Index','Asymmetrique Profile Score'],1)

# These replacements aren't random. Mumbai, Others and the 'Will revert after reading the email etc.
data['City'] = data['City'].replace(np.nan, 'Mumbai')
data['Specialization'] = data['Specialization'].replace(np.nan, 'Others')
data['Tags'] = data['Tags'].replace(np.nan, 'Will revert after reading the email')
data['What matters most to you in choosing a course'] = data['What matters most to you in choosing a course'].replace(np.nan, 'Better Career Prospects')
data['What is your current occupation'] = data['What is your current occupation'].replace(np.nan, 'Unemployed')
data['Country'] = data['Country'].replace(np.nan, 'India')

# The remaining values have less than 2% missing values, so we remove them
data.dropna(inplace = True)
data.to_csv('Leads_cleaned')    

data['Lead Source'] = data['Lead Source'].replace(['google'], 'Google')
data['Lead Source'] = data['Lead Source'].replace(['Click2call', 'Live Chat', 'NC_EDM', 'Pay per Click Ads', 'Press_Release',
                                                    'Social Media', 'WeLearn', 'bing', 'blog', 'testone', 'welearnblog_Home', 'youtubechannel'], 'Others')
percentiles = data['TotalVisits'].quantile([0.05,0.95]).values
data['TotalVisits'][data['TotalVisits'] <= percentiles[0]] = percentiles[0]
data['TotalVisits'][data['TotalVisits'] >= percentiles[1]] = percentiles[1]
data['Specialization'] = data['Specialization'].replace(['Others'], 'Other_Specialization')
data['What is your current occupation'] = data['What is your current occupation'].replace(['Other'], 'Other_Occupation')
# Let's keep considerable last activities as such and club all others to "Other_Activity"
data['Tags'] = data['Tags'].replace(['In confusion whether part time or DLP', 'in touch with EINS','Diploma holder (Not Eligible)',
                                    'Approached upfront','Graduation in progress','number not provided', 'opp hangup','Still Thinking',
                                'Lost to Others','Shall take in the next coming month','Lateral student','Interested in Next batch',
                                'Recognition issue (DEC approval)','Want to take admission but has financial problems',
                                'University not recognized'], 'Other_Tags')



data = data.drop(['Lead Number','What matters most to you in choosing a course','Search','Magazine','Newspaper Article','X Education Forums','Newspaper',
        'Digital Advertisement','Through Recommendations','Receive More Updates About Our Courses','Update me on Supply Chain Content',
        'Get updates on DM Content','I agree to pay the amount through cheque','A free copy of Mastering The Interview','Country'],1)

# List of variables to map
varlist =  ['Do Not Email', 'Do Not Call']
# Defining the map function
def binary_map(x):
    return x.map({'Yes': 1, "No": 0})

# Applying the function to the housing list
data[varlist] = data[varlist].apply(binary_map)

determining_cols += list(data.columns)
crucial_data = data

dummy1 = pd.get_dummies(data[['Lead Origin', 'Lead Source', 'Last Activity', 'Specialization','What is your current occupation',
                            'Tags','Lead Quality','City','Last Notable Activity']], drop_first=True)
data = pd.concat([data, dummy1], axis=1) # creating one-hot encoded values for categorical data

data = data.drop(['Lead Origin', 'Lead Source', 'Last Activity', 'Specialization','What is your current occupation','Tags','Lead Quality','City','Last Notable Activity'], axis = 1)

training_cols += list(data.columns)

from sklearn.model_selection import train_test_split

# Putting feature variable to X
X = data.drop(['Prospect ID','Converted'], axis=1)
# print(X.shape)
y = data['Converted']
def load_dataset():
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)
    return X_train, X_test, y_train, y_test

def prepare_input(test):
    test = pd.DataFrame(test)
    test = pd.get_dummies(test)
    
    X_train, _, _, _ = load_dataset()
    
    X_train, test = X_train.align(test, join='left', axis=1, fill_value=0)
    
    # Ensure that the test dataset has all the columns of the train dataset
    for col in X_train.columns:
        if col not in test.columns:
            test[col] = 0
    
    test = test[X_train.columns] # reorder the columns
    test.drop(test.columns[0], axis=1, inplace=True) # removing the first added index column
    test = pd.DataFrame.to_numpy(test)
    test.reshape(1, -1)
    return test

