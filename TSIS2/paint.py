import sys
import datetime
import pygame

from tools import (
    PencilTool, LineTool, RectangleTool, CircleTool,
    SquareTool, RightTriangleTool, EqTriangleTool,
    RhombusTool, EraserTool, FillTool, TextTool,
)

WIN_W, WIN_H = 1200, 780
TOOLBAR_W = 200
CANVAS_X = TOOLBAR_W
CANVAS_W = WIN_W - TOOLBAR_W
CANVAS_H = WIN_H

PALETTE = [
    (0, 0, 0), (32, 32, 32), (64, 64, 64), (128, 128, 128),
    (192, 192, 192), (255, 255, 255),
    (139, 0, 0), (200, 0, 0), (255, 0, 0), (255, 69, 0),
    (255, 140, 0), (255, 200, 0),
    (255, 255, 0), (173, 255, 47), (0, 200, 0), (0, 128, 0),
    (0, 100, 0), (0, 255, 128),
    (0, 255, 255), (0, 191, 255), (30, 144, 255), (0, 0, 255),
    (0, 0, 139), (75, 0, 130),
    (138, 43, 226), (255, 0, 255), (255, 20, 147), (255, 105, 180),
    (139, 69, 19), (205, 133, 63),
]

BRUSH_SIZES = {"S": 2, "M": 5, "L": 10}

TOOL_DEFS = [
    ("Pencil",    PencilTool,        pygame.K_p),
    ("Line",      LineTool,          pygame.K_l),
    ("Rectangle", RectangleTool,     pygame.K_r),
    ("Circle",    CircleTool,        pygame.K_c),
    ("Square",    SquareTool,        pygame.K_q),
    ("RTriangle", RightTriangleTool, pygame.K_t),
    ("EqTri",     EqTriangleTool,    pygame.K_e),
    ("Rhombus",   RhombusTool,       pygame.K_h),
    ("Eraser",    EraserTool,        pygame.K_x),
    ("Fill",      FillTool,          pygame.K_f),
    ("Text",      TextTool,          pygame.K_w),
]

BG_COLOR     = (22, 22, 30)
TOOLBAR_BG   = (30, 30, 42)
PANEL_BORDER = (60, 60, 80)
BTN_NORMAL   = (45, 45, 62)
BTN_HOVER    = (65, 65, 90)
BTN_ACTIVE   = (80, 130, 220)
BTN_TEXT     = (220, 220, 240)
HEADER_COLOR = (140, 160, 255)
CANVAS_BG    = (255, 255, 255)


def draw_rounded_rect(surf, color, rect, radius=8, border=0, border_color=None):
    r = pygame.Rect(rect)
    pygame.draw.rect(surf, color, r, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, r, border, border_radius=radius)


def draw_text(surf, text, font, color, rect, align="center"):
    ts = font.render(text, True, color)
    tr = ts.get_rect()
    if align == "center":
        tr.center = pygame.Rect(rect).center
    elif align == "left":
        tr.midleft = (pygame.Rect(rect).left + 8, pygame.Rect(rect).centery)
    surf.blit(ts, tr)


class Button:
    def __init__(self, rect, label, font, key=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.font = font
        self.key = key
        self.hovered = False
        self.active = False

    def draw(self, surf):
        if self.active:
            col = BTN_ACTIVE
        elif self.hovered:
            col = BTN_HOVER
        else:
            col = BTN_NORMAL
        draw_rounded_rect(surf, col, self.rect, radius=6,
                          border=1, border_color=PANEL_BORDER)
        draw_text(surf, self.label, self.font, BTN_TEXT, self.rect)


class PaintApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("Paint Studio")

        self.font_sm  = pygame.font.SysFont("segoeui,arial", 13)
        self.font_med = pygame.font.SysFont("segoeui,arial", 15, bold=True)
        self.font_hdr = pygame.font.SysFont("segoeui,arial", 16, bold=True)

        self.canvas = pygame.Surface((CANVAS_W, CANVAS_H))
        self.canvas.fill(CANVAS_BG)

        self.preview = pygame.Surface((CANVAS_W, CANVAS_H), pygame.SRCALPHA)

        self.color = (0, 0, 0)
        self.brush_size = BRUSH_SIZES["M"]
        self.active_tool_idx = 0

        self.tool_instances = {label: cls() for label, cls, _ in TOOL_DEFS}
        self._tool_labels = [label for label, _, _ in TOOL_DEFS]

        self._build_buttons()

        self.clock = pygame.time.Clock()
        self.running = True

    def _build_buttons(self):
        bw = TOOLBAR_W - 20
        bh = 34
        x0 = 10
        y = 50

        self.tool_buttons = []
        for i, (label, _, key) in enumerate(TOOL_DEFS):
            btn = Button((x0, y, bw, bh), label, self.font_sm, key=key)
            btn.active = (i == self.active_tool_idx)
            self.tool_buttons.append(btn)
            y += bh + 4

        y += 12

        sw = (bw - 8) // 3
        self.size_buttons = {}
        sx = x0
        for label in ("S", "M", "L"):
            btn = Button((sx, y, sw, bh), label, self.font_med)
            btn.active = (BRUSH_SIZES[label] == self.brush_size)
            self.size_buttons[label] = btn
            sx += sw + 4

        y += bh + 16

        self.palette_rects = []
        self.palette_top = y
        swatch = 22
        gap = 3
        cols = 6
        for i in range(len(PALETTE)):
            col_i = i % cols
            row_i = i // cols
            rx = x0 + col_i * (swatch + gap)
            ry = y + row_i * (swatch + gap)
            self.palette_rects.append(pygame.Rect(rx, ry, swatch, swatch))

    @property
    def current_tool(self):
        return self.tool_instances[self._tool_labels[self.active_tool_idx]]

    def _select_tool(self, idx):
        self.active_tool_idx = idx
        for i, btn in enumerate(self.tool_buttons):
            btn.active = (i == idx)

    def _select_size(self, label):
        self.brush_size = BRUSH_SIZES[label]
        for lbl, btn in self.size_buttons.items():
            btn.active = (lbl == label)

    def _canvas_pos(self, screen_pos):
        return (screen_pos[0] - CANVAS_X, screen_pos[1])

    def _on_canvas(self, screen_pos):
        return screen_pos[0] >= CANVAS_X

    def _save(self):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"canvas_{ts}.png"
        pygame.image.save(self.canvas, filename)
        pygame.display.set_caption(f"Paint Studio — Saved: {filename}")

    def run(self):
        while self.running:
            self._handle_events()
            self._draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        for btn in self.tool_buttons:
            btn.hovered = btn.rect.collidepoint(mouse_pos)
        for btn in self.size_buttons.values():
            btn.hovered = btn.rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    self._save()
                    continue

                tool = self.current_tool
                if isinstance(tool, TextTool) and tool.active:
                    tool.handle_key(event, self.canvas, self.color, self.brush_size)
                    continue

                if event.key == pygame.K_1:
                    self._select_size("S")
                elif event.key == pygame.K_2:
                    self._select_size("M")
                elif event.key == pygame.K_3:
                    self._select_size("L")
                else:
                    for i, (_, _, key) in enumerate(TOOL_DEFS):
                        if key == event.key:
                            self._select_tool(i)
                            break

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                handled = False

                for i, btn in enumerate(self.tool_buttons):
                    if btn.rect.collidepoint(pos):
                        self._select_tool(i)
                        handled = True
                        break

                if not handled:
                    for lbl, btn in self.size_buttons.items():
                        if btn.rect.collidepoint(pos):
                            self._select_size(lbl)
                            handled = True
                            break

                if not handled:
                    for i, r in enumerate(self.palette_rects):
                        if r.collidepoint(pos):
                            self.color = PALETTE[i]
                            handled = True
                            break

                if not handled and self._on_canvas(pos):
                    cp = self._canvas_pos(pos)
                    self.current_tool.on_mouse_down(cp, self.canvas,
                                                    self.color, self.brush_size)

            elif event.type == pygame.MOUSEMOTION:
                if self._on_canvas(event.pos):
                    cp = self._canvas_pos(event.pos)
                    self.current_tool.on_mouse_move(cp, self.canvas,
                                                    self.color, self.brush_size)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self._on_canvas(event.pos):
                    cp = self._canvas_pos(event.pos)
                    self.current_tool.on_mouse_up(cp, self.canvas,
                                                  self.color, self.brush_size)

    def _draw(self):
        self.screen.fill(BG_COLOR)

        draw_rounded_rect(self.screen, TOOLBAR_BG, (0, 0, TOOLBAR_W, WIN_H),
                          radius=0, border=1, border_color=PANEL_BORDER)

        hdr_rect = (0, 0, TOOLBAR_W, 42)
        draw_rounded_rect(self.screen, (40, 40, 60), hdr_rect, radius=0,
                          border=1, border_color=PANEL_BORDER)
        draw_text(self.screen, "Paint Studio", self.font_hdr,
                  HEADER_COLOR, hdr_rect)

        draw_text(self.screen, "TOOLS", self.font_sm, (100, 100, 140),
                  (10, 30, TOOLBAR_W - 20, 18), align="left")
        for btn in self.tool_buttons:
            btn.draw(self.screen)

        size_label_y = list(self.size_buttons.values())[0].rect.top - 20
        draw_text(self.screen, "BRUSH SIZE  (1/2/3)", self.font_sm,
                  (100, 100, 140), (10, size_label_y, TOOLBAR_W - 20, 18),
                  align="left")
        for btn in self.size_buttons.values():
            btn.draw(self.screen)

        pal_label_y = self.palette_top - 20
        draw_text(self.screen, "COLORS", self.font_sm, (100, 100, 140),
                  (10, pal_label_y, TOOLBAR_W - 20, 18), align="left")
        for r, col in zip(self.palette_rects, PALETTE):
            pygame.draw.rect(self.screen, col, r, border_radius=3)
            if col == self.color:
                pygame.draw.rect(self.screen, (255, 255, 255), r, 2,
                                 border_radius=3)

        ind_y = self.palette_rects[-1].bottom + 12
        ind_rect = pygame.Rect(10, ind_y, TOOLBAR_W - 20, 28)
        draw_rounded_rect(self.screen, self.color, ind_rect, radius=6,
                          border=2, border_color=(200, 200, 220))
        lum = 0.299 * self.color[0] + 0.587 * self.color[1] + 0.114 * self.color[2]
        label_col = (0, 0, 0) if lum > 128 else (255, 255, 255)
        draw_text(self.screen, "Active Color", self.font_sm, label_col, ind_rect)

        self.screen.blit(self.canvas, (CANVAS_X, 0))

        self.preview.fill((0, 0, 0, 0))
        self.current_tool.draw_preview(self.preview, self.color, self.brush_size)
        self.screen.blit(self.preview, (CANVAS_X, 0))

        pygame.draw.line(self.screen, PANEL_BORDER,
                         (CANVAS_X, 0), (CANVAS_X, WIN_H), 2)

        status_y = WIN_H - 80
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x >= CANVAS_X:
            status = f"({mouse_x - CANVAS_X}, {mouse_y})"
        else:
            status = ""
        draw_text(self.screen, status, self.font_sm, (80, 80, 110),
                  (0, status_y, TOOLBAR_W, 20), align="center")

        tname = self._tool_labels[self.active_tool_idx]
        bs_label = next(k for k, v in BRUSH_SIZES.items() if v == self.brush_size)
        draw_text(self.screen, f"{tname}  [{bs_label}]", self.font_sm,
                  (120, 140, 200), (0, status_y + 20, TOOLBAR_W, 20),
                  align="center")

        draw_text(self.screen, "Ctrl+S = Save", self.font_sm, (70, 70, 100),
                  (0, WIN_H - 36, TOOLBAR_W, 20), align="center")


if __name__ == "__main__":
    app = PaintApp()
    app.run()