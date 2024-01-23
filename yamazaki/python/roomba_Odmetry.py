import math

class RoombaOdometry:
    def __init__(self, radius=0, tread=0):
        self.r = radius / 1000.0
        self.t = tread / 1000.0

        self.now_time = 0.0
        self.pre_time = 0.0
        self.dt = 0.0
        self.L_pulse = 0.0
        self.R_pulse = 0.0
        self.L_theta = 0.0
        self.R_theta = 0.0
        self.L_omega = 0.0
        self.R_omega = 0.0
        self.L_V = 0.0
        self.R_V = 0.0
        self.V = 0.0
        self.omega = 0.0
        self.theta = 0.0
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.V_pre = 0.0
        self.omega_pre = 0.0
        self.L_theta_pre = 0.0
        self.R_theta_pre = 0.0
        self.theta_pre = 0.0
        self.x_pos_pre = 0.0
        self.y_pos_pre = 0.0

    def get_odometry(self, get_now, get_L_pulse, get_R_pulse):
        self.now_time = float(get_now) / 1000.0
        print("{:.1f},".format(self.now_time), end='')

        self.dt = self.now_time - self.pre_time
        self.L_pulse, self.R_pulse = float(get_L_pulse), float(get_R_pulse)

        self.L_theta = 2 * math.pi * (self.L_pulse / 508.8)
        self.R_theta = 2 * math.pi * (self.R_pulse / 508.8)

        self.L_omega = (self.L_theta - self.L_theta_pre) / self.dt
        self.R_omega = (self.R_theta - self.R_theta_pre) / self.dt

        self.L_V, self.R_V = self.r * self.L_omega, self.r * self.R_omega

        self.V = 0.5 * (self.L_V + self.R_V)
        self.omega = 1 / self.t * (self.R_V - self.L_V)

        self.theta = self.omega_pre * self.dt + self.theta_pre
        self.x_pos += self.V_pre * math.cos(self.theta_pre) * self.dt
        self.y_pos += self.V_pre * math.sin(self.theta_pre) * self.dt

        print("{:.2f},{:.2f},{:.2f},".format(self.theta, self.x_pos, self.y_pos), end='')

        self.V_pre, self.omega_pre = self.V, self.omega
        self.L_theta_pre, self.R_theta_pre = self.L_theta, self.R_theta
        self.theta_pre, self.x_pos_pre, self.y_pos_pre = self.theta, self.x_pos, self.y_pos
        self.pre_time = self.now_time

    def get_r(self):
        return self.r

    def get_t(self):
        return self.t

    def get_now_time(self):
        return self.now_time

    def get_dt(self):
        return self.dt

    def get_L_pulse(self):
        return self.L_pulse

    def get_R_pulse(self):
        return self.R_pulse

    def get_L_theta(self):
        return self.L_theta

    def get_R_theta(self):
        return self.R_theta

    def get_L_omega(self):
        return self.L_omega

    def get_R_omega(self):
        return self.R_omega

    def get_L_V(self):
        return self.L_V

    def get_R_V(self):
        return self.R_V

    def get_V(self):
        return self.V

    def get_omega(self):
        return self.omega

    def get_x_pos(self):
        return self.x_pos

    def get_y_pos(self):
        return self.y_pos

    def get_theta(self):
        return self.theta
