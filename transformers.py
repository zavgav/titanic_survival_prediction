# transformers.py
import pandas as pd
from sklearn.preprocessing import FunctionTransformer

def age_transformer(df):
    df = df.copy()
    df["Age"] = df.groupby(['Sex', 'Pclass'])['Age'].transform(lambda x: x.fillna(x.median()))
    return df["Age"].to_frame()

def family_size(df):
    df = df.copy()
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)
    return df[['FamilySize', 'IsAlone']]

def has_cabin(df):
    df = df.copy()
    df['HasCabin'] = df["Cabin"].notnull().astype(int)
    return df['HasCabin'].to_frame()

age_transform = FunctionTransformer(age_transformer)
family_transform = FunctionTransformer(family_size)
cabin_transform = FunctionTransformer(has_cabin)