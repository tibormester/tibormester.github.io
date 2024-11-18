# Portfolio

**Table Of Contents**

**My Journey Into Game Development**
* [Background](https://github.com/tibormester/tibormester.github.io/blob/master/README.md?#33)
* [Crucible - 3D Procedural RPG ](https://github.com/tibormester/tibormester.github.io/blob/master/README.md?#L57)
* [Endless - 2D Procedural RPG](https://github.com/tibormester/tibormester.github.io/blob/master/README.md?#L76)
* [Rogue Royale - 2D Battle Royale](https://github.com/tibormester/tibormester.github.io/blob/master/README.md?#L112)
* [Sinking Labryinth - 2D Rogue-like](https://github.com/tibormester/tibormester.github.io/blob/master/README.md?#L139)
* [Bug Souls - 3D Action RPG](https://github.com/tibormester/tibormester.github.io/blob/master/README.md?#L135)
  
**Data Structures**
* [AVL Tree](https://github.com/tibormester/tibormester.github.io/blob/master/avl.py) An AVL tree is a BST that self balances through rotations
* [Binary Search Tree](https://github.com/tibormester/tibormester.github.io/blob/master/bst.py) An implementation of a standard BST that tallies key counts that can be incremented and decremented through insertion and deletion
* [B Tree](https://github.com/tibormester/tibormester.github.io/blob/master/btree.py) Similar to a BST, but has several keys and values per node enabling denser data storage as well as easy access to neighboring values
* [KD Tree](https://github.com/tibormester/tibormester.github.io/blob/master/kd.py) A multi-dimensional approach to a BST that is often used in game engines for storing physics objects
* [Skip List](https://github.com/tibormester/tibormester.github.io/blob/master/skiplist.py) A variation of a linked list that at the cost of space enables O(log n) search complexity. Basically a BST and Linked List together.
* [Splay Tree](https://github.com/tibormester/tibormester.github.io/blob/master/splay.py) A BST that stays balanced by requiring splay operations. This is done through mathematical magic.

**Algorithms**
* [Mixed Nash Equilibrium Solver](https://github.com/tibormester/tibormester.github.io/blob/master/Mixed.java) Mixed Nash Equilibrium is a concept in game theory that represents a state where no agent can unilaterally change their choice of action for a better outcome
* [Expected Value](https://github.com/tibormester/tibormester.github.io/blob/master/expectation.py) Just a simple script to compute the expected value for a Game Theory Homework problem
* [Reversi Competition](https://github.com/tibormester/tibormester.github.io/blob/master/reversi.py) A group project where we compete against other groups in a game of reversi. Our algorithm picks the best move by calculating not only the payoff of its turn but the best move for the opponent given our move

**Other**
* [Blackjack](https://github.com/tibormester/tibormester.github.io/blob/master/Blackjack.java) A simple Java project to play blackjack against the Computer Dealer
* [Projective Geometry Presentation.pptx](https://github.com/tibormester/tibormester.github.io/files/14003304/Projective.Geometry.Presentation.pptx) Slides for a minor presentation I gave on Applications of Projective Geometry for Computer Graphics, which I gave during my course in Euclidean and Non-Euclidean Geometry

**My Journey Into Game Development**

**Background**

*Scratch and Mobile Games*

My journey into Game Dev started with Scratch, it's a drag-and-drop engine but I think that's fair considering I was still in elementary school. And eventually, I was even able to use my familiarity with the engine to win the Game Programming event at my State’s High School Science Olympiads competition.
My first real experience with non-drag-and-drop programming came during my summers during middle school. My cousins and I would meet in person or over Skype to design and develop mobile games. Over the years, we managed to release four apps on the Apple App Store and two on Google Play.

https://falling-cats-on-pug.apk.dog

*Changing Careers*

At first, I didn’t take game development seriously as a career path—I viewed it as play not work. When I entered college at the University of Maryland, I was a math and physics major, with probably the slightly too ambitious dream of one day following in the footsteps of someone like Einstein.

I came to college with a lot of credits, so I jumped straight into the upper-level classes. It was humbling. I was no longer at the top of my class, and I realized that to truly excel, I would need to live and breathe physics. After some serious soul-searching, I realized that while I loved physics, I couldn’t make it my life.

Crafting a game that can entertain people seems far more fulfilling than publishing papers that might only be read by a handful of people in academia. So, for the past year and a half, I’ve been working through my computer science degree, while also self-studying game development and design.

*Picking Game Engines*

When I finally made the career pivot, I started by experimenting with engines.

I first tried using JMonkeyEngine and LibGDX since I was really into the idea of building my own game engine back in middle school and wanted to start from the ground up. But I quickly realized that I’d rather focus on developing fun and novel gameplay mechanics than worry about reinventing the wheel.

Eventually, I settled on Godot because its documentation is the best, it being free was also a huge plus. 

**Crucible - 3D Procedural RPG**

*Procedural Mesh and Terrain Generation*

My first big project started with the idea of creating a completely procedurally generated game. I didn't want to get distracted from fun mechanics by messing with assets.

I started with some tutorials on mesh and terrain generation, first creating a hexagonal mesh, applying noise to generate mountainous terrain, and then using shaders to modify the appearance of the terrain.

insert image here

*Character Controller and Procedural Animations*

Once the terrain was ready, my next challenge was creating a character controller with procedural animations. Initially, I tried using Godot’s built-in physics engine and inverse kinematics systems, but I struggled. My vision was to create a ballistics system like in War Thunder, but for organs and body parts, with animations adjusting accordingly and in an active ragdoll. Unfortunately, the physics engine and the deprecated inverse kinematics tools in Godot didn’t make it easy, so I decided to switch to Unity.
In Unity, I quickly realized a lot of the tools require the use of their humanoid avatar system, which was too specific for my design, so instead, I implemented the FABRIK algorithm myself. I also created a spring-based ground collision model to help the character walk on stairs and added wall-running mechanics. However, as the semester progressed and my school workload grew, I had to pause the project.

https://github.com/tibormester/EndlessRPG/assets/67936278/d4d2cde1-c196-454d-ad3d-754eeb0c9c3c

https://github.com/tibormester/EndlessRPG/assets/67936278/b5947b28-d26b-4ae0-8f54-376a636938ce

**Endless - 2D Procedural Game RPG**

*Back to Godot*

Just as I found the time to return to the project, Unity made changes to its pricing model, so I decided to restart in Godot. This time, I planned on taking advantage of the strong support they have for 2D inverse kinematics.

insert gif here

*Wave Function Collapse Terrain Generation*

During the semester break, I had been studying AI, specifically constraint satisfaction problems, which is a generalization of the Wave Function Collapse algorithm. I implemented this to procedurally generate 2D terrain by treating each chunk of the world as a constraint satisfaction problem. The goal was to save the chunks as constraints and generate them deterministically.

However, I ran into several challenges. For instance, getting chunk boundaries to align with adjacent chunks proved difficult, especially when circling around unloaded chunks. Through trial and error, I was able to reduce most of these issues, though I wasn’t fully satisfied with the output or runtime. But it was good enough for now.

insert gif here

*Learning AI in a Simulation Game*

For the gameplay mechanics, I was inspired by Rimworld and instead of focusing on a handcrafted narrative, I again wanted to go procedural. I started working on a simulation where the world would be populated by AI characters with basic needs and tasks that would create an emergent story. These characters have different need meters that fall over time, requiring them to perform actions to refill them. Each need and action has a weight applied to its base urgency and predicted net need outputs. I plan on having individuals mutate these weights away from the species template, and at the end of their lives, a fitness score is calculated and used to update the species template. This would make species behaviors use reinforcement learning over time, so that they could adapt to changes in the environment.

insert gif here

*Rotating Sprites in 3D in 2D*

Before iterating on the AI learning aspect, I needed to finish the ability system so I had some variety to test with. I wanted the game to be top-down, with abilities cast in any direction. Since abilities are collision-based, this creates an asymmetry between the top vs. bottom of the screen (as opposed to left vs. right). Looking back, I think this could lead to emergent strategies in gameplay that I plan on revisiting, but at the time, I saw it as an issue. My first thought was that I needed to make the game fully top-down. An orthographic top-down view would’ve been easy to implement, but it would also hide all the character limbs, making it difficult to see the variation in characters.

So, my second solution was to keep the 2D billboard sprites and shear their transforms to make them appear as if they were rendered and rotated in 3D. This worked surprisingly well, except when swapping sides, the left and right sides would get mirrored.

insert gif here

*Back to 3D and implementing FABRIK in Godot*

Eventually, I concluded that a physical organ system would be best interacted with in 3D like I originally planned because aiming in 2D just isn’t the same. And with my experience working on procedural animations in Unity, it was a breeze getting it working in Godot.

insert gif here

**Rogue Royale - Battle Royale 2D**

*Scaling Down and Focusing on Scope*

Despite the progress I was making, the procedural game was far from finished and I realized my aversion to creating and using assets was making things more difficult for myself. So I decided to come up with a new design with a more focused scope: a 2D battle royale with both combat and PVE elements, inspired by League of Legends. 

The core combat mechanics had some mechanical depth but were surprisingly simple to implement, and I was able to quickly assemble a character controller with modular attack combos, projectile weapons, and status effects.

insert gif here

*Multiplayer Rollback through ENet and Steam*

But where I made a mistake was assuming that adding multiplayer would be a plug-and-play type of situation. When testing two clients locally, everything worked fine. However once I tried connecting different machines over Steam, I realized that desync issues made the game unplayable. 
To fix these issues, I eventually settled on implementing rollback net code, except I had to rewrite everything, and even then there were still many bugs. 

insert gif here

**Sinking Labyrinth - 2D Roguelike**

Wanting to get something on Steam before graduation, I decided to put polishing multiplayer on pause and returned to my roots of procedural generation. I kept the League of Legends inspired ability system and transformed the project into a rogue-like game where players race up a tower, avoiding obstacles like rising water and falling ceilings, while also fending off a minotaur. The game is missing a few mechanics and needs a lot of polish, but should be released soon.

insert gif here

**Bug Souls - Action RPG**

Now, in my final semester of undergrad, I’m a member of a team in my Game Programming class. We are working on a demo for our game called Bug Souls, an action RPG inspired by Dark Souls. In the game, you play as a bug climbing a tree, and we’re experimenting with unique mechanics, like throwable objects that orbit the tree due to gravity relative to the branches. This mechanic allows for trick shots and sneak attacks during boss fights. 

I voted for the RPG genre because I wanted to lean into using assets and environmental design to create a compelling narrative. In class, we discussed different types of play and narrative design. And I think we did a pretty good job of putting our lessons into practice.

Collaborating with my four teammates has been a rewarding experience. Working in a team not only allows us to share expertise but also fosters a vital sense of camaraderie. In my solo projects, I often felt demoralized when I made slow progress. However, with Bug Souls, we support each other through rough patches, alleviating the stresses that come with working on large projects.


