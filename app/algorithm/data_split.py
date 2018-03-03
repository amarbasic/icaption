import pandas as pd
from sklearn.model_selection import train_test_split

from app.algorithm import helper


def split_data():
    print("Data splitting . . ", end="")
    data = pd.read_table(helper.root_dir() + '/data/data.txt', sep="*")

    train_data, test_data = train_test_split(data, test_size=0.1, shuffle=True)

    train_data.to_csv(helper.root_dir() + '/data/train.txt', sep="*", index=None)
    test_data.to_csv(helper.root_dir() + '/data/test.txt', sep="*", index=None)
    print("Done. Data saved to data folder. Test: {} rows. Train: {} rows.".format(train_data.shape[0], test_data.shape[0]))


if __name__ == '__main__':
    split_data()
