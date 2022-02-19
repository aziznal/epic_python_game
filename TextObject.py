import pygame

pygame.font.init()
# todo: maybe add function to allow to text to be movable in the future


class TextObject:
    def __init__(self, screen, color=(0, 0, 0), x=0, y=0, size=20, static=True, changing=False, font="consolas",
                 bold=False, italic=False, text=None):
        """
        Init method.
        :param screen: Display to render to
        :param color: black by default
        :param x: 0 by default
        :param y: 0 by default
        :param size: 20 by default
        :param static: for moving or non-moving text
        :param changing: for text that might change later
        :param font: font name
        :param bold: false by default
        :param italic: false by default
        :param text: is None by default.
        """
        self.x, self.y, self.screen, self.color, self.size = x, y, screen, color, size
        self.text = text
        self.static = static    # whether the object is supposed to move or not
        self.changing = changing    # whether the object's text is supposed to update or not

        self.font = pygame.font.SysFont(font, self.size, bold, italic)
        self.font_size = pygame.font.Font.size(self.font, self.text)
        self.rect = pygame.Rect((self.x, self.y), (self.font_size[0], self.font_size[1]))

        # render here if not changing
        if not self.changing:
            self.font_render = self.font.render(self.text, True, self.color)
        # Otherwise, do it in draw_changing_text method
        else:
            self.font_render = self.font.render(self.text, True, self.rect)

    def draw_non_changing(self):
        """
        function for blitting non changing text
        :return: None
        """
        self.screen.blit(self.font_render, self.rect)

    def draw_changing_text(self, changed_text):
        """
        Function to blit changing text
        :param changed_text: Text to change to
        :return: None
        """

        # Only Update when needed
        if self.text != changed_text:
            self.text = changed_text

            self.font_render = self.font.render(self.text, True, self.color)

        self.screen.blit(self.font_render, self.rect)

    def update(self, changed_text=None):
        if self.changing:
            self.draw_changing_text(changed_text)
        elif not self.changing:
            self.draw_non_changing()
