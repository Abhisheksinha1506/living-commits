import os
import datetime

def get_neighbors(x, y):
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0: continue
            neighbors.append((x + dx, y + dy))
    return neighbors

def evolve():
    base_dir = os.path.dirname(__file__)
    grid_dir = os.path.join(base_dir, 'grid')
    log_path = os.path.join(base_dir, 'life-log.md')

    if not os.path.exists(grid_dir):
        os.makedirs(grid_dir)

    # 1. Read current alive cells
    alive_cells = set()
    for filename in os.listdir(grid_dir):
        if filename.startswith('cell_') and filename.endswith('.txt'):
            try:
                parts = filename.replace('cell_', '').replace('.txt', '').split('_')
                x, y = int(parts[0]), int(parts[1])
                alive_cells.add((x, y))
            except ValueError:
                continue

    # 2. Apply Conway's rules
    neighbor_counts = {}
    for x, y in alive_cells:
        for nx, ny in get_neighbors(x, y):
            neighbor_counts[(nx, ny)] = neighbor_counts.get((nx, ny), 0) + 1

    next_alive_cells = set()
    
    # Stay alive: 2 or 3 neighbors
    for cell in alive_cells:
        count = neighbor_counts.get(cell, 0)
        if count == 2 or count == 3:
            next_alive_cells.add(cell)
            
    # Birth: exactly 3 neighbors
    for cell, count in neighbor_counts.items():
        if count == 3:
            next_alive_cells.add(cell)

    # 3. Prevent infinite expansion (optional but recommended)
    # Filter to a bounded area if desired. Let's keep it simple but maybe limit to a window.
    # Actually, let's just let it grow unless it gets crazy.

    # 4. Update file system
    # Delete cells that died
    for cell in alive_cells - next_alive_cells:
        cell_file = os.path.join(grid_dir, f"cell_{cell[0]}_{cell[1]}.txt")
        if os.path.exists(cell_file):
            os.remove(cell_file)
            
    # Create cells that were born
    for cell in next_alive_cells - alive_cells:
        cell_file = os.path.join(grid_dir, f"cell_{cell[0]}_{cell[1]}.txt")
        with open(cell_file, 'w') as f:
            f.write("alive")

    # 5. Log snapshot
    if next_alive_cells:
        min_x = min(c[0] for c in next_alive_cells) - 2
        max_x = max(c[0] for c in next_alive_cells) + 2
        min_y = min(c[1] for c in next_alive_cells) - 2
        max_y = max(c[1] for c in next_alive_cells) + 2
    else:
        min_x, max_x, min_y, max_y = 0, 10, 0, 10

    # Limit snapshot size for log readability
    rows = []
    for y in range(max_y, min_y - 1, -1):
        row = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in next_alive_cells:
                row += '█'
            else:
                row += ' '
        rows.append(row)
    
    ascii_snapshot = "\n".join(rows)
    date_str = datetime.date.today().isoformat()
    
    # Count generations
    gen_count = 0
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            for line in f:
                if line.startswith('|') and not line.startswith('| Generation') and not line.startswith('|------------'):
                    gen_count += 1

    with open(log_path, 'a') as f:
        f.write(f"| {gen_count + 1} | {date_str} | Alive: {len(next_alive_cells)} | \n```\n{ascii_snapshot}\n``` |\n")

    # Generate human summary
    born = len(next_alive_cells - alive_cells)
    died = len(alive_cells - next_alive_cells)
    summary = f"Generation {gen_count + 1} of the digital colony is here. "
    summary += f"Today, {born} new cells were born and {died} cells passed away. "
    summary += f"The total population now stands at {len(next_alive_cells)} living cells."
    
    if len(next_alive_cells) == 0:
        summary += " The colony has unfortunately collapsed and is now empty."

    with open(os.path.join(base_dir, 'summary.txt'), 'w') as f:
        f.write(summary)

    update_readme(summary)

def update_readme(summary):
    from pathlib import Path
    readme_path = Path("README.md")
    if not readme_path.exists(): return
    try:
        content = readme_path.read_text()
        start = "<!-- LATEST_STATUS_START -->"
        end = "<!-- LATEST_STATUS_END -->"
        if start not in content or end not in content: return
        parts = content.split(start)
        suffix_parts = parts[1].split(end)
        prefix = parts[0] + start
        suffix = end + suffix_parts[1]
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_inner = f"\n*{summary} ({timestamp})*\n"
        readme_path.write_text(prefix + new_inner + suffix)
    except Exception as e: print(f"⚠️ README Update Failed: {e}")

if __name__ == "__main__":
    evolve()
