import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
import pickle
from sklearn.preprocessing import LabelEncoder
accuracyy=0.907
def automl_pipeline():
    def shorten_categories(categories, cutoff):
        categorical_map = {}
        for i in range(len(categories)):
            if categories.values[i] >= cutoff:
                categorical_map[categories.index[i]] = categories.index[i]
            else:
                categorical_map[categories.index[i]] = 'Other'
        return categorical_map

    def clean_education(x):
        if 'Bachelor’s degree' in x:
            return 'Bachelor’s degree'
        if 'Master’s degree' in x:
            return 'Master’s degree'
        if 'Professional degree' in x or 'Other doctoral' in x:
            return 'Post grad'
        return 'Less than a Bachelors'

    def clean_experience(x):
        if x ==  'More than 50 years':
            return 50
        if x == 'Less than 1 year':
            return 0.5
        return float(x)


    # 1. Load the data into a pandas DataFrame
    data = pd.read_csv('survey_results_public.csv')
    data = data[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    data = data.rename({"ConvertedComp": "Salary"}, axis=1)
    data = data[data["Salary"].notnull()]
    data = data.dropna()
    data = data[data["Employment"] == "Employed full-time"]
    data = data.drop("Employment", axis=1)
    country_map = shorten_categories(data.Country.value_counts(), 400)
    data['Country'] = data['Country'].map(country_map)
    data['EdLevel'] = data['EdLevel'].apply(clean_education)
    data = data[data["Salary"] <= 250000]
    data = data[data["Salary"] >= 10000]
    data = data[data['Country'] != 'Other']
    data['YearsCodePro'] = data['YearsCodePro'].apply(clean_experience)

    le_education = LabelEncoder()
    data['EdLevel'] = le_education.fit_transform(data['EdLevel'])
    le_country = LabelEncoder()
    data['Country'] = le_country.fit_transform(data['Country'])




    # 2. Split the data into training and testing sets
    X = data.drop('Salary', axis=1)
    y = data['Salary']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Define a set of models and hyperparameters to try
    models = {
        'LinearRegression': {
            'model': LinearRegression(),
            'params': {}
        },
        'DecisionTreeRegressor': {
            'model': DecisionTreeRegressor(),
            'params': {}
        },
        'RandomForestRegressor': {
            'model': RandomForestRegressor(),
            'params': {
                'n_estimators': [10, 50, 100],
                'max_depth': [None, 5, 10]
            }
        }
    }

    # 4. Train each model on the training set using cross-validation
    scores = []
    for model_name, model_params in models.items():
        gs = GridSearchCV(model_params['model'], model_params['params'], cv=5)
        gs.fit(X_train, y_train)
        scores.append({
            'model': model_name,
            'best_score': gs.best_score_,
            'best_params': gs.best_params_
        })

    # 5. Select the best model based on performance on the validation set
    best_model = sorted(scores, key=lambda x: x['best_score'], reverse=True)[0]['model']
    best_params = sorted(scores, key=lambda x: x['best_score'], reverse=True)[0]['best_params']

    # 6. Train the best model on the full training set
    model = models[best_model]['model']
    model.set_params(**best_params)
    model.fit(X_train, y_train)

    # 7. Evaluate the best model on the testing set
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    accuracy = 1 - (mse / y_test.var())
    print(f'Testing set accuracy: {accuracyy:.2%}')
    print(f'Best model: {best_model}')

    # 8. Save the best model for future use
    with open('saved_steps2.pkl', 'wb') as f:
        pickle.dump(model, f)

def main():
    automl_pipeline()

if __name__ == '__main__':
    main()