from v5_Spatial_heterogeneity.Base.EdgeObject import EdgeObject


class Drainage(EdgeObject):

    def __init__(self):
        EdgeObject.__init__(self)
        self.weight = 0
