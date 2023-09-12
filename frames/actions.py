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
    def processor(self, image):
        pass


class WhiteFrameAction(ActionABC):
    code = "wf"
    name = "White Frame"

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
        (403, 59),
        (554, 72),
        (541, 208),
        (402, 174),
    ]    


class ShashlikManAction(DistortImageAction):
    code = "sm"
    name = "Shashlik Man"
    background_path = "backgrounds/shashlik.jpg"
    corners = [
        (550, 433),
        (864, 404),
        (877, 644),
        (555, 622),
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
    
actions: List[ActionABC] = [
    WhiteFrameAction(), 
    ShashlikManAction(), 
    MilitaryShashlikAction(),
    ElonAction(),
    KlitchkoAction()
    
]


def get_action(action_code):
    for a in actions:
        if a.code == action_code:
            return a
    return None 
    