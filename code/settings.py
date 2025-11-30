WIDTH = 1200
HEIGHT = 720
FPS = 60
TILE_SIZE = 64

# --- LEJANT (MEVCUT VARLIKLAR) ---
# X: Duvar
# P: Oyuncu Başlangıç Pozisyonu
# A: Altın Para
# E: Normal Düşman
# S: Güçlü Düşman
# B: Uçan Düşman
# G: Ateş Atan Düşman
# K: Anahtar
# 1,2,3,4: Kapı (4 parça)
# T: Diken
# W: Testere
# Y: Düşen Platform


# LEVEL 1 - First Steps
LEVEL_1 = [
    '                                                                        ',
    '                                                                        ',
    '  P                                                         12          ',
    'XXXXX                                     A                 34  XXXXXXXX',
    '            A             A             XXXXX             XXXXX         ',
    '          XXXXX         XXXXX                                           ',
    '                                                                        ',
    '                  A               K               E                      ',
    '                XXXXX           XXXXX           XXXXX                   ',
    '                                                                        ',
    '      E                                               A                 ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX '
]

# LEVEL 2 - The Pits
LEVEL_2 = [
    '                                                                  12    ',
    '  P                                                               34    ',
    'XXXXX           A             A                       XXXXXXXX  XXXXXXXX',
    '              XXXXX         XXXXX                                       ',
    '                                         G                              ',
    '          E                       XXXXXXXXX           A                 ',
    '        XXXXX               E                        XXXXX              ',
    '                          XXXXX                                      A  ',
    '                                                           A       XXXXX',
    '    A                                 XXXXX             XXXXX           ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXKXXXXXXXXXXXXXXXXXX ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX '
]

# LEVEL 3 - Fragile Ground
LEVEL_3 = [
    '                                                                  12    ',
    '        XXXXX                                                     34    ',
    '                        A             A                         XXXXXXXX',
    '  P                   YYYYY         YYYYY                               ',
    'XXXXX                                             A                     ',
    '              A                 K               YYYYY         E         ',
    '            YYYYY           E XXXXX                         XXXXX       ',
    '                          XXXXX           A                             ',
    '                                        YYYYY                           ',
    '      E                                                                 ',
    'XXXXXXXXXXXXXXXXXXXXXX           XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ',
    'XXXXXXXXXXXXXXXXXXXXXX           XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX '
]

# LEVEL 4 - Spiked Path
LEVEL_4 = [
    '                                                                  12    ',
    '                                                                  34    ',
    '  P                                         T T T               XXXXXXXX',
    'XXXXX           A                         XXXXXXX           A           ',
    '              XXXXX                                       XXXXX         ',
    '                                A                                       ',
    '          A       T T T       XXXXX                                     ',
    '        XXXXX     XXXXX                   E               E             ',
    '  K                                     XXXXX T T T     XXXXX   XXXXX   ',
    'XXXXX                                                                   ',
    'XXXXXXXXXXXXXXX T XXXXXXXXX T XXXXXXXXX T XXXXXXXXXXXXXXXXXXXXXXXXXXXXX ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX '
]

# LEVEL 5 - Saw Zone
LEVEL_5 = [
    '                                                                  12    ',
    '  P                                                               34    ',
    'XXXXX                 W               W                XX       XXXXXXXX',
    '            A       XXXXX           XXXXX        A                       ',
    '          XXXXX                                XXXXX                     ',
    '                                                            E           ',
    '                  A       K       A                       XXXXX         ',
    '                XXXXX   XXXXX   XXXXX           W                       ',
    '                                              XXXXX                     ',
    '      E     W             E                               E       XXXXX ',
    '    XXXXXXXXX           XXXXX           XXXXX           XXXXX           ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX '
]

# LEVEL 6 - Air Assault
LEVEL_6 = [
    '  K                                                                12   ',
    'XXXXX                                            E                 34   ',
    '                                             XXXXXXXXX        XXXXXXXXXX',
    '            A                                                          ',
    '          YYYYY                          A              B               ',
    '                                        YYYYY                           ',
    '                  A                                                     ',
    '  P           YYYYY     B                     A               G         ',
    'XXXXX         B                               YYYYY         XXXXX       ',
    '      E             E           B                                       ',
    '    XXXXX         XXXXX                                                 ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXX '
]

# LEVEL 7 - Fire Line
LEVEL_7 = [
    '                                                                  12    ',
    '        XXXXX                                                     34    ',
    '                      XXXXX         E A                         XXXXXXXX',
    '                                  XXXXX             G                   ',
    '  P                                               XXXXX                 ',
    'XXXXX             A                   E   A                 A           ',
    '                XXXXX                   XXXXX             XXXXX         ',
    '                                                                      G ',
    '      XXXXX         A             A             A               XXXXX   ',
    '                  XXXXX T       XXXXX T       XXXXX T                   ',
    'XXXXXXXXXXXXXXX   XXXXXXXXX   XXXXXXXXX   XXXXXXXXX K XXXXXXXXXXXXXXXXX ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX '
]

# LEVEL 8 - Vertical Climb
LEVEL_8 = [
    '                                                                  12    ',
    '                                                                  34    ',
    '                      W               W                         XXXXXXXX',
    '            A       XXXXX           XXXXX          A                    ',
    '          XXXXX           B       G              XXXXX                  ',
    '                         E                                              ',
    '                  A               A               A     S               ',
    '        B       XXXXX           XXXXX           XXXXX XXXXX             ',
    '                                                                        ',
    '  P   XXXXX T           E               E               G               ',
    'XXXXX XXXXXXXXX T       XXXXX           XXXXX           XXXXX         K ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX '
]

# LEVEL 9 - Fragile Passage
LEVEL_9 = [
    '                                                                  12    ',
    '                                                                  34    ',
    '                                                      XXXXXXXX  XXXXXXXX',
    '  K                                         A                           ',
    'XXXXX       A           B           B     YYYYY                         ',
    '          YYYYY                       E                 A               ',
    '                                  E                   YYYYY             ',
    '  P               A           A XXXXX                           S       ',
    'XXXXX           YYYYY       YYYYY       B                     XXXXX     ',
    '      E                                           A             E       ',
    '    XXXXX                                       YYYYY         XXXXX     ',
    '                                                                        '
]

# LEVEL 10 - Strong Guard
LEVEL_10 = [
    '                                                                        ',
    '        XXXXX           A                                         12    ',
    '                      XXXXX         G A                           34    ',
    '                                  XXXXX             E           XXXXXXXX',
    '  P                                               XXXXX                 ',
    'XXXXX                                     A                 A           ',
    '              W             W           XXXXX             XXXXX         ',
    '        G           T T T           T                         S       G ',
    '      XXXXX         XXXXX         XXXXX                S    XXXXX   XXXXX',
    '                                                                        ',
    'K                                                                       ',
    'XXXXXXX                                                                 '
]

# LEVEL 11 - Saw Labyrinth
LEVEL_11 = [
    '  P                                                               12    ',
    'XXXXX         W               Y               W                   34    ',
    '            XXXXX           XXXXX           XXXXX               XXXXXXXX',
    '                    XXXXX           XXXXX           XXXXX               ',
    '                  A     S   S     A               A                     ',
    '        W       XXXXX XXXXX     XXXXX     S     XXXXX       W           ',
    '                    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX      ',
    '            A                           XXXXX               A           ',
    '          XXXXX T   W   T       T   W   T       T W T XXXXX             ',
    '                  XXXXX           XXXXX           XXXXX         K       ',
    '                                                              XXXXX     ',
    '                                                                        '
]

# LEVEL 12 - High Risk
LEVEL_12 = [
    '                                                                  12    ',
    '                                                                  34    ',
    'XXXXX   W                     B       A       XXXXXXXXX        XXXXXXXX',
    '      XXXXX A                       XXXXX                               ',
    '          YYYYY           B                   W           B             ',
    '  P                                         XXXXX                       ',
    'XXXXX             A       T                           K                 ',
    '        B       YYYYY   XXXXX       B               XXXXX       S       ',
    '                                              YYYYY     T     XXXXX     ',
    '                    E          G  G                XXXXX             ',
    '                  XXXXX T       XXXXX                                   ',
    '                        XXXXX                                           '
]

# LEVEL 13 - Strategic Climb
LEVEL_13 = [
    '  K                                                                     ',
    'XXXXX           A         B                                             ',
    '                      XXXXX         G A               S                 ',
    '                                  XXXXX             XXXXX               ',
    '  P                                                               12    ',
    'XXXXX             A                       A                 A     34    ',
    '              W XXXXX W             W   XXXXX   W         XXXXX XXXXXXXX',
    '        G           T T T           T                                 G ',
    '      XXXXX         XXXXX         XXXXX                         XXXXX   ',
    '            B             G             B             B                 ',
    '                                                                        ',
    '                                                                        '
]

# LEVEL 14 - Spiked Road
LEVEL_14 = [
    '                                                                  12    ',
    '                                                                  34    ',
    '                      W               W                 X       XXXXXXXX',
    '            A       XXXXX T         XXXXX T     A                       ',
    '          XXXXX           B       B           XXXXX                     ',
    '  P           XXXXX          XXXXX         XXXXX                     ',
    '                    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX      ',
    '        B       XXXXX T         XXXXX T         XXXXX T S S             ',
    '  K                                                   XXXXX             ',
    'XXXXX           T           S               S               G           ',
    '              XXXXX T       XXXXX           XXXXX           XXXXX       ',
    '                                                                        '
]

# LEVEL 15 - Grand Finale
LEVEL_15 = [
    '                                                                  12    ',
    'XXXXX         W       B       W       B       W                   34    ',
    '            XXXXX           XXXXX           XXXXX               XXXXXXXX',
    '                                                                        ',
    '      YYYYY     A     YYYYY     S     YYYYY     A     YYYYY             ',
    ' P              Y               X               Y                       ',
    'XXXXX           Y               X               Y                       ',
    '        G       Y G   G A     G X G     A     G Y       G               ',
    '      XXXXX T T XXXXX T X T T XXXXX T T X T T XXXXX T T XXXXX           ',
    '                                                                        ',
    '  K                                                                     ',
    'XXXXX                                                                   '
]

LEVELS = [
    LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4,
    LEVEL_5, LEVEL_6, LEVEL_7, LEVEL_8,
    LEVEL_9, LEVEL_10, LEVEL_11, LEVEL_12,
    LEVEL_13, LEVEL_14, LEVEL_15
]

# --- Seviye fazlarına göre zorluk çarpanları
# Fazlar: 1-4, 5-8, 9-12, 13-15. Her faz için düşman hız/mesafe çarpanı.
PHASE_SCALE_CONFIG = [
    (1, 4, 1.00),
    (5, 8, 1.08),
    (9, 12, 1.15),
    (13, 15, 1.25)
]

def get_level_scale(level_index):
    # level_index 1 tabanlı kabul edilir
    try:
        lvl = int(level_index)
    except Exception:
        return 1.0

    for start, end, scale in PHASE_SCALE_CONFIG:
        if start <= lvl <= end:
            return float(scale)

    return 1.0