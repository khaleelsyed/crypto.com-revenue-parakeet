import os

import pandas as pd


def load_data(directory, filenames=('SPOT_ORDER', 'SPOT_TRADE')):
    """
    Preload required data

    :param directory: File directory in question
    :param filenames: The files containing the Spot orders. Helps to
        have both the trade and order files so that they can be interlinked easily
    """
    raw_data = (pd.read_csv(directory + file + '.csv', delimiter=',', header='infer') for file in filenames)
    raw_orders = raw_data[0]
    raw_trades = raw_data[1]
    return clean_data(raw_orders, raw_trades)


def clean_data(orders, trades):

    # NOTE: A single order may result in multiple trades
    new_df = pd.DataFrame()

    i = 0
    while i < len(orders):
        df_cursor = orders.iloc[i]

        if df_cursor['Status'] == 'FILLED':
            new_df.append(df_cursor)
            # TODO: Add data from trades

        elif df_cursor['Status'] != 'CANCELLED':
            # Something went wrong -> Investigate
            raise Exception(f'Invalid Order status: \n'
                            f'{df_cursor["Order ID"]}: {df_cursor["Status"]}')
        i += 1
    return new_df


data = load_data(os.getcwd() + '/data/' + 'Spot Wallet - Order History,2021-09-01 - 2021-12-15,/')
