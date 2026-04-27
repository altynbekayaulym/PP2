import pygame
import math
from collections import deque


class Tool:
    def __init__(self):
        self.start_pos = None
        self.active = False

    def on_mouse_down(self, pos, canvas, color, size):
        self.start_pos = pos
        self.active = True

    def on_mouse_move(self, pos, canvas, color, size):
        pass

    def on_mouse_up(self, pos, canvas, color, size):
        self.active = False
        self.start_pos = None

    def draw_preview(self, surface, color, size):
        pass


class PencilTool(Tool):
    def __init__(self):
        super().__init__()
        self.last_pos = None

    def on_mouse_down(self, pos, canvas, color, size):
        super().on_mouse_down(pos, canvas, color, size)
        self.last_pos = pos
        pygame.draw.circle(canvas, color, pos, size // 2)

    def on_mouse_move(self, pos, canvas, color, size):
        if self.active and self.last_pos:
            pygame.draw.line(canvas, color, self.last_pos, pos, size)
            pygame.draw.circle(canvas, color, pos, size // 2)
            self.last_pos = pos

    def on_mouse_up(self, pos, canvas, color, size):
        super().on_mouse_up(pos, canvas, color, size)
        self.last_pos = None


class LineTool(Tool):
    def __init__(self):
        super().__init__()
        self._preview_pos = None

    def on_mouse_move(self, pos, canvas, color, size):
        if self.active:
            self._preview_pos = pos

    def on_mouse_up(self, pos, canvas, color, size):
        if self.active and self.start_pos:
            pygame.draw.line(canvas, color, self.start_pos, pos, size)
        super().on_mouse_up(pos, canvas, color, size)
        self._preview_pos = None

    def draw_preview(self, surface, color, size):
        if self.active and self.start_pos and self._preview_pos:
            pygame.draw.line(surface, color, self.start_pos, self._preview_pos, size)


class RectangleTool(Tool):
    def __init__(self):
        super().__init__()
        self._preview_pos = None

    def on_mouse_move(self, pos, canvas, color, size):
        if self.active:
            self._preview_pos = pos

    def on_mouse_up(self, pos, canvas, color, size):
        if self.active and self.start_pos:
            rect = _make_rect(self.start_pos, pos)
            pygame.draw.rect(canvas, color, rect, size)
        super().on_mouse_up(pos, canvas, color, size)
        self._preview_pos = None

    def draw_preview(self, surface, color, size):
        if self.active and self.start_pos and self._preview_pos:
            rect = _make_rect(self.start_pos, self._preview_pos)
            pygame.draw.rect(surface, color, rect, size)


class SquareTool(Tool):
    def __init__(self):
        super().__init__()
        self._preview_pos = None

    def on_mouse_move(self, pos, canvas, color, size):
        if self.active:
            self._preview_pos = pos

    def on_mouse_up(self, pos, canvas, color, size):
        if self.active and self.start_pos:
            rect = _square_rect(self.start_pos, pos)
            pygame.draw.rect(canvas, color, rect, size)
        super().on_mouse_up(pos, canvas, color, size)
        self._preview_pos = None

    def draw_preview(self, surface, color, size):
        if self.active and self.start_pos and self._preview_pos:
            rect = _square_rect(self.start_pos, self._preview_pos)
            pygame.draw.rect(surface, color, rect, size)


class CircleTool(Tool):
    def __init__(self):
        super().__init__()
        self._preview_pos = None

    def on_mouse_move(self, pos, canvas, color, size):
        if self.active:
            self._preview_pos = pos

    def on_mouse_up(self, pos, canvas, color, size):
        if self.active and self.start_pos:
            rect = _make_rect(self.start_pos, pos)
            if rect.width > 0 and rect.height > 0:
                pygame.draw.ellipse(canvas, color, rect, size)
        super().on_mouse_up(pos, canvas, color, size)
        self._preview_pos = None

    def draw_preview(self, surface, color, size):
        if self.active and self.start_pos and self._preview_pos:
            rect = _make_rect(self.start_pos, self._preview_pos)
            if rect.width > 0 and rect.height > 0:
                pygame.draw.ellipse(surface, color, rect, size)


class RightTriangleTool(Tool):
    def __init__(self):
        super().__init__()
        self._preview_pos = None

    def on_mouse_move(self, pos, canvas, color, size):
        if self.active:
            self._preview_pos = pos

    def on_mouse_up(self, pos, canvas, color, size):
        if self.active and self.start_pos:
            pts = _right_triangle_pts(self.start_pos, pos)
            pygame.draw.polygon(canvas, color, pts, size)
        super().on_mouse_up(pos, canvas, color, size)
        self._preview_pos = None

    def draw_preview(self, surface, color, size):
        if self.active and self.start_pos and self._preview_pos:
            pts = _right_triangle_pts(self.start_pos, self._preview_pos)
            pygame.draw.polygon(surface, color, pts, size)


class EqTriangleTool(Tool):
    def __init__(self):
        super().__init__()
        self._preview_pos = None

    def on_mouse_move(self, pos, canvas, color, size):
        if self.active:
            self._preview_pos = pos

    def on_mouse_up(self, pos, canvas, color, size):
        if self.active and self.start_pos:
            pts = _eq_triangle_pts(self.start_pos, pos)
            pygame.draw.polygon(canvas, color, pts, size)
        super().on_mouse_up(pos, canvas, color, size)
        self._preview_pos = None

    def draw_preview(self, surface, color, size):
        if self.active and self.start_pos and self._preview_pos:
            pts = _eq_triangle_pts(self.start_pos, self._preview_pos)
            pygame.draw.polygon(surface, color, pts, size)


class RhombusTool(Tool):
    def __init__(self):
        super().__init__()
        self._preview_pos = None

    def on_mouse_move(self, pos, canvas, color, size):
        if self.active:
            self._preview_pos = pos

    def on_mouse_up(self, pos, canvas, color, size):
        if self.active and self.start_pos:
            pts = _rhombus_pts(self.start_pos, pos)
            pygame.draw.polygon(canvas, color, pts, size)
        super().on_mouse_up(pos, canvas, color, size)
        self._preview_pos = None

    def draw_preview(self, surface, color, size):
        if self.active and self.start_pos and self._preview_pos:
            pts = _rhombus_pts(self.start_pos, self._preview_pos)
            pygame.draw.polygon(surface, color, pts, size)


class EraserTool(Tool):
    def __init__(self):
        super().__init__()
        self.last_pos = None

    def on_mouse_down(self, pos, canvas, color, size):
        super().on_mouse_down(pos, canvas, color, size)
        self.last_pos = pos
        pygame.draw.circle(canvas, (255, 255, 255), pos, size * 2)

    def on_mouse_move(self, pos, canvas, color, size):
        if self.active and self.last_pos:
            pygame.draw.line(canvas, (255, 255, 255), self.last_pos, pos, size * 4)
            pygame.draw.circle(canvas, (255, 255, 255), pos, size * 2)
            self.last_pos = pos

    def on_mouse_up(self, pos, canvas, color, size):
        super().on_mouse_up(pos, canvas, color, size)
        self.last_pos = None


class FillTool(Tool):
    def on_mouse_down(self, pos, canvas, color, size):
        super().on_mouse_down(pos, canvas, color, size)
        flood_fill(canvas, pos, color)
        self.active = False


def flood_fill(surface, start_pos, fill_color):
    x0, y0 = int(start_pos[0]), int(start_pos[1])
    w, h = surface.get_size()
    if not (0 <= x0 < w and 0 <= y0 < h):
        return

    target_color = surface.get_at((x0, y0))[:3]
    fill_rgb = fill_color[:3] if len(fill_color) >= 3 else fill_color

    if target_color == tuple(fill_rgb):
        return

    visited = set()
    queue = deque()
    queue.append((x0, y0))
    visited.add((x0, y0))

    surface.lock()
    while queue:
        cx, cy = queue.popleft()
        surface.set_at((cx, cy), fill_color)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = cx + dx, cy + dy
            if (nx, ny) not in visited and 0 <= nx < w and 0 <= ny < h:
                if surface.get_at((nx, ny))[:3] == target_color:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    surface.unlock()


class TextTool(Tool):
    def __init__(self):
        super().__init__()
        self.cursor_pos = None
        self.text_buffer = ""
        self.font = None
        self._blink_timer = 0

    def _get_font(self, size):
        font_size = {2: 16, 5: 24, 10: 36}.get(size, 20)
        return pygame.font.SysFont("consolas,monospace", font_size)

    def on_mouse_down(self, pos, canvas, color, size):
        self.cursor_pos = pos
        self.text_buffer = ""
        self.active = True
        self.font = self._get_font(size)
        self._blink_timer = 0

    def handle_key(self, event, canvas, color, size):
        if not self.active:
            return False
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._commit(canvas, color)
            return True
        elif event.key == pygame.K_ESCAPE:
            self._cancel()
            return True
        elif event.key == pygame.K_BACKSPACE:
            self.text_buffer = self.text_buffer[:-1]
            return True
        else:
            char = event.unicode
            if char and char.isprintable():
                self.text_buffer += char
            return True

    def _commit(self, canvas, color):
        if self.text_buffer and self.cursor_pos and self.font:
            surf = self.font.render(self.text_buffer, True, color)
            canvas.blit(surf, self.cursor_pos)
        self._cancel()

    def _cancel(self):
        self.active = False
        self.cursor_pos = None
        self.text_buffer = ""

    def draw_preview(self, surface, color, size):
        if not self.active or not self.cursor_pos or not self.font:
            return
        if self.text_buffer:
            surf = self.font.render(self.text_buffer, True, color)
            surface.blit(surf, self.cursor_pos)
        self._blink_timer += 1
        if self._blink_timer % 40 < 20:
            x = self.cursor_pos[0]
            if self.text_buffer:
                x += self.font.size(self.text_buffer)[0]
            y = self.cursor_pos[1]
            h = self.font.get_height()
            pygame.draw.line(surface, color, (x, y), (x, y + h), 2)


def _make_rect(p1, p2):
    x = min(p1[0], p2[0])
    y = min(p1[1], p2[1])
    w = abs(p2[0] - p1[0])
    h = abs(p2[1] - p1[1])
    return pygame.Rect(x, y, w, h)


def _square_rect(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    side = max(abs(dx), abs(dy))
    x = p1[0] if dx >= 0 else p1[0] - side
    y = p1[1] if dy >= 0 else p1[1] - side
    return pygame.Rect(x, y, side, side)


def _right_triangle_pts(p1, p2):
    return [p1, (p1[0], p2[1]), p2]


def _eq_triangle_pts(p1, p2):
    dx = p2[0] - p1[0]
    base_len = abs(dx)
    height = int(base_len * math.sqrt(3) / 2)
    sign = 1 if (p2[1] - p1[1]) >= 0 else -1
    apex = (p1[0] + dx // 2, p1[1] + sign * height)
    return [p1, p2, apex]


def _rhombus_pts(p1, p2):
    cx = (p1[0] + p2[0]) // 2
    cy = (p1[1] + p2[1]) // 2
    return [
        (cx, p1[1]),
        (p2[0], cy),
        (cx, p2[1]),
        (p1[0], cy),
    ]
