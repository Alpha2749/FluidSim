class fluid_FLIP:
    def __init__(self, fluid_density, sim_width, sim_height, grid_size_h):
        self.fluid_density = fluid_density
        self.sim_width = sim_width
        self.sim_height = sim_height
        self.grid_size_h = grid_size_h
        self.num_cells_x = sim_width * sim_height