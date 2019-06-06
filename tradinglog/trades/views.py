import os

from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .utils import handle_uploaded_file
from .forms import TradeForm
from .models import Trade


@login_required
def dashboard(request):

    open_object_list = Trade.objects.filter(status=Trade.STATUS_OPEN)

    context = {
        'Trade': Trade,
        'open_object_list': open_object_list,
    }

    return render(request, 'dashboard.html', context)


@login_required
def history(request):

    closed_object_list = Trade.objects.filter(status=Trade.STATUS_CLOSED)

    context = {
        'Trade': Trade,
        'closed_object_list': closed_object_list,
    }

    return render(request, 'history.html', context)


@login_required
def edit(request, pk=None):

    trade = Trade.objects.get(pk=pk) if pk else Trade()

    if request.method == 'POST':
        form = TradeForm(request.POST, request.FILES)
        if form.is_valid():
            trade = form.save(trade)
            if 'image' in request.FILES:
                # temppath = settings.MEDIA_ROOT.child('_tempfile')
                filename = 'uploads/%s.%s' % (str(trade.pk).zfill(5), form.cleaned_data['image'].name.lower()[-3:])
                handle_uploaded_file(os.path.join(settings.MEDIA_ROOT, filename), request.FILES['image'])
                # reduce_image_size(temppath, os.path.join(settings.MEDIA_ROOT, filename))
                trade.image.name = filename
                trade.save()
            if pk is None:
                messages.success(request, '<h3 style="margin:0;">New Trade created successfully!</h3>')
            else:
                messages.success(request, '<h3 style="margin:0;">Trade updated successfully!</h3>')
            return redirect(reverse('trades:edit', args=[trade.pk]))
        else:
            messages.error(request, '<h3 style="margin:0;">Your form contains errors!</h3>')
    else:
        initial = {}
        if trade.pk:
            initial = {
                'symbol': trade.symbol,
                'timeframe': trade.timeframe,
                'market_cycle': trade.market_cycle,
                'acctype': trade.acctype,
                'optype': trade.optype,
                'duration': trade.duration,
                'strategy': trade.strategy,
                'open_error': trade.open_error,
                'conduction_error': trade.conduction_error,
                'close_error': trade.close_error,
                'status': trade.status,
                'result': trade.result,
                'notes': trade.notes,
            }
            if trade.close_date:
                initial['close_date'] = trade.close_date.astimezone().strftime('%d/%m/%Y %H:%M')
        form = TradeForm(initial=initial)

    context = {
        'form': form,
        'trade': trade,
    }

    return render(request, 'edit.html', context)
