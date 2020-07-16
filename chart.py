from random import randrange
from pyecharts import options as opts
from pyecharts.charts import Bar, Gauge


def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
        .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar", subtitle="test"))
    )
    return c


def gauge_base(perce: float) -> Gauge:
    c = (
        Gauge(init_opts=opts.InitOpts(width="600px", height="800px"))
        .add(series_name="业务指标", data_pair=[["完成率", perce]])
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(
                is_show=True, formatter="{a} <br/>{b} : {c}%"),
            title_opts=opts.TitleOpts(title="Gauge", subtitle="test"))
    )
    return c