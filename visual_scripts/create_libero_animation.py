import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation, FFMpegWriter
import matplotlib

# Fix Type 3 font issue
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# Set seaborn style
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'Helvetica'

# Data from the table
models_without_pretrain = [
    'Diffusion\nPolicy',
    'π₀-FAST\n(Paligemma)',
    'SmolVLA\n(0.24B)',
    'SmolVLA\n(2.25B)',
    'OpenVLA\n-OFT',
    'π₀.₅-KI',
    r'$\mathbf{VLA\text{-}0}$' + '\n' + r'$\mathbf{(Ours)}$'
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
    r'$\mathbf{VLA\text{-}0}$' + '\n' + r'$\mathbf{(Ours)}$'
]
scores_with_pretrain = [75.1, 76.5, 86.0, 86.8, 93.9, 94.2, 94.3, 97.1, 94.7]

# Colors - Light theme for Twitter
color_without = '#10b981'  # Emerald green
color_with = '#3b82f6'     # Royal blue
color_ours = '#f97316'     # Vibrant orange for VLA-0
bg_color = '#ffffff'       # White background
text_color = '#1e293b'     # Dark text

def create_animated_plot():
    """Create animated bar chart with both plots stacked vertically"""
    
    # Create figure with two subplots (vertical) with more spacing
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 11))
    fig.patch.set_facecolor(bg_color)  # Light background for Twitter
    fig.subplots_adjust(hspace=0.45)  # More space between plots
    
    # Total frames for animation (11 seconds at 20fps)
    n_frames = 220
    
    # Initialize empty bars for both plots
    x1 = np.arange(len(models_without_pretrain))
    x2 = np.arange(len(models_with_pretrain))
    width = 0.6
    
    bars1 = []
    bars2 = []
    value_texts1 = []
    value_texts2 = []
    
    def init():
        """Initialize the animation"""
        # Setup first subplot (without pretraining)
        ax1.set_facecolor('#f8fafc')
        for i, (model, score) in enumerate(zip(models_without_pretrain, scores_without_pretrain)):
            color = color_ours if 'Ours' in model else color_without
            # Baselines at full height, VLA-0 starts at 0
            initial_height = 0 if 'Ours' in model else score
            bar = ax1.bar(x1[i], initial_height, width, color=color, alpha=0.9, 
                         edgecolor='#334155', linewidth=2, zorder=3)
            bars1.append(bar)
            
            # Add 3D shadow effect
            shadow_offset = 0.03
            shadow = Rectangle((x1[i] - width/2 + shadow_offset, shadow_offset), 
                             width, initial_height if not 'Ours' in model else 0,
                             facecolor='#cbd5e1', alpha=0.5 if not 'Ours' in model else 0, zorder=1,
                             edgecolor='none')
            ax1.add_patch(shadow)
            
            # Value text (show baselines, hide VLA-0 initially)
            text_val = f'{score:.1f}' if not 'Ours' in model else ''
            text = ax1.text(x1[i], initial_height + 1 if not 'Ours' in model else 0, text_val,
                          ha='center', va='bottom', 
                          fontsize=15, fontweight='bold', color=text_color, zorder=4)
            value_texts1.append(text)
        
        # Add "SOTA" text annotation (invisible initially, no box visible)
        ax1.sota_text = ax1.text(len(models_without_pretrain) - 1, 97, 'SOTA',
                                ha='center', va='bottom',
                                fontsize=18, fontweight='bold', color='white',
                                alpha=0, zorder=5)
        ax1.sota_box = None  # Will create when text appears
        
        # Horizontal line starts invisible, will appear at VLA-0's score
        line1 = ax1.axhline(y=94.7, color='#64748b', linestyle='--', linewidth=3, 
                           alpha=0, zorder=4)
        ax1.baseline_line = line1
        ax1.set_ylabel('Success Rate (%)', fontsize=19, fontweight='bold', color=text_color)
        ax1.set_title('LIBERO: Models Without Large-Scale Action Pretraining', fontsize=18, 
                     fontweight='600', pad=20, color=text_color)
        ax1.set_xticks(x1)
        ax1.set_xticklabels(models_without_pretrain, fontsize=14, rotation=0, color=text_color)
        ax1.set_ylim(60, 100)
        ax1.tick_params(axis='y', labelsize=17, colors=text_color)
        ax1.tick_params(axis='x', labelsize=14, colors=text_color)
        ax1.yaxis.grid(True, alpha=0.3, linestyle='-', linewidth=0.8, color='#cbd5e1', zorder=0)
        ax1.set_axisbelow(True)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['left'].set_color(text_color)
        ax1.spines['left'].set_linewidth(1.5)
        ax1.spines['bottom'].set_color(text_color)
        ax1.spines['bottom'].set_linewidth(1.5)
        
        # Setup second subplot (with pretraining) - starts invisible
        ax2.set_facecolor('#f8fafc')
        for i, (model, score) in enumerate(zip(models_with_pretrain, scores_with_pretrain)):
            color = color_ours if 'Ours' in model else color_with
            # Show baselines at full height, VLA-0 at 0, all invisible initially
            initial_height = 0 if 'Ours' in model else score
            bar = ax2.bar(x2[i], initial_height, width, color=color, alpha=0, 
                         edgecolor='#334155', linewidth=2, zorder=3)
            bars2.append(bar)
            
            # Add 3D shadow effect (invisible initially)
            if not 'Ours' in model:
                shadow_offset = 0.03
                shadow = Rectangle((x2[i] - width/2 + shadow_offset, shadow_offset), 
                                 width, initial_height,
                                 facecolor='#cbd5e1', alpha=0, zorder=1,
                                 edgecolor='none')
                ax2.add_patch(shadow)
            
            text_content = f'{score:.1f}' if not 'Ours' in model else ''
            text = ax2.text(x2[i], initial_height + 1 if not 'Ours' in model else 0, 
                          text_content, ha='center', va='bottom', 
                          fontsize=15, fontweight='bold', color=text_color, 
                          alpha=0, zorder=4)
            value_texts2.append(text)
        
        # Horizontal line starts invisible
        line2 = ax2.axhline(y=94.7, color='#64748b', linestyle='--', linewidth=3, 
                           alpha=0, zorder=4)
        ax2.baseline_line = line2
        
        # Add annotation text (invisible initially) - position above VLA-0
        vla0_index = len(models_with_pretrain) - 1  # VLA-0 is last
        ax2.annotation_text = ax2.text(vla0_index, 97.5, 
                                      'No Pretraining - Outperforms Most',
                                      ha='center', va='bottom',
                                      fontsize=19, fontweight='bold', color='white',
                                      alpha=0, zorder=5)
        ax2.annotation_box = None  # Will create when text appears
        ax2.set_ylabel('Success Rate (%)', fontsize=19, fontweight='bold', color=text_color)
        ax2.set_title('LIBERO: Models With Large-Scale Action Pretraining', fontsize=18, 
                     fontweight='600', pad=20, color=text_color, alpha=0)
        ax2.set_xticks(x2)
        ax2.set_xticklabels(models_with_pretrain, fontsize=14, rotation=0, color=text_color)
        for label in ax2.get_xticklabels():
            label.set_alpha(0)
        ax2.set_ylim(60, 100)
        ax2.tick_params(axis='y', labelsize=17, colors=text_color)
        for label in ax2.get_yticklabels():
            label.set_alpha(0)
        ax2.tick_params(axis='x', labelsize=14, colors=text_color)
        ax2.yaxis.grid(True, alpha=0, linestyle='-', linewidth=0.8, color='#cbd5e1', zorder=0)
        ax2.set_axisbelow(True)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_color(text_color)
        ax2.spines['left'].set_linewidth(1.5)
        ax2.spines['left'].set_alpha(0)
        ax2.spines['bottom'].set_color(text_color)
        ax2.spines['bottom'].set_linewidth(1.5)
        ax2.spines['bottom'].set_alpha(0)
        
        return bars1 + bars2 + value_texts1 + value_texts2
    
    def animate(frame):
        """Slower sequence with more reading time"""
        # 0-20: Plot 1 shows (baselines visible) - 1s
        # 20-50: VLA-0 bar grows from 0 to 94.7 - 1.5s  
        # 50-60: Horizontal line appears and blinks, "SOTA" text - 0.5s
        # 60-100: Pause for reading SOTA - 2s (INCREASED)
        # 100-120: Plot 1 fades to 30% opacity - 1s
        # 120-130: Plot 2 baselines fade in - 0.5s
        # 130-170: VLA-0 grows in plot 2 - 2s
        # 170-180: Horizontal line and text blink - 0.5s
        # 180-220: Pause for reading text - 2s
        
        if frame < 20:
            # Plot 1 baselines visible, VLA-0 at 0 - just hold (1s)
            pass
        
        elif frame < 50:
            # VLA-0 bar grows in first plot
            progress = min((frame - 20) / 30, 1.0)  # 1.5 seconds to grow
            for i, model in enumerate(models_without_pretrain):
                if 'Ours' in model:
                    target_height = 94.7  # Explicitly set to 94.7
                    current_height = target_height * progress
                    bars1[i][0].set_height(current_height)
                    
                    # Update shadow
                    shadow_idx = len(models_without_pretrain) + i
                    if shadow_idx < len(ax1.patches):
                        ax1.patches[shadow_idx].set_height(current_height)
                        ax1.patches[shadow_idx].set_alpha(0.5 * progress)
                    
                    if progress > 0.5:
                        value_texts1[i].set_text('94.7')
                        value_texts1[i].set_y(current_height + 1)
                        value_texts1[i].set_alpha((progress - 0.5) / 0.5)
                    
                    # Ensure final height is exactly 94.7 at frame 49
                    if frame >= 49:
                        bars1[i][0].set_height(94.7)
        
        elif frame < 60:
            # Keep VLA-0 at 94.7 and show line/text with blink
            for i, model in enumerate(models_without_pretrain):
                if 'Ours' in model:
                    bars1[i][0].set_height(94.7)
            
            # Horizontal line appears and blinks with "SOTA" text and box
            line_progress = (frame - 50) / 10
            blink = 0.5 + 0.5 * np.sin(line_progress * np.pi * 2)  # 1 full blink
            ax1.baseline_line.set_alpha(blink * 0.9)
            
            # Make text visible with box
            ax1.sota_text.set_alpha(blink)
            ax1.sota_text.set_color(color_ours)
            ax1.sota_text.set_bbox(dict(boxstyle='round,pad=0.5', facecolor='white',
                                        edgecolor=color_ours, linewidth=2.5, alpha=blink))
        
        elif frame < 100:
            # Pause - keep SOTA text and line visible, ensure bar at 94.7
            for i, model in enumerate(models_without_pretrain):
                if 'Ours' in model:
                    bars1[i][0].set_height(94.7)
            # Keep SOTA visible
            ax1.baseline_line.set_alpha(0.9)
            ax1.sota_text.set_alpha(1.0)
        
        elif frame < 120:
            # Fade plot 1 to 30% opacity
            fade_progress = (frame - 100) / 20
            for i, bar in enumerate(bars1):
                bars1[i][0].set_alpha(0.9 - fade_progress * 0.6)
                value_texts1[i].set_alpha(1.0 - fade_progress * 0.7)
            ax1.baseline_line.set_alpha(0.9 - fade_progress * 0.6)
            ax1.sota_text.set_alpha(1.0 - fade_progress)
        
        elif frame < 130:
            # Fade in plot 2 baselines
            fade_progress = (frame - 120) / 10
            ax2.title.set_alpha(fade_progress)
            for label in ax2.get_xticklabels():
                label.set_alpha(fade_progress)
            for label in ax2.get_yticklabels():
                label.set_alpha(fade_progress)
            ax2.spines['left'].set_alpha(fade_progress)
            ax2.spines['bottom'].set_alpha(fade_progress)
            ax2.yaxis.grid(True, alpha=fade_progress * 0.3)
            
            for i, model in enumerate(models_with_pretrain):
                if not 'Ours' in model:
                    bars2[i][0].set_alpha(fade_progress * 0.9)
                    value_texts2[i].set_alpha(fade_progress)
                    # Fade in shadow
                    shadow_idx = len(bars2) + [j for j, m in enumerate(models_with_pretrain) if not 'Ours' in m].index(i)
                    if shadow_idx < len(ax2.patches):
                        ax2.patches[shadow_idx].set_alpha(fade_progress * 0.5)
        
        elif frame < 170:
            # VLA-0 grows in second plot (slower - 2 seconds)
            progress = min((frame - 130) / 40, 1.0)  # 2 seconds to grow
            for i, model in enumerate(models_with_pretrain):
                if 'Ours' in model:
                    target_height = 94.7  # Explicitly set to 94.7
                    current_height = target_height * progress
                    bars2[i][0].set_height(current_height)
                    bars2[i][0].set_alpha(0.9)
                    
                    if progress > 0.5:
                        value_texts2[i].set_text('94.7')
                        value_texts2[i].set_y(current_height + 1)
                        value_texts2[i].set_alpha((progress - 0.5) / 0.5)
                    
                    # Ensure final height is exactly 94.7 at frame 169
                    if frame >= 169:
                        bars2[i][0].set_height(94.7)
        
        elif frame < 180:
            # Keep VLA-0 at 94.7 and show line/text with blink
            for i, model in enumerate(models_with_pretrain):
                if 'Ours' in model:
                    bars2[i][0].set_height(94.7)
            
            # Horizontal line and text appear with blink
            line_progress = (frame - 170) / 10
            blink = 0.5 + 0.5 * np.sin(line_progress * np.pi * 2)  # 1 full blink
            ax2.baseline_line.set_alpha(blink * 0.9)
            
            # Make text visible with box
            ax2.annotation_text.set_alpha(blink)
            ax2.annotation_text.set_color(color_ours)
            ax2.annotation_text.set_bbox(dict(boxstyle='round,pad=0.6', facecolor='white',
                                             edgecolor=color_ours, linewidth=2.5, alpha=blink))
        
        elif frame >= 180:
            # Pause - keep everything visible for reading
            # Fade plot 1 back to full opacity
            fade_back_progress = min((frame - 180) / 20, 1.0)  # 1 second to fade back
            for i, bar in enumerate(bars1):
                bars1[i][0].set_alpha(0.3 + fade_back_progress * 0.6)
                value_texts1[i].set_alpha(0.3 + fade_back_progress * 0.7)
            ax1.baseline_line.set_alpha(0.3 + fade_back_progress * 0.6)
            
            # Keep plot 2 visible
            for i, model in enumerate(models_with_pretrain):
                if 'Ours' in model:
                    bars2[i][0].set_height(94.7)
            ax2.baseline_line.set_alpha(0.9)
            ax2.annotation_text.set_alpha(1.0)
        
        return bars1 + bars2 + value_texts1 + value_texts2
    
    # Create animation
    anim = FuncAnimation(fig, animate, init_func=init, frames=n_frames, 
                        interval=50, blit=False, repeat=True)
    
    # Save as MP4
    writer = FFMpegWriter(fps=20, bitrate=2000, 
                         extra_args=['-pix_fmt', 'yuv420p', '-vcodec', 'libx264'])
    
    output_path = '/Users/angoyal/Documents/code/simplevla_webpage/Videos/libero_results.mp4'
    anim.save(output_path, writer=writer)
    print(f"\nAnimation saved: {output_path}")
    
    plt.close()

if __name__ == "__main__":
    print("Creating LIBERO results animation...")
    print("This will take ~30 seconds...")
    create_animated_plot()
    print("\n✅ Done! Check Videos/libero_results.mp4")

