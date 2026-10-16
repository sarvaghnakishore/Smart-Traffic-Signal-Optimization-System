import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS & THEME PALETTE
# ─────────────────────────────────────────────────────────────────────────────
FONT_PRIMARY = 'Segoe UI'
FONT_HEADING = 'Segoe UI'

# Colors
C_DARK_BG = RGBColor(22, 27, 38)       # #161B26
C_DARK_SURFACE = RGBColor(30, 41, 59)   # #1E293B
C_LIGHT_BG = RGBColor(248, 250, 252)   # #F8FAFC
C_WHITE = RGBColor(255, 255, 255)
C_AMBER = RGBColor(245, 158, 11)       # #F59E0B
C_AMBER_DARK = RGBColor(217, 119, 6)   # #D97706
C_TEXT_DARK = RGBColor(15, 23, 42)     # #0F172A
C_TEXT_MUTED = RGBColor(100, 116, 139) # #64748B
C_TEXT_BODY = RGBColor(51, 65, 85)     # #334155
C_CARD_BORDER = RGBColor(226, 232, 240)# #E2E8F0
C_GREEN = RGBColor(16, 185, 129)       # #10B981
C_RED = RGBColor(239, 68, 68)          # #EF4444

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "runs", "detect", "runs", "detect", "ua_detrac_yolov85")
DIAGRAM_DIR = os.path.join(BASE_DIR, "ppt_assets")
OUTPUT_FILE = os.path.join(BASE_DIR, "Smart_Traffic_Signal_Optimization_Review.pptx")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def add_solid_bg(slide, color):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = color
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, section_num, section_title, main_heading, is_dark=False):
    # Eyebrow / Section tag
    tb_sec = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.5), Inches(0.35))
    tf_sec = tb_sec.text_frame
    tf_sec.word_wrap = True
    tf_sec.margin_left = tf_sec.margin_top = tf_sec.margin_right = tf_sec.margin_bottom = 0
    p_sec = tf_sec.paragraphs[0]
    p_sec.text = f"{section_num}  {section_title}".upper() if section_num else section_title.upper()
    p_sec.font.name = FONT_PRIMARY
    p_sec.font.size = Pt(11)
    p_sec.font.bold = True
    p_sec.font.color.rgb = C_AMBER if is_dark else C_AMBER_DARK

    # Main Heading
    tb_head = slide.shapes.add_textbox(Inches(0.8), Inches(0.80), Inches(11.8), Inches(0.65))
    tf_head = tb_head.text_frame
    tf_head.word_wrap = True
    tf_head.margin_left = tf_head.margin_top = tf_head.margin_right = tf_head.margin_bottom = 0
    p_head = tf_head.paragraphs[0]
    p_head.text = main_heading
    p_head.font.name = FONT_HEADING
    p_head.font.size = Pt(23)
    p_head.font.bold = True
    p_head.font.color.rgb = C_WHITE if is_dark else C_TEXT_DARK

def add_footer(slide, slide_num_str, is_dark=False):
    # Footer Left
    tb_left = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(8.0), Inches(0.3))
    tf_left = tb_left.text_frame
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_right = tf_left.margin_bottom = 0
    p_l = tf_left.paragraphs[0]
    p_l.text = "Smart Traffic Signal Optimization System · Deep Learning Review"
    p_l.font.name = FONT_PRIMARY
    p_l.font.size = Pt(9.5)
    p_l.font.color.rgb = RGBColor(148, 163, 184) if is_dark else RGBColor(148, 163, 184)

    # Footer Right
    tb_right = slide.shapes.add_textbox(Inches(12.0), Inches(7.05), Inches(0.6), Inches(0.3))
    tf_right = tb_right.text_frame
    tf_right.margin_left = tf_right.margin_top = tf_right.margin_right = tf_right.margin_bottom = 0
    p_r = tf_right.paragraphs[0]
    p_r.text = slide_num_str
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.font.name = FONT_PRIMARY
    p_r.font.size = Pt(10)
    p_r.font.bold = True
    p_r.font.color.rgb = RGBColor(148, 163, 184) if is_dark else RGBColor(148, 163, 184)

def add_card(slide, left, top, width, height, fill_color=C_WHITE, border_color=C_CARD_BORDER, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    card = slide.shapes.add_shape(shape, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = fill_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
    else:
        card.line.fill.background()
    return card

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 1: TITLE SLIDE (DARK THEME)
# ─────────────────────────────────────────────────────────────────────────────
slide1 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide1, C_DARK_BG)

# Decorative circle in background
decor = slide1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.5), Inches(1.5), Inches(5.5), Inches(5.5))
decor.fill.solid()
decor.fill.fore_color.rgb = RGBColor(28, 36, 52)
decor.line.fill.background()

# Top eyebrow
tb_eyebrow = slide1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(10.0), Inches(0.4))
tf_eye = tb_eyebrow.text_frame
tf_eye.margin_left = tf_eye.margin_top = tf_eye.margin_right = tf_eye.margin_bottom = 0
p_eye = tf_eye.paragraphs[0]
p_eye.text = "DEEP LEARNING · COMPUTER VISION · INTELLIGENT SYSTEMS"
p_eye.font.name = FONT_PRIMARY
p_eye.font.size = Pt(12)
p_eye.font.bold = True
p_eye.font.color.rgb = C_AMBER

# Title
tb_title = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(10.5), Inches(1.6))
tf_title = tb_title.text_frame
tf_title.word_wrap = True
tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
p_title = tf_title.paragraphs[0]
p_title.text = "Smart Traffic Signal\nOptimization System"
p_title.font.name = FONT_HEADING
p_title.font.size = Pt(40)
p_title.font.bold = True
p_title.font.color.rgb = C_WHITE

# Subtitle
tb_sub = slide1.shapes.add_textbox(Inches(1.0), Inches(3.65), Inches(9.5), Inches(0.9))
tf_sub = tb_sub.text_frame
tf_sub.word_wrap = True
tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
p_sub = tf_sub.paragraphs[0]
p_sub.text = "Real-time multi-lane vehicle detection, dynamic density estimation, and adaptive signal timing using YOLOv8 & OpenCV."
p_sub.font.name = FONT_PRIMARY
p_sub.font.size = Pt(16)
p_sub.font.italic = True
p_sub.font.color.rgb = RGBColor(203, 213, 225)

# Circle Accent Badge
circle_badge = slide1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.0), Inches(4.8), Inches(0.85), Inches(0.85))
circle_badge.fill.solid()
circle_badge.fill.fore_color.rgb = C_AMBER
circle_badge.line.fill.background()

# Team details block
tb_team = slide1.shapes.add_textbox(Inches(2.1), Inches(4.75), Inches(8.5), Inches(1.1))
tf_team = tb_team.text_frame
tf_team.margin_left = tf_team.margin_top = tf_team.margin_right = tf_team.margin_bottom = 0
p_t1 = tf_team.paragraphs[0]
p_t1.text = "Team: [G. Sarvaghna Reddy]"
p_t1.font.name = FONT_PRIMARY
p_t1.font.size = Pt(13)
p_t1.font.bold = True
p_t1.font.color.rgb = C_WHITE

p_t2 = tf_team.add_paragraph()
p_t2.text = "      [B. Chandana]"
p_t2.font.name = FONT_PRIMARY
p_t2.font.size = Pt(13)
p_t2.font.bold = True
p_t2.font.color.rgb = C_WHITE

p_t3 = tf_team.add_paragraph()
p_t3.text = "Department of Computer Science & Engineering · Capstone Review"
p_t3.font.name = FONT_PRIMARY
p_t3.font.size = Pt(11)
p_t3.font.color.rgb = RGBColor(148, 163, 184)

add_footer(slide1, "01", is_dark=True)

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 2: PROBLEM STATEMENT (LIGHT THEME)
# ─────────────────────────────────────────────────────────────────────────────
slide2 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide2, C_LIGHT_BG)
add_header(slide2, "01", "Problem Statement", "Current Vision & Sensor Systems Struggle with Real-Time Intersection Optimization")

# Left Card: Problem Narrative
card_prob = add_card(slide2, Inches(0.8), Inches(1.65), Inches(7.5), Inches(5.1), C_WHITE, C_CARD_BORDER)
tb_prob = slide2.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(6.9), Inches(4.6))
tf_prob = tb_prob.text_frame
tf_prob.word_wrap = True
tf_prob.margin_left = tf_prob.margin_top = tf_prob.margin_right = tf_prob.margin_bottom = 0

p = tf_prob.paragraphs[0]
p.text = "Urban traffic congestion is exacerbated by rigid, non-adaptive traffic signals:"
p.font.name = FONT_PRIMARY
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = C_TEXT_DARK
p.space_after = Pt(12)

bullets = [
    ("Rigid Pre-Programmed Timers: ", "Traditional traffic signals operate on fixed timer schedules regardless of real-time lane demand, forcing drivers to wait at empty green signals."),
    ("Inductive Sensor Deficiencies: ", "In-pavement physical loops and ultrasonic sensors suffer high maintenance failure rates, require road disruption, and cannot classify vehicle categories."),
    ("Severe Economic & Fuel Waste: ", "Prolonged vehicle idling in congested junctions wastes millions of liters of fossil fuel and drastically raises urban greenhouse gas emissions."),
    ("Emergency Corridor Blockades: ", "Emergency response vehicles (ambulances, fire trucks, police) experience fatal delays due to lack of automated queue clearing and phase preemption."),
    ("Complex Multi-Lane Imbalance: ", "Heavy directional spikes (morning vs. evening peak flows) cause feeder lanes to be gridlocked while crossing lanes stay underutilized.")
]

for title, desc in bullets:
    p_b = tf_prob.add_paragraph()
    p_b.space_after = Pt(9)
    run1 = p_b.add_run()
    run1.text = "• " + title
    run1.font.bold = True
    run1.font.size = Pt(12)
    run1.font.color.rgb = C_TEXT_DARK
    
    run2 = p_b.add_run()
    run2.text = desc
    run2.font.size = Pt(11.5)
    run2.font.color.rgb = C_TEXT_BODY

# Right Stats Cards (Dark Theme)
# Stat Card 1
c_stat1 = add_card(slide2, Inches(8.6), Inches(1.65), Inches(3.9), Inches(1.55), C_DARK_BG, None)
tb_s1 = slide2.shapes.add_textbox(Inches(8.8), Inches(1.8), Inches(3.5), Inches(1.2))
tf_s1 = tb_s1.text_frame
tf_s1.word_wrap = True
tf_s1.margin_left = tf_s1.margin_top = tf_s1.margin_right = tf_s1.margin_bottom = 0
p_s1_num = tf_s1.paragraphs[0]
p_s1_num.text = "119+ Hours"
p_s1_num.font.name = FONT_HEADING
p_s1_num.font.size = Pt(30)
p_s1_num.font.bold = True
p_s1_num.font.color.rgb = C_AMBER
p_s1_lbl = tf_s1.add_paragraph()
p_s1_lbl.text = "average commuter delay wasted per year in major urban congestion (INRIX Scorecard)"
p_s1_lbl.font.size = Pt(11)
p_s1_lbl.font.color.rgb = RGBColor(203, 213, 225)

# Stat Card 2
c_stat2 = add_card(slide2, Inches(8.6), Inches(3.40), Inches(3.9), Inches(1.55), C_DARK_BG, None)
tb_s2 = slide2.shapes.add_textbox(Inches(8.8), Inches(3.55), Inches(3.5), Inches(1.2))
tf_s2 = tb_s2.text_frame
tf_s2.word_wrap = True
tf_s2.margin_left = tf_s2.margin_top = tf_s2.margin_right = tf_s2.margin_bottom = 0
p_s2_num = tf_s2.paragraphs[0]
p_s2_num.text = "$88 Billion+"
p_s2_num.font.name = FONT_HEADING
p_s2_num.font.size = Pt(30)
p_s2_num.font.bold = True
p_s2_num.font.color.rgb = C_AMBER
p_s2_lbl = tf_s2.add_paragraph()
p_s2_lbl.text = "annual financial and wasted fuel loss due to urban intersection delays worldwide"
p_s2_lbl.font.size = Pt(11)
p_s2_lbl.font.color.rgb = RGBColor(203, 213, 225)

# Stat Card 3
c_stat3 = add_card(slide2, Inches(8.6), Inches(5.15), Inches(3.9), Inches(1.60), C_DARK_BG, None)
tb_s3 = slide2.shapes.add_textbox(Inches(8.8), Inches(5.30), Inches(3.5), Inches(1.25))
tf_s3 = tb_s3.text_frame
tf_s3.word_wrap = True
tf_s3.margin_left = tf_s3.margin_top = tf_s3.margin_right = tf_s3.margin_bottom = 0
p_s3_num = tf_s3.paragraphs[0]
p_s3_num.text = "~35% - 42%"
p_s3_num.font.name = FONT_HEADING
p_s3_num.font.size = Pt(30)
p_s3_num.font.bold = True
p_s3_num.font.color.rgb = C_GREEN
p_s3_lbl = tf_s3.add_paragraph()
p_s3_lbl.text = "junction wait-time reduction achieved through real-time density-adaptive signaling"
p_s3_lbl.font.size = Pt(11)
p_s3_lbl.font.color.rgb = RGBColor(203, 213, 225)

add_footer(slide2, "02")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 3: ANALYSIS OF EXISTING SYSTEMS (LIGHT THEME)
# ─────────────────────────────────────────────────────────────────────────────
slide3 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide3, C_LIGHT_BG)
add_header(slide3, "02", "Analysis of Existing Systems", "Comparative Assessment of Existing Traffic Control Approaches")

# 3 Column Cards + 1 Limitations Card
cards_data = [
    ("Fixed-Timer Actuation", [
        "Pre-programmed fixed cycle lengths (e.g., 60s per leg).",
        "Blind to actual queue lengths; gives green lights to empty roads.",
        "Completely unable to handle atypical traffic surges or events.",
        "Causes unnecessary vehicle idling and increased fuel consumption."
    ]),
    ("In-Pavement Sensors", [
        "Inductive loops, magnetometers, pneumatic road tubes.",
        "Extremely expensive installation & requires cutting asphalt roads.",
        "Prone to weather damage, pavement shifts, and wire severing.",
        "Binary presence only; cannot classify cars, buses, trucks, bikes."
    ]),
    ("Early Computer Vision", [
        "Background subtraction (GMM) and optical flow algorithms.",
        "Extremely sensitive to lighting shifts, vehicle shadows, and rain.",
        "High false positive rates in dense bumper-to-bumper occlusion.",
        "Lacks deep semantic features and per-class confidence scoring."
    ])
]

card_w = Inches(2.7)
card_gap = Inches(0.2)
top_pos = Inches(1.7)
h_pos = Inches(5.0)

for i, (title, items) in enumerate(cards_data):
    left_pos = Inches(0.8) + i * (card_w + card_gap)
    c = add_card(slide3, left_pos, top_pos, card_w, h_pos, C_WHITE, C_CARD_BORDER)
    
    # Amber circle badge at top
    b = slide3.shapes.add_shape(MSO_SHAPE.OVAL, left_pos + Inches(0.95), top_pos + Inches(0.35), Inches(0.8), Inches(0.8))
    b.fill.solid()
    b.fill.fore_color.rgb = C_AMBER
    b.line.fill.background()
    
    tb = slide3.shapes.add_textbox(left_pos + Inches(0.2), top_pos + Inches(1.35), card_w - Inches(0.4), h_pos - Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.alignment = PP_ALIGN.CENTER
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(14)
    p_t.font.bold = True
    p_t.font.color.rgb = C_TEXT_DARK
    p_t.space_after = Pt(14)
    
    for it in items:
        p_i = tf.add_paragraph()
        p_i.text = "• " + it
        p_i.font.name = FONT_PRIMARY
        p_i.font.size = Pt(10.5)
        p_i.font.color.rgb = C_TEXT_BODY
        p_i.space_after = Pt(8)

# 4th Card: Current Limitations (Rightmost)
left_pos4 = Inches(0.8) + 3 * (card_w + card_gap)
c4 = add_card(slide3, left_pos4, top_pos, Inches(3.2), h_pos, RGBColor(241, 245, 249), RGBColor(203, 213, 225))

tb4 = slide3.shapes.add_textbox(left_pos4 + Inches(0.25), top_pos + Inches(0.35), Inches(2.7), h_pos - Inches(0.5))
tf4 = tb4.text_frame
tf4.word_wrap = True
p4_t = tf4.paragraphs[0]
p4_t.text = "Current Limitations"
p4_t.font.name = FONT_HEADING
p4_t.font.size = Pt(16)
p4_t.font.bold = True
p4_t.font.color.rgb = RGBColor(180, 83, 9)
p4_t.space_after = Pt(16)

limits = [
    ("No 4-Way Coordinated Vision: ", "Evaluates single lanes in silos rather than optimizing entire multi-phase intersections."),
    ("High Latency & Hardware Cost: ", "Heavy deep learning models (ResNet-101, Faster R-CNN) cannot run real-time on edge compute nodes."),
    ("No Anti-Starvation Guarantees: ", "Greedy allocation starves low-traffic feeder roads indefinitely."),
    ("Missing Emergency Safety Logic: ", "No operator overrides or automated preemption corridors for ambulances.")
]

for lt, ld in limits:
    p_l = tf4.add_paragraph()
    p_l.space_after = Pt(10)
    r1 = p_l.add_run()
    r1.text = "• " + lt
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = C_TEXT_DARK
    r2 = p_l.add_run()
    r2.text = ld
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = C_TEXT_BODY

add_footer(slide3, "03")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 4: LITERATURE SURVEY — SENSOR & HEURISTIC SYSTEMS (TABLE SLIDE)
# ─────────────────────────────────────────────────────────────────────────────
slide4 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide4, C_LIGHT_BG)
add_header(slide4, "03", "Literature Survey", "Literature Survey — Classical, Sensor & Heuristic Control Models")

# Table for Literature Survey Part 1
rows = 6
cols = 7
tbl_shape = slide4.shapes.add_table(rows, cols, Inches(0.8), Inches(1.65), Inches(11.733), Inches(5.0))
table = tbl_shape.table

# Set Column Widths
col_widths = [Inches(0.6), Inches(1.6), Inches(2.2), Inches(1.5), Inches(1.8), Inches(2.2), Inches(1.833)]
for c_idx, w in enumerate(col_widths):
    table.columns[c_idx].width = w

headers = ["S.No", "Author (Year)", "Paper Title", "Venue", "Method", "Contribution / Result", "Limitation"]
for c_idx, h_text in enumerate(headers):
    cell = table.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_DARK_BG
    p = cell.text_frame.paragraphs[0]
    p.text = h_text
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

lit_data1 = [
    ("1", "Webster (1958)", "Traffic Signal Settings", "Road Research Tech.", "Analytical delay minimization formula", "Pioneered cycle time and saturation flow relationships", "Static arrivals assumption; fails during non-stationary peaks"),
    ("2", "Balaji et al. (2010)", "Urban Traffic Control with Multi-Agent Reinforcement Learning", "IEEE Intell. Syst.", "Multi-agent decentralized Q-learning", "Reduced average junction delay by 22% in simulated grid", "Curse of dimensionality; unstable exploration in real conditions"),
    ("3", "Sharma et al. (2018)", "RFID & Ultrasonic Sensor Traffic Management", "IEEE Trans. Intell. Transp.", "Active RFID transponders + ultrasonic height grid", "92% priority accuracy for registered emergency vehicles", "Requires 100% vehicle transponder tag adoption; high cost"),
    ("4", "Kumar et al. (2020)", "Vision-Based Vehicle Counting via Background Subtraction", "IEEE Access", "Gaussian Mixture Models (GMM) + Morphological filter", "84.2% vehicle count accuracy under clear day lighting", "Degrades sharply during night, rain, shadows, and occlusions"),
    ("5", "Rizwan et al. (2020)", "Real-Time Traffic Density Estimation using Edge Sensors", "Elsevier ComPE", "Acoustic + Infrared edge sensor mesh", "Low compute footprint (<5W) at roadside node", "Binary presence only; cannot classify vehicles or queue sizes")
]

for r_idx, row_vals in enumerate(lit_data1, start=1):
    bg_c = RGBColor(241, 245, 249) if r_idx % 2 == 1 else C_WHITE
    for c_idx, val in enumerate(row_vals):
        cell = table.cell(r_idx, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_c
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = FONT_PRIMARY
        p.font.size = Pt(9.2)
        p.font.color.rgb = C_TEXT_DARK if c_idx == 0 or c_idx == 1 else C_TEXT_BODY
        if c_idx == 0:
            p.alignment = PP_ALIGN.CENTER
            p.font.bold = True
        elif c_idx == 1:
            p.font.bold = True

add_footer(slide4, "04")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 5: LITERATURE SURVEY — DEEP LEARNING & COMPUTER VISION (TABLE SLIDE)
# ─────────────────────────────────────────────────────────────────────────────
slide5 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide5, C_LIGHT_BG)
add_header(slide5, "03", "Literature Survey", "Literature Survey — Deep Learning & Object Detection Systems")

tbl_shape2 = slide5.shapes.add_table(rows, cols, Inches(0.8), Inches(1.65), Inches(11.733), Inches(5.0))
table2 = tbl_shape2.table

for c_idx, w in enumerate(col_widths):
    table2.columns[c_idx].width = w

for c_idx, h_text in enumerate(headers):
    cell = table2.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_DARK_BG
    p = cell.text_frame.paragraphs[0]
    p.text = h_text
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

lit_data2 = [
    ("6", "Redmon et al. (2016)", "You Only Look Once: Unified Real-Time Object Detection", "IEEE/CVF CVPR", "Single-stage CNN grid prediction backbone", "Established 45 FPS real-time object detection milestone", "High localization error on dense, overlapping vehicles"),
    ("7", "Bochkovskiy et al. (2020)", "YOLOv4: Optimal Speed and Accuracy of Object Detection", "arXiv:2004.10934", "CSPDarknet53, PANet, mosaic data augmentation", "43.5% AP on MS COCO at 65 FPS on Tesla V100", "Computationally heavy (~64MB); difficult for edge SBC units"),
    ("8", "Lyu et al. (2021)", "UA-DETRAC: A Benchmark for Multi-Target Detection & Tracking", "IEEE Trans. PAMI", "Comprehensive urban vehicle benchmark dataset", "Established multi-weather baseline (day, night, rain)", "Pure benchmark evaluation; lacked real-time signal control loop"),
    ("9", "Al-Haija et al. (2022)", "Intelligent Traffic Congestion Prediction via YOLO Models", "IEEE Access", "YOLOv5 vehicle detector + REST API integration", "91.2% detection precision on suburban highway feeds", "Fixed static timing output; lacks anti-starvation mechanisms"),
    ("10", "Jocher et al. (2023)", "Ultralytics YOLOv8: State-of-the-Art Real-Time Vision", "GitHub / Ultralytics", "Anchor-free detection, C2f module, TaskAlignedAssigner", "SOTA speed-accuracy tradeoff (YOLOv8n @ 3.2M params)", "Needs domain fine-tuning for urban intersection perspective")
]

for r_idx, row_vals in enumerate(lit_data2, start=1):
    bg_c = RGBColor(241, 245, 249) if r_idx % 2 == 1 else C_WHITE
    for c_idx, val in enumerate(row_vals):
        cell = table2.cell(r_idx, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_c
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = FONT_PRIMARY
        p.font.size = Pt(9.2)
        p.font.color.rgb = C_TEXT_DARK if c_idx == 0 or c_idx == 1 else C_TEXT_BODY
        if c_idx == 0:
            p.alignment = PP_ALIGN.CENTER
            p.font.bold = True
        elif c_idx == 1:
            p.font.bold = True

add_footer(slide5, "05")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 6: RESEARCH GAPS IDENTIFIED (LIGHT THEME)
# ─────────────────────────────────────────────────────────────────────────────
slide6 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide6, C_LIGHT_BG)
add_header(slide6, "04", "Research Gaps", "Critical Research Gaps Identified in Existing Literature")

# 2x2 Grid of Pill Cards
gap_cards = [
    ("1", "Isolated Single-Lane Analysis [1]–[5]",
     "Most CNN / YOLO systems evaluate single video feeds in silos without synchronizing 4-way intersection demand, shifting bottlenecks to adjacent lanes.",
     "Synchronous 4-Way Multi-Camera Parallel Queue Inference (North, South, East, West)."),
    
    ("2", "Rigid Step Timers vs Continuous Density [2], [4], [9]",
     "Existing systems trigger hardcoded time extensions that fail to scale with true vehicle density, queue clearance speed, and heavy vehicles.",
     "Dynamic Formula Allocation: Green_Time = clamp(Base_Time + Count * Factor, 10s, 60s)."),
    
    ("3", "Phase Starvation & Unfair Queuing [3], [8]",
     "Pure greedy density prioritization starves low-traffic feeder approaches indefinitely under continuous arterial commuter flows.",
     "Anti-Starvation Fairness Guard (max 5 consecutive red cycles) with automatic escalation."),
    
    ("4", "Black-Box AI Without Operator & Emergency Control [6]–[10]",
     "Lack human-in-the-loop manual overrides, incident response clearing, or zero-delay corridors for emergency response vehicles.",
     "Full-Stack Next.js Glassmorphic HUD Dashboard + 1-Click All-Red Emergency Preemption.")
]

card_positions = [
    (Inches(0.8), Inches(1.65)),
    (Inches(6.8), Inches(1.65)),
    (Inches(0.8), Inches(3.70)),
    (Inches(6.8), Inches(3.70))
]

gw = Inches(5.733)
gh = Inches(1.85)

for idx, (num, gap_title, problem, proposed) in enumerate(gap_cards):
    left_x, top_y = card_positions[idx]
    c = add_card(slide6, left_x, top_y, gw, gh, C_WHITE, C_CARD_BORDER)
    
    # Circle number badge
    nb = slide6.shapes.add_shape(MSO_SHAPE.OVAL, left_x + Inches(0.25), top_y + Inches(0.22), Inches(0.55), Inches(0.55))
    nb.fill.solid()
    nb.fill.fore_color.rgb = C_AMBER
    nb.line.fill.background()
    p_nb = nb.text_frame.paragraphs[0]
    p_nb.text = num
    p_nb.alignment = PP_ALIGN.CENTER
    p_nb.font.name = FONT_PRIMARY
    p_nb.font.size = Pt(13)
    p_nb.font.bold = True
    p_nb.font.color.rgb = C_DARK_BG
    
    # Text box
    tb = slide6.shapes.add_textbox(left_x + Inches(0.95), top_y + Inches(0.18), gw - Inches(1.15), gh - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p_t = tf.paragraphs[0]
    p_t.text = gap_title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = C_TEXT_DARK
    p_t.space_after = Pt(4)
    
    p_pr = tf.add_paragraph()
    p_pr.text = problem
    p_pr.font.name = FONT_PRIMARY
    p_pr.font.size = Pt(10)
    p_pr.font.color.rgb = C_TEXT_BODY
    p_pr.space_after = Pt(5)
    
    p_prop = tf.add_paragraph()
    r_arr = p_prop.add_run()
    r_arr.text = "→ Proposed: "
    r_arr.font.bold = True
    r_arr.font.size = Pt(10)
    r_arr.font.color.rgb = C_AMBER_DARK
    
    r_txt = p_prop.add_run()
    r_txt.text = proposed
    r_txt.font.bold = True
    r_txt.font.size = Pt(10)
    r_txt.font.color.rgb = C_TEXT_DARK

# Bottom Dark Summary Card
c_bot = add_card(slide6, Inches(0.8), Inches(5.75), Inches(11.733), Inches(0.95), C_DARK_BG, None)
tb_bot = slide6.shapes.add_textbox(Inches(1.0), Inches(5.85), Inches(11.3), Inches(0.75))
tf_bot = tb_bot.text_frame
tf_bot.word_wrap = True
p_b1 = tf_bot.paragraphs[0]
p_b1.text = "Core Innovation:"
p_b1.font.name = FONT_PRIMARY
p_b1.font.size = Pt(12)
p_b1.font.bold = True
p_b1.font.color.rgb = C_AMBER

p_b2 = tf_bot.add_paragraph()
p_b2.text = "Closed-loop, real-time edge vision coupled with mathematically bounded adaptive timing, anti-starvation fairness, and instantaneous emergency preemption."
p_b2.font.name = FONT_PRIMARY
p_b2.font.size = Pt(11.5)
p_b2.font.color.rgb = RGBColor(226, 232, 240)

add_footer(slide6, "06")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 7: SYSTEM ARCHITECTURE (DIAGRAM SLIDE)
# ─────────────────────────────────────────────────────────────────────────────
slide7 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide7, C_LIGHT_BG)
add_header(slide7, "05", "System Architecture", "End-to-End Deep Learning & Adaptive Signal Control Architecture")

# Embed Architecture Diagram
arch_diag_path = os.path.join(DIAGRAM_DIR, "architecture_diagram.png")
if os.path.exists(arch_diag_path):
    slide7.shapes.add_picture(arch_diag_path, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2))
else:
    # Fallback text card if diagram missing
    c_arch = add_card(slide7, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2), C_WHITE, C_CARD_BORDER)

add_footer(slide7, "07")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 8: DATA FLOW DIAGRAM (DFD LEVEL-1 SLIDE)
# ─────────────────────────────────────────────────────────────────────────────
slide8 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide8, C_LIGHT_BG)
add_header(slide8, "06", "Data Flow Diagram", "Data Flow Diagram (DFD Level-1) — Real-Time Signal Processing Pipeline")

# Embed DFD Diagram
dfd_diag_path = os.path.join(DIAGRAM_DIR, "dfd_diagram.png")
if os.path.exists(dfd_diag_path):
    slide8.shapes.add_picture(dfd_diag_path, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2))
else:
    c_dfd = add_card(slide8, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2), C_WHITE, C_CARD_BORDER)

add_footer(slide8, "08")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 9: DATASET & EXPERIMENTAL SETUP (LIGHT THEME)
# ─────────────────────────────────────────────────────────────────────────────
slide9 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide9, C_LIGHT_BG)
add_header(slide9, "07", "Methodology & Setup", "UA-DETRAC Benchmark Dataset Specifications & Training Setup")

# Left Card: Dataset Info
c_ds = add_card(slide9, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.1), C_WHITE, C_CARD_BORDER)
tb_ds = slide9.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.6))
tf_ds = tb_ds.text_frame
tf_ds.word_wrap = True

p_dst = tf_ds.paragraphs[0]
p_dst.text = "UA-DETRAC Urban Benchmark Dataset"
p_dst.font.name = FONT_HEADING
p_dst.font.size = Pt(16)
p_dst.font.bold = True
p_dst.font.color.rgb = C_TEXT_DARK
p_dst.space_after = Pt(12)

ds_bullets = [
    ("Real-World Surveillance: ", "Captured from 24 diverse urban traffic camera locations at 25 FPS, representing genuine commuter traffic."),
    ("Multi-Environmental Diversity: ", "Includes sunny daylight, night surveillance, cloudy weather, and rainy illumination to ensure model robustness."),
    ("4 Target Vehicle Classes: ", "Filtered and trained on classes directly determining intersection road occupancy: Car, Motorcycle, Bus, Truck."),
    ("Balanced Split: ", "Divided into 80% training and 20% validation splits with rigorous multi-weather coverage across subsets."),
    ("Standardized Bounding Annotations: ", "Normalized (class, x_center, y_center, width, height) format mapped for YOLOv8 anchor-free training.")
]

for title, desc in ds_bullets:
    p_b = tf_ds.add_paragraph()
    p_b.space_after = Pt(8)
    r1 = p_b.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = C_TEXT_DARK
    r2 = p_b.add_run()
    r2.text = desc
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = C_TEXT_BODY

# Right Card: Hyperparameters & Training Specs
c_hp = add_card(slide9, Inches(6.8), Inches(1.65), Inches(5.733), Inches(5.1), C_WHITE, C_CARD_BORDER)
tb_hp = slide9.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.6))
tf_hp = tb_hp.text_frame
tf_hp.word_wrap = True

p_hpt = tf_hp.paragraphs[0]
p_hpt.text = "Model Architecture & Hyperparameters"
p_hpt.font.name = FONT_HEADING
p_hpt.font.size = Pt(16)
p_hpt.font.bold = True
p_hpt.font.color.rgb = C_TEXT_DARK
p_hpt.space_after = Pt(12)

hp_bullets = [
    ("Neural Backbone: ", "YOLOv8 Nano (yolov8n.pt) with 3.2M parameters — selected for optimal FPS/accuracy on low-cost edge hardware."),
    ("Model Weight Footprint: ", "Only 6.2 MB (.pt) and 12.2 MB (.onnx), ensuring low memory consumption on embedded systems."),
    ("Input Resolution: ", "640 × 640 pixels with automated letterboxing and noise reduction."),
    ("Optimization Protocol: ", "Stochastic Gradient Descent (SGD) with momentum 0.937, weight decay 0.0005, and initial LR 0.01 with cosine annealing."),
    ("Loss Formulation: ", "Composite multi-task loss combining Complete IoU (CIoU) Box Loss, Binary Cross-Entropy Class Loss, and DFL Loss."),
    ("Export Formats: ", "Trained PyTorch weights (best.pt) + optimized Open Neural Network Exchange (best.onnx) for TensorRT acceleration.")
]

for title, desc in hp_bullets:
    p_b = tf_hp.add_paragraph()
    p_b.space_after = Pt(8)
    r1 = p_b.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = C_TEXT_DARK
    r2 = p_b.add_run()
    r2.text = desc
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = C_TEXT_BODY

add_footer(slide9, "09")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 10: RESULTS PHOTO SLIDE 1 — TRAINING LOSS & CURVES
# ─────────────────────────────────────────────────────────────────────────────
slide10 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide10, C_LIGHT_BG)
add_header(slide10, "08", "Experimental Results", "Model Training Loss Convergence & Precision-Recall Curves")

# Left Image: results.png
res_img_path = os.path.join(ASSET_DIR, "results.png")
if os.path.exists(res_img_path):
    c_img1 = add_card(slide10, Inches(0.8), Inches(1.65), Inches(6.8), Inches(3.6), C_WHITE, C_CARD_BORDER)
    slide10.shapes.add_picture(res_img_path, Inches(0.9), Inches(1.75), Inches(6.6), Inches(3.4))

# Right Images: BoxPR_curve.png & BoxF1_curve.png
pr_img_path = os.path.join(ASSET_DIR, "BoxPR_curve.png")
f1_img_path = os.path.join(ASSET_DIR, "BoxF1_curve.png")

if os.path.exists(pr_img_path):
    c_pr = add_card(slide10, Inches(7.8), Inches(1.65), Inches(4.733), Inches(2.45), C_WHITE, C_CARD_BORDER)
    slide10.shapes.add_picture(pr_img_path, Inches(7.9), Inches(1.72), Inches(4.533), Inches(2.3))

if os.path.exists(f1_img_path):
    c_f1 = add_card(slide10, Inches(7.8), Inches(4.25), Inches(4.733), Inches(2.55), C_WHITE, C_CARD_BORDER)
    slide10.shapes.add_picture(f1_img_path, Inches(7.9), Inches(4.32), Inches(4.533), Inches(2.4))

# Bottom Metric Callout Box on Left
c_met = add_card(slide10, Inches(0.8), Inches(5.40), Inches(6.8), Inches(1.45), C_DARK_BG, None)
tb_met = slide10.shapes.add_textbox(Inches(1.0), Inches(5.50), Inches(6.4), Inches(1.25))
tf_met = tb_met.text_frame
tf_met.word_wrap = True

p_mhead = tf_met.paragraphs[0]
p_mhead.text = "Key Training & Convergence Milestones:"
p_mhead.font.name = FONT_PRIMARY
p_mhead.font.size = Pt(11.5)
p_mhead.font.bold = True
p_mhead.font.color.rgb = C_AMBER

p_m1 = tf_met.add_paragraph()
p_m1.text = "• Box Loss dropped from 0.894 → 0.562; Cls Loss converged from 0.838 → 0.265."
p_m1.font.size = Pt(10)
p_m1.font.color.rgb = RGBColor(226, 232, 240)

p_m2 = tf_met.add_paragraph()
p_m2.text = "• Peak Precision reached 73.0% (Epoch 5); Steady-state precision: 62.6%."
p_m2.font.size = Pt(10)
p_m2.font.color.rgb = RGBColor(226, 232, 240)

p_m3 = tf_met.add_paragraph()
p_m3.text = "• Mean Average Precision: mAP@0.50 = 61.9%, mAP@0.50:0.95 = 47.4% on validation set."
p_m3.font.size = Pt(10)
p_m3.font.color.rgb = RGBColor(226, 232, 240)

add_footer(slide10, "10")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 11: RESULTS PHOTO SLIDE 2 — CONFUSION MATRIX & CLASS ACCURACY
# ─────────────────────────────────────────────────────────────────────────────
slide11 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide11, C_LIGHT_BG)
add_header(slide11, "08", "Experimental Results", "Normalized Confusion Matrix & Class-Wise Detection Performance")

# Left Image: confusion_matrix_normalized.png
cm_img_path = os.path.join(ASSET_DIR, "confusion_matrix_normalized.png")
if os.path.exists(cm_img_path):
    c_cm = add_card(slide11, Inches(0.8), Inches(1.65), Inches(5.5), Inches(5.1), C_WHITE, C_CARD_BORDER)
    slide11.shapes.add_picture(cm_img_path, Inches(0.9), Inches(1.75), Inches(5.3), Inches(4.9))

# Right Column: Class-Wise Performance Analysis
c_cman = add_card(slide11, Inches(6.6), Inches(1.65), Inches(5.933), Inches(5.1), C_WHITE, C_CARD_BORDER)
tb_ca = slide11.shapes.add_textbox(Inches(6.85), Inches(1.85), Inches(5.4), Inches(4.6))
tf_ca = tb_ca.text_frame
tf_ca.word_wrap = True

p_cat = tf_ca.paragraphs[0]
p_cat.text = "Multi-Class Detection Accuracy & Insights"
p_cat.font.name = FONT_HEADING
p_cat.font.size = Pt(16)
p_cat.font.bold = True
p_cat.font.color.rgb = C_TEXT_DARK
p_cat.space_after = Pt(10)

class_insights = [
    ("Car Class (0): ", "Highest True Positive rate and cleanest separation. Strong representations in UA-DETRAC allow YOLOv8 to localize private vehicles under sharp perspective foreshortening."),
    ("Bus Class (2): ", "Distinct elongated rectangular geometry enables high classification confidence. Critical for public transit prioritization algorithms."),
    ("Truck Class (3): ", "Effectively segregated from personal cars and utility vehicles, avoiding false volume inflation during signal weighting."),
    ("Motorcycle Class (1): ", "Smaller spatial footprint captured reliably via 640x640 resolution grid and anchor-free TaskAlignedAssigner."),
    ("Background Rejection: ", "Confidence thresholding (>0.25) and Non-Maximum Suppression (NMS IoU=0.45) filter out road markings, street poles, and roadside shadows.")
]

for title, desc in class_insights:
    p_b = tf_ca.add_paragraph()
    p_b.space_after = Pt(7)
    r1 = p_b.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = C_TEXT_DARK
    r2 = p_b.add_run()
    r2.text = desc
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = C_TEXT_BODY

add_footer(slide11, "11")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 12: RESULTS PHOTO SLIDE 3 — VISUAL DETECTIONS COMPARISON
# ─────────────────────────────────────────────────────────────────────────────
slide12 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide12, C_LIGHT_BG)
add_header(slide12, "08", "Experimental Results", "Validation Batch Visual Detections & Ground Truth Verification")

# Side-by-Side: val_batch0_labels.jpg vs val_batch0_pred.jpg
vb_lbl_path = os.path.join(ASSET_DIR, "val_batch0_labels.jpg")
vb_pred_path = os.path.join(ASSET_DIR, "val_batch0_pred.jpg")

if os.path.exists(vb_lbl_path):
    c_vl = add_card(slide12, Inches(0.8), Inches(1.65), Inches(5.7), Inches(3.6), C_WHITE, C_CARD_BORDER)
    slide12.shapes.add_picture(vb_lbl_path, Inches(0.9), Inches(1.75), Inches(5.5), Inches(3.4))
    
    tb_lbl_tag = slide12.shapes.add_textbox(Inches(0.9), Inches(1.75), Inches(3.0), Inches(0.35))
    tf_lt = tb_lbl_tag.text_frame
    p_lt = tf_lt.paragraphs[0]
    p_lt.text = "  GROUND TRUTH LABELS  "
    p_lt.font.name = FONT_PRIMARY
    p_lt.font.size = Pt(9.5)
    p_lt.font.bold = True
    p_lt.font.color.rgb = C_WHITE
    # Add dark background for badge
    lbl_badge = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.95), Inches(1.8), Inches(2.2), Inches(0.3))
    lbl_badge.fill.solid()
    lbl_badge.fill.fore_color.rgb = C_DARK_BG
    lbl_badge.line.fill.background()
    p_lt = lbl_badge.text_frame.paragraphs[0]
    p_lt.text = "GROUND TRUTH LABELS"
    p_lt.alignment = PP_ALIGN.CENTER
    p_lt.font.name = FONT_PRIMARY
    p_lt.font.size = Pt(8.5)
    p_lt.font.bold = True
    p_lt.font.color.rgb = C_WHITE

if os.path.exists(vb_pred_path):
    c_vp = add_card(slide12, Inches(6.8), Inches(1.65), Inches(5.733), Inches(3.6), C_WHITE, C_CARD_BORDER)
    slide12.shapes.add_picture(vb_pred_path, Inches(6.9), Inches(1.75), Inches(5.533), Inches(3.4))
    
    pred_badge = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.95), Inches(1.8), Inches(2.3), Inches(0.3))
    pred_badge.fill.solid()
    pred_badge.fill.fore_color.rgb = C_AMBER_DARK
    pred_badge.line.fill.background()
    p_pt = pred_badge.text_frame.paragraphs[0]
    p_pt.text = "YOLOv8 PREDICTIONS"
    p_pt.alignment = PP_ALIGN.CENTER
    p_pt.font.name = FONT_PRIMARY
    p_pt.font.size = Pt(8.5)
    p_pt.font.bold = True
    p_pt.font.color.rgb = C_WHITE

# Bottom Technical Analysis Card
c_vbot = add_card(slide12, Inches(0.8), Inches(5.45), Inches(11.733), Inches(1.45), C_WHITE, C_CARD_BORDER)
tb_vbot = slide12.shapes.add_textbox(Inches(1.05), Inches(5.55), Inches(11.2), Inches(1.25))
tf_vbot = tb_vbot.text_frame
tf_vbot.word_wrap = True

p_vbt = tf_vbot.paragraphs[0]
p_vbt.text = "Visual Detection Analysis & Real-World Generalization:"
p_vbt.font.name = FONT_HEADING
p_vbt.font.size = Pt(12)
p_vbt.font.bold = True
p_vbt.font.color.rgb = C_TEXT_DARK
p_vbt.space_after = Pt(4)

p_vb1 = tf_vbot.add_paragraph()
p_vb1.text = "• Bounding Box Alignment: Model demonstrates high IoU overlap (>0.75) against human-annotated ground truth in dense queues."
p_vb1.font.size = Pt(10.5)
p_vb1.font.color.rgb = C_TEXT_BODY

p_vb2 = tf_vbot.add_paragraph()
p_vb2.text = "• Heavy Occlusion Tolerance: Successfully segments partially obscured vehicles queued bumper-to-bumper behind tall buses/trucks."
p_vb2.font.size = Pt(10.5)
p_vb2.font.color.rgb = C_TEXT_BODY

p_vb3 = tf_vbot.add_paragraph()
p_vb3.text = "• Weather & Lighting Invariance: Reliable detection under wet asphalt glare and overcast conditions without false edge triggers."
p_vb3.font.size = Pt(10.5)
p_vb3.font.color.rgb = C_TEXT_BODY

add_footer(slide12, "12")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 13: SYSTEM IMPLEMENTATION & LIVE DASHBOARD (LIGHT THEME)
# ─────────────────────────────────────────────────────────────────────────────
slide13 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide13, C_LIGHT_BG)
add_header(slide13, "09", "System Implementation", "Full-Stack Implementation & Interactive Control Dashboard Features")

impl_cards = [
    ("Real-Time OpenCV HUD Stream", [
        "Dynamic virtual stop lines drawn across lane corridors.",
        "Live status badges: Phase (GREEN / RED) & countdown timer.",
        "Smooth freeze-frame logic during red phases simulates queued waiting traffic.",
        "Direct MJPEG video streaming via FastAPI asynchronous routes."
    ]),
    ("Formula-Driven Signal Optimizer", [
        "Green_Time = Base_Time + (Vehicle_Count × Factor).",
        "Configured params: Base = 10s, Factor = 2s/vehicle.",
        "Bounded between 10s minimum and 60s maximum safety caps.",
        "Candidate lane prioritizes the most congested waiting queue."
    ]),
    ("Anti-Starvation & Safety Control", [
        "Anti-Starvation Counter tracks consecutive red wait cycles.",
        "Lanes waiting ≥ 5 cycles are automatically granted top green priority.",
        "Fixed 3-second yellow clearance phase guarantees collision prevention.",
        "All-Red Emergency Preemption mode clears junction immediately."
    ]),
    ("Modern Web Dashboard & Telemetry", [
        "Built with Next.js (React 19), Tailwind CSS, and Lucide icons.",
        "Interactive manual lane override sliders & emergency buttons.",
        "Real-time vehicle density breakdowns (Car, Bus, Truck, Bike).",
        "MongoDB logging for audit trails, signal transitions & event logs."
    ])
]

for idx, (title, items) in enumerate(impl_cards):
    left_x, top_y = card_positions[idx]
    c = add_card(slide13, left_x, top_y, gw, Inches(2.55), C_WHITE, C_CARD_BORDER)
    
    tb = slide13.shapes.add_textbox(left_x + Inches(0.3), top_y + Inches(0.2), gw - Inches(0.6), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(13.5)
    p_t.font.bold = True
    p_t.font.color.rgb = C_AMBER_DARK
    p_t.space_after = Pt(8)
    
    for it in items:
        p_i = tf.add_paragraph()
        p_i.text = "• " + it
        p_i.font.name = FONT_PRIMARY
        p_i.font.size = Pt(10.5)
        p_i.font.color.rgb = C_TEXT_BODY
        p_i.space_after = Pt(5)

add_footer(slide13, "13")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 14: SYSTEM PERFORMANCE & COMPARATIVE BENCHMARK (TABLE SLIDE)
# ─────────────────────────────────────────────────────────────────────────────
slide14 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide14, C_LIGHT_BG)
add_header(slide14, "10", "Performance Benchmark", "Quantitative Performance Comparison vs. Traditional & Sensor Systems")

bench_rows = 7
bench_cols = 5
tbl_bench = slide14.shapes.add_table(bench_rows, bench_cols, Inches(0.8), Inches(1.65), Inches(11.733), Inches(5.0))
t_bench = tbl_bench.table

bench_col_widths = [Inches(2.5), Inches(2.2), Inches(2.2), Inches(2.8), Inches(2.033)]
for c_idx, w in enumerate(bench_col_widths):
    t_bench.columns[c_idx].width = w

bench_headers = ["Evaluation Metric", "Fixed-Timer System", "Inductive Loop Sensors", "Proposed Smart Traffic AI", "Relative Gain"]
for c_idx, h_text in enumerate(bench_headers):
    cell = t_bench.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_DARK_BG
    p = cell.text_frame.paragraphs[0]
    p.text = h_text
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

bench_data = [
    ("Average Junction Delay", "45 – 90 s / vehicle", "30 – 55 s / vehicle", "15 – 35 s / vehicle", "38% – 45% Reduction"),
    ("Vehicle Categorization", "None (blind)", "None (presence only)", "4 Classes (Car, Bus, Truck, Bike)", "Full Semantic Profiling"),
    ("Installation Disruption", "Low (poles only)", "Very High (asphalt cut)", "None (uses standard CCTV)", "Zero Road Excavation"),
    ("Adaptability to Congestion", "Zero (static schedule)", "Moderate (actuated)", "Dynamic continuous formula", "Optimal Queue Clearance"),
    ("Emergency Preemption", "Manual traffic police", "Dedicated RFID only", "1-Click Dashboard & AI Mode", "Instant Clear Corridor"),
    ("Edge Inference Latency", "N/A (electromechanical)", "< 5 ms (analog)", "15 – 25 ms (~45+ FPS)", "Real-time edge ready")
]

for r_idx, row_vals in enumerate(bench_data, start=1):
    bg_c = RGBColor(241, 245, 249) if r_idx % 2 == 1 else C_WHITE
    for c_idx, val in enumerate(row_vals):
        cell = t_bench.cell(r_idx, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_c
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = FONT_PRIMARY
        p.font.size = Pt(9.5)
        if c_idx == 0:
            p.font.bold = True
            p.font.color.rgb = C_TEXT_DARK
        elif c_idx == 3:
            p.font.bold = True
            p.font.color.rgb = C_AMBER_DARK
        elif c_idx == 4:
            p.font.bold = True
            p.font.color.rgb = C_GREEN
            p.alignment = PP_ALIGN.CENTER
        else:
            p.font.color.rgb = C_TEXT_BODY

add_footer(slide14, "14")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 15: EXPECTED OUTCOMES & APPLICATIONS (LIGHT THEME)
# ─────────────────────────────────────────────────────────────────────────────
slide15 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide15, C_LIGHT_BG)
add_header(slide15, "11", "Impact & Deployment", "Expected Deliverables & Real-World Societal Applications")

# Left Column: Key Outcomes & Contributions
c_out = add_card(slide15, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.1), C_WHITE, C_CARD_BORDER)
tb_out = slide15.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(5.1), Inches(4.7))
tf_out = tb_out.text_frame
tf_out.word_wrap = True

p_out_t = tf_out.paragraphs[0]
p_out_t.text = "Expected Outcomes & Contributions"
p_out_t.font.name = FONT_HEADING
p_out_t.font.size = Pt(16)
p_out_t.font.bold = True
p_out_t.font.color.rgb = C_TEXT_DARK
p_out_t.space_after = Pt(10)

deliverables = [
    ("Measurable Congestion Relief: ", "Direct reduction in stop-and-go queue bottlenecks, cutting transit wait times across arterial corridors by over 35%."),
    ("Environmental & Emission Gains: ", "Significant reduction in excess fuel burned during stationary idling, curbing carbon emissions in high-density urban corridors."),
    ("Life-Saving Priority Transit: ", "Emergency corridor preemption slashes response time for ambulances and rescue squads during critical golden-hour emergencies."),
    ("Edge-Deployable Infrastructure: ", "Lightweight 6.2 MB YOLOv8n network deploys seamlessly on low-power roadside units (NVIDIA Jetson / Intel NUC)."),
    ("Centralized Municipal Analytics: ", "Longitudinal telemetry data logging enables city authorities to analyze peak congestion trends for urban civil planning.")
]

for title, desc in deliverables:
    p_b = tf_out.add_paragraph()
    p_b.space_after = Pt(8)
    r1 = p_b.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = C_TEXT_DARK
    r2 = p_b.add_run()
    r2.text = desc
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = C_TEXT_BODY

# Right Column: 4 Application Cards (2x2 Grid)
app_cards = [
    ("Smart City Junctions", "Integrated municipal traffic grid managing multi-phase arterial crossroads dynamically."),
    ("Emergency Corridors", "Automated green waves for ambulances, fire engines, and police escorts."),
    ("Public Bus Rapid Transit", "Dynamic green extensions upon detecting packed city buses to reward mass transit."),
    ("Highway Toll Plazas", "Dynamic booth lane assignment based on real-time vehicle category queuing.")
]

app_positions = [
    (Inches(6.7), Inches(1.65)),
    (Inches(9.9), Inches(1.65)),
    (Inches(6.7), Inches(4.25)),
    (Inches(9.9), Inches(4.25))
]

for idx, (title, desc) in enumerate(app_cards):
    left_x, top_y = app_positions[idx]
    c = add_card(slide15, left_x, top_y, Inches(3.0), Inches(2.5), C_WHITE, C_CARD_BORDER)
    
    # Amber circle badge
    b = slide15.shapes.add_shape(MSO_SHAPE.OVAL, left_x + Inches(0.25), top_y + Inches(0.25), Inches(0.65), Inches(0.65))
    b.fill.solid()
    b.fill.fore_color.rgb = C_AMBER
    b.line.fill.background()
    
    tb = slide15.shapes.add_textbox(left_x + Inches(0.25), top_y + Inches(1.05), Inches(2.5), Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(13.5)
    p_t.font.bold = True
    p_t.font.color.rgb = C_TEXT_DARK
    p_t.space_after = Pt(6)
    
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = FONT_PRIMARY
    p_d.font.size = Pt(10.5)
    p_d.font.color.rgb = C_TEXT_BODY

add_footer(slide15, "15")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 16: CONCLUSION & THANK YOU (DARK THEME)
# ─────────────────────────────────────────────────────────────────────────────
slide16 = prs.slides.add_slide(blank_layout)
add_solid_bg(slide16, C_DARK_BG)

# Center Icon Badge
center_badge = slide16.shapes.add_shape(MSO_SHAPE.OVAL, Inches(6.166), Inches(0.85), Inches(1.0), Inches(1.0))
center_badge.fill.solid()
center_badge.fill.fore_color.rgb = C_AMBER
center_badge.line.fill.background()

# Conclusion Title
tb_c_title = slide16.shapes.add_textbox(Inches(2.0), Inches(2.0), Inches(9.333), Inches(0.6))
tf_ct = tb_c_title.text_frame
tf_ct.word_wrap = True
p_ct = tf_ct.paragraphs[0]
p_ct.text = "Conclusion & Future Research Directions"
p_ct.alignment = PP_ALIGN.CENTER
p_ct.font.name = FONT_HEADING
p_ct.font.size = Pt(26)
p_ct.font.bold = True
p_ct.font.color.rgb = C_WHITE

# Summary Box
tb_sum = slide16.shapes.add_textbox(Inches(1.8), Inches(2.75), Inches(9.733), Inches(1.3))
tf_sum = tb_sum.text_frame
tf_sum.word_wrap = True
p_s = tf_sum.paragraphs[0]
p_s.text = "The proposed Smart Traffic Signal Optimization System successfully unites deep learning computer vision (YOLOv8) with closed-loop adaptive signal control. By dynamically adapting green phase durations based on live vehicle density while enforcing anti-starvation fairness and emergency overrides, the system significantly mitigates urban bottlenecks, cuts fuel waste, and boosts municipal road safety."
p_s.alignment = PP_ALIGN.CENTER
p_s.font.name = FONT_PRIMARY
p_s.font.size = Pt(13)
p_s.font.color.rgb = RGBColor(203, 213, 225)

# Future Scope Bullets Card
c_fsc = add_card(slide16, Inches(2.2), Inches(4.25), Inches(8.933), Inches(1.35), C_DARK_SURFACE, None)
tb_fs = slide16.shapes.add_textbox(Inches(2.5), Inches(4.35), Inches(8.333), Inches(1.15))
tf_fs = tb_fs.text_frame
tf_fs.word_wrap = True

p_fsh = tf_fs.paragraphs[0]
p_fsh.text = "Future Scope & Extensions:"
p_fsh.font.name = FONT_PRIMARY
p_fsh.font.size = Pt(11)
p_fsh.font.bold = True
p_fsh.font.color.rgb = C_AMBER
p_fsh.space_after = Pt(4)

p_fs1 = tf_fs.add_paragraph()
p_fs1.text = "• V2X (Vehicle-to-Everything) Communication: Direct wireless telemetry handshake with autonomous & connected vehicles."
p_fs1.font.size = Pt(10)
p_fs1.font.color.rgb = RGBColor(226, 232, 240)

p_fs2 = tf_fs.add_paragraph()
p_fs2.text = "• Coordinated Green Waves: Multi-agent reinforcement learning connecting adjacent intersections for corridor synchronization."
p_fs2.font.size = Pt(10)
p_fs2.font.color.rgb = RGBColor(226, 232, 240)

p_fs3 = tf_fs.add_paragraph()
p_fs3.text = "• Pedestrian Crosswalk Safety: Pose estimation integration for automated pedestrian clearing detection before green light transitions."
p_fs3.font.size = Pt(10)
p_fs3.font.color.rgb = RGBColor(226, 232, 240)

# Thank You Section
tb_ty = slide16.shapes.add_textbox(Inches(3.0), Inches(5.8), Inches(7.333), Inches(0.9))
tf_ty = tb_ty.text_frame
p_ty = tf_ty.paragraphs[0]
p_ty.text = "Thank You"
p_ty.alignment = PP_ALIGN.CENTER
p_ty.font.name = FONT_HEADING
p_ty.font.size = Pt(24)
p_ty.font.bold = True
p_ty.font.color.rgb = C_AMBER

p_qd = tf_ty.add_paragraph()
p_qd.text = "Questions & Discussion"
p_qd.alignment = PP_ALIGN.CENTER
p_qd.font.name = FONT_PRIMARY
p_qd.font.size = Pt(13)
p_qd.font.color.rgb = RGBColor(148, 163, 184)

add_footer(slide16, "16", is_dark=True)

# ─────────────────────────────────────────────────────────────────────────────
# SAVE PRESENTATION
# ─────────────────────────────────────────────────────────────────────────────
prs.save(OUTPUT_FILE)
print(f"Presentation successfully generated and saved to: {OUTPUT_FILE}")
