import pygame
import variables as var

class Thing:
    def __init__(self,name,coo):
        self.name = name
        self.image_name = "images/img_sprite_plane_default.png"
        self.orig_image = pygame.image.load(self.image_name).convert_alpha()
        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.rect[0] = coo[0]
        self.rect[1] = coo[1]

    def move(self,coo):
        self.rect[0] = coo[0]
        self.rect[1] = coo[1]
    
    def turn(self,angle):
            """Rotate the image of the sprite around its center."""
            # `rotozoom` usually looks nicer than `rotate`. Pygame's rotation
            # functions return new images and don't modify the originals.
            self.image = pygame.transform.rotozoom(self.orig_image, angle, 1)
            # Create a new rect with the center of the old rect.
            self.rect = self.image.get_rect(center=self.rect.center)

    def delete(self):
        if self in var.objectList:
            var.objectList.remove(self)
        if self in var.blitList:
            var.blitList.remove(self)
        del self

class PE(Thing):
    def __init__(self,name,coo):
        super().__init__(name,coo)
        self.image_name = "images/img_sprite_plane_red_player.png"
        self.orig_image = pygame.image.load(self.image_name).convert_alpha()
        self.image = self.orig_image
        self.rect = self.image.get_rect()

class PF(Thing):
    def __init__(self,name,coo):
        super().__init__(name,coo)
        self.image_name = "images/img_sprite_plane_blue_player.png"
        self.orig_image = pygame.image.load(self.image_name).convert_alpha()
        self.image = self.orig_image
        self.rect = self.image.get_rect()

class IE(Thing):
    def __init__(self,name,coo):
        super().__init__(name,coo)
        self.image_name = "images/img_sprite_plane_red_IA.png"
        self.orig_image = pygame.image.load(self.image_name).convert_alpha()
        self.image = self.orig_image
        self.rect = self.image.get_rect()

class IF(Thing):
    def __init__(self,name,coo):
        super().__init__(name,coo)
        self.image_name = "images/img_sprite_plane_blue_IA.png"
        self.orig_image = pygame.image.load(self.image_name).convert_alpha()
        self.image = self.orig_image
        self.rect = self.image.get_rect()