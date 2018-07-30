# I'll use this laters
from collections import defaultdict
from json import dumps
from datetime import datetime
from errors import TradeAppError, TradeAppValueError

# we are assuming that the time is in this format '23-10-2018 6:20PM'


def format_trades(trades):
    try:
        results = []
        for trade in trades:
            # we are assuming that each trade has a unique id
            results.append(
                {
                    "trade_id": trade["trade_id"],
                    "market_value": market_value(trade["price"], trade["quantity"]),
                }
            )
        results.append({"instruments": process_instruments(trades)})
        results.append({"per_day": process_per_day(trades)})
        return results
    except TradeAppValueError as error:
        raise TradeAppError(unicode(error))


def process_instruments(trades):
    instruments = trades_per_instrument(trades)
    results = []
    for instrument_name, instrument_values in instruments.items():
        instrument_per_day = []
        # trades per day based on a specific instrument
        instrument_days = trades_per_day(instrument_values)
        for timestamp, instrument_trades in instrument_days.items():
            # convert timestamp to a datetime object
            instrument_per_day.append(
                {
                    "total_market_value": total_trades(instrument_trades),
                    "closing_value": closing_value(instrument_trades).isoformat(),
                    "avrage_priceper_day": avrage_price_per_day(instrument_trades),
                }
            )

        results.append(
            {
                "instrument_name": instrument_name,
                "instrument_per_day": instrument_per_day,
            }
        )
    return results


def process_per_day(trades):
    # trades per day
    per_day = trades_per_day(trades)
    results = []
    for day, trades in per_day.items():
        results.append(
            {
                "day": day,
                "trades_per_day": {
                    "total_traded_value": total_trades(trades),
                    "closing_value": closing_value(trades).isoformat(),
                    "closing_position": "I have no idea about this :/",
                },
            }
        )
    return results


def trades_per_day(trades):
    """
    This function returns a dictionary
        <keys> : day number based on timestamps that is been given
        <value> : list of dict that is in the same time stamp
    """
    group_by_day = defaultdict(list)
    for trade in trades:
        parsed_timestamp = datetime.strptime(trade["timestamp"], "%d-%m-%Y %I:%M%p")
        group_by_day[parsed_timestamp.day].append(trade)
    return group_by_day


def trades_per_instrument(trades):
    """
    This function returns a dictionary
        <keys> : instrument name
        <value> : list of trades for the same instrument
    """
    group_by_instrument = defaultdict(list)
    for trade in trades:
        group_by_instrument[trade["instrument"]].append(trade)
    return group_by_instrument


def market_value(price, quantity):
    try:
        return int(price) * int(quantity)
    except ValueError as error:
        raise TradeAppValueError(unicode(error))


def total_trades(ordered_trade):
    try:
        return sum(
            [
                market_value(trade_per_day["price"], trade_per_day["quantity"])
                for trade_per_day in ordered_trade
            ]
        )
    except ValueError as error:
        raise TradeAppValueError(unicode(error))


def closing_value(ordered_trade):
    try:
        return max(
            [
                datetime.strptime(trade["timestamp"], "%d-%m-%Y %I:%M%p")
                for trade in ordered_trade
            ]
        )
    except ValueError as error:
        raise TradeAppValueError(unicode(error))


def avrage_price_per_day(ordered_trade):
    try:
        return sum(
            [int(trade_per_day["price"]) for trade_per_day in ordered_trade]
        ) / len(ordered_trade)
    except ValueError as error:
        raise TradeAppValueError(unicode(error))
