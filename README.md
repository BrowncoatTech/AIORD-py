(Due to technical issues, the search service is temporarily unavailable.)


# Game Object Recognition Dataset Tools

A toolkit for creating and managing image datasets for AI training, consisting of:
1. **Screen Capture Tool** - Captures game screenshots on right-click hold
2. **Dataset Deduplicator** - Removes duplicate/similar images

## Prerequisites

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Windows OS** (Screen Capture tool requires Windows)
- **Administrator Privileges** (For package installations)

## Installation

### 1. Clone/Create Project Directory
```
mkdir game_dataset_tools
cd game_dataset_tools
```

### 2. Save the Scripts
Create two files in the directory:
- `screenshot_capture.py` (First application code)
- `dataset_deduplicator.py` (Second application code)

### 3. Install Dependencies
```
pip install pillow pynput pywin32 imagehash
```

## Usage Guide

---

### 🖥️ Screen Capture Tool

#### Step 1: Run the Capture Tool
```
python screenshot_capture.py
```

#### Step 2: Name Your Object Class
```
Enter the object name for the dataset: enemy_character
```

#### Step 3: Prepare Your Game/Application
1. Launch your target game/software
2. Position it where you want to capture
3. Keep it in foreground (don't minimize)

#### Step 4: Capture Images
1. **Start Capturing**: Hold right mouse button
2. **Stop Capturing**: Release right mouse button
3. **Capture Rate**: 1 image every 400ms (2.5 images/sec)

#### Step 5: View Results
- Images saved to: `dataset/<object_name>/`
- Example path: `dataset/enemy_character/`

---

### 🧹 Dataset Deduplicator

#### Basic Deduplication (Recommended)
```
python dataset_deduplicator.py dataset/enemy_character --method phash --threshold 95 --action move
```

#### Common Usage Patterns

1. **Safe Mode** (Move duplicates to subfolder):
```
python dataset_deduplicator.py path/to/dataset --action move
```

2. **Aggressive Cleaning** (Delete duplicates immediately):
```
python dataset_deduplicator.py path/to/dataset --action delete
```

3. **Exact File Duplicates**:
```
python dataset_deduplicator.py path/to/dataset --method md5
```

4. **Loose Deduplication** (80% similarity threshold):
```
python dataset_deduplicator.py path/to/dataset --threshold 80
```

---

## Command Reference

### Screenshot Capture Options
| Action                | Control           |
|-----------------------|-------------------|
| Start/Stop Capturing  | Right Mouse Click |
| Exit Program          | Ctrl+C in console |

### Deduplicator Arguments
| Argument      | Values            | Default | Description                          |
|---------------|-------------------|---------|--------------------------------------|
| --method      | phash, ahash, md5 | phash   | Hashing algorithm for comparison     |
| --threshold   | 1-100             | 95      | Similarity percentage threshold      |
| --action      | move, delete      | move    | How to handle duplicates             |

---

## Troubleshooting

**Common Issues:**
1. **Captures Wrong Window**
   - Ensure target window is active/focused
   - Wait 1 second after clicking into window

2. **Permission Errors**
   - Run command prompt as Administrator
   ```bash
   Right-click Command Prompt > Run as Administrator
   ```

3. **Missing Dependencies**
   - Reinstall requirements:
   ```bash
   pip install --force-reinstall pillow pynput pywin32 imagehash
   ```

4. **Black/Blank Screenshots**
   - Disable hardware acceleration in game/software
   - Run game/software in windowed mode

5. **Duplicate Detection Errors**
   - Try different threshold values
   ```bash
   python dataset_deduplicator.py path/to/dataset --threshold 85
   ```

---

## Best Practices

1. **Dataset Organization**
   ```
   dataset/
   ├── enemy_character/
   ├── powerup/
   └── health_pack/
   ```

2. **Capture Tips**
   - Capture from multiple angles/lighting conditions
   - Vary object positions in screen
   - Include partial occlusions

3. **Deduplication Workflow**
   ```
   graph TD
     A[Raw Captures] --> B(First Pass: md5)
     B --> C(Second Pass: phash 95%)
     C --> D(Manual Review)
     D --> E[Clean Dataset]
   ```

4. **Performance Notes**
   - 1000 images ≈ 1GB storage
   - Deduplication time: ~1000 images/minute
```
