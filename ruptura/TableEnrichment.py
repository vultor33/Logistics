# visits
# -- store
#    -- visit date1
#        -- product
#           -- x (characteristics)
#           -- status (present, absent)
#    -- visit date2
#       ...
#    -- info
#       -- allProducts
#          -- all products that appear on that store


class TableEnrichment:
    def __init__(self, version):
        self.__version = version
        self.DATA = 'data'
        self.ALL_PRODUCTS = 'allProducts'
        self.INFO = 'info'
        self.STATUS = 'status'
        self.STATUS_PRESENT = 'present'
        self.STATUS_ABSENT = 'absent'
        self.X_FLAG = 'x'
       
    
    def generate(self, samples):
        visits = self.generateVisits(samples)
        visits = self.addAllProductsInfo(visits)
        visits = self.addStatusInfo(visits)
        return visits
        
    def generateVisits(self, samples):
        visits = {}
        for storeProduct in samples: # esse amostras vem do tabledict antes do encoder
            store, product = storeProduct.split('-')
            if store not in visits:
                visits[store] = {}
            for i, date in enumerate(samples[storeProduct][self.DATA]):
                if date not in visits[store]:
                    visits[store][date] = {}
                visits[store][date][product] = samples[storeProduct][self.X_FLAG][i]
        return visits

    def addAllProductsInfo(self, visits):
        for store in visits:
            allProducts = set([])
            for date in visits[store]:
                for product in visits[store][date]:
                    allProducts.add(product)
            visits[store][self.INFO] = {}
            visits[store][self.INFO][self.ALL_PRODUCTS] = list(allProducts)
        return visits
        
    def addStatusInfo(self, visits):
        for store in visits:
            allProducts = visits[store][self.INFO][self.ALL_PRODUCTS]
            for date in visits[store]:
                if date == self.INFO:
                    continue
                for product in allProducts:
                    if product in visits[store][date]:
                        visits[store][date][product][self.STATUS] = self.STATUS_PRESENT
                    else:
                        visits[store][date][product] = {}
                        visits[store][date][product][self.STATUS] = self.STATUS_ABSENT
        return visits
        