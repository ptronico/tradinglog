from django.db.models import Count, Q

from .models import Trade


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
