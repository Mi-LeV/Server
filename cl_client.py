import pygame
import variables as var

class PE:
    def __init__(self,name,coo):
        self.name = name
        self.image_name = "img_sprite_plane_red_player.png"
        self.image = pygame.image.load(self.image_name).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect[0] = coo[0]
        self.rect[1] = coo[1]

    def move(self,coo):
        self.rect[0] = coo[0]
        self.rect[1] = coo[1]

    def delete(self):
        if self in var.objectList:
            var.objectList.remove(self)
        if self in var.blitList:
            var.blitList.remove(self)
        del self

