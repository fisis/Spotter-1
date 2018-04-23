import numpy as np
from pykalman import KalmanFilter
import math

Observation_CoeffVal=20

class KFilter:
    """
        Kalman filter for smoothing and predicting the missing coordinates. if there was a coordinate recorded, it uses that for the update
         if there wasn't, it uses the last predicted value
    """
    def __init__(self, initpoint=None):
        self.measured_state = []
        self.updated_state = []

    def start_filter(self, initpoint=None):
        deltaT = 0.5
        # Fk: transition matrix
        self.Fk = np.array([[1, 0, deltaT, 0], [0, 1, 0, deltaT], [0, 0, 1, 0], [0, 0, 0, 1]])
        # Hk:observation matrix
        self.Hk = np.eye(4, 4)  # not going to change
        # Pk: transition covariance
        self.Pk = np.eye(4, 4)
        self.Pk2 = np.eye(4, 4)
        # Rk: observation covariance
        self.Rk = np.eye(4, 4) * Observation_CoeffVal
        # self.measurement_covariance = np.eye(4, 4)
        # self.R = 5  # estimate of measurement variance, change to see effect
        # Q
        # self.Q = 0.1  # process variance
        if initpoint is not None:
            self.initial_state = [initpoint[0], initpoint[1], 1, 1]
        else:
            self.initial_state = [1, 1, 1, 1]
        self.filter = KalmanFilter(transition_matrices=self.Fk,
                                   observation_matrices=self.Hk,
                                   transition_covariance=self.Pk,
                                   observation_covariance=self.Rk,
                                   random_state=0)
        self.measured_state = self.initial_state
       # self.updated_state.append(self.initial_state)

    def update_filter(self):
        #self.Rk = np.eye(4, 4) * Observation_CoeffVal
        #self.Fk = np.array( [[1, 0, dt, 0],[0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])
        online_means, self.Pk = self.filter.filter_update(self.updated_state[-1], self.Pk, self.measured_state)
        self.updated_state.append(online_means)
        return (math.ceil(online_means[0]), math.ceil(online_means[1]))

    def update_missing(self):
        self.measured_state=self.updated_state[-1]
        return self.measured_state
    #    self.update_filter()

    def update_measurement(self, x, y, dt):
        if len(self.updated_state)==0:
            self.updated_state.append([x,y,1,1])
            self.measured_state = [x, y, 1, 1]

        else:
            if dt > 0:
                vx = (x - self.updated_state[-1][0]) / dt
                vy = (y - self.updated_state[-1][1]) / dt
            else:
                vx = 1
                vy = 1
            self.measured_state=[x, y, vx, vy]
        return self.measured_state
    #    self.update_filter()

    def stop_filter(self):
        self.measured_state=None
        self.updated_state=[]
        self.filter=None