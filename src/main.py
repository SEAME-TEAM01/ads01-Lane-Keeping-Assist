import os
import shutil
import pygame
import carla
from carla_class.HUD import HUD
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.keras as keras
from focal_loss import BinaryFocalLoss
from carla_class.World import World
from predict import predict_steering_angle
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from loss import dice_coef, dice_loss
load_dotenv('.env')

build = tf.sysconfig.get_build_info()
build['cuda_version'] = '11.3'
build['cudnn_version'] = '8.6'

HOST = 'localhost'
PORT = 2000

class Control(object):
    def __init__(self, world) -> None:
        self._control = carla.VehicleControl()
        self._world = world
        self.model = keras.models.load_model(os.getenv('MODEL_PATH'), custom_objects={'dice_coef': dice_coef, 'BinaryFocalLoss': BinaryFocalLoss})

    def control(self, steering, throttle):
        self._control.steer = steering
        self._control.throttle = throttle
        self._control.brake = 0.0

        self._world.player.apply_control(self._control)

    def predict(self,image):
        steer_angle = predict_steering_angle(image=image, model=self.model)
        normalized_angle = steer_angle - 90

        normalized_angle = normalized_angle / 90
        self.control(steering=normalized_angle, throttle=0.3)

def main():
  pygame.init()
  pygame.font.init()
  world = None

  try:
    print(1)
    client = carla.Client(HOST, PORT)
    client.set_timeout(2.0)
    settings = client.get_world().get_settings()
    settings.fixed_delta_seconds = 0.05  # (1/20 = 0.05sec)

    print(2)
    
    display = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
    hud = HUD(800, 600)
    world = World(client.get_world(), hud, "vehicle.ford.mustang")
    controler = Control(world)
    print(3)
    clock = pygame.time.Clock()
    while True:
        clock.tick_busy_loop(60)
        world.tick(clock)
        world.render(display)
        if world.img_queue.empty() == False:
            with tf.device('/GPU:0'):
                image = world.img_queue.get()
                controler.predict(image)
        pygame.display.flip()

  finally:
    if world is not None:
        world.destroy()
    pygame.quit()
    shutil.rmtree('_out')
    
    
if __name__ == '__main__':
    main()
