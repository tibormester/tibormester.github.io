### Portfolio

---

#### **Table of Contents**
1. [My Journey Into Game Development](#my-journey-into-game-development)
   - [Background](#background)
   - [Crucible - 3D Procedural RPG](#crucible---3d-procedural-rpg)
   - [Endless - 2D Procedural RPG](#endless---2d-procedural-rpg)
   - [Rogue Royale - 2D Battle Royale](#rogue-royale---2d-battle-royale)
   - [Sinking Labyrinth - 2D Rogue-like](#sinking-labyrinth---2d-rogue-like)
   - [Bug Souls - 3D Action RPG](#bug-souls---3d-action-rpg)
2. [Data Structures](#data-structures)
3. [Algorithms](#algorithms)
4. [Other](#other)

---

### **My Journey Into Game Development**

#### **Background**

##### *Scratch and Mobile Games*

My journey into Game Dev started with Scratch, a drag-and-drop engine, which I think is fair considering I was still in elementary school. I eventually used my familiarity with Scratch to win the Game Programming event at my State’s High School Science Olympiad competition. 

My first real experience with non-drag-and-drop programming came during middle school summers. My cousins and I would meet in person or over Skype to design and develop mobile games. Over the years, we managed to release four apps on the Apple App Store and two on Google Play.

[Download Falling Cats on Pug](https://falling-cats-on-pug.apk.dog)

##### *Changing Careers*

At first, I didn’t take game development seriously as a career path—I viewed it as play, not work. When I entered college at the University of Maryland, I was a math and physics major, with the ambitious dream of one day following in the footsteps of someone like Einstein.

However, my first college experience was humbling. I wasn’t at the top of my class anymore and realized that to truly excel, I’d need to live and breathe physics. After some soul-searching, I decided that while I loved physics, I couldn’t make it my life.

Crafting games that entertain people seemed far more fulfilling than publishing papers that might only be read by a handful in academia. So, for the past year and a half, I’ve been working on my computer science degree while also self-studying game development and design.

##### *Picking Game Engines*

When I finally made the career pivot, I started experimenting with engines. Initially, I tried JMonkeyEngine and LibGDX, as I had always wanted to build my own game engine. But I soon realized that I’d rather focus on developing fun gameplay mechanics rather than reinventing the wheel.

Eventually, I settled on Godot because of its solid documentation and the fact that it's free.

---

### **Crucible - 3D Procedural RPG**

#### *Procedural Mesh and Terrain Generation*

My first big project started with the idea of creating a completely procedurally generated game. I didn’t want to get distracted by asset creation.

I began with tutorials on mesh and terrain generation. First, I created a hexagonal mesh, applied noise to generate mountainous terrain, and then used shaders to modify the appearance of the terrain.

![Crucible Mesh 1](https://github.com/tibormester/tibormester.github.io/blob/master/terrain.jpeg)

#### *Character Controller and Procedural Animations*

Once the terrain was ready, I moved on to creating a character controller with procedural animations. Initially, I tried using Godot’s built-in physics engine and inverse kinematics systems but struggled. My goal was to create a ballistics system similar to War Thunder, where organ and body part animations adjust accordingly in an active ragdoll. But Godot’s tools weren’t ideal, so I switched to Unity.

In Unity, I quickly realized that many tools required their humanoid avatar system, which was too specific for my design. Instead, I implemented the FABRIK algorithm and created a spring-based ground collision model to help the character walk on stairs and add wall-running mechanics. However, as the semester progressed, I had to pause the project.

![Crucible Animation 1](https://github.com/tibormester/EndlessRPG/assets/67936278/d4d2cde1-c196-454d-ad3d-754eeb0c9c3c)

![Crucible Animation 2](https://github.com/tibormester/EndlessRPG/assets/67936278/b5947b28-d26b-4ae0-8f54-376a636938ce)

---

### **Endless - 2D Procedural RPG**

#### *Back to Godot*

As I returned to the project, Unity’s pricing changes made me decide to restart in Godot, taking advantage of its strong 2D inverse kinematics support.

![Endless Animation 1](https://github.com/tibormester/tibormester.github.io/blob/master/2dIK.mov)

#### *Wave Function Collapse Terrain Generation*

During the previous school semester, I studied AI, particularly constraint satisfaction problems, and implemented the Wave Function Collapse algorithm to procedurally generate 2D terrain. I treated each chunk of the world as a constraint satisfaction problem, trying to align chunk boundaries with adjacent chunks. It wasn’t perfect, but it worked for the time being.

![Endless Animation 1](https://github.com/tibormester/tibormester.github.io/blob/master/wfc.mov)

#### *Learning AI in a Simulation Game*

For the gameplay, I was inspired by *Rimworld* and focused on procedural content instead of a handcrafted narrative. I created a simulation where AI characters with basic needs perform tasks to satisfy their needs, with emergent stories. 

I plan on implementing a system where needs and tasks have weights that modify their priority. An individual will mutate their weights away from the species template, and upon death, a fitness score will be calculated and used to update the template through reinforcement learning.

![Endless Simulation](https://github.com/tibormester/tibormester.github.io/blob/master/huntingAI.mov)

#### *Rotating Sprites in 3D in 2D*

To address asymmetry in top-down abilities, I kept 2D sprites but used shear transforms to make them appear rotated in 3D. This solution worked well, but the left-right mirroring issue remained when swapping sides.

![Endless Animation](https://github.com/tibormester/tibormester.github.io/blob/master/2d3drotation.mov)

#### *Back to 3D and Implementing FABRIK in Godot*

Eventually, I realized that a physical organ system would be best experienced in 3D since aiming in 2D has fewer degrees of freedom. With my prior experience coding FABRIK in Unity, it was easy to implement it into Godot.

![Endless 3D](https://github.com/tibormester/tibormester.github.io/blob/master/fabrikGodot.mov)

---

### **Rogue Royale - 2D Battle Royale**

#### *Scaling Down and Focusing on Scope*

Despite progress on the procedural RPG, I decided to scale down the project. I created a 2D Battle Royale game that is PvPvE inspired by *League of Legends*, focusing on both combat and PVE elements. The core mechanics were simple to code but allowed room for complexity. I quickly implemented a character controller, modular attack combos, projectile weapons, and status effects.

![Rogue Royale](https://github.com/tibormester/tibormester.github.io/blob/master/rogueRoyale.mov)

#### *Multiplayer Rollback through ENet and Steam*

I made a mistake in assuming that multiplayer would be easy. Although I got clients on the same machine to play through ENet, when using Steam to play across machines, I quickly ran into desync issues. To fix this, I implemented rollback net code, rewriting all of the code, but bugs persisted.

![Rogue Royale](https://github.com/tibormester/tibormester.github.io/blob/master/multiplayer2.mov)

---

### **Sinking Labyrinth - 2D Rogue-like**

Wanting to release something on Steam before graduation, I paused multiplayer work and returned to my roots of procedural generation. I turned the *League of Legends* inspired project into a rogue-like game where players are chased up a tower, avoiding obstacles like rising water and falling ceilings while fending off monsters. While there are still a few mechanics missing and polishing to do, it's almost ready for release.

![Sinking Labyrinth](https://github.com/tibormester/tibormester.github.io/blob/master/labyrinth.mov)

---

### **Bug Souls - 3D Action RPG**

In my final college semester, I’m working with a team on *Bug Souls*, an action RPG inspired by *Dark Souls*. In the game, you play as a bug climbing a tree. In class, we discussed different types of play and narrative design. And I think we did a pretty good job of putting our lessons into practice: Most notably, we are evoking a sense of vertigo due to the shrunk scale and nonstandard gravity (the player sticks to the branches).

Collaborating with my four teammates has been a rewarding experience. Working in a team not only allows us to share expertise but also fosters a sense of camaraderie. In my solo projects, I often felt demoralized when I made slow progress. However, with Bug Souls, we support each other through rough patches.

---

### **Data Structures**

- [AVL Tree](https://github.com/tibormester/tibormester.github.io/blob/master/avl.py) - An AVL tree is a self-balancing Binary Search Tree (BST) that uses rotations to maintain balance.
- [Binary Search Tree](https://github.com/tibormester/tibormester.github.io/blob/master/bst.py) - A standard BST implementation that tracks key counts, incremented and decremented through insertion and deletion.
- [B Tree](https://github.com/tibormester/tibormester.github.io/blob/master/btree.py) - A type of BST optimized for dense data storage and efficient access to neighboring values.
- [KD Tree](https://github.com/tibormester/tibormester.github.io/blob/master/kd.py) - A multi-dimensional approach to BSTs, often used in game engines for storing physics objects.
- [Skip List](https://github.com/tibormester/tibormester.github.io/blob/master/skiplist.py) - A linked list variant that supports O(log n) search complexity, combining BST and Linked List functionality.
- [Splay Tree](https://github.com/tibormester/tibormester.github.io/blob/master/splay.py) - A self-balancing BST that uses splay operations to maintain balance.

---

### **Algorithms**

- [Mixed Nash Equilibrium Solver](https://github.com/tibormester/tibormester.github.io/blob/master/Mixed.java) - A solver for the Mixed Nash Equilibrium, a game theory concept where no player can improve their outcome by changing their strategy alone.


- [Expected Value](https://github.com/tibormester/tibormester.github.io/blob/master/expectation.py) - A simple script to compute the expected value for game theory problems.
- [Reversi Competition](https://github.com/tibormester/tibormester.github.io/blob/master/reversi.py) - A project where we competed against other teams in Reversi, using algorithms that account for both our and the opponent’s possible moves.

---

### **Other**

- [Blackjack](https://github.com/tibormester/tibormester.github.io/blob/master/Blackjack.java) - A simple Java-based Blackjack game against the Computer Dealer.
- [Projective Geometry Presentation.pptx](https://github.com/tibormester/tibormester.github.io/files/14003304/Projective.Geometry.Presentation.pptx) - A slide deck for a presentation I gave on the applications of projective geometry in computer graphics.
