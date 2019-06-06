from django import forms

from .models import Trade


# class TradeForm(forms.ModelForm):
#     class Meta:
#         model = Trade
#         fields = '__all__'


class TradeForm(forms.Form):

    symbol = forms.CharField(label='Ativo', max_length=50, initial=Trade.DEFAULT_SYMBOL,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    timeframe = forms.TypedChoiceField(label='Timeframe', choices=Trade.TIMEFRAME_CHOICES, initial=Trade.TIMEFRAME_M5,
                                       coerce=int, widget=forms.Select(attrs={'class': 'form-control'}))
    market_cycle = forms.TypedChoiceField(label='Ciclo', choices=Trade.MARKET_CYCLE_CHOICES,
                                          initial=Trade.MARKET_CYCLE_TR, coerce=int,
                                          widget=forms.Select(attrs={'class': 'form-control'}))

    acctype = forms.TypedChoiceField(label='Conta', choices=Trade.ACC_TYPE_CHOICES, initial=Trade.ACC_TYPE_REAL,
                                     coerce=int, widget=forms.Select(attrs={'class': 'form-control'}))
    optype = forms.TypedChoiceField(label='Operação', choices=Trade.OP_TYPE_CHOICES, initial=Trade.OP_TYPE_SWING,
                                    coerce=int, widget=forms.Select(attrs={'class': 'form-control'}))
    duration = forms.TypedChoiceField(label='Duração', choices=Trade.DURATION_CHOICES,
                                      initial=Trade.DURATION_DAYTRADE, coerce=int,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    strategy = forms.CharField(label='Estratégia', max_length=50, initial=Trade.DEFAULT_STRATEGY,
                               widget=forms.Select(attrs={'class': 'form-control'}))

    open_error = forms.CharField(label='Erro na abertura', max_length=50, initial=Trade.DEFAULT_ERROR,
                                 required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    conduction_error = forms.CharField(label='Erro na condução', max_length=50, initial=Trade.DEFAULT_ERROR,
                                       required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    close_error = forms.CharField(label='Erro no fechamento', max_length=50, initial=Trade.DEFAULT_ERROR,
                                  required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    status = forms.TypedChoiceField(label='Status', choices=Trade.STATUS_CHOICES, initial=Trade.STATUS_OPEN,
                                    coerce=int, widget=forms.Select(attrs={'class': 'form-control'}))
    result = forms.TypedChoiceField(label='Resultado', choices=Trade.RESULT_CHOICES, initial=Trade.RESULT_NONE,
                                    coerce=int, widget=forms.Select(attrs={'class': 'form-control'}))
    close_date = forms.DateTimeField(label='Fechamento', required=False, input_formats=['%d/%m/%Y %H:%M'],
                                     widget=forms.DateTimeInput(format='%d/%m/%Y %H:%M',
                                     attrs={'class': 'form-control'}))

    image = forms.ImageField(label='Imagem', required=False)
    notes = forms.CharField(label='Descrição da operação', max_length=5000, required=False,
                            widget=forms.Textarea(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(TradeForm, self).__init__(*args, **kwargs)

        strategy_list = list(Trade.objects.values_list('strategy', flat=True).order_by('strategy').distinct())
        open_error_list = list(Trade.objects.values_list('open_error', flat=True).order_by('open_error').distinct())
        conduction_error_list = list(Trade.objects.values_list('conduction_error', flat=True).order_by(
                                                               'conduction_error').distinct())
        close_error_list = list(Trade.objects.values_list('close_error', flat=True).order_by('close_error').distinct())

        self.fields['strategy'].widget.choices = [('', '')] + [(s, s) for s in strategy_list if s]
        self.fields['open_error'].widget.choices = [('', '')] + [(s, s) for s in open_error_list if s]
        self.fields['conduction_error'].widget.choices = [('', '')] + [(s, s) for s in conduction_error_list if s]
        self.fields['close_error'].widget.choices = [('', '')] + [(s, s) for s in close_error_list if s]

    def save(self, trade):
        trade.symbol = self.cleaned_data['symbol']
        trade.timeframe = self.cleaned_data['timeframe']
        trade.market_cycle = self.cleaned_data['market_cycle']
        trade.acctype = self.cleaned_data['acctype']
        trade.optype = self.cleaned_data['optype']
        trade.duration = self.cleaned_data['duration']
        trade.strategy = self.cleaned_data['strategy']
        trade.open_error = self.cleaned_data['open_error']
        trade.conduction_error = self.cleaned_data['conduction_error']
        trade.close_error = self.cleaned_data['close_error']
        trade.status = self.cleaned_data['status']
        trade.result = self.cleaned_data['result']
        trade.notes = self.cleaned_data['notes']
        trade.close_date = self.cleaned_data['close_date']
        trade.save()
        return trade
