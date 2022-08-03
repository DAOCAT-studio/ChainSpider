from glassnode import GNSpider
from nomics import NMSpider


def startGlassnode():
    GNSpider().run_main()


def startNomics():
    N = NMSpider()
    N.get_tickers(N.labels["active"])
    N.get_tickers(N.labels["dead"])
    N.handle_historical()
