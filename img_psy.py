from psychopy import visual, core, event

win = visual.Window(
    size=[400, 400],
    units="pix",
    fullscr=False
)

img = visual.ImageStim(
    win=win,
    image="arrow.png",
    units="pix"
 )

img.draw()

win.flip()

psychopy.event.waitKeys()
