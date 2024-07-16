from typing import List, Tuple
from frames.expand_canvas import ExpandCanvasParamsFactory
from frames.image_processing import ExpandCanvasParamsType
from frames.processors import (
    DistortImageProcessor, 
    LandscapeImageProcessor,
    PortraitImageProcessor,
    SquareImageProcessor,
)

class ActionABC:    
    code: str
    name: str
    answer_type: str = 'image'
    def processor(self, image):
        pass


class WhiteFrameAction(ActionABC):
    code = "wf"
    name = "White Frame"
    answer_type = 'document'

    def processor(self, image):
        rate = image.height() / image.width()
        params_factory = ExpandCanvasParamsFactory()
        if rate > 1.1:
            params = params_factory.params(image, ExpandCanvasParamsType.CENTER)
            return PortraitImageProcessor(image, params)
        elif rate < 0.9:
            params = params_factory.params(image, ExpandCanvasParamsType.GOLDEN_RATIO)
            return LandscapeImageProcessor(image, params)
        else:
            params = params_factory.params(image, ExpandCanvasParamsType.CENTER)
            return SquareImageProcessor(image, params)


class DistortImageAction(ActionABC):
    background_path: str
    corners: List[Tuple[int, int]]
    def processor(self, image):
        return DistortImageProcessor(image, self.background_path, self.corners)

        
class ElonAction(DistortImageAction):
    code = "em"
    name = "Elon"
    background_path = "backgrounds/elon.jpg"
    corners = [
        (1911, 286),
        (2628, 338),
        (2567, 989),
        (1905, 825),
    ]    


class ShashlikManAction(DistortImageAction):
    code = "sm"
    name = "Shashlik Man"
    background_path = "backgrounds/shashlik.jpg"
    corners = [
        (1175, 524),
        (1851, 456),
        (1877, 979),
        (1189, 927),
    ]    



class MilitaryShashlikAction(DistortImageAction):
    code = "milsm"
    name = "Military Shashlik Man"
    background_path = "backgrounds/military_shashlik.jpg"
    corners = [
        (550, 433),
        (864, 404),
        (877, 644),
        (555, 622),
    ]    

class KlitchkoAction(DistortImageAction):
    code = "kl"
    name = "Klitchko"
    background_path = "backgrounds/klitchko.jpeg"
    corners = [
        (141, 219),
        (365, 223),
        (364, 383),
        (136, 413),
    ]    
    
class CatMusicAction(DistortImageAction):
    code = "cm"
    name = "Cat Music"
    background_path = "backgrounds/catmusic.jpg"
    corners = [
        (1232, 131),
        (1635, 23),
        (1850, 760),
        (1396, 866),
    ]        

class BezuhlaAction(DistortImageAction):
    code = "bz"
    name = "Bezuhla"
    background_path = "backgrounds/bezuhla.jpg"
    corners = [
        (438, 462),
        (603, 381),
        (735, 652),
        (603, 734),
    ]        
    
actions: List[ActionABC] = [
    WhiteFrameAction(), 
    ShashlikManAction(), 
    MilitaryShashlikAction(),
    ElonAction(),
    KlitchkoAction(),
    CatMusicAction(),
    BezuhlaAction(),
]


def get_action(action_code):
    for a in actions:
        if a.code == action_code:
            return a
    return None 
    