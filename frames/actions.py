from typing import List
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
        
class ElonAction(ActionABC):
    code = "em"
    name = "Elon"
    
    def processor(self, image):
        background_path = "elon.jpg"
        corners = [
            (403, 59),
            (554, 72),
            (541, 208),
            (402, 174),
        ]
        return DistortImageProcessor(image, background_path, corners)


class ShashlikManAction(ActionABC):
    code = "sm"
    name = "Shashlik Man"
    
    def processor(self, image):
        background_path = "16400267487971.jpg"
        corners = [
            (550, 433),
            (864, 404),
            (877, 644),
            (555, 622),
        ]
        return DistortImageProcessor(image, background_path, corners)
    
    
actions: List[ActionABC] = [WhiteFrameAction(), ShashlikManAction(), ElonAction()]


def get_action(action_code):
    for a in actions:
        if a.code == action_code:
            return a
    return None 
    