class DBS_Electrode:
    # DBS Electrode
    def __init__(self, x_tip, y_tip, z_tip, tip_r, dz_el1, di_ze1e2, dz_el2):
        self.x_tip = x_tip  # lowest center point of the electrode
        self.y_tip = y_tip  # .
        self.z_tip = z_tip  # .
        self.tip_r = tip_r  # electrode radius
        self.dz_el1 = dz_el1  # electrpde 1 z-len
        self.di_ze1e2 = di_ze1e2  # isolator distance
        self.dz_el2 = dz_el2  # electrode 2 z-len

    def create_mesh(self):
        print("TBD")
        pass