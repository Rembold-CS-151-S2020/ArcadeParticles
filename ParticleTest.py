import arcade
import random
import numpy as np


class ParticleTest(arcade.Window):
    def __init__(self):
        self.w = 600
        self.h = 600
        arcade.Window.__init__(self, self.w, self.h, "Particles!")
        arcade.set_background_color(arcade.color.EERIE_BLACK)

        # Sprite for particle from image (try changing to other item numbers! 17 is hearts!)
        self.text_blue = arcade.load_texture(
            "Sprites/PNG/Items/platformPack_item001.png"
        )
        # Sprite for particle pregenerated
        self.text_red = arcade.make_soft_circle_texture(20, arcade.color.RED)
        self.text_green = arcade.make_soft_square_texture(
            50, arcade.color.GREEN, 200, 150
        )

        # Timer for cosine/sine purposes later
        self.timer = 0

        # Empty list to store our emitters for easy drawing and updating
        self.emitters = []

        # Make the center, moving emitter
        self.fountain = arcade.Emitter(
            center_xy=(self.w / 2, self.h / 2),  # Position
            emit_controller=arcade.EmitInterval(0.01),  # When to make more particles
            particle_factory=lambda emitter: arcade.FadeParticle(  # Type of particle
                filename_or_texture=self.text_blue,  # Particle texture
                change_xy=arcade.rand_in_circle((0, 0), 4.5),  # Particle velocity
                lifetime=1.0,  # Particle lifetime
                scale=0.5,  # Particle scaling
            ),
        )

        self.cursor = arcade.Emitter(
            center_xy=(self.w / 2, self.h / 2),
            emit_controller=arcade.EmitMaintainCount(30),  # Alway keep 30 on screen
            particle_factory=lambda emitter: arcade.LifetimeParticle(  # Stay bright till end
                filename_or_texture=self.text_red,
                change_xy=(random.uniform(-1, 1), random.uniform(-1, 1)),
                lifetime=random.random(),  # die out at random times, or else this looked weird
                scale=1,
            ),
        )

        # Add our current, always-on emitters to the list
        self.emitters.extend([self.fountain, self.cursor])

    def make_boom(self, x, y):
        """
        Function to return a shortlived burst emitter whenever we want. Potentially I
        could have had this appended directly to the emitter list, but instead I return
        the emitter itself and will have to add it to the list after that.

        Inputs:
            x (float): the center x position of the burst
            y (float): the center y position of the burst
        Outputs:
            (emitter object): circular green burst of spinning square particles
        """
        return arcade.Emitter(
            center_xy=(x, y),
            emit_controller=arcade.EmitBurst(100),
            particle_factory=lambda emitter: arcade.FadeParticle(
                filename_or_texture=self.text_green,
                change_xy=arcade.rand_in_circle((0, 0), 10),
                change_angle=10,
                lifetime=3,
                scale=0.5,
            ),
        )

    def on_draw(self):
        arcade.start_render()
        for e in self.emitters:
            e.draw()

    def on_update(self, dt):
        for e in self.emitters:
            e.update()

        # Some emitters are only active for a short period of time and then
        # are emitting no particles. can_reap() tells us if that emitter is
        # inactive. So if it is, we'll clean up after ourselves (we aren't animals)
        for e in self.emitters:
            if e.can_reap():
                self.emitters.remove(e)

        # Click the time forward just so I can use it as a parameter in my trig functions
        self.timer += 1
        self.fountain.center_x = self.w / 2 + 100 * np.cos(0.05 * self.timer)
        self.fountain.center_y = self.h / 2 + 100 * np.sin(0.05 * self.timer)

    def on_mouse_motion(self, x, y, dx, dy):
        # Update the cursor emitter position to wherever my mouse is
        self.cursor.center_x = x
        self.cursor.center_y = y

    def on_mouse_press(self, x, y, button, mod):
        # left click = spectacular green explosion
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.emitters.append(self.make_boom(x, y))


ParticleTest()
arcade.run()
