import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class BaseAnomaly:
    def __init__(self, template, *args, **kwargs):
        self.template = pd.Series(template).copy()
        self.anomaly = template.copy()
        self.transformations = args
        if args:
            self.parameters = args
        else:
            self.parameters = kwargs
        self.__dict__.update(**kwargs)
        self.anomaly = self._generate()
    
    def insert(self, timeseries, index=None):
        anomaly = self.anomaly
        if index is not None:
            timeseries = pd.concat([timeseries.iloc[:index], 
                                    pd.Series(anomaly), 
                                    timeseries.iloc[index:]], ignore_index=True)
        # TODO: Accept ratio
        else:
            timeseries = pd.concat([timeseries, pd.Series(anomaly)], ignore_index=True)
        return timeseries
    
    def plot(self):
        n = len(self.template)
        combined = pd.concat([self.template, self.anomaly], ignore_index=True)
        plt.title(self.__str__())
        plt.plot(combined[:n])
        plt.plot(combined[n:], c='r')
        plt.show()
    
    def _generate(self):
        return None
    def __str__(self):
        return self.__class__.__name__+' - ' + str(self.parameters)
    def __repr__(self):
        return self.__str__()


class NoisyAnomaly(BaseAnomaly):
    """
    Create a synthetic anomaly augmented by noise.
    E.g.
        noisy_anomaly = NoisyAnomaly(template, mu=0, sigma=5)
        noisy_anomaly.plot()
        augmented_timeseries = noisy_anomaly.insert(ts, index=None)
    """
    def __init__(self, template, mu=0, sigma=1):
        """
        Args:
            template - template timeseries to augment
            mu - mean, modelling normal distribution of noise
            sigma - sigma, modelling normal distribution of noise
        """
        super().__init__(template, mu=mu, sigma=sigma)
    def _generate(self):
        anomaly = self.template.copy()
        noise = np.random.normal(self.mu, self.sigma, len(anomaly))
        return anomaly + noise


class RangeShiftAnomaly(BaseAnomaly):
    """
    Create a synthetic anomaly augmented by a range shift (max-min).
    E.g.
        rangeshift_anomaly = RangeShiftAnomaly(template, ratio=1/3)
        rangeshift_anomaly.plot()
        augmented_timeseries = rangeshift_anomaly.insert(timeseries, index=None)
    """
    def __init__(self, template, ratio):
        """
        Args:
            template - template timeseries to augment
            ratio - fraction of original range to scale to
        """
        super().__init__(template, ratio=ratio)
    def _generate(self):
        anomaly = self.template.copy()
        return anomaly * self.ratio


class AmplitudeShiftAnomaly(BaseAnomaly):
    """
    Create a synthetic anomaly augmented by an amplitude shift (raw value).

    """
    def __init__(self, template, ratio):
        """
        Args:
            template - template timeseries to augment
            ratio - fraction of original range to translate to
        """
        super().__init__(template, ratio=ratio)        
    def _generate(self):
        _max = self.template.max()
        _min = self.template.min()
        _shift = (_max-_min) * self.ratio
        anomaly = self.template.copy()
        return anomaly + _shift


class PointAnomaly(BaseAnomaly):
    """
    Create a synthetic anomaly augmented by points outside of the boundaries.
    Note:
        Anomalous points generate alternate between upper and lower boundaries.
        i.e. Given template timeseries [11, 12, ..., 20], following points generated:
            [22, 8, 23, 7, 22, 9, ...]
    E.g.
        point_anomaly = PointAnomaly(template, ratio=1/2, mu=0, sigma=10, count=100)
        point_anomaly.plot()
        augmented_timeseries = point_anomaly.insert(timeseries, index=None)
    """
    def __init__(self, template, ratio=1/3, mu=0, sigma=1, count=1):
        """
        Args:
            template - template timeseries to augment
            ratio - fraction of original range as threshold that points must exceed
            mu - mean, modelling normal distribution of noise
            sigma - sigma, modelling normal distribution of noise
            count - no. of point anomalies to generate
        """
        super().__init__(template, ratio=ratio, mu=mu, sigma=sigma, count=count)
    def _generate(self):
        _max = self.template.max()
        _min = self.template.min()
        _mid = (_max-_min) * self.ratio
        _upper = _max + _mid
        _lower = _min - _mid
        point = pd.Series([_upper, _lower])
        anomaly = pd.Series([])
        for i in range(self.count):
            noise = np.random.normal(self.mu, self.sigma, 2)
            point_anomaly = point + noise
            anomaly = anomaly.append(point_anomaly, ignore_index=True)
        return anomaly
    def plot(self):
        n = len(self.template)
        combined = pd.concat([self.template, self.anomaly], ignore_index=True)
        plt.title(self.__str__())
        plt.plot(combined[:n])
        plt.plot(combined[n:], '.', c='r')
        plt.show()


class FrequencyShiftAnomaly(BaseAnomaly):
    """
    Create a synthetic anomaly augmented by frequency shift.
    E.g.
    """
    def __init__(self, template, ratio):
        """
        Args:
            template - template timeseries to augment
            ratio - (0-1), fraction of original length of timeseries to generate
        """
        super().__init__(template, ratio=ratio)
    def _generate(self):
        if 0 < self.ratio <= 1:
            _ratio = int(1/self.ratio)
            frag = self.template.iloc[::_ratio].reset_index(drop=True)
        else:
            # TODO: Accept >1
            raise NotImplementedError("FrequencyShiftAnomaly 'ratio' accepts only values between >0 and <=1.")
        return frag


class CompoundAnomaly(BaseAnomaly):
    """
    Create a compound anomaly of multiple anomaly shifts.
    E.g.
        args = [
            # [Generator, {Arguments}],
            [FrequencyShiftAnomaly, {'ratio': 1/3}],
            [AmplitudeShiftAnomaly, {'ratio': 1/3}],
            [RangeShiftAnomaly, {'ratio': 1/2}],
        ]
        compound_anomaly = CompoundAnomaly(template, *args)
        compound_anomaly.plot()
        compound_anomaly.insert(timeseries, index=None)
    """
    def __init__(self, template, *args):
        super().__init__(template, *args)
    def _generate(self):
        anomaly = self.anomaly.copy()
        for Anomaly, kwargs in self.transformations:
            anomaly = Anomaly(anomaly, **kwargs).anomaly
        return anomaly
    def __str__(self):
        print_string = str([Anomaly.__name__ for Anomaly, _ in self.transformations])
        return self.__class__.__name__ + ' - ' + str(print_string)