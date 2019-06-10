from django.db import models


class Trade(models.Model):

    DEFAULT_ERROR = ''
    DEFAULT_SYMBOL = 'WIN'
    DEFAULT_STRATEGY = ''

    TIMEFRAME_NONE = 0
    TIMEFRAME_M1 = 1
    TIMEFRAME_M2 = 2
    TIMEFRAME_M3 = 3
    TIMEFRAME_M5 = 5
    TIMEFRAME_M15 = 15
    TIMEFRAME_H1 = 60
    TIMEFRAME_D1 = 1440
    TIMEFRAME_W1 = 10080
    TIMEFRAME_CHOICES = (
        (TIMEFRAME_NONE, '----'),
        (TIMEFRAME_M1, 'M1'),
        (TIMEFRAME_M2, 'M2'),
        (TIMEFRAME_M3, 'M3'),
        (TIMEFRAME_M5, 'M5'),
        (TIMEFRAME_M15, 'M15'),
        (TIMEFRAME_H1, 'H1'),
        (TIMEFRAME_D1, 'D1'),
        (TIMEFRAME_W1, 'W1'),
    )

    OP_TYPE_NONE = 0
    OP_TYPE_SCALP = 1
    OP_TYPE_SWING = 2
    OP_TYPE_CHOICES = (
        (OP_TYPE_NONE, '----'),
        (OP_TYPE_SCALP, 'Scalp'),
        (OP_TYPE_SWING, 'Swing'),
    )

    ACC_TYPE_DEMO = 1
    ACC_TYPE_REAL = 2
    ACC_TYPE_CHOICES = (
        (ACC_TYPE_DEMO, 'Demo'),
        (ACC_TYPE_REAL, 'Real'),
    )

    DURATION_DAYTRADE = 1
    DURATION_SWINGTRADE = 2
    DURATION_POSITIONTRADE = 3
    DURATION_CHOICES = (
        (DURATION_DAYTRADE, 'Day Trade'),
        (DURATION_SWINGTRADE, 'Swing Trade'),
        (DURATION_POSITIONTRADE, 'Position Trade'),
    )

    MARKET_CYCLE_NONE = 0
    MARKET_CYCLE_BO = 1
    MARKET_CYCLE_TC = 2
    MARKET_CYCLE_TC = 3
    MARKET_CYCLE_TR = 4
    MARKET_CYCLE_TTR = 5
    MARKET_CYCLE_CHOICES = (
        (MARKET_CYCLE_BO, 'BO - Breakout'),
        (MARKET_CYCLE_TC, 'TC - Tight Channel'),
        (MARKET_CYCLE_TC, 'BC - Broad Channel'),
        (MARKET_CYCLE_TR, 'TR - Trading Range'),
        (MARKET_CYCLE_TTR, 'TTR - Tight Trading Range'),
    )

    STATUS_OPEN = 1
    STATUS_CLOSED = 2
    STATUS_CHOICES = (
        (STATUS_OPEN, 'Open'),
        (STATUS_CLOSED, 'Closed'),
    )

    RESULT_NONE = 0
    RESULT_GAIN = 1
    RESULT_LOSS = 2
    RESULT_BREAK_EVEN = 3
    RESULT_CHOICES = (
        (RESULT_NONE, '--'),
        (RESULT_GAIN, 'GAIN'),
        (RESULT_LOSS, 'LOSS'),
        (RESULT_BREAK_EVEN, 'BREAK EVEN'),
    )

    symbol = models.CharField(max_length=50, default=DEFAULT_SYMBOL)

    timeframe = models.SmallIntegerField(choices=TIMEFRAME_CHOICES, default=TIMEFRAME_M5)
    market_cycle = models.SmallIntegerField(choices=MARKET_CYCLE_CHOICES, default=MARKET_CYCLE_NONE)

    optype = models.SmallIntegerField(choices=OP_TYPE_CHOICES, default=OP_TYPE_NONE)
    acctype = models.SmallIntegerField(choices=ACC_TYPE_CHOICES, default=ACC_TYPE_REAL)
    duration = models.SmallIntegerField(choices=DURATION_CHOICES, default=DURATION_DAYTRADE)
    strategy = models.CharField(max_length=50, blank=True, default=DEFAULT_STRATEGY)

    is_open_correct = models.BooleanField(default=True)
    is_close_correct = models.BooleanField(default=True)
    is_conduction_correct = models.BooleanField(default=True)

    open_error = models.CharField(max_length=50, blank=True, default=DEFAULT_ERROR)
    close_error = models.CharField(max_length=50, blank=True, default=DEFAULT_ERROR)
    conduction_error = models.CharField(max_length=50, blank=True, default=DEFAULT_ERROR)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_OPEN)
    result = models.SmallIntegerField(choices=RESULT_CHOICES, default=RESULT_NONE)
    profit = models.FloatField(default=0)

    notes = models.TextField(blank=True, default='')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, default='')
    close_date = models.DateTimeField(blank=True, null=True, default=None)

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-close_date', '-id', )

    def __str__(self):
        if self.close_date:
            return '%s %s/%s - %s' % (self.symbol, self.get_optype_display(), self.get_duration_display(),
                                      self.close_date.strftime('%Hh%M'))
        return '%s %s/%s - (Op. Aberta)' % (self.symbol, self.get_optype_display(), self.get_duration_display())
