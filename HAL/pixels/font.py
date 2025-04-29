from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont



font = TTFont('HAL/fonts/InterVariable.ttf')

instance = instantiateVariableFont(font, {"wght": 800}, inplace=False)


instance.save("HAL/fonts/font_test.ttf")