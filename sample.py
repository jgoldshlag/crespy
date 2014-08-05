from crespy import get_crest_root

root = get_crest_root()

print root

specs = root.industry.specialities.href
specs.load()
#print specs

prices = root.marketPrices.href
prices.load()
#print prices
