import abc


class MetadataElement(abc.ABC):
    @property
    @abc.abstractmethod
    def properties(self) -> dict:
        pass
