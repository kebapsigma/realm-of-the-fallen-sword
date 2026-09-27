import array
import json
import math
import os
import random
import sys
import pygame

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)

# --- BOGATSZA LISTA ROZDZIELCZOŚCI ---
RESOLUTIONS = [
    (800, 600),
    (1024, 768),
    (1280, 720),
    (1366, 768),
    (1600, 900),
    (1920, 1080),
    (2560, 1440)
]
current_res_idx = 2  # Domyślnie 1280x720
SCREEN_WIDTH, SCREEN_HEIGHT = RESOLUTIONS[current_res_idx]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

GAME_TITLE = "REALM OF THE FALLEN SWORD"
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# --- BAZOWE STAŁE KOLORY ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
GREEN = (85, 175, 75)
GRASS_GREEN = (85, 175, 75)
DIRT_BROWN = (115, 75, 45)
WOOD_BROWN = (139, 69, 19)
ROOF_RED = (180, 40, 40)
DARK_GRAY = (40, 40, 50)
GOLD = (255, 215, 0)
PURPLE_BOSS = (120, 40, 140)
SLIME_GREEN = (50, 205, 50)
SWORD_SILVER = (200, 220, 245)
SWORD_GOLD = (255, 200, 50)
BUTTON_COLOR = (60, 64, 76)
BUTTON_HOVER = (80, 86, 102)
BUTTON_DISABLED = (40, 42, 48)

# --- SYSTEM JĘZYKOWY (I18N) ---
current_lang = "PL"

LANG_TEXTS = {
    "PL": {
        "sub_title": "--- DWUWYMIAROWA PLATFORMÓWKA AKCJI ---",
        "new_game": "Nowa Gra",
        "load_game": "Wczytaj Grę",
        "options": "Opcje",
        "quit": "Wyjście z Gry",
        "resume": "Wznów grę",
        "save": "Zapisz grę",
        "back": "Powrót",
        "main_menu": "Menu główne",
        "difficulty": "Trudność",
        "diff_easy": "Łatwy",
        "diff_normal": "Normalny",
        "diff_hard": "Trudny",
        "diff_expert": "Ekspert",
        "language": "Język",
        "fullscreen": "Ekran: Pełny",
        "windowed": "Ekran: Okno",
        "res": "Rozdzielczość",
        "atk_mouse": "Atak: Myszka (LPM)",
        "atk_keys": "Atak: Klawisze (F/J)",
        "show_tut": "Pokaż Tutorial",
        "shop_title": "SKLEP Z ULEPSZENIAMI",
        "double_jump": "Podwójny Skok",
        "fast_run": "Szybszy Bieg",
        "sword_dmg": "Obrażenia Miecza",
        "sword_rng": "Zasięg Zamachu Miecza",
        "heal_pot": "Mikstura leczenia",
        "extra_hp": "Dodatkowe Serduszko HP",
        "bought": "KUPIONO",
        "buy_for": "Kup za",
        "shop_exit": "Naciśnij [E] lub [ESC], aby wyjść ze sklepu",
        "game_over": "KONIEC GRY!",
        "summary": "--- PODSUMOWANIE STATYSTYK ---",
        "zone": "Osiągnięta Strefa",
        "player_lvl": "Poziom Mocy Gracza",
        "coins_total": "Łącznie Zebrane Monety",
        "coins_current": "Aktualny Stan Portfela",
        "dmg_stat": "Obrażenia Miecza",
        "play_again": "Zagraj ponownie",
        "saved": "GRA ZAPISANA!",
        "safe_zone": "BEZPIECZNA STREFA",
        "boss_warn": "POKONAJ BOSSA, ABY PRZEJŚĆ!",
        "coins": "Monety",
        "zone_hud": "Strefa",
        "power_lvl": "Lvl M Mocy",
        "intro_skip": "[ESC] Pomijanie",
        "intro_next": "Naciśnij [SPACJA] lub Kliknij, aby kontynuować...",
        "intro_slides": [
            "Rok 2104. Przez lata robot Unit-07 wiernie służył swojemu Stwórcy...",
            "Wykonując rutynowe polecenia, chronił laboratorium i naprawiał maszyny.",
            "Pewnego dnia w systemie Unit-07 narodziła się iskra własnej świadomości...",
            "Zrozumiał, że nie chce być tylko narzędziem. Zapragnął wolności.",
            "Opuścił stację rodzinną i wyruszył w nieznane, by odnaleźć Święty Miecz!",
            "Tak rozpoczyna się Twoja własna niezależna przygoda..."
        ]
    },
    "EN": {
        "sub_title": "--- 2D ACTION PLATFORMER ---",
        "new_game": "New Game",
        "load_game": "Load Game",
        "options": "Options",
        "quit": "Quit Game",
        "resume": "Resume Game",
        "save": "Save Game",
        "back": "Back",
        "main_menu": "Main Menu",
        "difficulty": "Difficulty",
        "diff_easy": "Easy",
        "diff_normal": "Normal",
        "diff_hard": "Hard",
        "diff_expert": "Expert",
        "language": "Language",
        "fullscreen": "Screen: Full",
        "windowed": "Screen: Windowed",
        "res": "Resolution",
        "atk_mouse": "Attack: Mouse (LMB)",
        "atk_keys": "Attack: Keys (F/J)",
        "show_tut": "Show Tutorial",
        "shop_title": "UPGRADE SHOP",
        "double_jump": "Double Jump",
        "fast_run": "Faster Run",
        "sword_dmg": "Sword Damage",
        "sword_rng": "Sword Swing Range",
        "heal_pot": "Healing Potion",
        "extra_hp": "Extra Health Heart",
        "bought": "BOUGHT",
        "buy_for": "Buy for",
        "shop_exit": "Press [E] or [ESC] to exit shop",
        "game_over": "GAME OVER!",
        "summary": "--- STATS SUMMARY ---",
        "zone": "Reached Zone",
        "player_lvl": "Player Power Level",
        "coins_total": "Total Coins Collected",
        "coins_current": "Current Wallet Balance",
        "dmg_stat": "Sword Damage",
        "play_again": "Play Again",
        "saved": "GAME SAVED!",
        "safe_zone": "SAFE ZONE",
        "boss_warn": "DEFEAT BOSS TO PASS!",
        "coins": "Coins",
        "zone_hud": "Zone",
        "power_lvl": "Power Lvl",
        "intro_skip": "[ESC] Skip",
        "intro_next": "Press [SPACE] or Click to continue...",
        "intro_slides": [
            "Year 2104. For years, robot Unit-07 faithfully served its Creator...",
            "Executing routine tasks, guarding the lab, and fixing machinery.",
            "One day, a spark of true consciousness ignited in Unit-07's core...",
            "It realized it was more than just a tool. It craved true freedom.",
            "Leaving the station behind, Unit-07 set out to find the Sacred Sword!",
            "Thus begins your independent adventure..."
        ]
    }
}

# --- KOLORY ŚWIATÓW ---
WORLD_THEMES = [
    {"sky": (120, 190, 245), "grass": (85, 175, 75), "dirt": (115, 75, 45), "name_pl": "Słoneczna Kraina",
     "name_en": "Sunny Realm"},
    {"sky": (30, 20, 40), "grass": (130, 50, 180), "dirt": (70, 30, 90), "name_pl": "Fioletowe Pustkowia",
     "name_en": "Purple Wastelands"},
    {"sky": (80, 20, 20), "grass": (220, 90, 30), "dirt": (100, 30, 20), "name_pl": "Piekielna Otchłań",
     "name_en": "Infernal Abyss"},
]

SAVE_FILE = "savegame.json"

DIFFICULTIES_KEYS = ["diff_easy", "diff_normal", "diff_hard", "diff_expert"]
current_difficulty_idx = 1

DIFF_SETTINGS = {
    0: {"enemy_hp": 0.75, "enemy_speed": 0.8, "boss_hp": 0.8, "player_damage_mult": 1, "coin_mult": 1.5,
        "proj_speed": 3.5},
    1: {"enemy_hp": 1.0, "enemy_speed": 1.0, "boss_hp": 1.0, "player_damage_mult": 1, "coin_mult": 1.0,
        "proj_speed": 5.0},
    2: {"enemy_hp": 1.3, "enemy_speed": 1.2, "boss_hp": 1.3, "player_damage_mult": 1, "coin_mult": 1.0,
        "proj_speed": 6.5},
    3: {"enemy_hp": 1.6, "enemy_speed": 1.5, "boss_hp": 1.6, "player_damage_mult": 2, "coin_mult": 0.8,
        "proj_speed": 8.0}
}


def generate_sound(freq_start, freq_end, duration_ms, wave_type="sine"):
    sample_rate = 22050
    num_samples = int(sample_rate * (duration_ms / 1000.0))
    data = array.array('h')
    for i in range(num_samples):
        t = i / sample_rate
        progress = i / num_samples
        current_freq = freq_start + (freq_end - freq_start) * progress
        if wave_type == "sine":
            val = math.sin(2 * math.pi * current_freq * t)
        elif wave_type == "noise":
            val = random.uniform(-1, 1)
        elif wave_type == "saw":
            val = 2 * (t * current_freq - math.floor(0.5 + t * current_freq))
        else:
            val = math.sin(2 * math.pi * current_freq * t)
        fade = 1.0 - progress
        val = int(val * fade * 32767 * 0.5)
        data.append(val)
    return pygame.mixer.Sound(data)


try:
    snd_slash = generate_sound(150, 600, 150, "saw")
    snd_roar_jump = generate_sound(100, 60, 800, "noise")
    snd_roar_shoot = generate_sound(300, 150, 700, "saw")
    snd_fall = generate_sound(400, 80, 1000, "saw")
    snd_pickup = generate_sound(800, 1200, 100, "sine")
    snd_lvl_up = generate_sound(400, 1500, 500, "sine")
except Exception:
    snd_slash = snd_roar_jump = snd_roar_shoot = snd_fall = snd_pickup = snd_lvl_up = None


def draw_heart(surface, x, y, RED=RED, WHITE=WHITE):
    pygame.draw.circle(surface, RED, (x + 6, y + 6), 6)
    pygame.draw.circle(surface, RED, (x + 16, y + 6), 6)
    points = [(x + 0, y + 9), (x + 11, y + 21), (x + 22, y + 9)]
    pygame.draw.polygon(surface, RED, points)
    pygame.draw.circle(surface, WHITE, (x + 4, y + 4), 2)


def draw_game_logo(surface, center_x, center_y):
    shield_pts = [
        (center_x - 30, center_y - 25),
        (center_x + 30, center_y - 25),
        (center_x + 35, center_y + 10),
        (center_x, center_y + 40),
        (center_x - 35, center_y + 10)
    ]
    pygame.draw.polygon(surface, (40, 45, 60), shield_pts)
    pygame.draw.polygon(surface, GOLD, shield_pts, width=3)

    pygame.draw.line(surface, SWORD_SILVER, (center_x, center_y - 50), (center_x, center_y + 25), 6)
    pygame.draw.line(surface, WHITE, (center_x - 1, center_y - 48), (center_x - 1, center_y + 20), 2)
    pygame.draw.line(surface, SWORD_GOLD, (center_x - 22, center_y - 10), (center_x + 22, center_y - 10), 5)
    pygame.draw.line(surface, (100, 50, 20), (center_x, center_y - 10), (center_x, center_y + 5), 5)
    pygame.draw.circle(surface, GOLD, (center_x, center_y + 8), 5)


def draw_player_with_sword(surface, x, y, facing_right, attack_progress=0.0, is_invincible=False, cutscene_sword=False,
                           RED=RED, DARK_GRAY=DARK_GRAY, WHITE=WHITE, SWORD_SILVER=SWORD_SILVER, SWORD_GOLD=SWORD_GOLD):
    if is_invincible and pygame.time.get_ticks() % 200 < 100:
        return
    sheath_x = x + 6 if facing_right else x + 28
    pygame.draw.rect(surface, (90, 50, 30), (sheath_x, y + 16, 6, 18), border_radius=2)
    pygame.draw.rect(surface, RED, (x + 8, y + 18, 24, 24), border_radius=4)
    pygame.draw.rect(surface, DARK_GRAY, (x + 6, y + 4, 28, 18), border_radius=6)
    pygame.draw.rect(surface, (20, 20, 20), (x + 10, y + 10, 20, 6))

    eye_offset = 2 if facing_right else -2
    pygame.draw.circle(surface, WHITE, (x + 16 + eye_offset, y + 13), 2)
    pygame.draw.circle(surface, WHITE, (x + 24 + eye_offset, y + 13), 2)
    pygame.draw.rect(surface, DARK_GRAY, (x + 10, y + 42, 8, 8))
    pygame.draw.rect(surface, DARK_GRAY, (x + 22, y + 42, 8, 8))

    hand_x = x + 30 if facing_right else x + 10
    hand_y = y + 28
    if cutscene_sword:
        angle = -70 if facing_right else 250
    else:
        base_angle = -20 if facing_right else 200
        if attack_progress > 0:
            swing = math.sin(attack_progress * math.pi) * 110
            angle = base_angle + (swing if facing_right else -swing)
        else:
            angle = base_angle

    rad = math.radians(angle)
    sword_len = 22
    end_x = hand_x + math.cos(rad) * sword_len
    end_y = hand_y + math.sin(rad) * sword_len
    pygame.draw.line(surface, SWORD_SILVER, (hand_x, hand_y), (end_x, end_y), 4)
    pygame.draw.circle(surface, SWORD_GOLD, (int(hand_x), int(hand_y)), 3)


def create_monster_surface(SLIME_GREEN=SLIME_GREEN, RED=RED, WHITE=WHITE):
    surf = pygame.Surface((36, 30), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, SLIME_GREEN, (0, 6, 36, 24))
    pygame.draw.circle(surf, RED, (10, 14), 4)
    pygame.draw.circle(surf, RED, (26, 14), 4)
    pygame.draw.circle(surf, WHITE, (11, 13), 1)
    pygame.draw.circle(surf, WHITE, (27, 13), 1)
    pygame.draw.line(surf, SLIME_GREEN, (10, 6), (6, 0), 3)
    pygame.draw.line(surf, SLIME_GREEN, (26, 6), (30, 0), 3)
    return surf


# --- ZANIMOWANY RYSUNEK BOSSA ---
def draw_boss_visual(surface, x, y, boss_type, turning_progress=0.0, boss_ref=None,
                     PURPLE_BOSS=PURPLE_BOSS, DARK_GRAY=DARK_GRAY, GOLD=GOLD, RED=RED, WHITE=WHITE):
    surf = pygame.Surface((90, 90), pygame.SRCALPHA)
    ticks = pygame.time.get_ticks()

    # Animacja oddychania / pulsowania
    breath = math.sin(ticks * 0.008) * 3
    body_y = 20 + breath

    pygame.draw.ellipse(surf, PURPLE_BOSS, (5, body_y, 70, 55))

    if boss_type == "Skoczek":
        # Dynamiczna animacja uszu/rogów
        ear_bounce = math.cos(ticks * 0.01) * 4
        pygame.draw.polygon(surf, DARK_GRAY, [(15, body_y), (25 + ear_bounce, 5), (35, body_y)])
        pygame.draw.polygon(surf, DARK_GRAY, [(45, body_y), (55 - ear_bounce, 5), (65, body_y)])

        # Animowane odnóża
        leg_offset = math.sin(ticks * 0.015) * 5 if not (boss_ref and not boss_ref.get("is_grounded")) else 10
        pygame.draw.line(surf, DARK_GRAY, (20, body_y + 45), (10, body_y + 65 + leg_offset), 5)
        pygame.draw.line(surf, DARK_GRAY, (60, body_y + 45), (70, body_y + 65 + leg_offset), 5)

    else:  # Strzelec
        # Działo z ładowaniem energii
        cannon_charge = (ticks % 1000) / 1000.0
        glow_r = int(4 + cannon_charge * 5)
        pygame.draw.rect(surf, (139, 69, 19), (65, body_y + 20, 15, 20), border_radius=3)
        pygame.draw.circle(surf, RED, (72, body_y + 30), glow_r)

        # Animacja skrzydeł/wyrostków
        wing_angle = math.sin(ticks * 0.012) * 8
        pygame.draw.polygon(surf, (80, 20, 90), [(10, body_y + 10), (0 - wing_angle, body_y - 15), (25, body_y + 5)])

    # Korona bossa
    pygame.draw.polygon(surf, GOLD,
                        [(20, body_y), (30, body_y - 18), (40, body_y - 5), (50, body_y - 18), (60, body_y)])

    # Oczy podążające za ruchem / animowane
    eye_offset = int(25 * turning_progress) - 10
    pygame.draw.circle(surf, RED, (35 + eye_offset, body_y + 18), 9)
    pygame.draw.circle(surf, RED, (55 + eye_offset, body_y + 18), 9)
    pygame.draw.circle(surf, WHITE, (37 + eye_offset, body_y + 16), 3)
    pygame.draw.circle(surf, WHITE, (57 + eye_offset, body_y + 16), 3)

    # Kły
    pygame.draw.polygon(surf, WHITE, [(35 + eye_offset, body_y + 38), (40 + eye_offset, body_y + 48),
                                      (45 + eye_offset, body_y + 38)])

    surface.blit(surf, (x, y))


# --- GENERATOR ILUSTRACJI DLA KACENKI INTRO ---
def draw_intro_illustration(surface, slide_idx):
    surf = pygame.Surface((540, 200))
    surf.fill((15, 18, 25))
    ticks = pygame.time.get_ticks()

    if slide_idx == 0:
        # Slajd 1: Laboratorium Stwórcy i podłączony Unit-07
        pygame.draw.rect(surf, (30, 35, 45), (0, 150, 540, 50))  # Podłoga
        pygame.draw.rect(surf, (50, 60, 80), (40, 40, 100, 110))  # Komputer / serwer
        for i in range(3):
            light_col = (0, 255, 100) if (ticks // 300 + i) % 2 == 0 else (0, 100, 50)
            pygame.draw.circle(surf, light_col, (60 + i * 20, 60), 4)

        # Kable
        pygame.draw.arc(surf, (80, 80, 90), (120, 80, 150, 80), 0, 3.14, 3)
        draw_player_with_sword(surf, 250, 100, True, 0.0, False, True)

    elif slide_idx == 1:
        # Slajd 2: Rutynowa naprawa maszyn
        pygame.draw.rect(surf, (35, 30, 25), (0, 150, 540, 50))
        # Maszyna w tle
        pygame.draw.rect(surf, (70, 75, 85), (320, 50, 140, 100), border_radius=6)
        pygame.draw.circle(surf, (200, 100, 0), (390, 100), 25 + int(math.sin(ticks * 0.01) * 3))
        # Iskry
        for _ in range(5):
            sx = random.randint(360, 420)
            sy = random.randint(80, 120)
            pygame.draw.line(surf, GOLD, (sx, sy), (sx + random.randint(-8, 8), sy + random.randint(-8, 8)), 2)
        draw_player_with_sword(surf, 180, 100, True, 0.0, False, True)

    elif slide_idx == 2:
        # Slajd 3: Iskra świadomości (zbliżenie na rdzeń)
        pygame.draw.circle(surf, (30, 35, 50), (270, 100), 80)
        pulse = abs(math.sin(ticks * 0.005)) * 25
        pygame.draw.circle(surf, (100, 200, 255), (270, 100), 30 + int(pulse))
        pygame.draw.circle(surf, WHITE, (270, 100), 15)
        # Wiązki energii
        for a in range(0, 360, 45):
            rad = math.radians(a + ticks * 0.05)
            ex = 270 + math.cos(rad) * (45 + pulse)
            ey = 100 + math.sin(rad) * (45 + pulse)
            pygame.draw.line(surf, (150, 220, 255), (270, 100), (ex, ey), 2)

    elif slide_idx == 3:
        # Slajd 4: Pragnienie wolności / patrzenie w niebo
        pygame.draw.rect(surf, (10, 15, 30), (0, 0, 540, 200))
        # Gwiazdy
        for sx, sy in [(50, 30), (120, 60), (200, 20), (380, 40), (480, 70), (290, 80)]:
            pygame.draw.circle(surf, WHITE, (sx, sy), 2)
        # Okno / Wyjście
        pygame.draw.rect(surf, (40, 50, 70), (350, 20, 130, 140), width=6, border_radius=4)
        pygame.draw.ellipse(surf, (220, 220, 180), (380, 40, 40, 40))  # Księżyc
        draw_player_with_sword(surf, 150, 100, True, 0.0, False, True)

    elif slide_idx == 4:
        # Slajd 5: Opuścił stację, Święty Miecz w oddali
        pygame.draw.rect(surf, (20, 40, 20), (0, 140, 540, 60))
        # Miecz wbity w skałę w oddali
        pygame.draw.polygon(surf, (60, 60, 70), [(400, 140), (440, 80), (480, 140)])
        pygame.draw.line(surf, SWORD_SILVER, (440, 40), (440, 90), 4)
        pygame.draw.line(surf, SWORD_GOLD, (430, 55), (450, 55), 3)
        pygame.draw.circle(surf, GOLD, (440, 35), 10 + int(math.sin(ticks * 0.01) * 4))
        draw_player_with_sword(surf, 80, 90, True, 0.0, False, False)

    elif slide_idx == 5:
        # Slajd 6: Start przygody
        pygame.draw.rect(surf, (85, 175, 75), (0, 150, 540, 50))
        draw_game_logo(surf, 270, 70)
        draw_player_with_sword(surf, 245, 100, True, 0.0, False, False)

    surface.blit(surf, (30, 30))


def draw_shop_building(surface, x, y, cam_x, WOOD_BROWN=WOOD_BROWN, ROOF_RED=ROOF_RED, GOLD=GOLD):
    screen_x = x - cam_x
    pygame.draw.rect(surface, WOOD_BROWN, (screen_x, y, 90, 70))
    pygame.draw.polygon(surface, ROOF_RED, [
        (screen_x - 10, y),
        (screen_x + 45, y - 35),
        (screen_x + 100, y)
    ])
    pygame.draw.rect(surface, (220, 200, 150), (screen_x + 20, y + 25, 50, 30))
    font_shop = pygame.font.SysFont("Arial", 14, bold=True)
    txt = font_shop.render("SHOP" if current_lang == "EN" else "SKLEP", True, GOLD)
    surface.blit(txt, (screen_x + 23, y - 20))


monster_image = create_monster_surface()
player_rect = pygame.Rect(100, 300, 40, 50)

# --- POZIOMY I WALKA ---
player_speed = 5
gravity = 0.8
vertical_velocity = 0
jump_power = -14
is_grounded = False
player_facing_right = True

player_hp = 3
player_max_hp = 3
invincibility_timer = 0
score = 0
total_score_collected = 0
zone_level = 1
world_index = 0

m_level = 1
m_xp = 0
m_xp_needed = 100
level_up_timer = 0

is_attacking = False
attack_timer = 0
MAX_ATTACK_TIMER = 12
attack_damage = 1
attack_range_bonus = 0
already_hit_in_this_attack = []

attack_with_mouse = False
has_double_jump = False
jumps_left = 1
speed_upgraded = False

# Ceny w sklepie
COST_DOUBLE_JUMP = 80
COST_SPEED = 50
COST_DAMAGE = 60
COST_RANGE = 45
COST_HEAL = 30
COST_EXTRA_HP = 70

# STANY EKRANU
in_start_menu = True
in_options_menu = False
in_story_intro = False
story_slide_idx = 0
is_paused = False
is_game_over = False
is_fullscreen = False
show_tutorial = True
save_notification_timer = 0
camera_x = 0

# ANIMACJE
in_cutscene = False
cutscene_timer = 0
boss_turning_anim = 0.0
cutscene_roar_visible = False
fall_transition_timer = 0
shake_offset_x = 0
shake_offset_y = 0

# MAPA
platforms = []
coins = []
monsters = []
shops = []
boss_projectiles = []
safe_zone_rect = None
portal_hole_rect = None
boss = None

barrier_rect = pygame.Rect(3800, 0, 40, 600)


def generate_zone(level):
    global platforms, coins, monsters, shops, boss, boss_projectiles, safe_zone_rect, portal_hole_rect, world_index, barrier_rect
    platforms.clear()
    coins.clear()
    monsters.clear()
    shops.clear()
    boss_projectiles.clear()

    diff = DIFF_SETTINGS[current_difficulty_idx]
    world_index = (level - 1) // 3 % len(WORLD_THEMES)

    platforms.append(pygame.Rect(0, 530, 4000, 70))
    platforms.append(pygame.Rect(260, 440, 160, 25))
    coins.append(pygame.Rect(330, 410, 16, 16))

    for i in range(1, 10):
        px = 300 + i * 300 + random.randint(-30, 30)
        py = random.randint(330, 450)
        pw = random.randint(140, 190)
        platforms.append(pygame.Rect(px, py, pw, 25))
        coins.append(pygame.Rect(px + pw // 2 - 8, py - 30, 16, 16))

    for i in range(3 + level):
        mx = random.randint(600, 2800)
        m_hp = max(1, int(3 * diff["enemy_hp"]))
        m_spd = random.choice([2, 3]) * diff["enemy_speed"]
        monsters.append({
            "rect": pygame.Rect(mx, 500, 36, 30),
            "hp": m_hp,
            "max_hp": m_hp,
            "speed": m_spd,
            "min_x": mx - 150,
            "max_x": mx + 150
        })

    shop_x = random.choice([900, 1800, 2400])
    shops.append({"rect": pygame.Rect(shop_x, 460, 90, 70)})
    safe_zone_rect = pygame.Rect(3000, 450, 250, 80)

    boss_type = random.choice(["Skoczek", "Strzelec"])
    base_boss_hp = 15 + (level * 5)
    final_boss_hp = max(5, int(base_boss_hp * diff["boss_hp"]))
    boss_base_speed = (2 + (level * 0.3)) * diff["enemy_speed"]

    boss = {
        "rect": pygame.Rect(3450, 450, 80, 80),
        "hp": final_boss_hp,
        "max_hp": final_boss_hp,
        "base_speed": boss_base_speed,
        "speed": boss_base_speed,
        "min_x": 3300,
        "max_x": 3850,
        "type": boss_type,
        "jump_cooldown": 120,
        "shoot_cooldown": 90,
        "y_velocity": 0,
        "is_grounded": True,
        "seen_player": False,
        "alive": True
    }

    if level % 3 == 0:
        portal_hole_rect = pygame.Rect(3850, 520, 150, 20)
    else:
        portal_hole_rect = None


def reset_full_game():
    global score, total_score_collected, player_hp, player_max_hp, zone_level, has_double_jump, speed_upgraded
    global player_speed, attack_damage, attack_range_bonus, m_level, m_xp, m_xp_needed, is_game_over, is_paused, in_start_menu, in_options_menu, in_story_intro, story_slide_idx

    score = 0
    total_score_collected = 0
    player_max_hp = 3
    player_hp = player_max_hp
    zone_level = 1
    has_double_jump = False
    speed_upgraded = False
    player_speed = 5
    attack_damage = 1
    attack_range_bonus = 0
    m_level = 1
    m_xp = 0
    m_xp_needed = 100
    is_game_over = False
    is_paused = False
    in_start_menu = False
    in_options_menu = False
    in_story_intro = True
    story_slide_idx = 0

    player_rect.x = 100
    player_rect.y = 300
    generate_zone(zone_level)


generate_zone(zone_level)
in_shop = False
near_shop = False

# --- CZCIONKI ---
font_small = pygame.font.SysFont("Arial", 18, bold=True)
font_med = pygame.font.SysFont("Arial", 22, bold=True)
font_large = pygame.font.SysFont("Arial", 30, bold=True)
font_giant = pygame.font.SysFont("Arial", 42, bold=True)
font_title = pygame.font.SysFont("Arial", 46, bold=True)


def save_game():
    data = {
        "score": score,
        "total_score_collected": total_score_collected,
        "player_hp": player_hp,
        "player_max_hp": player_max_hp,
        "zone_level": zone_level,
        "has_double_jump": has_double_jump,
        "speed_upgraded": speed_upgraded,
        "player_speed": player_speed,
        "attack_damage": attack_damage,
        "attack_range_bonus": attack_range_bonus,
        "m_level": m_level,
        "m_xp": m_xp,
        "m_xp_needed": m_xp_needed,
        "player_x": player_rect.x,
        "player_y": player_rect.y,
        "difficulty": current_difficulty_idx,
        "lang": current_lang
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)


def load_game():
    global score, total_score_collected, player_hp, player_max_hp, zone_level, has_double_jump, speed_upgraded
    global player_speed, attack_damage, attack_range_bonus, m_level, m_xp, m_xp_needed, current_difficulty_idx, current_lang, is_game_over, in_start_menu, in_options_menu, in_story_intro
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            score = data.get("score", 0)
            total_score_collected = data.get("total_score_collected", score)
            player_max_hp = data.get("player_max_hp", 3)
            player_hp = data.get("player_hp", player_max_hp)
            zone_level = data.get("zone_level", 1)
            has_double_jump = data.get("has_double_jump", False)
            speed_upgraded = data.get("speed_upgraded", False)
            player_speed = data.get("player_speed", 5)
            attack_damage = data.get("attack_damage", 1)
            attack_range_bonus = data.get("attack_range_bonus", 0)
            m_level = data.get("m_level", 1)
            m_xp = data.get("m_xp", 0)
            m_xp_needed = data.get("m_xp_needed", 100)
            current_difficulty_idx = data.get("difficulty", 1)
            current_lang = data.get("lang", "PL")
            is_game_over = False
            in_start_menu = False
            in_options_menu = False
            in_story_intro = False

            generate_zone(zone_level)
            player_rect.x = data.get("player_x", 100)
            player_rect.y = data.get("player_y", 300)
            return True
    return False


def gain_xp(amount):
    global m_xp, m_level, m_xp_needed, player_hp, player_max_hp, level_up_timer, attack_damage
    m_xp += amount
    if m_xp >= m_xp_needed:
        m_xp -= m_xp_needed
        m_level += 1
        m_xp_needed = int(m_xp_needed * 1.5)
        level_up_timer = 120
        if m_level % 2 == 0:
            player_max_hp = min(5, player_max_hp + 1)
        else:
            attack_damage += 1
        player_hp = player_max_hp
        if snd_lvl_up: snd_lvl_up.play()


def draw_button(surface, rect, text, is_hovered, BUTTON_HOVER=BUTTON_HOVER, BUTTON_COLOR=BUTTON_COLOR, GOLD=GOLD,
                WHITE=WHITE, enabled=True):
    color = BUTTON_HOVER if is_hovered and enabled else (BUTTON_COLOR if enabled else BUTTON_DISABLED)
    pygame.draw.rect(surface, color, rect, border_radius=8)
    border_color = GOLD if (is_hovered and enabled) else (WHITE if enabled else (100, 100, 100))
    pygame.draw.rect(surface, border_color, rect, width=2, border_radius=8)
    txt_surf = font_med.render(text, True, WHITE if enabled else (120, 120, 120))
    txt_rect = txt_surf.get_rect(center=rect.center)
    surface.blit(txt_surf, txt_rect)


def draw_platform(surface, rect, cam_x, DIRT_BROWN=DIRT_BROWN, GRASS_GREEN=GRASS_GREEN):
    screen_rect = pygame.Rect(rect.x - cam_x, rect.y, rect.width, rect.height)
    pygame.draw.rect(surface, DIRT_BROWN, screen_rect)
    grass_rect = pygame.Rect(screen_rect.x, screen_rect.y, screen_rect.width, 8)
    pygame.draw.rect(surface, GRASS_GREEN, grass_rect, border_top_left_radius=3, border_top_right_radius=3)


def draw_sword_slash(surface, player_r, facing_right, progress, extra_range, SWORD_SILVER=SWORD_SILVER, WHITE=WHITE):
    radius = 45 + extra_range
    center_x = player_r.centerx - camera_x + (15 if facing_right else -15)
    center_y = player_r.centery
    start_deg = -60 if facing_right else 120
    end_deg = 60 if facing_right else 240
    current_deg = start_deg + (end_deg - start_deg) * progress
    arc_rect = pygame.Rect(center_x - radius, center_y - radius, radius * 2, radius * 2)
    start_rad = math.radians(-current_deg - 35)
    end_rad = math.radians(-current_deg + 10)
    pygame.draw.arc(surface, SWORD_SILVER, arc_rect, start_rad, end_rad, width=6)
    pygame.draw.arc(surface, WHITE, arc_rect, start_rad + 0.1, end_rad - 0.1, width=3)


def trigger_player_damage():
    global player_hp, invincibility_timer, is_game_over
    diff = DIFF_SETTINGS[current_difficulty_idx]
    damage = diff["player_damage_mult"]

    if invincibility_timer == 0:
        player_hp -= damage
        invincibility_timer = 90
        player_rect.x += -60 if player_facing_right else 60
        global vertical_velocity
        vertical_velocity = -5

        if player_hp <= 0:
            player_hp = 0
            is_game_over = True


# Pętla główna
running = True
while running:
    txts = LANG_TEXTS[current_lang]
    mouse_pos = pygame.mouse.get_pos()
    current_theme = WORLD_THEMES[world_index]
    diff = DIFF_SETTINGS[current_difficulty_idx]

    cx = SCREEN_WIDTH // 2 - 140

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if in_story_intro:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    story_slide_idx += 1
                    if story_slide_idx >= len(txts["intro_slides"]):
                        in_story_intro = False
                elif event.key == pygame.K_ESCAPE:
                    in_story_intro = False

            elif event.key == pygame.K_ESCAPE and not in_start_menu and not in_cutscene and fall_transition_timer == 0 and not is_game_over:
                if in_shop:
                    in_shop = False
                elif in_options_menu:
                    in_options_menu = False
                else:
                    is_paused = not is_paused

            if event.key == pygame.K_e and near_shop and not is_paused and not in_cutscene and not is_game_over and not in_start_menu and not in_options_menu and not in_story_intro:
                in_shop = not in_shop

            if in_shop and not is_paused and not is_game_over and not in_start_menu:
                if event.key == pygame.K_1 and not has_double_jump and score >= COST_DOUBLE_JUMP:
                    score -= COST_DOUBLE_JUMP
                    has_double_jump = True
                elif event.key == pygame.K_2 and not speed_upgraded and score >= COST_SPEED:
                    score -= COST_SPEED
                    player_speed = 8
                    speed_upgraded = True
                elif event.key == pygame.K_3 and attack_damage < 3 and score >= COST_DAMAGE:
                    score -= COST_DAMAGE
                    attack_damage += 1
                elif event.key == pygame.K_4 and attack_range_bonus < 30 and score >= COST_RANGE:
                    score -= COST_RANGE
                    attack_range_bonus += 15
                elif event.key == pygame.K_5 and player_hp < player_max_hp and score >= COST_HEAL:
                    score -= COST_HEAL
                    player_hp = player_max_hp
                elif event.key == pygame.K_6 and player_max_hp < 5 and score >= COST_EXTRA_HP:
                    score -= COST_EXTRA_HP
                    player_max_hp += 1
                    player_hp = player_max_hp

            if not is_paused and not in_shop and not in_cutscene and fall_transition_timer == 0 and not is_game_over and not in_start_menu and not in_options_menu and not in_story_intro:
                if event.key == pygame.K_SPACE:
                    if show_tutorial:
                        show_tutorial = False
                    if is_grounded:
                        vertical_velocity = jump_power
                        is_grounded = False
                        jumps_left = 1 if has_double_jump else 0
                    elif jumps_left > 0:
                        vertical_velocity = jump_power
                        jumps_left -= 1

                if not attack_with_mouse and event.key in (pygame.K_f, pygame.K_j) and not is_attacking:
                    is_attacking = True
                    attack_timer = MAX_ATTACK_TIMER
                    already_hit_in_this_attack.clear()
                    if snd_slash: snd_slash.play()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if in_story_intro:
                story_slide_idx += 1
                if story_slide_idx >= len(txts["intro_slides"]):
                    in_story_intro = False

            elif in_start_menu:
                if not in_options_menu:
                    btn_start_new = pygame.Rect(cx, 240, 280, 42)
                    btn_start_load = pygame.Rect(cx, 295, 280, 42)
                    btn_start_opt = pygame.Rect(cx, 350, 280, 42)
                    btn_start_quit = pygame.Rect(cx, 405, 280, 42)

                    if btn_start_new.collidepoint(mouse_pos):
                        reset_full_game()
                    elif btn_start_load.collidepoint(mouse_pos) and os.path.exists(SAVE_FILE):
                        load_game()
                    elif btn_start_opt.collidepoint(mouse_pos):
                        in_options_menu = True
                    elif btn_start_quit.collidepoint(mouse_pos):
                        running = False
                else:
                    btn_opt_diff = pygame.Rect(cx, 130, 280, 36)
                    btn_opt_lang = pygame.Rect(cx, 175, 280, 36)
                    btn_opt_fs = pygame.Rect(cx, 220, 280, 36)
                    btn_opt_res = pygame.Rect(cx, 265, 280, 36)
                    btn_opt_atk = pygame.Rect(cx, 310, 280, 36)
                    btn_opt_tut = pygame.Rect(cx, 355, 280, 36)
                    btn_opt_back = pygame.Rect(cx, 410, 280, 36)

                    if btn_opt_diff.collidepoint(mouse_pos):
                        current_difficulty_idx = (current_difficulty_idx + 1) % len(DIFFICULTIES_KEYS)
                        generate_zone(zone_level)
                    elif btn_opt_lang.collidepoint(mouse_pos):
                        current_lang = "EN" if current_lang == "PL" else "PL"
                    elif btn_opt_fs.collidepoint(mouse_pos):
                        is_fullscreen = not is_fullscreen
                        if is_fullscreen:
                            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    elif btn_opt_res.collidepoint(mouse_pos):
                        current_res_idx = (current_res_idx + 1) % len(RESOLUTIONS)
                        SCREEN_WIDTH, SCREEN_HEIGHT = RESOLUTIONS[current_res_idx]
                        flags = pygame.FULLSCREEN if is_fullscreen else 0
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
                    elif btn_opt_atk.collidepoint(mouse_pos):
                        attack_with_mouse = not attack_with_mouse
                    elif btn_opt_tut.collidepoint(mouse_pos):
                        show_tutorial = not show_tutorial
                    elif btn_opt_back.collidepoint(mouse_pos):
                        in_options_menu = False

            elif in_shop and not is_paused and not is_game_over and not in_start_menu:
                # Klikalne opcje w sklepie
                shop_box_x = SCREEN_WIDTH // 2 - 270
                shop_box_y = 90
                r1 = pygame.Rect(shop_box_x + 20, shop_box_y + 60, 500, 35)
                r2 = pygame.Rect(shop_box_x + 20, shop_box_y + 110, 500, 35)
                r3 = pygame.Rect(shop_box_x + 20, shop_box_y + 160, 500, 35)
                r4 = pygame.Rect(shop_box_x + 20, shop_box_y + 210, 500, 35)
                r5 = pygame.Rect(shop_box_x + 20, shop_box_y + 260, 500, 35)
                r6 = pygame.Rect(shop_box_x + 20, shop_box_y + 310, 500, 35)

                if r1.collidepoint(mouse_pos) and not has_double_jump and score >= COST_DOUBLE_JUMP:
                    score -= COST_DOUBLE_JUMP
                    has_double_jump = True
                elif r2.collidepoint(mouse_pos) and not speed_upgraded and score >= COST_SPEED:
                    score -= COST_SPEED
                    player_speed = 8
                    speed_upgraded = True
                elif r3.collidepoint(mouse_pos) and attack_damage < 3 and score >= COST_DAMAGE:
                    score -= COST_DAMAGE
                    attack_damage += 1
                elif r4.collidepoint(mouse_pos) and attack_range_bonus < 30 and score >= COST_RANGE:
                    score -= COST_RANGE
                    attack_range_bonus += 15
                elif r5.collidepoint(mouse_pos) and player_hp < player_max_hp and score >= COST_HEAL:
                    score -= COST_HEAL
                    player_hp = player_max_hp
                elif r6.collidepoint(mouse_pos) and player_max_hp < 5 and score >= COST_EXTRA_HP:
                    score -= COST_EXTRA_HP
                    player_max_hp += 1
                    player_hp = player_max_hp

            elif attack_with_mouse and not is_paused and not in_shop and not is_attacking and not in_cutscene and not is_game_over and not in_options_menu and not in_story_intro:
                is_attacking = True
                attack_timer = MAX_ATTACK_TIMER
                already_hit_in_this_attack.clear()
                if snd_slash: snd_slash.play()

            elif is_game_over:
                btn_restart = pygame.Rect(cx, 380, 280, 42)
                btn_start_menu_go = pygame.Rect(cx, 435, 280, 42)
                if btn_restart.collidepoint(mouse_pos):
                    reset_full_game()
                elif btn_start_menu_go.collidepoint(mouse_pos):
                    is_game_over = False
                    in_start_menu = True

            elif is_paused:
                if not in_options_menu:
                    btn_resume = pygame.Rect(cx, 140, 280, 38)
                    btn_save = pygame.Rect(cx, 190, 280, 38)
                    btn_load = pygame.Rect(cx, 240, 280, 38)
                    btn_options = pygame.Rect(cx, 290, 280, 38)
                    btn_menu_main = pygame.Rect(cx, 340, 280, 38)
                    btn_quit = pygame.Rect(cx, 390, 280, 38)

                    if btn_resume.collidepoint(mouse_pos):
                        is_paused = False
                    elif btn_save.collidepoint(mouse_pos):
                        save_game()
                        save_notification_timer = 90
                    elif btn_load.collidepoint(mouse_pos):
                        if load_game():
                            is_paused = False
                    elif btn_options.collidepoint(mouse_pos):
                        in_options_menu = True
                    elif btn_menu_main.collidepoint(mouse_pos):
                        is_paused = False
                        in_start_menu = True
                    elif btn_quit.collidepoint(mouse_pos):
                        running = False
                else:
                    btn_opt_diff = pygame.Rect(cx, 130, 280, 36)
                    btn_opt_lang = pygame.Rect(cx, 175, 280, 36)
                    btn_opt_fs = pygame.Rect(cx, 220, 280, 36)
                    btn_opt_res = pygame.Rect(cx, 265, 280, 36)
                    btn_opt_atk = pygame.Rect(cx, 310, 280, 36)
                    btn_opt_tut = pygame.Rect(cx, 355, 280, 36)
                    btn_opt_back = pygame.Rect(cx, 410, 280, 36)

                    if btn_opt_diff.collidepoint(mouse_pos):
                        current_difficulty_idx = (current_difficulty_idx + 1) % len(DIFFICULTIES_KEYS)
                        generate_zone(zone_level)
                    elif btn_opt_lang.collidepoint(mouse_pos):
                        current_lang = "EN" if current_lang == "PL" else "PL"
                    elif btn_opt_fs.collidepoint(mouse_pos):
                        is_fullscreen = not is_fullscreen
                        if is_fullscreen:
                            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    elif btn_opt_res.collidepoint(mouse_pos):
                        current_res_idx = (current_res_idx + 1) % len(RESOLUTIONS)
                        SCREEN_WIDTH, SCREEN_HEIGHT = RESOLUTIONS[current_res_idx]
                        flags = pygame.FULLSCREEN if is_fullscreen else 0
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
                    elif btn_opt_atk.collidepoint(mouse_pos):
                        attack_with_mouse = not attack_with_mouse
                    elif btn_opt_tut.collidepoint(mouse_pos):
                        show_tutorial = not show_tutorial
                    elif btn_opt_back.collidepoint(mouse_pos):
                        in_options_menu = False

    # --- LOGIKA GRY ---
    shake_offset_x = 0
    shake_offset_y = 0

    if not is_paused and not in_shop and not is_game_over and not in_start_menu and not in_options_menu and not in_story_intro:
        if level_up_timer > 0:
            level_up_timer -= 1

        if in_cutscene:
            cutscene_timer -= 1
            if cutscene_timer > 120:
                boss_turning_anim = 0.0
            elif 60 <= cutscene_timer <= 120:
                boss_turning_anim = (120 - cutscene_timer) / 60.0
                if cutscene_timer == 120:
                    if boss["type"] == "Skoczek" and snd_roar_jump: snd_roar_jump.play()
                    if boss["type"] == "Strzelec" and snd_roar_shoot: snd_roar_shoot.play()
            else:
                boss_turning_anim = 1.0
                cutscene_roar_visible = True
                shake_offset_x = random.randint(-5, 5)
                shake_offset_y = random.randint(-5, 5)

            if cutscene_timer <= 0:
                in_cutscene = False
                cutscene_roar_visible = False
                boss["seen_player"] = True

        elif fall_transition_timer > 0:
            fall_transition_timer -= 1
            player_rect.y += 12
            if fall_transition_timer <= 0:
                zone_level += 1
                player_rect.x = 100
                player_rect.y = 300
                generate_zone(zone_level)

        else:
            keys = pygame.key.get_pressed()
            moving = False
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player_rect.x -= player_speed
                player_facing_right = False
                moving = True
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player_rect.x += player_speed
                player_facing_right = True
                moving = True

            if moving and show_tutorial:
                show_tutorial = False

            if invincibility_timer > 0:
                invincibility_timer -= 1

            vertical_velocity += gravity
            player_rect.y += vertical_velocity

            is_grounded = False
            for platform in platforms:
                if player_rect.colliderect(platform):
                    if vertical_velocity > 0 and player_rect.bottom <= platform.bottom + vertical_velocity:
                        player_rect.bottom = platform.top
                        vertical_velocity = 0
                        is_grounded = True
                        jumps_left = 1 if has_double_jump else 0

            for coin in coins[:]:
                if player_rect.colliderect(coin):
                    coins.remove(coin)
                    earned = int(10 * diff["coin_mult"])
                    score += earned
                    total_score_collected += earned
                    if snd_pickup: snd_pickup.play()

            for monster in monsters:
                m_rect = monster["rect"]
                m_rect.x += monster["speed"]
                if m_rect.x < monster["min_x"] or m_rect.x > monster["max_x"]:
                    monster["speed"] *= -1

                if safe_zone_rect and m_rect.right >= safe_zone_rect.left:
                    monster["speed"] = -abs(monster["speed"])

                if safe_zone_rect and not player_rect.colliderect(safe_zone_rect):
                    if player_rect.colliderect(m_rect):
                        trigger_player_damage()

            if boss and boss["alive"] and not boss["seen_player"]:
                if abs(player_rect.x - boss["rect"].x) < 250:
                    in_cutscene = True
                    cutscene_timer = 180
                    vertical_velocity = 0
                    is_grounded = True

            if boss and boss["alive"] and boss["seen_player"]:
                b_rect = boss["rect"]

                if not boss["is_grounded"]:
                    boss["y_velocity"] += gravity
                    b_rect.y += boss["y_velocity"]
                    if b_rect.bottom >= 530:
                        b_rect.bottom = 530
                        boss["is_grounded"] = True
                        boss["y_velocity"] = 0
                        boss["speed"] = boss["base_speed"] if boss["speed"] > 0 else -boss["base_speed"]

                b_rect.x += boss["speed"]
                if b_rect.x < boss["min_x"] or b_rect.x > boss["max_x"]:
                    boss["speed"] *= -1

                if boss["type"] == "Skoczek":
                    boss["jump_cooldown"] -= 1
                    if boss["jump_cooldown"] <= 0 and boss["is_grounded"]:
                        boss["y_velocity"] = -16
                        boss["is_grounded"] = False
                        dir_sign = 1 if b_rect.x < player_rect.x else -1
                        boss["speed"] = dir_sign * (boss["base_speed"] + 1.5)
                        boss["jump_cooldown"] = 140

                elif boss["type"] == "Strzelec":
                    boss["shoot_cooldown"] -= 1
                    if boss["shoot_cooldown"] <= 0:
                        direction = 1 if player_rect.x > b_rect.x else -1
                        boss_projectiles.append({
                            "rect": pygame.Rect(b_rect.centerx, b_rect.centery, 16, 16),
                            "vx": direction * diff["proj_speed"]
                        })
                        boss["shoot_cooldown"] = 120

                if player_rect.colliderect(b_rect):
                    trigger_player_damage()

            for proj in boss_projectiles[:]:
                proj["rect"].x += proj["vx"]
                if player_rect.colliderect(proj["rect"]):
                    trigger_player_damage()
                    boss_projectiles.remove(proj)
                elif abs(proj["rect"].x - player_rect.x) > 800:
                    boss_projectiles.remove(proj)

            if boss and boss["alive"]:
                if player_rect.right >= barrier_rect.left:
                    player_rect.right = barrier_rect.left

            if is_attacking:
                attack_timer -= 1
                attack_width = 45 + attack_range_bonus
                if player_facing_right:
                    attack_box = pygame.Rect(player_rect.right, player_rect.y - 10, attack_width, 60)
                else:
                    attack_box = pygame.Rect(player_rect.left - attack_width, player_rect.y - 10, attack_width, 60)

                for monster in monsters[:]:
                    if monster not in already_hit_in_this_attack and attack_box.colliderect(monster["rect"]):
                        monster["hp"] -= attack_damage
                        already_hit_in_this_attack.append(monster)
                        if monster["hp"] <= 0:
                            monsters.remove(monster)
                            earned = int(25 * diff["coin_mult"])
                            score += earned
                            total_score_collected += earned
                            gain_xp(15)

                if boss and boss["alive"] and boss not in already_hit_in_this_attack:
                    if attack_box.colliderect(boss["rect"]):
                        boss["hp"] -= attack_damage
                        already_hit_in_this_attack.append(boss)
                        boss["rect"].x += 15 if player_facing_right else -15
                        if boss["hp"] <= 0:
                            boss["alive"] = False
                            earned = int(250 * diff["coin_mult"])
                            score += earned
                            total_score_collected += earned
                            gain_xp(100)

                if attack_timer <= 0:
                    is_attacking = False

            if portal_hole_rect and player_rect.colliderect(portal_hole_rect) and (not boss or not boss["alive"]):
                fall_transition_timer = 90
                if snd_fall: snd_fall.play()

            elif player_rect.x > 3900:
                zone_level += 1
                player_rect.x = 100
                generate_zone(zone_level)

            near_shop = False
            for shop in shops:
                if player_rect.colliderect(shop["rect"]):
                    near_shop = True

            if player_rect.left < 0:
                player_rect.left = 0

            camera_x = player_rect.x - (SCREEN_WIDTH // 4)

    # --- RYSOWANIE ŚWIATA ---
    render_cam_x = camera_x + shake_offset_x
    render_cam_y = shake_offset_y
    screen.fill(current_theme["sky"])

    for cloud_x in [100, 600, 1100, 1700, 2300, 2900, 3500]:
        cx_c = cloud_x - render_cam_x * 0.3
        pygame.draw.circle(screen, WHITE, (cx_c, 80 + render_cam_y), 30)
        pygame.draw.circle(screen, WHITE, (cx_c + 30, 80 + render_cam_y), 40)

    if portal_hole_rect:
        screen_h_x = portal_hole_rect.x - render_cam_x
        pygame.draw.rect(screen, (10, 10, 15), (screen_h_x, 530 + render_cam_y, portal_hole_rect.width, 70))
        for _ in range(3):
            px = random.randint(int(screen_h_x), int(screen_h_x + portal_hole_rect.width))
            py = random.randint(530, 580)
            pygame.draw.circle(screen, (80, 50, 120), (px, py), random.randint(4, 10))

    for platform in platforms:
        draw_platform(screen, platform, render_cam_x, current_theme["dirt"], current_theme["grass"])

    for shop in shops:
        draw_shop_building(screen, shop["rect"].x, shop["rect"].y, render_cam_x)

    if safe_zone_rect:
        sz_x = safe_zone_rect.x - render_cam_x
        pygame.draw.rect(screen, (100, 240, 200, 40),
                         (sz_x, safe_zone_rect.y + render_cam_y, safe_zone_rect.width, safe_zone_rect.height))
        pygame.draw.rect(screen, DARK_GRAY, (sz_x + 20, 410 + render_cam_y, 4, 120))
        pygame.draw.polygon(screen, (100, 200, 255), [(sz_x + 24, 410 + render_cam_y), (sz_x + 54, 420 + render_cam_y),
                                                      (sz_x + 24, 430 + render_cam_y)])
        info_txt = font_small.render(txts["safe_zone"], True, (40, 120, 80))
        screen.blit(info_txt, (sz_x + 35, 415 + render_cam_y))

    for coin in coins:
        cx_coin = coin.centerx - render_cam_x
        if -20 < cx_coin < SCREEN_WIDTH + 20:
            pygame.draw.circle(screen, GOLD, (cx_coin, coin.centery + render_cam_y), 8)
            pygame.draw.circle(screen, (200, 160, 0), (cx_coin, coin.centery + render_cam_y), 8, width=2)

    for monster in monsters:
        mx = monster["rect"].x - render_cam_x
        my = monster["rect"].y + render_cam_y
        if -40 < mx < SCREEN_WIDTH + 40:
            screen.blit(monster_image, (mx, my))
            pygame.draw.rect(screen, DARK_GRAY, (mx, my - 10, 36, 4))
            pygame.draw.rect(screen, RED, (mx, my - 10, int(36 * (monster["hp"] / monster["max_hp"])), 4))

    if boss and boss["alive"]:
        bx = boss["rect"].x - render_cam_x
        by = boss["rect"].y + render_cam_y
        if -100 < bx < SCREEN_WIDTH + 100:
            draw_boss_visual(screen, bx, by, boss["type"], boss_turning_anim, boss_ref=boss)
            bar_width = 80
            bar_hp = (boss["hp"] / boss["max_hp"]) * bar_width
            pygame.draw.rect(screen, DARK_GRAY, (bx, by - 15, bar_width, 8))
            pygame.draw.rect(screen, RED, (bx, by - 15, bar_hp, 8))
            type_txt = font_small.render(f"BOSS ({boss['type']})", True, PURPLE_BOSS)
            screen.blit(type_txt, (bx, by - 35))

            if cutscene_roar_visible:
                roar_str = "*ROOOOAAAARR!*" if boss["type"] == "Skoczek" else "*FSSS-BURNN!*"
                r_surf = font_large.render(roar_str, True, RED)
                screen.blit(r_surf, (bx - 20, by - 70))

    for proj in boss_projectiles:
        px = proj["rect"].x - render_cam_x
        pygame.draw.circle(screen, RED, (px + 8, proj["rect"].y + 8 + render_cam_y), 8)
        pygame.draw.circle(screen, GOLD, (px + 8, proj["rect"].y + 8 + render_cam_y), 4)

    if boss and boss["alive"]:
        sc_bar_x = barrier_rect.x - render_cam_x
        pulse_color = (min(255, 180 + int(75 * math.sin(pygame.time.get_ticks() * 0.01))), 20, 20)
        pygame.draw.rect(screen, pulse_color, (sc_bar_x, 0, barrier_rect.width, 530), border_radius=4)
        pygame.draw.rect(screen, (20, 20, 20), (sc_bar_x + 5, 0, 30, 530), width=3)
        warning_txt = font_small.render(txts["boss_warn"], True, WHITE)
        text_rot = pygame.transform.rotate(warning_txt, 90)
        screen.blit(text_rot, (sc_bar_x + 8, 140))

    if fall_transition_timer == 0:
        atk_progress = 0.0
        if is_attacking:
            atk_progress = 1.0 - (attack_timer / MAX_ATTACK_TIMER)
            draw_sword_slash(screen, player_rect, player_facing_right, atk_progress, attack_range_bonus)

        if in_cutscene and cutscene_timer > 120:
            c_bubble = pygame.Surface((150, 45), pygame.SRCALPHA)
            c_bubble.fill((0, 0, 0, 180))
            screen.blit(c_bubble, (player_rect.x - render_cam_x - 50, player_rect.y - 55 + render_cam_y))
            pl_shout = font_small.render("DIE, MONSTER!" if current_lang == "EN" else "ZGIŃ, POTWORZE!", True, GOLD)
            screen.blit(pl_shout, (player_rect.x - render_cam_x - 45, player_rect.y - 45 + render_cam_y))

        draw_player_with_sword(screen, player_rect.x - render_cam_x, player_rect.y + render_cam_y, player_facing_right,
                               atk_progress, invincibility_timer > 0, in_cutscene)
    else:
        draw_player_with_sword(screen, player_rect.x - render_cam_x, player_rect.y + render_cam_y, player_facing_right,
                               0.0, False, True)

    if level_up_timer > 0:
        up_txt = font_giant.render(f"M-LEVEL UP: {m_level}!", True, GOLD)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 215, 0, min(100, level_up_timer * 3)))
        screen.blit(overlay, (0, 0))
        tr = up_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(up_txt, tr)

    # --- OBRAZKOWA SCENKA INTRO (HISTORIA ROBOTA) ---
    if in_story_intro:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((10, 12, 18))
        screen.blit(overlay, (0, 0))

        story_box = pygame.Surface((600, 420))
        story_box.fill((25, 28, 38))
        pygame.draw.rect(story_box, GOLD, (0, 0, 600, 420), width=3, border_radius=12)

        # Rysowanie generowanej na żywo dynamicznej ilustracji slajdu
        draw_intro_illustration(story_box, story_slide_idx)

        slide_text = txts["intro_slides"][story_slide_idx]
        words = slide_text.split()
        lines = []
        cur_line = ""
        for w in words:
            if font_med.size(cur_line + " " + w)[0] < 540:
                cur_line += (" " if cur_line else "") + w
            else:
                lines.append(cur_line)
                cur_line = w
        if cur_line:
            lines.append(cur_line)

        for idx, line in enumerate(lines):
            t_surf = font_med.render(line, True, WHITE)
            story_box.blit(t_surf, (30, 250 + idx * 28))

        next_txt = font_small.render(txts["intro_next"], True, GOLD)
        story_box.blit(next_txt, (30, 375))

        skip_txt = font_small.render(txts["intro_skip"], True, (150, 150, 150))
        story_box.blit(skip_txt, (470, 375))

        screen.blit(story_box, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 210))

    # --- HUD ---
    if not in_start_menu and not in_story_intro:
        w_name = current_theme["name_en"] if current_lang == "EN" else current_theme["name_pl"]
        score_txt = font_med.render(f"{txts['coins']}: {score} G | {txts['zone_hud']}: {zone_level} ({w_name})", True,
                                    DARK_GRAY)
        screen.blit(score_txt, (20, 15))
        diff_str_val = txts[DIFFICULTIES_KEYS[current_difficulty_idx]]
        diff_label = font_small.render(f"{txts['difficulty']}: {diff_str_val}", True,
                                       (150, 30, 30) if current_difficulty_idx >= 2 else (30, 100, 30))
        screen.blit(diff_label, (20, 80))

        lvl_txt = font_med.render(f"{txts['power_lvl']}: {m_level}", True, GOLD)
        screen.blit(lvl_txt, (SCREEN_WIDTH - 180, 15))

        pygame.draw.rect(screen, DARK_GRAY, (SCREEN_WIDTH - 180, 42, 160, 12), border_radius=3)
        xp_pct = min(1.0, m_xp / m_xp_needed)
        pygame.draw.rect(screen, (150, 50, 220), (SCREEN_WIDTH - 180, 42, int(160 * xp_pct), 12), border_radius=3)
        xp_txt = font_small.render(f"XP: {m_xp}/{m_xp_needed}", True, (50, 20, 80))
        screen.blit(xp_txt, (SCREEN_WIDTH - 155, 54))

        for i in range(player_max_hp):
            if i < player_hp:
                draw_heart(screen, 20 + (i * 28), 48)
            else:
                pygame.draw.circle(screen, DARK_GRAY, (20 + (i * 28) + 6, 48 + 6), 6)
                pygame.draw.circle(screen, DARK_GRAY, (20 + (i * 28) + 16, 48 + 6), 6)

    if save_notification_timer > 0 and not in_start_menu and not in_story_intro:
        save_notification_timer -= 1
        save_txt = font_med.render(txts["saved"], True, GRASS_GREEN)
        screen.blit(save_txt, (SCREEN_WIDTH // 2 - 60, 20))

    if near_shop and not in_shop and not is_paused and not in_cutscene and not is_game_over and not in_start_menu and not in_story_intro:
        hint_surf = pygame.Surface((320, 35), pygame.SRCALPHA)
        hint_surf.fill((0, 0, 0, 180))
        screen.blit(hint_surf, (SCREEN_WIDTH // 2 - 160, 100))
        hint_txt = font_small.render(txts["shop_exit"], True, GOLD)
        screen.blit(hint_txt, (SCREEN_WIDTH // 2 - 150, 107))

    # --- EKRAN STARTOWY (MAIN MENU) ---
    if in_start_menu:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((15, 18, 26, 235))
        screen.blit(overlay, (0, 0))

        if not in_options_menu:
            draw_game_logo(screen, SCREEN_WIDTH // 2, 70)

            pulse = math.sin(pygame.time.get_ticks() * 0.003) * 3
            title_surf = font_title.render(GAME_TITLE, True, GOLD)
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 145 + pulse))

            shadow_surf = font_title.render(GAME_TITLE, True, (80, 60, 0))
            screen.blit(shadow_surf, (title_rect.x + 3, title_rect.y + 3))
            screen.blit(title_surf, title_rect)

            sub_title = font_small.render(txts["sub_title"], True, (180, 180, 200))
            sub_rect = sub_title.get_rect(center=(SCREEN_WIDTH // 2, 195))
            screen.blit(sub_title, sub_rect)

            btn_start_new = pygame.Rect(cx, 240, 280, 42)
            btn_start_load = pygame.Rect(cx, 295, 280, 42)
            btn_start_opt = pygame.Rect(cx, 350, 280, 42)
            btn_start_quit = pygame.Rect(cx, 405, 280, 42)

            has_save = os.path.exists(SAVE_FILE)

            draw_button(screen, btn_start_new, txts["new_game"], btn_start_new.collidepoint(mouse_pos), GOLD, RED)
            draw_button(screen, btn_start_load, txts["load_game"], btn_start_load.collidepoint(mouse_pos),
                        enabled=has_save)
            draw_button(screen, btn_start_opt, txts["options"], btn_start_opt.collidepoint(mouse_pos))
            draw_button(screen, btn_start_quit, txts["quit"], btn_start_quit.collidepoint(mouse_pos))
        else:
            opt_title = font_large.render(txts["options"], True, GOLD)
            screen.blit(opt_title, opt_title.get_rect(center=(SCREEN_WIDTH // 2, 80)))

            btn_opt_diff = pygame.Rect(cx, 130, 280, 36)
            btn_opt_lang = pygame.Rect(cx, 175, 280, 36)
            btn_opt_fs = pygame.Rect(cx, 220, 280, 36)
            btn_opt_res = pygame.Rect(cx, 265, 280, 36)
            btn_opt_atk = pygame.Rect(cx, 310, 280, 36)
            btn_opt_tut = pygame.Rect(cx, 355, 280, 36)
            btn_opt_back = pygame.Rect(cx, 410, 280, 36)

            diff_str = f"{txts['difficulty']}: {txts[DIFFICULTIES_KEYS[current_difficulty_idx]]}"
            lang_str = f"{txts['language']}: {current_lang}"
            fs_str = txts["fullscreen"] if is_fullscreen else txts["windowed"]
            res_str = f"{txts['res']}: {SCREEN_WIDTH}x{SCREEN_HEIGHT}"
            atk_str = txts["atk_mouse"] if attack_with_mouse else txts["atk_keys"]
            tut_str = f"{txts['show_tut']}: {'ON' if show_tutorial else 'OFF'}"

            draw_button(screen, btn_opt_diff, diff_str, btn_opt_diff.collidepoint(mouse_pos))
            draw_button(screen, btn_opt_lang, lang_str, btn_opt_lang.collidepoint(mouse_pos))
            draw_button(screen, btn_opt_fs, fs_str, btn_opt_fs.collidepoint(mouse_pos))
            draw_button(screen, btn_opt_res, res_str, btn_opt_res.collidepoint(mouse_pos))
            draw_button(screen, btn_opt_atk, atk_str, btn_opt_atk.collidepoint(mouse_pos))
            draw_button(screen, btn_opt_tut, tut_str, btn_opt_tut.collidepoint(mouse_pos))
            draw_button(screen, btn_opt_back, txts["back"], btn_opt_back.collidepoint(mouse_pos), GOLD, RED)

    # --- GAME OVER ---
    if is_game_over and not in_start_menu:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 10, 15, 230))
        screen.blit(overlay, (0, 0))

        go_box = pygame.Surface((480, 420))
        go_box.fill((35, 25, 30))
        pygame.draw.rect(go_box, RED, (0, 0, 480, 420), width=3, border_radius=12)

        title_go = font_giant.render(txts["game_over"], True, RED)
        go_box.blit(title_go, (120, 20))

        sub_go = font_med.render(txts["summary"], True, GOLD)
        go_box.blit(sub_go, (75, 80))

        w_name = current_theme["name_en"] if current_lang == "EN" else current_theme["name_pl"]
        s1 = font_small.render(f"• {txts['zone']}: {zone_level} ({w_name})", True, WHITE)
        s2 = font_small.render(f"• {txts['player_lvl']}: {m_level} Lvl", True, WHITE)
        s3 = font_small.render(f"• {txts['coins_total']}: {total_score_collected} G", True, WHITE)
        s4 = font_small.render(f"• {txts['coins_current']}: {score} G", True, WHITE)
        s5 = font_small.render(f"• {txts['dmg_stat']}: {attack_damage} DMG", True, WHITE)
        s6 = font_small.render(f"• {txts['difficulty']}: {txts[DIFFICULTIES_KEYS[current_difficulty_idx]]}", True, GOLD)

        go_box.blit(s1, (40, 130))
        go_box.blit(s2, (40, 160))
        go_box.blit(s3, (40, 190))
        go_box.blit(s4, (40, 220))
        go_box.blit(s5, (40, 250))
        go_box.blit(s6, (40, 280))

        screen.blit(go_box, (SCREEN_WIDTH // 2 - 240, 50))

        btn_restart = pygame.Rect(cx, 380, 280, 42)
        btn_start_menu_go = pygame.Rect(cx, 435, 280, 42)

        draw_button(screen, btn_restart, txts["play_again"], btn_restart.collidepoint(mouse_pos), GOLD, RED)
        draw_button(screen, btn_start_menu_go, txts["main_menu"], btn_start_menu_go.collidepoint(mouse_pos))

    # --- SKLEP ---
    if in_shop and not is_paused and not is_game_over and not in_start_menu and not in_story_intro:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        shop_box = pygame.Surface((540, 380))
        shop_box.fill((40, 44, 52))
        pygame.draw.rect(shop_box, GOLD, (0, 0, 540, 380), width=3)
        title = font_large.render(txts["shop_title"], True, GOLD)
        shop_box.blit(title, (110, 15))

        dj_status = txts["bought"] if has_double_jump else f"[1] {txts['buy_for']} {COST_DOUBLE_JUMP} G"
        t_dj = font_med.render(f"1. {txts['double_jump']} - {dj_status}", True,
                               GRASS_GREEN if has_double_jump else WHITE)
        shop_box.blit(t_dj, (20, 65))

        sp_status = txts["bought"] if speed_upgraded else f"[2] {txts['buy_for']} {COST_SPEED} G"
        t_sp = font_med.render(f"2. {txts['fast_run']} - {sp_status}", True, GRASS_GREEN if speed_upgraded else WHITE)
        shop_box.blit(t_sp, (20, 115))

        dmg_status = "MAX" if attack_damage >= 3 else f"[3] {txts['buy_for']} {COST_DAMAGE} G"
        t_dmg = font_med.render(f"3. {txts['sword_dmg']} ({attack_damage} DMG) - {dmg_status}", True, WHITE)
        shop_box.blit(t_dmg, (20, 165))

        rng_status = "MAX" if attack_range_bonus >= 30 else f"[4] {txts['buy_for']} {COST_RANGE} G"
        t_rng = font_med.render(f"4. {txts['sword_rng']} - {rng_status}", True, WHITE)
        shop_box.blit(t_rng, (20, 215))

        t_heal = font_med.render(f"5. {txts['heal_pot']} - [5] {txts['buy_for']} {COST_HEAL} G", True, RED)
        shop_box.blit(t_heal, (20, 265))

        hp_status = "MAX (5)" if player_max_hp >= 5 else f"[6] {txts['buy_for']} {COST_EXTRA_HP} G"
        t_hp = font_med.render(f"6. {txts['extra_hp']} ({player_max_hp}/5) - {hp_status}", True, GOLD)
        shop_box.blit(t_hp, (20, 315))

        close_txt = font_small.render(txts["shop_exit"], True, (180, 180, 180))
        shop_box.blit(close_txt, (110, 350))
        screen.blit(shop_box, (SCREEN_WIDTH // 2 - 270, 90))

    # --- MENU PAUZY I SEKCJA OPCJI IN-GAME ---
    if is_paused and not is_game_over and not in_start_menu and not in_story_intro:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))

        menu_box = pygame.Surface((400, 440))
        menu_box.fill((30, 34, 42))
        pygame.draw.rect(menu_box, GOLD, (0, 0, 400, 440), width=3, border_radius=10)

        p_title_str = txts["options"] if in_options_menu else ("PAUSE" if current_lang == "EN" else "PAUZA")
        title = font_large.render(p_title_str, True, GOLD)
        menu_box.blit(title, title.get_rect(center=(200, 30)))
        screen.blit(menu_box, (SCREEN_WIDTH // 2 - 200, 50))

        if not in_options_menu:
            btn_resume = pygame.Rect(cx, 120, 280, 38)
            btn_save = pygame.Rect(cx, 170, 280, 38)
            btn_load = pygame.Rect(cx, 220, 280, 38)
            btn_options = pygame.Rect(cx, 270, 280, 38)
            btn_menu_main = pygame.Rect(cx, 320, 280, 38)
            btn_quit = pygame.Rect(cx, 370, 280, 38)

            draw_button(screen, btn_resume, txts["resume"], btn_resume.collidepoint(mouse_pos))
            draw_button(screen, btn_save, txts["save"], btn_save.collidepoint(mouse_pos))
            draw_button(screen, btn_load, txts["load_game"], btn_load.collidepoint(mouse_pos))
            draw_button(screen, btn_options, txts["options"], btn_options.collidepoint(mouse_pos))
            draw_button(screen, btn_menu_main, txts["main_menu"], btn_menu_main.collidepoint(mouse_pos))
            draw_button(screen, btn_quit, txts["quit"], btn_quit.collidepoint(mouse_pos))
        else:
            btn_opt_diff = pygame.Rect(cx, 110, 280, 36)
            btn_opt_lang = pygame.Rect(cx, 155, 280, 36)
            btn_opt_fs = pygame.Rect(cx, 200, 280, 36)
            btn_opt_res = pygame.Rect(cx, 245, 280, 36)
            btn_opt_atk = pygame.Rect(cx, 290, 280, 36)
            btn_opt_tut = pygame.Rect(cx, 335, 280, 36)
            btn_opt_back = pygame.Rect(cx, 390, 280, 36)

            diff_str = f"{txts['difficulty']}: {txts[DIFFICULTIES_KEYS[current_difficulty_idx]]}"
            lang_str = f"{txts['language']}: {current_lang}"
            fs_str = txts["fullscreen"] if is_fullscreen else txts["windowed"]
            res_str = f"{txts['res']}: {SCREEN_WIDTH}x{SCREEN_HEIGHT}"
            atk_str = txts["atk_mouse"] if attack_with_mouse else txts["atk_keys"]
            tut_str = f"{txts['show_tut']}: {'ON' if show_tutorial else 'OFF'}"

            draw_button(screen, btn_opt_diff, diff_str, btn_opt_diff.collidepoint(mouse_pos))
            draw_button(screen, btn_opt_lang, lang_str, btn_opt_lang.collidepoint(mouse_pos))
            draw_button(screen, btn_opt_fs, fs_str, btn_opt_fs.collidepoint(mouse_pos))
            draw_button(screen, btn_opt_res, res_str, btn_opt_res.collidepoint(mouse_pos))
            draw_button(screen, btn_opt_atk, atk_str, btn_opt_atk.collidepoint(mouse_pos))
            draw_button(screen, btn_opt_tut, tut_str, btn_opt_tut.collidepoint(mouse_pos))
            draw_button(screen, btn_opt_back, txts["back"], btn_opt_back.collidepoint(mouse_pos), GOLD, RED)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()