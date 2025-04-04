### Portfolio

---

#### **Table of Contents**
1. [My Journey Into Game Development](#my-journey-into-game-development)
   - [Mobile Game Dev](#mobile-game-dev)
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

##### *Mobile Game Dev*

My first real experience with non-drag-and-drop programming came during middle school summers (10-14 years old). My cousins and I would meet in person or over Skype to design and develop mobile games. Over the years, we managed to release four apps on the Apple App Store and two on Google Play. Most of the links are gone now

[Download Falling Cats on Pug](https://falling-cats-on-pug.apk.dog)

### **Crucible - 3D Procedural RPG**

#### *Procedural Mesh and Terrain Generation*

My first big project started 3 years ago during my Junior Year of Undergrad with the idea of creating a completely procedurally generated game. I didn’t want to get distracted by asset creation.

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

In my last college semester, I worked with a small team to make *Bug Souls*, an action RPG inspired by *Dark Souls*. In the game, you play as an ant fighting off the corrupting vine that animates corpses and threatens to choke out life as you know it.

![Bug Souls Demo Playthrough](https://youtu.be/h6drcPZ13dw)

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
