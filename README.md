# CNC and 3D Printing Cases

A Python-based CAD project for generating parametric enclosures and panels using CadQuery. This project creates STL and STEP files for CNC machining and 3D printing of electronic enclosures.

## Project Overview

This repository contains two main case designs:

### AGC (Apollo Guidance Computer) Case
A replica enclosure inspired by the Apollo Guidance Computer, featuring:
- Modular top and bottom sections
- Configurable hole patterns for different panel layouts
- M4 mounting holes with proper clearances
- LEMO connector cutouts
- Chamfered edges and professional finish

### Typ-I Case
A modern electronic enclosure with:
- Wafer-style internal structure for component mounting
- Multiple LEMO connector positions
- Configurable panel patterns
- Integrated mounting system

## Features

- **Parametric Design**: All dimensions are configurable through variables
- **Multiple Export Formats**: Generates both STL (for 3D printing) and STEP (for CNC) files
- **Pattern System**: Configurable hole patterns for different use cases
- **Professional Finish**: Chamfers, fillets, and proper tolerances
- **Modular Architecture**: Reusable components and functions

## Project Structure

```
├── README.md           # This file
├── agc.py             # AGC case generator
├── typ_i.py           # Typ-I case generator
├── lib/
│   ├── __init__.py
│   ├── ddd.py         # 3D modeling utilities
│   └── tools.py       # Common functions and patterns
├── STL/               # Generated STL files
└── STEP/              # Generated STEP files
```

## Requirements

- Python 3.7+
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

This generates:
- `STL/AGC01.stl` - Top section
- `STL/AGC10.stl` - Bottom section  
- `STL/AGC11.stl` - Complete assembly
- `STEP/AGC01.step` - Top section (CNC)
- `STEP/AGC10.step` - Bottom section (CNC)

### Generate Typ-I Case Files

```bash
python typ_i.py
```

This generates:
- `Case.stl` - Main enclosure
- `Panel.stl` - Front panel with default pattern
- `Case_x_Panel.stl` - Complete assembly
- `Panel_*.stl` - Panels with different hole patterns

## Configuration

### AGC Case Parameters

Key dimensions in `agc.py`:
- `w`, `h`: Overall case dimensions (4.5" × 7")
- `t`: Case thickness (30mm)
- `wt`: Wall thickness (3mm)
- `col`: Corner offset for mounting holes
- `m4xr`, `m4dr`: M4 screw hole radii

### Typ-I Case Parameters

Key dimensions in `typ_i.py`:
- `mw`, `h`: Module dimensions (4.25" × 7")
- `t`: Case depth (30mm)
- `wt1`, `wt2`, `wt3`: Various wall thicknesses
- `cell`: Grid cell size (1 inch)

### Hole Patterns

Available patterns (defined in `lib/tools.py`):
- `"ll"`: Limited layout (middle columns only)
- `"w"`: W-shaped pattern
- `"<>"`: Diamond pattern
- `"x"`: X-shaped pattern
- `ptn_all`: All holes (default)

## Library Functions

### `lib/ddd.py`
- `mov(x, y, z)`: Translation function
- `mirror(*plane)`: Mirroring operations
- `grid(tfm)`: 4×6 grid layout generator
- `lemo(wt)`: LEMO connector cutout
- `holes()`: Mounting hole patterns

### `lib/tools.py`
- Mathematical constants and unit conversions
- Functional programming utilities (`com`, `sum`, `dif`)
- Pattern definitions and mapping functions
- Type definitions for better code clarity

## Images

The AGC case design:

<img width="640" alt="back" src="https://github.com/user-attachments/assets/2b7f5edb-d0ec-4cd6-b03e-41857a65d4e9" />
<img width="640" alt="top" src="https://github.com/user-attachments/assets/1ec490e0-bd97-4850-b158-a097b2be7ce7" />
<img width="640" alt="side" src="https://github.com/user-attachments/assets/d5fdf7ed-cecb-4f92-9b72-a1102162a627" />
<img width="640" alt="AGC" src="https://github.com/user-attachments/assets/65121879-15d9-4e74-9665-d9e2e4905170" />
<img width="640" alt="Threads spec" src="https://github.com/user-attachments/assets/29d0c16e-53fa-4c6e-8650-96d677aaa50b" />

## Manufacturing Notes

### 3D Printing
- Use 0.2mm layer height for best surface finish
- Support material may be needed for overhangs
- Print orientation: bottom face down for best dimensional accuracy

### CNC Machining
- STEP files provided for CAM software
- Recommended materials: Aluminum 6061, ABS, or HDPE
- Consider tool access for internal features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the generated files
5. Submit a pull request

## License

This project is open source. Please check the repository for license details.
