start_ts = 1514736000
# bar_list = {"1m", "5m", "15m", "30m", "1H", "4H", "1D", "1W"}
bar_list = {"1H", "4H", "1D", "1W"}
bar_sec_dict = {"1m": 60, "5m": 300, "15m": 900, "30m": 1800, "1H": 3600, "4H": 14400, "1D": 86400, "1W": 604800}

contract_list = {'BTC', 'ETH', 'MATIC', 'LTC', 'XRP', 'BCH', 'SOL', 'PEPE', 'DOGE', 'FIL', '1INCH', 'AAVE', 'ACE', 'ADA',
                 'AGIX', 'AGLD', 'AIDOGE', 'ALGO', 'ALPHA', 'ANT', 'APE', 'API3', 'APT', 'AR', 'ARB', 'ATOM', 'AUCTION',
                 'AVAX', 'AXS', 'BADGER', 'BAL', 'BAND', 'BAT', 'BICO', 'BIGTIME', 'BLUR', 'BNB', 'BNT', 'BONK', 'BSV',
                 'CEL', 'CELO', 'CETUS', 'CFX', 'CHZ', 'COMP', 'CORE', 'CRO', 'CRV', 'CSPR', 'CTC', 'CVC', 'DMAIL', 'DOT',
                 'DYDX', 'EGLD', 'ENS', 'EOS', 'ETC', 'ETHW', 'FET', 'FITFI', 'FLM', 'FLOKI', 'FLOW', 'FLR', 'FRONT', 'FTM',
                 'FXS', 'GAL', 'GALA', 'GAS', 'GFT', 'GMT', 'GMX', 'GODS', 'GRT', 'HBAR', 'ICP', 'ID', 'IMX', 'INJ', 'IOST',
                 'IOTA', 'JOE', 'JST', 'JTO', 'JUP', 'KISHU', 'KLAY', 'KNC', 'KSM', 'LDO', 'LINK', 'LOOKS', 'LPT', 'LQTY',
                 'LRC', 'LSK', 'LUNA', 'LUNC', 'MAGIC', 'MANA', 'MASK', 'MEME', 'METIS', 'MINA', 'MKR', 'MOVR', 'NEAR',
                 'NEO', 'NFT', 'NMR', 'OMG', 'ONT', 'OP', 'ORBS', 'ORDI', 'PEOPLE', 'PERP', 'PYTH', 'QTUM', 'RACA', 'RDNT',
                 'REN', 'RNDR', 'RON', 'RSR', 'RVN', 'SAND', 'SATS', 'SHIB', 'SLP', 'SNX', 'SSV', 'STARL', 'STORJ', 'STX',
                 'SUI', 'SUSHI', 'SWEAT', 'THETA', 'TIA', 'TON', 'TRB', 'TRX', 'TURBO', 'UMA', 'UNI', 'USDC', 'USTC', 'VRA',
                 'WAXP', 'WLD', 'WOO', 'WSM', 'XCH', 'XLM', 'XTZ', 'YFI', 'YGG', 'ZETA', 'ZIL', 'ZRX'}

spot_list = {'BTC', 'ETH', 'OKB', 'MATIC', 'LTC', 'XRP', 'BCH', 'SOL', 'PEPE', 'DOGE', 'FIL', '1INCH', 'AAVE', 'ACA', 'ACE',
             'ACH', 'ADA', 'AERGO', 'AGIX', 'AGLD', 'AIDOGE', 'AKITA', 'ALCX', 'ALGO', 'ALPHA', 'ANT', 'APE', 'API3', 'APM',
            'APT', 'AR', 'ARB', 'ARG', 'ARTY', 'AST', 'ASTR', 'ATOM', 'AUCTION', 'AVAX', 'AVIVE', 'AXS', 'AZY', 'BABYDOGE',
        'BADGER', 'BAL', 'BAND', 'BAT', 'BETH', 'BICO', 'BIGTIME', 'BLOK', 'BLUR', 'BNB', 'BNT', 'BONE', 'BONK',
        'BORA', 'BORING', 'BRWL', 'BSV', 'BTT', 'BZZ', 'CEEK', 'CEL', 'CELO', 'CELR', 'CETUS', 'CFG', 'CFX', 'CGL',
        'CHZ', 'CITY', 'CLV', 'COMP', 'CONV', 'CORE', 'CQT', 'CRO', 'CRV', 'CSPR', 'CTC', 'CTXC', 'CVC', 'CVX', 'DAI',
        'DAO', 'DCR', 'DEP', 'DGB', 'DIA', 'DMAIL', 'DORA', 'DOSE', 'DOT', 'DYDX', 'EGLD', 'ELF', 'ELON', 'EM', 'ENJ',
        'ENS', 'EOS', 'ERN', 'ETC', 'ETHW', 'EURT', 'FET', 'FITFI', 'FLM', 'FLOKI', 'FLOW', 'FLR', 'FORTH', 'FRONT',
        'FTM', 'FXS', 'GAL', 'GALA', 'GALFT', 'GARI', 'GAS', 'GEAR', 'GF', 'GFT', 'GHST', 'GLM', 'GLMR', 'GMT', 'GMX',
        'GOAL', 'GODS', 'GOG', 'GRT', 'HBAR', 'HC', 'ICE', 'ICP', 'ICX', 'ID', 'IGU', 'ILV', 'IMX', 'INJ', 'IOST',
        'IOTA', 'IQ', 'JOE', 'JPG', 'JST', 'JTO', 'JUP', 'KAN', 'KAR', 'KCAL', 'KDA', 'KINE', 'KISHU', 'KLAY', 'KNC',
        'KP3R', 'KSM', 'LAMB', 'LAT', 'LBR', 'LDO', 'LEASH', 'LEO', 'LET', 'LHINU', 'LING', 'LINK', 'LITH', 'LON',
        'LOOKS', 'LPT', 'LQTY', 'LRC', 'LSK', 'LUNA', 'LUNC', 'MAGIC', 'MANA', 'MASK', 'MDT', 'MEME', 'MENGO', 'METIS',
        'MILO', 'MINA', 'MKR', 'MLN', 'MOVEZ', 'MOVR', 'MRST', 'MXC', 'MYRIA', 'NEAR', 'NEO', 'NFT', 'NMR', 'NULS',
        'NYM', 'OAS', 'OKT', 'OM', 'OMG', 'OMI', 'OMN', 'ONE', 'ONT', 'OP', 'ORB', 'ORBS', 'ORDI', 'OXT', 'PCI',
        'PEOPLE', 'PERP', 'PHA', 'PIT', 'POLS', 'POLYDOGE', 'POR', 'PRQ', 'PSTAKE', 'PYTH', 'QTUM', 'RACA', 'RADAR',
        'RAY', 'RDNT', 'REN', 'REP', 'REVV', 'RIO', 'RNDR', 'RON', 'RPL', 'RSR', 'RSS3', 'RVN', 'SAMO', 'SAND', 'SATS',
        'SC', 'SD', 'SHIB', 'SIS', 'SKEB', 'SKL', 'SLP', 'SNT', 'SNX', 'SPELL', 'SPURS', 'SSV', 'SSWP', 'STARL', 'STC',
        'STETH', 'STORJ', 'STX', 'SUI', 'SUN', 'SUSHI', 'SWEAT', 'SWFTC', 'T', 'TAKI', 'TAMA', 'THETA', 'THG', 'TIA',
        'TON', 'TRA', 'TRB', 'TRX', 'TUP', 'TURBO', 'UMA', 'UNI', 'USDC', 'USDT', 'USTC', 'UTK', 'VELA', 'VELO',
        'VELODROME', 'VRA', 'VSYS', 'WAXP', 'WBTC', 'WIFI', 'WIN', 'WLD', 'WNCG', 'WOO', 'WSM', 'WXT', 'XAUT', 'XCH',
        'XEC', 'XEM', 'XETA', 'XLM', 'XNO', 'XPR', 'XTZ', 'YFI', 'YFII', 'YGG', 'ZBC', 'ZETA', 'ZIL', 'ZRX'}
