class Mine:
    def __init__(self, x, y, known, power, new, location, stable):
        self.array_x = x
        self.array_y = y
        self.status = True
        self.small_img = None
        self.large_img = None

        # Attributes for decision tree
        self.known = known     # 0 - 'no', 1 - 'yes'
        self.power = power     # 0 - 'no', 1 - 'yes'
        self.new = new       # 0 - 'no', 1 - 'yes'
        self.location = location  # 0 - 'standard', 1 - 'sand', 2 - 'water', 3 - 'swamp'
        self.stable = stable    # 0 - 'no', 1 - 'yes'
        self.chain_reaction = 0    # 0 - 'no', 1 - 'yes'
