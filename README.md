# 🧬 Living Commits (Game of Life)

> "A zero-player game of birth, survival, and death unfolding in Git history."

### 📢 Latest Status
<!-- LATEST_STATUS_START -->
*Generation 130 of the digital colony is here. Today, 2 new cells were born and 2 cells passed away. The total population now stands at 5 living cells. (2026-02-17 13:45)*
<!-- LATEST_STATUS_END -->

### 📖 The Analogy
Think of this repository as a petri dish. Each file in the [Grid](grid/) is a living "cell." 
- If a cell is too lonely (fewer than 2 neighbors), it dies.
- If a cell is too crowded (more than 3 neighbors), it dies.
- If a dead space has exactly 3 neighbors, a new cell is born!

This is Conway's "Game of Life." It's not a game you play; it's a simulation you watch. From these simple rules of biology, complex "creatures" like gliders, blinkers, and spaceships emerge and move across the repository.

### 🌱 How it Evolves
The simulation runs autonomously every day:
1. **Scanning the Colony**: The script looks at which [files](grid/) currently exist.
2. **Applying Biology**: It calculates which cells should live or die today.
3. **Updating the Filesystem**: Files are created for births and deleted for deaths.
4. **Recording Generations**: A visual snapshot is appended to the [Life Log](life-log.md).

**This ecosystem requires no human intervention to thrive or collapse.**

### 🔍 Quick Links
- [The Life Log](life-log.md) — See the generations of cells unfolding.
- [The Cell Grid](grid/) — View the currently "alive" files.
- [The Logic](evolve.py) — The rules of life, death, and reproduction.
