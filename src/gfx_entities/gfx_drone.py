from src.data_entities.zone import Zone
import pygame as pg


class GfxDrone:
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

    def set_target(self, target_zone: Zone):
        self.target_x = target_zone.zone_x
        self.target_y = target_zone.zone_y

    def update_speed(self):
        dx = self.target_x - self.current_x
        dy = self.target_y - self.current_y
        self.drone_speed_x = dx / self.drone_acceleration
        self.drone_speed_y = dy / self.drone_acceleration

    def update_cord(self):
        self.current_x += self.drone_speed_x
        self.current_y += self.drone_speed_y
        if abs(self.target_x - self.current_x) < abs(self.drone_speed_x):
            self.current_x = self.target_x
            self.drone_speed_x = 0
        if abs(self.target_y - self.current_y) < abs(self.drone_speed_y):
            self.current_y = self.target_y
            self.drone_speed_y = 0

    def draw(self, screen, camera):
        position = camera.world_to_screen(self.current_x, self.current_y)
        drone_rect = self.drone_img.get_rect(center=position)
        screen.blit(self.drone_img, drone_rect)
