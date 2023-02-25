from abc import ABC, abstractmethod
from enum import Enum



fotovramke_default_height = 2075
fotovramke_default_width = 3130
fotovramke_result_width = 3246
FV_BORDER_THICKNESS_MULTIPLIER = fotovramke_result_width / fotovramke_default_width


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

    @abstractmethod
    def distort(self) -> 'ImageABC':
        pass

class NotAnImageException(BaseException):
    pass


class ImageProcessorABC(ABC):
    @abstractmethod
    def modified_image(self, border_thickness_multiplier: float = FV_BORDER_THICKNESS_MULTIPLIER) -> ImageABC:
        pass


class ExpandCanvasParamsType(Enum):
    CENTER = 'center'
    GOLDEN_RATIO = 'golden_ratio'


class ExpandCanvasParamsFactoryABC(ABC):
    @abstractmethod
    def params(self, image: ImageABC, param_type: ExpandCanvasParamsType) -> ExpandCanvasParams:
        pass
