import json
import re

import requests
from lxml import etree
from util import db_handle

def t1():
    # insert your API key here
    API_KEY = '2BPofIMYS789jEMXbi8dcEiF4Xj'

    params = {
        'a': 'BTC',
        'i': '24h',
        'api_key': API_KEY
    }
    coin_list = ['BTC', 'ETH', 'AAVE', 'ABT', 'AMPL', 'ANT', 'ARMOR', 'BADGER', 'BAL', 'BAND', 'BAT', 'BIX', 'BNT',
                 'BOND',
                 'BRD', 'BUSD', 'BZRX', 'CELR', 'CHSB', 'CND', 'COMP', 'CREAM', 'CRO', 'CRV', 'CVC', 'CVP', 'DAI',
                 'DDX',
                 'DENT', 'DGX', 'DHT', 'DMG', 'DODO', 'DOUGH', 'DRGN', 'ELF', 'ENG', 'ENJ', 'EURS', 'FET', 'FTT', 'FUN',
                 'GNO', 'GUSD', 'HEGIC', 'HOT', 'HPT', 'HT', 'HUSD', 'INDEX', 'KCS', 'LAMB', 'LBA', 'LDO', 'LEO',
                 'LINK',
                 'LOOM', 'LRC', 'MANA', 'MATIC', 'MCB', 'MCO', 'MFT', 'MIR', 'MKR', 'MLN', 'MTA', 'MTL', 'MX', 'NDX',
                 'NEXO', 'NFTX', 'NMR', 'Nsure', 'OCEAN', 'OKB', 'OMG', 'PAY', 'PERP', 'PICKLE', 'PNK', 'PNT', 'POLY',
                 'POWR', 'PPT', 'QASH', 'QKC', 'QNT', 'RDN', 'REN', 'REP', 'RLC', 'ROOK', 'RPL', 'RSR', 'SAI', 'SAN',
                 'SNT',
                 'SNX', 'STAKE', 'STORJ', 'sUSD', 'SUSHI', 'TEL', 'TOP', 'UBT', 'UMA', 'UNI', 'USDC', 'USDK', 'USDP',
                 'USDT', 'UTK', 'VERI', 'WaBi', 'WAX', 'WBTC', 'WETH', 'wNXM', 'WTC', 'YAM', 'YFI', 'ZRX']

    api_url = 'https://api.glassnode.com/v1/metrics/derivatives/futures_open_interest_latest'
    res = requests.get(api_url,
                       params=params)
    print(res)
    result_list = json.loads(res.text)
    print(result_list)
    db_handle(api_url, 'BTC', result_list)


def t2():
    test = '/v1/metrics/addresses/sending_to_exchanges_count'
    result = re.match(r'/v1/metrics/[a-z/_]+', test)
    if result:
        print(result)
        print('ok')
    else:
        print('failed')


def t3():
    url = "https://docs.glassnode.com/api/addresses"
    r = requests.get(url=url)
    tree = etree.HTML(r.text)
    print(r)
    print(r.text)
    # result = re.match(r'/v1/metrics/[a-z]*', r.text)
    result = tree.xpath(
        '/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[1]/div[2]/div[2]/div')
    print(result)
    for i in result:
        print(i.text)
    # print(result.string)


def t4():
    tup = (('addresses_active_count_v',), ('addresses_count_v',), ('addresses_min_100_count_v',),
           ('addresses_min_10_count_v',), ('addresses_min_10k_count_v',), ('addresses_min_1_count_v',),
           ('addresses_min_1k_count_v',), ('addresses_min_point_1_count_v',), ('addresses_min_point_zero_1_count_v',),
           ('addresses_new_non_zero_count_v',), ('addresses_non_zero_count_v',), ('addresses_receiving_count_v',),
           ('addresses_sending_count_v',), ('blockchain_block_count_v',), ('blockchain_block_height_v',),
           ('blockchain_block_interval_mean_v',), ('blockchain_block_interval_median_v',),
           ('blockchain_block_size_mean_v',), ('blockchain_block_size_sum_v',), ('blockchain_utxo_created_count_v',),
           ('blockchain_utxo_created_value_mean_v',), ('blockchain_utxo_created_value_median_v',),
           ('blockchain_utxo_created_value_sum_v',), ('blockchain_utxo_loss_count_v',),
           ('blockchain_utxo_profit_count_v',), ('blockchain_utxo_profit_relative_v',),
           ('blockchain_utxo_spent_count_v',), ('blockchain_utxo_spent_value_mean_v',),
           ('blockchain_utxo_spent_value_median_v',), ('blockchain_utxo_spent_value_sum_v',),
           ('derivatives_futures_open_interest_latest_data',), ('derivatives_futures_volume_daily_latest_data',),
           ('derivatives_options_25delta_skew_1_month_v',), ('derivatives_options_25delta_skew_1_week_v',),
           ('derivatives_options_25delta_skew_3_months_v',), ('derivatives_options_25delta_skew_6_months_v',),
           ('derivatives_options_25delta_skew_all_o',), ('distribution_balance_1pct_holders_v',),
           ('distribution_balance_exchanges_all_o',), ('distribution_balance_exchanges_relative_v',),
           ('distribution_balance_exchanges_v',), ('distribution_balance_mtgox_trustee_v',),
           ('distribution_balance_wbtc_v',), ('distribution_exchange_net_position_change_v',), ('distribution_gini_v',),
           ('distribution_herfindahl_v',), ('eth2_staking_deposits_count_v',), ('eth2_staking_phase_0_goal_percent_v',),
           ('eth2_staking_total_deposits_count_v',), ('eth2_staking_total_validators_count_v',),
           ('eth2_staking_total_volume_sum_v',), ('eth2_staking_validators_count_v',), ('eth2_staking_volume_sum_v',),
           ('fees_fee_ratio_multiple_v',), ('fees_volume_mean_v',), ('fees_volume_median_v',), ('fees_volume_sum_v',),
           ('id',), ('indicators_asol_v',), ('indicators_average_dormancy_supply_adjusted_v',),
           ('indicators_average_dormancy_v',), ('indicators_balanced_price_usd_v',),
           ('indicators_cdd90_age_adjusted_v',), ('indicators_cdd_supply_adjusted_binary_v',),
           ('indicators_cdd_supply_adjusted_v',), ('indicators_cdd_v',), ('indicators_cvdd_v',),
           ('indicators_cyd_supply_adjusted_v',), ('indicators_cyd_v',),
           ('indicators_difficulty_ribbon_compression_v',), ('indicators_difficulty_ribbon_o',),
           ('indicators_dormancy_flow_v',), ('indicators_hash_ribbon_o',), ('indicators_liveliness_v',),
           ('indicators_msol_v',), ('indicators_net_realized_profit_loss_v',),
           ('indicators_net_unrealized_profit_loss_v',), ('indicators_nvt_v',), ('indicators_nvts_v',),
           ('indicators_puell_multiple_v',), ('indicators_realized_loss_v',),
           ('indicators_realized_profit_loss_ratio_v',), ('indicators_realized_profit_v',),
           ('indicators_reserve_risk_v',), ('indicators_rhodl_ratio_v',), ('indicators_soab_o',),
           ('indicators_sol_1d_1w_v',), ('indicators_sol_1h_24h_v',), ('indicators_sol_1h_v',),
           ('indicators_sol_1m_3m_v',), ('indicators_sol_1w_1m_v',), ('indicators_sol_1y_2y_v',),
           ('indicators_sol_2y_3y_v',), ('indicators_sol_3m_6m_v',), ('indicators_sol_3y_5y_v',),
           ('indicators_sol_5y_7y_v',), ('indicators_sol_6m_12m_v',), ('indicators_sol_7y_10y_v',),
           ('indicators_sol_more_10y_v',), ('indicators_sopr_adjusted_v',), ('indicators_sopr_v',),
           ('indicators_ssr_o',), ('indicators_ssr_oscillator_v',), ('indicators_stock_to_flow_deflection_v',),
           ('indicators_stock_to_flow_ratio_o',), ('indicators_svab_o',), ('indicators_svl_1d_1w_v',),
           ('indicators_svl_1h_24h_v',), ('indicators_svl_1h_v',), ('indicators_svl_1m_3m_v',),
           ('indicators_svl_1w_1m_v',), ('indicators_svl_1y_2y_v',), ('indicators_svl_2y_3y_v',),
           ('indicators_svl_3m_6m_v',), ('indicators_svl_3y_5y_v',), ('indicators_svl_5y_7y_v',),
           ('indicators_svl_6m_12m_v',), ('indicators_svl_7y_10y_v',), ('indicators_unrealized_loss_v',),
           ('indicators_unrealized_profit_v',), ('indicators_velocity_v',), ('lightning_channel_size_mean_v',),
           ('lightning_channel_size_median_v',), ('lightning_channels_count_v',), ('lightning_network_capacity_sum_v',),
           ('lightning_nodes_count_v',), ('market_price_usd_close_v',), ('mining_difficulty_latest_v',),
           ('mining_hash_rate_mean_v',), ('mining_marketcap_thermocap_ratio_v',), ('mining_revenue_from_fees_v',),
           ('mining_revenue_sum_v',), ('mining_thermocap_v',), ('mining_volume_mined_sum_v',),
           ('supply_active_1d_1w_v',), ('supply_active_1m_3m_v',), ('supply_active_1w_1m_v',),
           ('supply_active_1y_2y_v',), ('supply_active_24h_v',), ('supply_active_2y_3y_v',), ('supply_active_3m_6m_v',),
           ('supply_active_3y_5y_v',), ('supply_active_5y_7y_v',), ('supply_active_6m_12m_v',),
           ('supply_active_7y_10y_v',), ('supply_active_more_10y_v',), ('supply_active_more_1y_percent_v',),
           ('supply_active_more_2y_percent_v',), ('supply_active_more_3y_percent_v',),
           ('supply_active_more_5y_percent_v',), ('supply_current_adjusted_v',), ('supply_current_v',),
           ('supply_hodl_waves_o',), ('supply_inflation_rate_v',), ('supply_issued_v',), ('supply_loss_sum_v',),
           ('supply_profit_relative_v',), ('supply_profit_sum_v',), ('supply_rcap_hodl_waves_o',),
           ('supply_supply_by_txout_type_o',), ('symbol',), ('t',), ('transactions_count_v',), ('transactions_rate_v',),
           ('transactions_size_mean_v',), ('transactions_size_sum_v',),
           ('transactions_transfers_between_exchanges_count_v',), ('transactions_transfers_to_exchanges_count_v',),
           ('transactions_transfers_volume_adjusted_mean_v',), ('transactions_transfers_volume_adjusted_sum_v',),
           ('transactions_transfers_volume_between_exchanges_sum_v',),
           ('transactions_transfers_volume_exchanges_net_v',), ('transactions_transfers_volume_mean_v',),
           ('transactions_transfers_volume_median_v',), ('transactions_transfers_volume_sum_v',),
           ('transactions_transfers_volume_to_exchanges_mean_v',),
           ('transactions_transfers_volume_to_exchanges_sum_v',))
    column_set = [i[0] for i in tup]
    print(column_set)


if __name__ == '__main__':
    t1()
