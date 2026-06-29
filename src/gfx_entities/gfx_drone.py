from src.data_entities.zone import Zone
import pygame as pg
from src.gfx_entities.camera import Camera


class GfxDrone:
    """
    Represents the graphical visualization and animation of a single drone.

    Handles the loading of the drone sprite, scaling, and the frame-by-frame
    interpolation required to smoothly animate the drone's movement from its
    current position to a new target zone.

    Attributes:
        drone_id (str): The unique identifier matching the logical Drone.
        current_x (float): The current horizontal screen coordinate.
        current_y (float): The current vertical screen coordinate.
        target_x (float): The destination horizontal screen coordinate.
        target_y (float): The destination vertical screen coordinate.
        drone_img (pygame.Surface): The scaled image sprite of the drone.
        drone_acceleration (int): Frame divider to control animation speed.
        drone_speed_x (float): The calculated per-frame movement
            step on the X-axis.
        drone_speed_y (float): The calculated per-frame movement
            step on the Y-axis.
    """
    def __init__(self, drone_id: str, zone: Zone):
        self.drone_id: str = drone_id

        self.current_x: float = zone.zone_x
        self.current_y: float = zone.zone_y
        self.target_x: float = 0.0
        self.target_y: float = 0.0

        original_img = (pg.image.
                        load("src/gfx_entities/assets/drone.png").
                        convert_alpha())
        self.drone_img = pg.transform.smoothscale(original_img, (30, 30))

        # faster <- 60(1sec), 30(0.5sec), 15(0.25sec), -> slower
        self.drone_acceleration: int = 30
        self.drone_speed_y: float = 0.0
        self.drone_speed_x: float = 0.0

    def set_target(self, target_zone: Zone) -> None:
        """
        Sets the new physical destination coordinates for the
            drone to fly towards.
        """
        self.target_x = target_zone.zone_x
        self.target_y = target_zone.zone_y

    def update_speed(self) -> None:
        """
        Calculates the required per-frame speed to reach the target smoothly.
        """
        dx = self.target_x - self.current_x
        dy = self.target_y - self.current_y
        self.drone_speed_x = dx / self.drone_acceleration
        self.drone_speed_y = dy / self.drone_acceleration

    def update_cord(self) -> None:
        """
        Updates the current position of the drone by applying the
            calculated speed.

        Includes snap-to-target logic to prevent jittering or overshooting when
        the drone is very close to its destination.
        """
        self.current_x += self.drone_speed_x
        self.current_y += self.drone_speed_y
        if abs(self.target_x - self.current_x) < abs(self.drone_speed_x):
            self.current_x = self.target_x
            self.drone_speed_x = 0
        if abs(self.target_y - self.current_y) < abs(self.drone_speed_y):
            self.current_y = self.target_y
            self.drone_speed_y = 0

    def draw(self, screen: pg.Surface, camera: Camera) -> None:
        """
        Translates world coordinates to screen space and blits
            the drone sprite.
        """
        position = camera.world_to_screen(self.current_x,
                                          self.current_y)
        drone_rect = self.drone_img.get_rect(center=position)
        screen.blit(self.drone_img, drone_rect)
