import pygame
transparent = (0, 0, 0, 0)
scalee = 1.0
pressedd = False

#button maker

class Button:
    global scalee
    def __init__(self, image_path, position, scale = 1.0):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rectt = self.image.get_rect(topleft = position)
        orig_width = self.image.get_width()
        orig_height = self.image.get_height()
        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.scale = scale

        self.image = pygame.transform.smoothscale(self.image, (new_width, new_height))
        self.pressed = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if self.rectt.collidepoint(mouse_pos):
            new_width = int(self.original_image.get_width() * (self.scale + 0.12))
            new_height = int(self.original_image.get_height() * (self.scale + 0.12))
            scaled_image = pygame.transform.smoothscale(self.original_image, (new_width, new_height))
            scaled_rect = scaled_image.get_rect(center=self.rectt.center)  # Center the scaled image
            screen.blit(scaled_image, scaled_rect)  # Draw the scaled image
        else:
            screen.blit(self.original_image, self.rectt)

    def is_pressed(self):
        mouse_posi = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        

        if self.rectt.collidepoint(mouse_posi):
            if mouse_pressed and not self.pressed:
                self.pressed = True
                return True
        if not mouse_pressed:
            self.pressed = False

        return False        
