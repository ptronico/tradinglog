from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncDate

from .models import Trade, TradeErrors


def get_general_info(start_date=None, end_date=None):
    """
    This function returns general information
    about the trading account.
    """
    qs_filter = {
        'status': Trade.STATUS_CLOSED,
    }
    if start_date:
        qs_filter['close_date__gte'] = start_date
    if end_date:
        qs_filter['close_date__lte'] = end_date

    totals = Trade.objects.filter(**qs_filter).aggregate(
            count=Count('pk'),
            gain_count=Count('pk', filter=Q(profit__gt=0)),
            loss_count=Count('pk', filter=Q(profit__lt=0)),
            breakeven_count=Count('pk', filter=Q(profit=0)),
            gain_profit=Sum('profit', filter=Q(profit__gt=0)),
            loss_profit=Sum('profit', filter=Q(profit__lt=0)))

    totals['loss_profit'] = abs(totals['loss_profit'])

    totals['avg_gain'] = totals['gain_profit'] / totals['gain_count'] if totals['gain_count'] else 0
    totals['avg_loss'] = totals['loss_profit'] / totals['loss_count'] if totals['gain_count'] else 0
    totals['winrate'] = 100.00 * totals['gain_count'] / totals['count'] if totals['count'] else 0
    totals['profit_factor'] = totals['gain_profit'] / totals['loss_profit'] if totals['loss_profit'] else 0
    totals['max_drawdown'] = None

    return totals


def get_result_profit():

    reais = 0
    ticks = 0
    result = []
    for obj in Trade.objects.filter().values('pk', 'profit', 'profit_ticks', 'close_date').order_by('id'):
        reais += obj['profit']
        ticks += obj['profit_ticks']
        result.append({
            'name': obj['pk'],
            'time': obj['close_date'],
            'reais': reais,
            'ticks': ticks,
        })

    return result


def get_result_totals(start_date=None, end_date=None):
    """
    Returns result statistics as GAIN, LOSS or BREAKEVEN.
    """
    qs_filter = {
        'status': Trade.STATUS_CLOSED,
    }
    if start_date:
        qs_filter['close_date__gte'] = start_date
    if end_date:
        qs_filter['close_date__lte'] = end_date
    totals = Trade.objects.filter(**qs_filter).aggregate(
            all=Count('pk'),
            none=Count('pk', filter=Q(result=Trade.RESULT_NONE)),
            gain=Count('pk', filter=Q(result=Trade.RESULT_GAIN)),
            loss=Count('pk', filter=Q(result=Trade.RESULT_LOSS)),
            breakeven=Count('pk', filter=Q(result=Trade.RESULT_BREAK_EVEN)))

    result = []
    result.append({
            'name': 'GAIN',
            'rate': totals['gain'] / totals['all'] if totals['all'] else 0,
            'total': totals['gain'],
    })
    result.append({
            'name': 'LOSS',
            'rate': totals['loss'] / totals['all'] if totals['all'] else 0,
            'total': totals['loss'],
    })
    result.append({
            'name': 'BREAKEVEN',
            'rate': totals['breakeven'] / totals['all'] if totals['all'] else 0,
            'total': totals['breakeven'],
    })
    if totals['none']:
        result.append({
            'name': 'NOT_SET',
            'rate': totals['none'] / totals['all'] if totals['all'] else 0,
            'total': totals['none'],
        })

    return result


def get_strategy_totals(start_date=None, end_date=None):
    """
    Returns result statistics as GAIN, LOSS or BREAKEVEN.
    """
    qs_filter = {
        'status': Trade.STATUS_CLOSED,
        'result__in': [Trade.RESULT_GAIN, Trade.RESULT_LOSS, Trade.RESULT_BREAK_EVEN],
    }
    if start_date:
        qs_filter['close_date__gte'] = start_date
    if end_date:
        qs_filter['close_date__lte'] = end_date
    strategy_list = Trade.objects.filter().values_list('strategy', flat=True).order_by('strategy').distinct()

    agg_gain = {}
    for s in strategy_list:
        agg_gain[s] = Count('pk', filter=Q(strategy=s, result=Trade.RESULT_GAIN))

    agg_loss = {}
    for s in strategy_list:
        agg_loss[s] = Count('pk', filter=Q(strategy=s, result=Trade.RESULT_LOSS))

    agg_breakeven = {}
    for s in strategy_list:
        agg_breakeven[s] = Count('pk', filter=Q(strategy=s, result=Trade.RESULT_BREAK_EVEN))

    result_gain = Trade.objects.filter(**qs_filter).aggregate(**agg_gain)
    result_loss = Trade.objects.filter(**qs_filter).aggregate(**agg_loss)
    result_breakeven = Trade.objects.filter(**qs_filter).aggregate(**agg_breakeven)

    result = []
    for s in strategy_list:
        total = result_gain[s] + result_loss[s] + result_breakeven[s]
        result.append({
            'name': s,
            'total': total,
            'gain': result_gain[s],
            'loss': result_loss[s],
            'breakeven': result_breakeven[s],
            'gain_rate': result_gain[s] / total if total else 0,
            'loss_rate': result_loss[s] / total if total else 0,
            'breakeven_rate': result_breakeven[s] / total if total else 0,
        })

    return sorted(result, key=lambda x: x['gain_rate'], reverse=True)


def get_errors_totals(start_date=None, end_date=None):
    """
    Returns result statistics as GAIN, LOSS or BREAKEVEN.
    """
    qs_filter = {
        'status': Trade.STATUS_CLOSED,
        'result__in': [Trade.RESULT_GAIN, Trade.RESULT_LOSS, Trade.RESULT_BREAK_EVEN],
    }
    if start_date:
        qs_filter['close_date__gte'] = start_date
    if end_date:
        qs_filter['close_date__lte'] = end_date

    result = []
    for te in TradeErrors.objects.all().prefetch_related('trade_set'):
        result.append({
            'name': te.name,
            'count': te.trade_set.all().count(),
        })

    return sorted(result, key=lambda x: x['count'], reverse=True)


def get_daily_report(start_date=None, end_date=None):
    qs_filter = {
        'close_date__isnull': False,
    }
    if start_date:
        qs_filter['close_date__gte'] = start_date
    if end_date:
        qs_filter['close_date__lte'] = end_date

    queryset = Trade.objects.filter(**qs_filter)
    queryset = queryset.annotate(cdate=TruncDate('close_date')).values('cdate')
    queryset = queryset.annotate(tprofit=Sum('profit'), count=Count('pk')).values('cdate', 'tprofit', 'count')
    queryset = queryset.order_by('cdate')

    result = []
    for data in queryset:
        result.append({
            'close_date': data['cdate'],
            'profit': data['tprofit'],
            'count': data['count'],
        })

    return result
