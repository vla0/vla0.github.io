# VLA-0 Website

Official website for **VLA-0: Building State-of-the-Art VLAs with Zero Modification**

**Live Site:** [https://vla0.github.io/](https://vla0.github.io/)

---

## About

VLA-0 achieves state-of-the-art results in Vision-Language-Action models without any architectural changes to the base VLM. This website showcases the research, results, and resources.

---

## Project Structure

```
vla0.github.io/
├── index.html              # Main website
├── style.css               # Styling with monochromatic slate theme
├── script.js               # Interactive features
├── Videos/                 # Video assets
│   ├── teaser.mp4          # Architecture diagram animation
│   ├── SimpleVLA-RealWorld.mp4  # Real robot demonstrations
│   ├── libero_results.mp4  # LIBERO results animation
│   └── realworld-thumbnail.jpg
├── data/                   # Paper and figures
│   ├── root.pdf            # Latest paper
│   └── figures/            # Converted PNG figures
└── visual_scripts/         # Scripts for generating visualizations
    ├── create_libero_animation.py  # Animated LIBERO results
    └── create_libero_plot.py       # Static LIBERO plots
```

---

## Visual Scripts

The `visual_scripts/` folder contains Python scripts for generating the data visualizations:

### `create_libero_plot.py`
Creates static bar charts showing VLA-0's performance on LIBERO benchmark.

**Generates:**
- `libero_without_pretraining.pdf` - Models without large-scale action pretraining
- `libero_with_pretraining.pdf` - Models with large-scale action pretraining

**Features:**
- Helvetica font for consistency
- Color-coded bars (green/blue with orange for VLA-0)
- 3D shadow effects
- Baseline comparison line

### `create_libero_animation.py`
Creates animated comparison showing VLA-0 achieving SOTA results.

**Generates:**
- `Videos/libero_results.mp4` - 11-second animation for Twitter/website

**Features:**
- Light theme optimized for Twitter
- Sequential reveal (plot 1 → plot 2)
- Text annotations ("SOTA", "No Pretraining - Outperforms Most")
- Blinking highlights for emphasis
- VLA-0 bars in bold orange with growth animation

**Usage:**
```bash
cd visual_scripts
python create_libero_animation.py
```

---

## Running Locally

```bash
python3 -m http.server 8000
```

Then visit: `http://localhost:8000`

---

## Updating Videos

When adding or updating videos for the website, optimize them for web playback using FFmpeg:

### **Web Optimization (Required)**
Videos MUST be optimized with the `faststart` flag for proper web streaming:

```bash
ffmpeg -i input_video.mp4 \
  -c:v libx264 \
  -preset fast \
  -crf 23 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  output_video.mp4 \
  -y
```

**Key flags:**
- `-movflags +faststart`: Moves metadata to beginning (enables streaming before full download)
- `-crf 23`: Good quality/size balance (lower = better quality, 18-28 recommended)
- `-pix_fmt yuv420p`: Ensures compatibility across all browsers
- `-preset fast`: Good encoding speed/quality trade-off

### **Generate Video Thumbnail**
Create a thumbnail from a specific timestamp:

```bash
ffmpeg -i video.mp4 -ss 00:00:01 -vframes 1 -q:v 2 output_thumbnail.jpg -y
```

**Parameters:**
- `-ss 00:00:01`: Extract frame at 1 second (adjust as needed)
- `-vframes 1`: Extract exactly 1 frame
- `-q:v 2`: High quality JPEG (1-5, lower = better)

### **File Size Guidelines**
- **Hero video (teaser):** Keep under 2MB for fast loading
- **Demo videos:** Keep under 10MB (use Git LFS for larger files)
- **Animations:** Keep under 2MB for Twitter compatibility

### **Example: Optimizing Both Videos**
```bash
# Optimize teaser video
ffmpeg -i Videos/teaser.mp4 -c:v libx264 -preset fast -crf 23 \
  -pix_fmt yuv420p -movflags +faststart Videos/teaser-web.mp4 -y

# Optimize real-world video  
ffmpeg -i Videos/SimpleVLA-RealWorld.mp4 -c:v libx264 -preset fast -crf 23 \
  -pix_fmt yuv420p -movflags +faststart Videos/SimpleVLA-RealWorld-web.mp4 -y

# Generate thumbnail
ffmpeg -i Videos/SimpleVLA-RealWorld-web.mp4 -ss 00:00:01 \
  -vframes 1 -q:v 2 Videos/realworld-thumbnail.jpg -y
```

---

## Design Features

- **Color Scheme:** Monochromatic slate with cyan accents
- **Typography:** Inter font family
- **Responsive:** Mobile-friendly design
- **Optimized:** Fast loading with Git LFS for large files
- **Analytics:** Google Analytics integrated

---

## Credits

**Authors:** Ankit Goyal, Hugo Hadfield, Xuning Yang, Valts Blukis, Fabio Ramos  
**Affiliation:** NVIDIA Research

---

© 2025 NVIDIA Research. All rights reserved.
