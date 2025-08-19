# CNC and 3D Printing Cases

A Python-based CAD project for generating parametric enclosures and panels using CadQuery. This project creates STL, STEP, and SVG files for CNC machining and 3D printing of electronic enclosures with advanced threading support.

### AGC (Apollo Guidance Computer) Case
An enclosure inspired by the Apollo Guidance Computer. Features include:
- **Multi-module configurations**
- **Configurable hole patterns**
- **M4 threads**
- **LEMO connector cutouts**

## Features

- **Parametric Design**: All dimensions are configurable
- **Multiple Export Formats**: Generates STL (3D printing), STEP (CNC), and SVG (technical drawings)
- **Pattern System**: Configurable hole patterns including diamond, X, W, and custom layouts
- **Multi-module Support**: 1M, 2M, and 3M case configurations for different setups
- **Technical Drawings**: Automatic SVG generation with three-view projections
- **Serge Compatibility**: Designed for 4×6 inch PCBs and Paperface era 1 inch control spacings.

## Requirements

- Python 3.12
- CadQuery
- ocp-vscode (for visualization)

## Installation

1. Install CadQuery following the [official installation guide](https://cadquery.readthedocs.io/en/latest/installation.html)
2. Clone this repository:
   ```bash
   git clone https://github.com/P0ed/DIY.git
   cd DIY
   ```

## Usage

### Generate AGC Case Files

```bash
python agc.py
```

This generates files for all three unit configurations:

**1M Configuration:**
- `STL/AGC-1M-01.stl` - Bottom section
- `STL/AGC-1M-10.stl` - Top section  
- `STL/AGC-1M-11.stl` - Complete assembly
- `STEP/AGC-1M-01.step` - Bottom section (CNC)
- `STEP/AGC-1M-10.step` - Top section (CNC)
- `SVG/AGC-1M-*.svg`, `AGC-01T.svg` - Technical drawings

**2M and 3M Configurations:**
- Similar naming pattern with `2M` and `3M` designations

## Images

The AGC case design:

<img width="640" alt="back" src="https://github.com/user-attachments/assets/2b7f5edb-d0ec-4cd6-b03e-41857a65d4e9" />
<img width="640" alt="top" src="https://github.com/user-attachments/assets/1ec490e0-bd97-4850-b158-a097b2be7ce7" />
<img width="640" alt="side" src="https://github.com/user-attachments/assets/d5fdf7ed-cecb-4f92-9b72-a1102162a627" />
<img width="640" alt="AGC" src="https://github.com/user-attachments/assets/65121879-15d9-4e74-9665-d9e2e4905170" />
<img width="640" alt="AGC01-Thread-Spec" src="https://github.com/user-attachments/assets/4fb63d46-3658-4474-a71f-17102c37c6ca" />

## Project Structure

```
├── README.md          # This file
├── agc.py             # AGC case generator (main script)
├── lib/
│   ├── __init__.py
│   ├── ddd.py         # 3D modeling utilities and transformations
│   ├── tools.py       # Common functions, patterns, and utilities
│   ├── thread.py      # ISO/UTS thread generation system
│   └── export.py      # Multi-format export with technical drawings
├── STL/               # Generated STL files for 3D printing
├── STEP/              # Generated STEP files for CNC machining
└── SVG/               # Generated technical drawings
```

## Configuration

### AGC Case Parameters

Key dimensions in `agc.py`:
- `modules`: Number of units (1, 2, or 3)
- `cw`, `ch`: Module card dimensions (4" × 6")
- `w`, `h`, `t`: Overall case dimensions
- `wt`: Wall thickness (3mm)
- `col`: Mounting column width (12mm)

### Hole Patterns

Available patterns (defined in `lib/tools.py`):
- `"ll"`: Vertical columns only
- `"w"`: W-shaped pattern
- `"<>"`: Diamond pattern
- `"x"`: X-shaped pattern
- `ptn_all`: All holes
- Custom patterns can be defined as boolean functions for specific module requirements

## Library Functions

### `lib/ddd.py` - 3D Modeling Utilities
- `mov(x, y, z)`: Translation function
- `mirror(*plane)`: Mirroring operations with union
- `rotz(angle)`: Z-axis rotation
- `grid(tfm)`: 4×6 grid layout generator
- `lemo(wt)`: LEMO connector cutout
- `holes()`: Mounting hole patterns
- `bounds()`: Bounding box calculation

### `lib/tools.py` - Utilities and Patterns
- Mathematical constants: `inch`, `s2`, `pl`
- Functional programming utilities: `com`, `sum`, `dif`, `flat`
- Pattern definitions and mapping functions
- Boolean pattern combinators

### `lib/thread.py` - Threading System
- Thread Generation: `thread(size, length, location, segments)`

### `lib/export.py` - Export System
- **Multi-format Export**: STL, STEP, SVG generation
- `export(name, workplane, stl, svg, step, hidden)`: Main export function
- **Technical Drawings**: Three-view projections with proper scaling
- `three_view()`: Generates orthographic projections

## Threading Support

```python
from lib.thread import thread

# Generate M4 internal thread, 15mm long
internal_thread = thread('M4', 15.0, 'internal')

# Generate M4 external thread, 10mm long  
external_thread = thread('M4', 10.0, 'external')
```

**Supported Thread Standards:**
- **ISO Metric**: M2 through M24 with standard and fine pitches
- **UTS (Unified Thread Standard)**: Common sizes from #2 to 1"
- **Custom Threads**: Extensible system for additional thread types

## Manufacturing Notes

### CNC Machining
- **Recommended Materials**: Aluminum 7075
- **STEP Files**: Provided for CAM software compatibility
- **Threading**: Can be tapped or thread-milled using generated specifications
- **Tolerances**: Designed for ±0.1mm machining accuracy

### 3D Printing
- **Recommended Processes**: `SLM`, `MJF`, `SLS`
- **Recommended Materials**:
  - **Metals**: `Ti TC4`, `AlSi10Mg`
  - **Plastics**: `PA12`, `PA11`, `3201PA-F`, `3301PA`
