import asyncio
from asciimatics.effects import Mirage, Snow, Print, Sprite
from asciimatics.renderers import FigletText, StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.paths import Path


TREE = (
r"""
       ${3,1}*
      / \
     /${1}o${2}  \
    /_   _\
     /   \${4}b
    /     \
   /   ${1}o${2}   \
  /__     __\
  ${1}d${2} / ${4}o${2}   \
   /       \
  / ${4}o     ${1}o${2}.\
 /___________\
      ${3}|||
      ${3}|||
""",
r"""
       ${3}*
      / \
     /${1}o${2}  \
    /_   _\
     /   \${4}b
    /     \
   /   ${1}o${2}   \
  /__     __\
  ${1}d${2} / ${4}o${2}   \
   /       \
  / ${4}o     ${1}o${2} \
 /___________\
      ${3}|||
      ${3}|||
"""
)


SNOWMAN = (
r"""
   _==_ _
 _,(",)|_|
  \/. \-|
__( :  )|_ 
""",)
SNOWMAN2 = (
r"""
 _ _==_
|_|(,"),_
 |-/ .\/
_|(  : )__
""",)


SANTA = (
r"""
   *        *        *        __o    *       *
*      *       *        *    /_| _     *         *    *  
   K  *     K      *        O'_)/ \  *    *   *   *
  <')____  <')____    __*   V   \  ) __  *   *       * 
   \ ___ )--\ ___ )--( (    (___|__)/ /*     *   *      * 
 *  |   |    |   |    \ \____| |___/ /  *  openSUSE Rocks!
    |*  |    |   |     \____________/       *      *    *
""",
r"""
   *        *         *       __o   *       *
*      *        *       *    /_| _     *         *    *  
   K  *     K       *       O'_)/ \  *    *   *   *
  <')____  <')____    __*   V   \  ) __  *   *       * 
   \ ___ )--\ ___ )--( (    (___|__)/ /*     *   *      * 
 *  /   |    |   /    \ \____| |___/ /  *  openSUSE Rocks!
    \   |    |   \     \____________/       *      *    *
""",
r"""
   *        *         *       __    *       *
*      *        *       *    /_|o_     *         *    *  
   K  *     K       *       O´_)/ \  *    *   *   *
  <')____  <')____    __*   V   \  ) __  *   *       * 
   \ ___ )--\ ___ )--( (    (___|__)/ /*     *   *      * 
 *  /   /    /   /    \ \____| |___/ /  *  openSUSE Rocks!
    \   \    \   \     \____________/       *      *    *
""",
r"""
   *        *         *       __o   *       *
*      *        *       *    /_| _     *         *    *  
   K  *     K       *       O´_)/ \  *    *   *   *
  <')____  <')____    __*   V   \  ) __  *   *       * 
   \ ___ )--\ ___ )--( (    (___|__)/ /*     *   *      * 
 *  |   /    |   /    \ \____| |___/ /  *  openSUSE Rocks!
    |   \    |   \     \____________/       *      *    *
""",
)


class Santa(Sprite):
    def __init__(self, screen):
        path = Path()
        path.jump_to(screen.width + 100, 10)
        path.move_straight_to(-100, 10, 100)
        path.wait(50)
        super().__init__(screen,
                         renderer_dict={
                            "default": StaticRenderer(images=SANTA),
                         },
                         path=path)

    def update(self, n):
        super().update(n)
        if self._path.is_finished():
            self.reset()


def add_santa(screen, scene):
    santa = Santa(screen)
    scene.add_effect(santa)
    scene.santa = santa


def update_screen(loop, screen, scene):
    ev = screen.get_key()
    if ev in (ord('Q'), ord('q')):
        loop.stop()

    screen.draw_next_frame()

    if screen.has_resized():
        screen = Screen.open()
        scene = setup(screen)

    if not hasattr(scene, "santa"):
        add_santa(screen, scene)

    loop.call_later(0.05, update_screen, loop, screen, scene)


def setup(screen):
    effects = [
        Mirage(
            screen,
            FigletText("MERRY XMAS", font="starwars"),
            screen.height // 2 - 8, Screen.COLOUR_RED,
        ),
        Mirage(
            screen,
            FigletText("From pack team", font="standard"),
            screen.height // 2 + 3, Screen.COLOUR_GREEN,
        ),
        Print(screen, StaticRenderer(images=TREE), y=screen.height - 15, x=15),
        Print(screen, StaticRenderer(images=TREE), y=screen.height - 15, x=screen.width // 2),
        Print(screen, StaticRenderer(images=TREE), y=screen.height - 15, x=screen.width - 40),
        Print(screen, StaticRenderer(images=SNOWMAN2), y=screen.height - 5, x=25),
        Print(screen, StaticRenderer(images=SNOWMAN2), y=screen.height - 5, x=screen.width // 2 - 20),
        Print(screen, StaticRenderer(images=SNOWMAN), y=screen.height - 5, x=screen.width // 2 + 20),
        Print(screen, StaticRenderer(images=SNOWMAN), y=screen.height - 5, x=screen.width - 15),
        Snow(screen),
    ]

    scene = Scene(effects, -1)
    screen.set_scenes([scene])
    return scene


def main():
    screen = Screen.open()
    scene = setup(screen)

    loop = asyncio.new_event_loop()
    loop.call_soon(update_screen, loop, screen, scene)

    # Blocking call interrupted by loop.stop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()

    loop.close()
    screen.close()
