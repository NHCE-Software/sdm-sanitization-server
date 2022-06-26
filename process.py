from pprint import pprint
import json
import pandas as pd
nan_value = float("NaN")
# asserting column list: incoming csv must contain these values
csvformat = ['bs', 'branch', 'enqno', 'dateofadmission', 'studentname', 'sex',
             'stream', 'dob', 'fathersname', 'fathersoccupation', 'income',
             'mothersname', 'contactnos/mobile/parents', 'contactnos/land/parents',
             'nameofthelocalgurdian', 'contactnos/mobile/gg', 'contactnos/land/gg',
             'mothertongue', 'thcollegename', 'state', 'documentssubmitted',
             'docdue', 'qlyexampassed', 'regno', 'yrofpassing', 'board', 'state',
             'marksobtained/phy', 'marksobtained/mth', 'marksobtained/chm',
             'marksobtained/bio', 'marksobtained/elc', 'marksobtained/comp',
             'marksobtained/total', 'pcmagg', 'pcm', 'methodofcalculation',
             'overall', 'caste', 'religion', 'nationality', 'address/city',
             'address/state', 'address/permanent', 'address/pincode',
             'address/communication', 'emailid', 'remarks']


def sanitze(string):
    string = string.lower()
    for i in string:
        if i not in "abcdefghijklmnopqrstuvwxyz/":
            string = string.replace(i, "")
    return string


def mergeheaders(df):
    cols = df.columns
    cols2 = df.values[0]
    # merging col names
    mergeCols = []
    for i, c in enumerate(cols):
        if "Unnamed:" in c:
            mergeCols.append(mergeCols[len(mergeCols) - 1])
        else:
            mergeCols.append(c)
    mergeCols2 = []
    for i, c in enumerate(cols2):
        col = mergeCols[i]
        if "nan" not in str(c):
            mergeCols2.append(col + "/" + c)
        else:
            mergeCols2.append(col)

    # print(mergeCols2)
    mergeCols2 = [sanitze(x) for x in mergeCols2]
    mergeCols2[12] = "contactnos/mobile/parents"
    mergeCols2[13] = "contactnos/land/parents"
    mergeCols2[15] = "contactnos/mobile/gg"
    mergeCols2[16] = "contactnos/land/gg"

    df.columns = mergeCols2
    df = df.iloc[1:, :]

    def sjoin(x): return ';'.join(x[x.notnull()].astype(str))
    df = df.groupby(level=0, axis=1).apply(lambda x: x.apply(sjoin, axis=1))
    print(df.columns)
    return df


def assertFormat(df):
    return set(df.columns) == set(csvformat)


# FA => failed assertion -> CSV is not following format
# SWA => something went wrong


def processCSV(file):
    df = pd.read_csv(file)
    try:
        df = mergeheaders(df)
        # asserting if csv is in correct format
        if not assertFormat(df):
            return {"message": "Cant process, please check CSV", "statusCode": "FA"}
        df.replace("", nan_value, inplace=True)
        df = df.dropna(axis=0)
        df = df.dropna(axis=1)
        lol = df.to_json(orient="records")
        return {"message": "processed", "payload": json.loads(lol)}
    except Exception as e:
        print(e)
        return {"message": "Something went wrong", "statusCode": "SWA"}
