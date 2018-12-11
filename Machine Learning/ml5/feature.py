import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mlbox.preprocessing import *
from mlbox.optimisation import *
from mlbox.prediction import *


def age(df, dtype=True):
    # remove age <= 15
    if dtype:
        df = df[df["age"] > 15]

    # age == 16
    mask = df["age"] <= 16
    df.loc[mask, "industryworkedin"] = "0000"
    df.loc[mask, "workerclass"] = "0"


def keep(df, proc_df):
    proc_df["idnum"] = df["idnum"]
    proc_df["age"] = df["age"]
    proc_df["interestincome"] = df["interestincome"]
    proc_df["industryworkedin"] = df["industryworkedin"]
    proc_df["ancestry"] = df["ancestry"]
    proc_df["sex"] = df["sex"]
    proc_df["hoursworkperweek"] = df["hoursworkperweek"].apply(
        lambda x: 0 if x == '?' else float(x))


def process_datetime(df, proc_df):
    proc_df["traveltimetowork"] = df["traveltimetowork"]
    proc_df["workarrivaltime"] = df["workarrivaltime"]
    proc_df["departtime"] = df["workarrivaltime"]
    proc_df["workhour"] = df["workarrivaltime"]
    proc_df["workminute"] = df["workarrivaltime"]
    proc_df["hasjob"] = 1

    # self employee, etc.
    not_move = (df['workerclass'] >= '6') & (df["traveltimetowork"] == '?')
    proc_df.loc[not_move, "traveltimetowork"] = 0
    proc_df.loc[not_move, "workarrivaltime"] = 0
    proc_df.loc[not_move, "departtime"] = 0
    proc_df.loc[not_move, "workhour"] = 0
    proc_df.loc[not_move, "workminute"] = 0

    # without job
    no_job = (df['workerclass'] == '?') & (df["traveltimetowork"] == '?')
    proc_df.loc[no_job, "hasjob"] = 0
    no_job = (df['workerclass'] == '9')
    proc_df.loc[no_job, "hasjob"] = 0

    # depart time
    travel = df["traveltimetowork"]
    arrive = df["workarrivaltime"]
    for i in df.index:
        if arrive.loc[i] == '?':
            continue
        t = float(arrive.loc[i])
        t = t * 5 - 2.5
        proc_df.loc[i, "workarrivaltime"] = t
        proc_df.loc[i, "departtime"] = t - float(travel.loc[i])
        proc_df.loc[i, "workhour"] = int(t / 60)
        proc_df.loc[i, "workminute"] = t - 60 * int(t / 60)


def school(df, proc_df):
    mask = df["schoolenrollment"] == 1
    proc_df.loc[mask, "joinschool"] = 0
    proc_df.loc[mask, "privateschool"] = "c3"
    mask = df["schoolenrollment"] == 2
    proc_df.loc[mask, "joinschool"] = 1
    proc_df.loc[mask, "privateschool"] = "c0"
    mask = df["schoolenrollment"] == 3
    proc_df.loc[mask, "joinschool"] = 1
    proc_df.loc[mask, "privateschool"] = "c1"


def degree_field(df, proc_df):
    # fill NA
    proc_df["degreefield"] = df["degreefield"]
    proc_df.loc[proc_df["degreefield"] == '?', "degreefield"] = "0000"

    proc_df["field"] = proc_df["degreefield"].apply(lambda x: str(x)[:2])
    proc_df["mixed"] = proc_df["degreefield"].apply(
        lambda x: int(str(x)[2:4] == "99"))


def cat_to_both(df, proc_df):
    mask = df["vehicleoccupancy"] == '?'
    df.loc[mask, "vehicleoccupancy"] = 0

    duplicate = ["vehicleoccupancy", "marital", "educationalattain"]
    for fea in duplicate:
        proc_df[fea + "nu"] = df[fea]


def cat_to_one_hot(train, processed_train, test, processed_test, col_name, threshold=0.01):
    if threshold == 0:
        keys = train[col_name].value_counts().keys()
    else:
        keys = train[col_name].value_counts(normalize=True)
        keys = set(keys[keys >= threshold].keys())

    def do_cat_to_one_hot(df, proc_df, *args, df_col_name=col_name):
        proc_col_name = df_col_name
        for item in args:
            proc_df[proc_col_name + '_is_' + str(item)] = 0
            mask = pd.Series(df[df_col_name] == item)
            proc_df.loc[mask, proc_col_name + '_is_' + str(item)] = 1

        proc_df[proc_col_name + '_is_other'] = 1
        for item in args:
            proc_df.loc[df[df_col_name] == item,
                        proc_col_name + '_is_other'] = 0

    do_cat_to_one_hot(train, processed_train, *list(keys))
    do_cat_to_one_hot(test, processed_test, *list(keys))


def mak_ca(df):
    ca = ["degreefield", "field", "industryworkedin", "ancestry"]

    for fea in ca:
        try:
            mask = df[fea] != '?'
            df.loc[mask, fea] = df.loc[mask, fea].apply(lambda x: "c" + x)
        except:
            df[fea] = df[fea].apply(lambda x: "c" + str(x))


def fill_na(df):
    for fea in df:
        try:
            mask = df[fea] == '?'
            df.loc[mask, fea] = df.loc[mask, fea].apply(lambda x: "NA")
        except:
            continue


def process_data():
    train = pd.read_csv("census_train.csv", names=["idnum", "age", "workerclass", "interestincome",
                                                   "traveltimetowork", "vehicleoccupancy",
                                                   "meansoftransport",
                                                   "marital", "schoolenrollment", "educationalattain",
                                                   "sex", "workarrivaltime", "hoursworkperweek",
                                                   "ancestry",
                                                   "degreefield", "industryworkedin", "wages"])

    test = pd.read_csv("census_test.csv", names=["idnum", "age", "workerclass", "interestincome",
                                                 "traveltimetowork", "vehicleoccupancy",
                                                 "meansoftransport",
                                                 "marital", "schoolenrollment", "educationalattain",
                                                 "sex", "workarrivaltime", "hoursworkperweek", "ancestry",
                                                 "degreefield", "industryworkedin"])

    processed_train = pd.DataFrame()
    processed_test = pd.DataFrame()

    # handle special case for age
    age(train, True)
    age(test, False)

    processed_train["wages"] = train["wages"]

    # process function
    funcs = keep, process_datetime, school, degree_field, cat_to_both

    for fun in funcs:
        fun(train, processed_train)
        fun(test, processed_test)

    dummification = ["workerclass", "vehicleoccupancy",
                     "meansoftransport", "marital", "educationalattain"]

    for fea in dummification:
        cat_to_one_hot(train, processed_train, test, processed_test, fea)

    mak_ca(processed_train)
    mak_ca(processed_test)
    fill_na(processed_train)
    fill_na(processed_test)

    processed_train.to_csv("train.csv", index=False)
    processed_test.to_csv("test.csv", index=False)


def train():
    paths = ["train.csv", "test.csv"]
    target_name = "wages"

    # Reader data
    rd = Reader(sep=',')
    df = rd.train_test_split(paths, target_name)

    dft = Drift_thresholder()
    df = dft.fit_transform(df)

    def my_custom_loss_func(y_true, y_pred):
        num = len(y_true)
        loss = 0.0
        mask = y_pred < 0
        loss += 100000000 * len(y_pred[mask])
        loss += np.sum((y_true - y_pred) ** 2)
        return np.sqrt(loss / num)

    rmse = make_scorer(my_custom_loss_func,
                       greater_is_better=False, needs_proba=False)
    opt = Optimiser(scoring=rmse, n_folds=3)

    space = {
        'ne__numerical_strategy': {"search": "choice",
                                   "space": ['mean']},
        'est__strategy': {"search": "choice",
                          "space": ["LightGBM"]},
        'est__n_estimators': {"search": "choice",
                              "space": [2100]},
        'est__colsample_bytree': {"search": "uniform",
                                  "space": [0.5, 0.95]},
        'fs__threshold': {"search": "uniform",
                          "space": [0.1, 0.5]},
        'fs__strategy': {"search": "choice",
                         "space": ['variance']},
        'ce__strategy': {"search": "choice",
                         "space": ['entity_embedding']},
        'est__subsample': {"search": "uniform",
                           "space": [0.5, 0.97]},
        'est__max_depth': {"search": "choice",
                           "space": [4, 5, 6]},
        'est__learning_rate': {"search": "uniform",
                               "space": [0.0005, 0.015]},
        'est__reg_alpha': {"search": "uniform",
                           "space": [0, 5]},
        'est__reg_lambda': {"search": "uniform",
                            "space": [0, 5]},
    }

    params = opt.optimise(space, df, 100)

    return params, df


def validate(params, df):
    # Mean Squre Error
    rmse1 = make_scorer(lambda y_true, y_pred: np.sqrt(np.sum(
        (y_true - y_pred) ** 2) / len(y_true)), greater_is_better=False, needs_proba=False)
    opt1 = Optimiser(scoring=rmse1, n_folds=3)
    opt1.evaluate(params, df)


def predict(params, df):
    prd = Predictor()
    prd.fit_predict(params, df)

    test = pd.read_csv("census_test.csv", names=["idnum", "age", "workerclass", "interestincome",
                                                 "traveltimetowork", "vehicleoccupancy",
                                                 "meansoftransport",
                                                 "marital", "schoolenrollment", "educationalattain",
                                                 "sex", "workarrivaltime", "hoursworkperweek", "ancestry",
                                                 "degreefield", "industryworkedin"])
    result = pd.read_csv("save/wages_predictions.csv", names=["idnum", "wages"], header=0)

    combine = pd.DataFrame()
    combine["Id"] = test["idnum"]
    combine["Wages"] = result["wages"].apply(lambda x: max(0, x))

    combine.to_csv("test outputs.csv", index=False)


if __name__ == "__main__":
    process_data()
    params, df = train()
    validate(params, df)
    predict(params, df)
