import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle

# Fix Type 3 font issue - use TrueType fonts instead
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42  # TrueType fonts
matplotlib.rcParams['ps.fonttype'] = 42   # TrueType fonts for EPS

# Set seaborn style
sns.set_style("whitegrid")

# Use Helvetica font
plt.rcParams['font.family'] = 'Helvetica'

# Data from the table
models_without_pretrain = [
    'Diffusion\nPolicy',
    'π₀-FAST\n(Paligemma)',
    'SmolVLA\n(0.24B)',
    'SmolVLA\n(2.25B)',
    'OpenVLA\n-OFT',
    'π₀.₅-KI',
    'VLA-0\n(Ours)'
]
scores_without_pretrain = [72.4, 71.8, 82.8, 88.8, 91.9, 93.3, 94.7]

models_with_pretrain = [
    'Octo',
    'OpenVLA',
    'π₀-FAST',
    'Molmo\nAct',
    'GR00T\n-N1',
    'π₀',
    'π₀.₅-KI',
    'OpenVLA\n-OFT',
    'VLA-0\n(Ours)'
]
scores_with_pretrain = [75.1, 76.5, 86.0, 86.8, 93.9, 94.2, 94.3, 97.1, 94.7]

# Color palette - different color for each plot, highlight "Ours" differently
color_without = '#7FD87F'  # Green
color_with = '#6BAED6'     # Blue
color_ours = '#FF9800'     # Orange for "Ours"

def create_plot(models, scores, base_color, title, filename, add_hatching=False):
    fig, ax = plt.subplots(figsize=(14, 4))
    
    x = np.arange(len(models))
    width = 0.6
    
    # Create bars individually to control colors
    bars = []
    for i, (model, score) in enumerate(zip(models, scores)):
        color = color_ours if 'Ours' in model else base_color
        alpha = 0.9 if 'Ours' in model else 0.85
        # Add hatching to "Ours" if requested (for second plot)
        hatch = '///' if (add_hatching and 'Ours' in model) else None
        bar = ax.bar(x[i], score, width,
                     color=color, alpha=alpha, 
                     edgecolor='black', linewidth=0.7,
                     hatch=hatch,
                     zorder=3)
        bars.extend(bar)
    
    # Add subtle shadow effect to bars
    shadow_offset = 0.04
    for bar in bars:
        shadow = Rectangle((bar.get_x() + shadow_offset, shadow_offset), 
                           bar.get_width(), bar.get_height(),
                           facecolor='gray', alpha=0.3, zorder=1,
                           edgecolor='none')
        ax.add_patch(shadow)
    
    # Add dotted horizontal line at VLA-0's score (94.7)
    ax.axhline(y=94.7, color='#FF6B6B', linestyle='--', linewidth=2, alpha=0.7, zorder=2,
               label='VLA-0 baseline')
    
    ax.set_ylabel('Average Success Rate (%)', fontsize=19, fontweight='bold')
    ax.set_xlabel('Models', fontsize=19, fontweight='bold')
    ax.set_title(title, fontsize=20, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=16, rotation=0, ha='center')
    
    ax.set_ylim(60, 100)
    
    # Enhanced grid styling
    ax.yaxis.grid(True, alpha=0.2, linestyle='-', linewidth=0.7, color='#CCCCCC', zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis='y', labelsize=18)
    ax.tick_params(axis='x', labelsize=16)
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1, 
               f'{height:.1f}', 
               ha='center', va='bottom', fontsize=15, fontweight='bold', zorder=4)
        
        # Add annotation for SimpleVLA in second plot (with hatching)
        if add_hatching and 'Ours' in models[i]:
            ax.text(bar.get_x() + bar.get_width()/2., height - 4, 
                   'No large-scale\naction pretrain', 
                   ha='center', va='top', fontsize=11, style='italic',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                            edgecolor='#FF9800', linewidth=1.5, alpha=0.9),
                   zorder=5)
    
    plt.tight_layout()
    plt.savefig(f'/Users/angoyal/Downloads/{filename}', dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {filename}")

# Create Plot 1: Without Large-scale Action Pretraining
create_plot(models_without_pretrain, scores_without_pretrain, color_without,
            'Models Without Large-scale Action Pretraining',
            'libero_without_pretraining.pdf', add_hatching=False)

# Create Plot 2: With Large-scale Action Pretraining (add hatching to SimpleVLA)
create_plot(models_with_pretrain, scores_with_pretrain, color_with,
            'Models With Large-scale Action Pretraining',
            'libero_with_pretraining.pdf', add_hatching=True)

print("\nBoth plots created successfully!")
print("Files:")
print("  - libero_without_pretraining.pdf")
print("  - libero_with_pretraining.pdf")