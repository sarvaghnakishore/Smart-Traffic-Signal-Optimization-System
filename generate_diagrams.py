import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle

os.makedirs("ppt_assets", exist_ok=True)

def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(15, 8), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    # Color Palette
    c_blue_border = '#1E3A8A'
    c_blue_bg = '#EFF6FF'
    c_green_border = '#047857'
    c_green_bg = '#ECFDF5'
    c_amber_border = '#B45309'
    c_amber_bg = '#FFFBEB'
    c_purple_border = '#6D28D9'
    c_purple_bg = '#F5F3FF'
    c_slate_border = '#334155'
    c_slate_bg = '#F1F5F9'
    c_dark = '#0F172A'

    # Title
    ax.text(0.5, 8.0, "SYSTEM ARCHITECTURE PIPELINE", fontsize=15, fontweight='bold', color='#1E293B', fontfamily='sans-serif')
    ax.text(0.5, 7.65, "End-to-End Deep Learning & Adaptive Signal Control Workflow", fontsize=10, color='#64748B', fontfamily='sans-serif')

    def draw_stage_box(x, y, w, h, stage_num, title, bg_color, border_color, items):
        # Header badge
        badge = FancyBboxPatch((x, y + h - 0.45), w, 0.45,
                               boxstyle="round,pad=0.03,rounding_size=0.1",
                               facecolor=border_color, edgecolor=border_color, lw=1)
        ax.add_patch(badge)
        ax.text(x + w/2, y + h - 0.22, f"{stage_num}. {title}", color='white',
                fontsize=9.5, fontweight='bold', ha='center', va='center', fontfamily='sans-serif')

        # Content box
        box = FancyBboxPatch((x, y), w, h - 0.45,
                             boxstyle="round,pad=0.03,rounding_size=0.1",
                             facecolor=bg_color, edgecolor=border_color, lw=1.5, ls='-')
        ax.add_patch(box)

        # Items
        line_y = y + h - 0.85
        for item in items:
            ax.text(x + 0.2, line_y, f"• {item}", fontsize=8.2, color='#1E293B', va='top', fontfamily='sans-serif')
            line_y -= 0.38

    # 1. Input Layer
    draw_stage_box(0.5, 3.8, 2.5, 3.3, "1", "Video Stream Ingestion", c_blue_bg, c_blue_border, [
        "4-Way Synchronous Feeds",
        "North, South, East, West",
        "UA-DETRAC Benchmark Data",
        "RTSP Camera Capture",
        "Dynamic Scene Jumps"
    ])

    # 2. AI Perception Pipeline
    draw_stage_box(3.3, 3.8, 3.0, 3.3, "2", "YOLOv8 Deep Perception", c_purple_bg, c_purple_border, [
        "Preprocess: 640x640 Resize",
        "Noise Red.: Gaussian Blur",
        "YOLOv8n Neural Backbone",
        "4-Class Vehicle Detector:",
        "  (Car, Bus, Truck, Bike)",
        "Batch GPU Inference (20ms)"
    ])

    # 3. Density & Queue Analysis
    draw_stage_box(6.6, 3.8, 2.7, 3.3, "3", "Lane & Density Engine", c_amber_bg, c_amber_border, [
        "LaneAnalyzer: Per-lane count",
        "Spatial Bounding Box Filter",
        "Density Classification:",
        "  - LOW (0-5 vehicles)",
        "  - MEDIUM (6-15 vehicles)",
        "  - HIGH (15+ vehicles)",
        "Congestion State Detection"
    ])

    # 4. Decision & Signal Optimizer
    draw_stage_box(9.6, 3.8, 2.8, 3.3, "4", "Signal Timing Optimizer", c_green_bg, c_green_border, [
        "Dynamic Formula Model:",
        "  T_green = T_base + N*factor",
        "Bounds: [10s min, 60s max]",
        "Starvation Guard (<= 5 cycles)",
        "Queue Fairness Balancing",
        "Emergency Priority Override"
    ])

    # 5. Actuation & Presentation
    draw_stage_box(12.7, 3.8, 2.0, 3.3, "5", "Actuation & HUD", c_slate_bg, c_slate_border, [
        "Signal Controller",
        "R/Y/G Transitions",
        "Yellow = 3s fixed",
        "OpenCV HUD Overlay",
        "Next.js Dashboard",
        "MongoDB Telemetry"
    ])

    # Connecting horizontal arrows between stages 1 -> 2 -> 3 -> 4 -> 5
    arrow_props = dict(arrowstyle="-|>", mutation_scale=15, color='#475569', lw=2)
    ax.annotate('', xy=(3.25, 5.4), xytext=(3.05, 5.4), arrowprops=arrow_props)
    ax.annotate('', xy=(6.55, 5.4), xytext=(6.35, 5.4), arrowprops=arrow_props)
    ax.annotate('', xy=(9.55, 5.4), xytext=(9.35, 5.4), arrowprops=arrow_props)
    ax.annotate('', xy=(12.65, 5.4), xytext=(12.45, 5.4), arrowprops=arrow_props)

    # Bottom Architecture Detail Banners
    # Banner 1: Safety & Starvation Controller
    b1 = FancyBboxPatch((0.5, 1.2), 6.8, 2.1, boxstyle="round,pad=0.03,rounding_size=0.1",
                        facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1.2)
    ax.add_patch(b1)
    ax.text(0.7, 2.9, "Safety & Anti-Starvation Mechanism", fontsize=9.5, fontweight='bold', color='#B45309')
    ax.text(0.7, 2.5, "• Anti-Starvation Counter: Each lane tracks consecutive waiting cycles.", fontsize=8.2, color='#334155')
    ax.text(0.7, 2.15, "• Fairness Constraint: If wait >= 5 cycles, lane receives highest priority immediately.", fontsize=8.2, color='#334155')
    ax.text(0.7, 1.8, "• All-Red Emergency Mode: Instant override clears junction for ambulances & emergency.", fontsize=8.2, color='#334155')
    ax.text(0.7, 1.45, "• Smooth Transition: 3s yellow interval guarantees safe deceleration clearance.", fontsize=8.2, color='#334155')

    # Banner 2: Telemetry & Closed-Loop Feedback
    b2 = FancyBboxPatch((7.7, 1.2), 7.0, 2.1, boxstyle="round,pad=0.03,rounding_size=0.1",
                        facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1.2)
    ax.add_patch(b2)
    ax.text(7.9, 2.9, "Closed-Loop Telemetry & Operator Supervision", fontsize=9.5, fontweight='bold', color='#1E3A8A')
    ax.text(7.9, 2.5, "• Real-Time Video HUD: Overlays lane ID, active phase, and countdown directly on frame.", fontsize=8.2, color='#334155')
    ax.text(7.9, 2.15, "• REST API & WebSockets: FastAPI streams telemetry to Next.js glassmorphic dashboard.", fontsize=8.2, color='#334155')
    ax.text(7.9, 1.8, "• Database Audit Logging: MongoDB logs every detection, phase change & timing.", fontsize=8.2, color='#334155')
    ax.text(7.9, 1.45, "• Manual Override Controls: Municipal traffic operators can force lane priority on demand.", fontsize=8.2, color='#334155')

    # Feedback arrow from Actuation back to Optimizer
    ax.annotate('', xy=(11.0, 3.75), xytext=(13.7, 3.75),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=15, color='#047857', lw=1.8))
    ax.text(12.35, 3.5, "Closed-loop feedback & cycle completion", fontsize=7.5, color='#047857', ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig("ppt_assets/architecture_diagram.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("architecture_diagram.png created successfully!")

def create_dfd_diagram():
    fig, ax = plt.subplots(figsize=(15, 8), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    # Title
    ax.text(0.5, 8.0, "DATA FLOW DIAGRAM (DFD LEVEL-1)", fontsize=15, fontweight='bold', color='#1E293B', fontfamily='sans-serif')
    ax.text(0.5, 7.65, "Process Flows, Data Stores, and External Entities in Traffic Optimization", fontsize=10, color='#64748B', fontfamily='sans-serif')

    def draw_entity(x, y, w, h, label):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                             facecolor='#1E293B', edgecolor='#0F172A', lw=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, label, color='white', fontsize=8.8, fontweight='bold',
                ha='center', va='center', fontfamily='sans-serif', multialignment='center')

    def draw_process(x, y, w, h, pid, pname, subtext):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1",
                             facecolor='#FFFFFF', edgecolor='#D97706', lw=1.8)
        ax.add_patch(box)
        ax.text(x + w/2, y + h - 0.35, pid, color='#D97706', fontsize=9.5, fontweight='bold',
                ha='center', va='center', fontfamily='sans-serif')
        ax.text(x + w/2, y + h - 0.75, pname, color='#0F172A', fontsize=9.0, fontweight='bold',
                ha='center', va='center', fontfamily='sans-serif', multialignment='center')
        ax.text(x + w/2, y + 0.45, subtext, color='#64748B', fontsize=7.5,
                ha='center', va='center', fontfamily='sans-serif', multialignment='center')

    def draw_datastore(x, y, w, h, ds_id, ds_name, subtext):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15",
                             facecolor='#F8FAFC', edgecolor='#475569', lw=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h - 0.32, ds_id, color='#1E3A8A', fontsize=8.8, fontweight='bold',
                ha='center', va='center', fontfamily='sans-serif')
        ax.text(x + w/2, y + h - 0.70, ds_name, color='#0F172A', fontsize=8.2, fontweight='bold',
                ha='center', va='center', fontfamily='sans-serif', multialignment='center')
        ax.text(x + w/2, y + 0.35, subtext, color='#64748B', fontsize=7.2,
                ha='center', va='center', fontfamily='sans-serif', multialignment='center')

    # External Entities
    draw_entity(0.4, 4.3, 1.8, 1.8, "4-Way Traffic\nCameras\n(Surveillance)")
    draw_entity(12.8, 4.3, 1.8, 1.8, "Traffic Operators\n& Emergency\nUnits")

    # Processes P1 to P4
    draw_process(2.7, 4.2, 2.1, 2.0, "P1", "Preprocessing", "16-frame buffer\n640x640 normalize\nGaussian filter")
    draw_process(5.3, 4.2, 2.1, 2.0, "P2", "Vehicle Detection", "YOLOv8n detector\n4 vehicle classes\nconf > 0.25, NMS")
    draw_process(7.9, 4.2, 2.1, 2.0, "P3", "Density & Queue", "Lane vehicle counts\nLow/Med/High states\nStarvation tracker")
    draw_process(10.3, 4.2, 2.1, 2.0, "P4", "Signal Optimization", "T_green = T_base+N*f\nPriority scheduler\nEmergency override")

    # Data Stores D1, D2, D3
    draw_datastore(3.7, 1.6, 2.4, 1.4, "D1: Benchmark Dataset", "UA-DETRAC Set", "Train & Val frames\nAnnotations & labels")
    draw_datastore(6.5, 1.6, 2.4, 1.4, "D2: Model Artifacts", "YOLOv8 Weights", "best.pt (6.2 MB)\nbest.onnx, conf params")
    draw_datastore(9.3, 1.6, 2.4, 1.4, "D3: Telemetry Store", "MongoDB Logs", "Phase history\nLane counts, alert logs")

    # Flow arrows
    def draw_flow_arrow(x1, y1, x2, y2, label="", offset_y=0.15):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", mutation_scale=15, color='#D97706', lw=2.0))
        if label:
            ax.text((x1 + x2)/2, (y1 + y2)/2 + offset_y, label, fontsize=7.2, color='#475569',
                    ha='center', va='center', fontfamily='sans-serif', fontweight='bold')

    # Entity -> P1
    draw_flow_arrow(2.2, 5.2, 2.7, 5.2, "Raw RTSP\nFrames", offset_y=0.35)
    # P1 -> P2
    draw_flow_arrow(4.8, 5.2, 5.3, 5.2, "Normalized\n640x640", offset_y=0.35)
    # P2 -> P3
    draw_flow_arrow(7.4, 5.2, 7.9, 5.2, "Vehicle BBoxes\n& Classes", offset_y=0.35)
    # P3 -> P4
    draw_flow_arrow(10.0, 5.2, 10.3, 5.2, "Lane Counts\n& Wait Cycles", offset_y=0.35)
    # P4 -> Entity
    draw_flow_arrow(12.4, 5.2, 12.8, 5.2, "Optimized Phase\n& HUD Stream", offset_y=0.35)

    # Data Store Flows
    # D1 -> P1 (training/simulation feed)
    ax.annotate('', xy=(3.7, 4.2), xytext=(4.4, 3.0),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=12, color='#64748B', lw=1.5))
    ax.text(3.7, 3.5, "Frame sequence", fontsize=7.0, color='#64748B')

    # D2 -> P2 (Model weights loaded)
    ax.annotate('', xy=(6.3, 4.2), xytext=(7.2, 3.0),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=12, color='#64748B', lw=1.5))
    ax.text(6.4, 3.5, "best.pt weights", fontsize=7.0, color='#64748B')

    # P4 -> D3 (Store decisions)
    ax.annotate('', xy=(10.5, 3.0), xytext=(11.3, 4.2),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=12, color='#64748B', lw=1.5))
    ax.text(11.1, 3.5, "Timing history", fontsize=7.0, color='#64748B')

    # Operator override flow to P4
    ax.annotate('', xy=(12.0, 4.2), xytext=(13.3, 4.3),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=12, color='#DC2626', lw=1.8))
    ax.text(12.8, 3.8, "Emergency / Manual\nOverride", fontsize=7.0, color='#DC2626', fontweight='bold', ha='center')

    # Legend at bottom
    leg_box = FancyBboxPatch((0.5, 0.4), 14.0, 0.65, boxstyle="round,pad=0.02,rounding_size=0.08",
                             facecolor='#FFFFFF', edgecolor='#E2E8F0', lw=1.0)
    ax.add_patch(leg_box)
    ax.text(0.7, 0.72, "Legend:", fontsize=8.2, fontweight='bold', color='#1E293B', va='center')

    # Legend items
    ax.add_patch(FancyBboxPatch((1.6, 0.55), 0.35, 0.22, boxstyle="round,pad=0.01", facecolor='#1E293B', edgecolor='#0F172A'))
    ax.text(2.1, 0.72, "External Entity", fontsize=7.8, color='#475569', va='center')

    ax.add_patch(FancyBboxPatch((3.7, 0.55), 0.35, 0.22, boxstyle="round,pad=0.01", facecolor='#FFFFFF', edgecolor='#D97706', lw=1.5))
    ax.text(4.2, 0.72, "Processing Module (P1-P4)", fontsize=7.8, color='#475569', va='center')

    ax.add_patch(FancyBboxPatch((6.8, 0.55), 0.35, 0.22, boxstyle="round,pad=0.01", facecolor='#F8FAFC', edgecolor='#475569', lw=1.5))
    ax.text(7.3, 0.72, "Data Store (D1-D3)", fontsize=7.8, color='#475569', va='center')

    ax.annotate('', xy=(10.0, 0.72), xytext=(9.4, 0.72),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=12, color='#D97706', lw=1.8))
    ax.text(10.2, 0.72, "Primary Data Flow", fontsize=7.8, color='#475569', va='center')

    ax.annotate('', xy=(12.4, 0.72), xytext=(11.8, 0.72),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=12, color='#DC2626', lw=1.8))
    ax.text(12.6, 0.72, "Control / Override Action", fontsize=7.8, color='#475569', va='center')

    plt.tight_layout()
    plt.savefig("ppt_assets/dfd_diagram.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("dfd_diagram.png created successfully!")

if __name__ == '__main__':
    create_architecture_diagram()
    create_dfd_diagram()
