import abc


class LSGProperty(abc.ABC):
    @property
    @abc.abstractmethod
    def val(self):
        pass
