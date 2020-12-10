from abc import ABC, abstractmethod
from enum import Enum



fotovramke_default_height = 2075
fotovramke_default_width = 3130
fotovramke_result_width = 3246
FV_MULTIPLIER = fotovramke_result_width / fotovramke_default_width


class ExpandCanvasParams(ABC):
    @abstractmethod
    def coord_h(self, new_height) -> int:
        pass

    @abstractmethod
    def coord_w(self, new_width) -> int:
        pass


class ImageABC(ABC):
    @abstractmethod
    def width(self) -> int:
        pass

    @abstractmethod
    def height(self) -> int:
        pass

    @abstractmethod
    def expand_canvas(self, new_height: int, new_width: int, params: ExpandCanvasParams) -> 'ImageABC':
        pass

    @abstractmethod
    def save(self, filename):
        pass


class NotAnImageException(BaseException):
    pass


class ImageProcessorABC(ABC):
    @abstractmethod
    def image_with_frame(self, multiplier: float = FV_MULTIPLIER) -> ImageABC:
        pass


class ExpandCanvasParamsType(Enum):
    CENTER = 'center'
    GOLDEN_RATIO = 'golden_ratio'



class ExpandCanvasParamsFactoryABC(ABC):
    @abstractmethod
    def params(self, image: ImageABC, param_type: ExpandCanvasParamsType) -> ExpandCanvasParams:
        pass
