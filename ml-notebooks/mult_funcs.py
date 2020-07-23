def gen_NN_mult(df,model='MLPRegressor',max_iter=20,solver='adam',kernel='rbf',verbose=False):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.neural_network import MLPRegressor
    from sklearn.svm import SVR
    from sklearn.linear_model import LinearRegression
    from sklearn.neighbors import KNeighborsRegressor

    route = df['LINEID'].unique()[0]
    direction = df['DIRECTION'].unique()[0]
    max_trip = df['TRIPLENGTH'].max()
    min_trip = df['TRIPLENGTH'].min()
    
    print(df['TRIPLENGTH'].min(),df['TRIPLENGTH'].max())
    
#     df['TRIPLENGTH'] = (df['TRIPLENGTH'] - df['TRIPLENGTH'].min())/(df['TRIPLENGTH'].max() - df['TRIPLENGTH'].min())
#     df['feels_like'] = (df['feels_like'] - df['feels_like'].min())/(df['feels_like'].max() - df['feels_like'].min())
    
    df_rev1 = pd.get_dummies(df.drop(['LINEID','DIRECTION'],axis=1))
        
#   print(route, direction)
    # y is the target
    max_trip = df_rev1['TRIPLENGTH'].max()
    min_trip = df_rev1['TRIPLENGTH'].min()
    y = (df_rev1['TRIPLENGTH'] - min_trip)/(max_trip - min_trip)
    # X is everything else
    X = df_rev1.drop(["TRIPLENGTH"],1)
    
#   Normalsie feels_like
    max_feels_like = X['feels_like'].max()
    min_feels_like = X['feels_like'].min()
    X['feels_like'] = (X['feels_like'] - min_feels_like)/(max_feels_like - min_feels_like)
    # Split the dataset into two datasets: 70% training and 30% test
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1,  test_size=0.3)

#   timetabled_values_train = X_train['PLANNEDTIME_ARR'] - X_train['PLANNEDTIME_DEP']
#   timetabled_values_test = X_test['PLANNEDTIME_ARR'] - X_test['PLANNEDTIME_DEP']
            
#   X_train.drop('PLANNEDTIME_ARR',axis=1,inplace=True)
#   X_test.drop('PLANNEDTIME_ARR',axis=1,inplace=True)
#   X_train.drop('PLANNEDTIME_DEP',axis=1,inplace=True)
#   X_test.drop('PLANNEDTIME_DEP',axis=1,inplace=True)
            
#   print("original range is: ",df_rev1.shape[0])
#   print("training range (70%):\t rows 0 to", round(X_train.shape[0]))
#   print("test range (30%): \t rows", round(X_train.shape[0]), "to", round(X_train.shape[0]) + X_test.shape[0])
            
# need to reset the index to allow contatenation with predicted values otherwise not joining on same index...
    X_train.reset_index(drop=True, inplace=True)
    y_train.reset_index(drop=True, inplace=True)
    X_test.reset_index(drop=True, inplace=True)
    y_test.reset_index(drop=True, inplace=True)
    X_train.head(5)
        
    timetabled_values_train = X_train['PLANNEDTIME_ARR'] - X_train['PLANNEDTIME_DEP']
    timetabled_values_test = X_test['PLANNEDTIME_ARR'] - X_test['PLANNEDTIME_DEP']
    X_train.drop('PLANNEDTIME_ARR',axis=1,inplace=True)
    X_test.drop('PLANNEDTIME_ARR',axis=1,inplace=True)
    X_train.drop('PLANNEDTIME_DEP',axis=1,inplace=True)
    X_test.drop('PLANNEDTIME_DEP',axis=1,inplace=True)
    
    if model == 'MLPRegressor':
        output_model = MLPRegressor(max_iter=max_iter,solver=solver,).fit(X_train, y_train)
    elif model == 'SVR':
        output_model = SVR(kernel=kernel).fit(X_train, y_train)
    elif model == 'LinearRegression':
        output_model = LinearRegression().fit(X_train, y_train)
    elif model == 'KNeighborsRegressor':
        output_model = KNeighborsRegressor().fit(X_train,y_train)
    
#     test_train_dict[key] = {
#                 'X_train':X_train,
#                 'X_test':X_test,
#                 'y_train':y_train,
#                 'y_test':y_test,
#                 'timetabled_values_train':timetabled_values_train,
#                 'timetabled_values_test':timetabled_values_test
#             }
    
    
    output = {
        'route':route,
        'direction':direction,
        'model':output_model,
        'X_train':X_train,
        'X_test':X_test,
        'y_train':y_train,
        'y_test':y_test,
        'timetabled_values_train':timetabled_values_train/max_trip,
        'timetabled_values_test':timetabled_values_test/max_trip,
        'max_trip':max_trip,
        'min_trip':min_trip,
        'max_feels_like':max_feels_like,
        'min_feels_like':min_feels_like
    }
    if verbose == True:
        print('Done: \t%s\t%s'%(route,direction))
    return output

def gen_NN_mult_200(df):
    return gen_NN_mult(df,max_iter=200)

def gen_NN_mult_500(df):
    return gen_NN_mult(df,max_iter=500)

def gen_NN_mult_1000(df):
    return gen_NN_mult(df,max_iter=1000)

def gen_NN_mult_2000(df):
    return gen_NN_mult(df,max_iter=2000)

def gen_NN_mult_4000(df):
    return gen_NN_mult(df,max_iter=4000)

def gen_NN_mult_6000(df):
    return gen_NN_mult(df,max_iter=6000)

def gen_NN_mult_8000(df):
    return gen_NN_mult(df,max_iter=8000)#

def gen_NN_mult_200_lbfgs(df):
    return gen_NN_mult(df,max_iter=200,solver='lbfgs')

def gen_NN_mult_1000_lbfgs(df):
    return gen_NN_mult(df,max_iter=1000,solver='lbfgs')

def gen_NN_mult_2000_lbfgs(df):
    return gen_NN_mult(df,max_iter=1000,solver='lbfgs')

def gen_SVR_mult_linear(df):
    return gen_NN_mult(df,model='SVR',kernel='linear')

def gen_SVR_mult(df):
    return gen_NN_mult(df,model='SVR',verbose=True)

def gen_LR_mult(df):
    return gen_NN_mult(df,model='LinearRegression')

def gen_KNR_mult(df):
    return gen_NN_mult(df,model='KNeighborsRegressor')