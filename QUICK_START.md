# 🚀 Quick Start - Auto Crop Tool

## One-Minute Guide

### What You Need
- Binary Impact card image in `Tip_XXX/TipXXX.png`
- Terminal access
- Python 3 (already installed on Mac)

### Run It (3 Steps)

```bash
# 1. Navigate to project
cd /Users/Yokesh_Work/Unity_Tips/Unity-Tips

# 2. Run auto-cropper
python3 auto_crop_card.py Tip_012/Tip012.png

# 3. Done! ✨
```

### What Happens
- ✅ Card automatically detected
- ✅ Background removed
- ✅ File size reduced ~65%
- ✅ Ready for README.md

---

## Common Commands

### Basic (Use This 99% of Time)
```bash
python3 auto_crop_card.py Tip_012/Tip012.png
```

### Keep Original
```bash
python3 auto_crop_card.py Tip_012/Tip012.png Tip_012/Tip012_cropped.png
```

### More/Less Margin
```bash
python3 auto_crop_card.py Tip_012/Tip012.png Tip_012/Tip012.png 10
```

### Batch (Multiple Tips)
```bash
for i in {012..015}; do python3 auto_crop_card.py Tip_$i/Tip$i.png; done
```

---

## Full Workflow

```bash
# 1. Place image
# → Tip_012/Tip012.png

# 2. Navigate and crop
cd /Users/Yokesh_Work/Unity_Tips/Unity-Tips
python3 auto_crop_card.py Tip_012/Tip012.png

# 3. Tell Claude
# → "Generate Tip 012, keep it developer vibe"

# 4. Done! 🎉
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `command not found` | Use `python` instead of `python3` |
| `No such file` | Check you're in the right directory: `pwd` |
| `No module PIL` | Install: `pip3 install Pillow numpy` |
| Poor detection | Try: Add more margin (10%) |

---

## Output Explained

```
📸 Original: 4284x5712 (24.5MP)        ← Original size
🤖 AI detecting card boundaries...      ← Processing
✂️  Detected: (1092, 1913) → (3619, 5404)  ← Found card
📐 Cropped: 2527x3491 (ratio: 1.38:1)  ← Perfect ratio!
💾 Saved: Tip_012/Tip012.png           ← Saved here
📊 Size: 15.86MB → 5.80MB (63.5% smaller)  ← File reduced
✨ Done!
```

---

## Need More Help?

Read the full guide:
```bash
open AUTO_CROP_GUIDE.md
```

Or just ask Claude!

---

**TL;DR**:
```bash
python3 auto_crop_card.py Tip_XXX/TipXXX.png
```
That's it. ✨
