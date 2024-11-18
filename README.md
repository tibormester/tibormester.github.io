# Portfolio

[![Game Dev Journey](https://img.youtube.com/vi/KM_zEdRPphk/0.jpg)](https://www.youtube.com/watch?v=KM_zEdRPphk)

**About Me**

I am a senior Computer Science and Math student at the University of Maryland expecting to graduate in the Fall of 2025. Originally, I was a Physics major and wanted to pursue a career in academia and learn more about the mechanics underlying our universe. However, I believe a career in software development will be more rewarding, enabling me to lean more heavily into my creative side. 

I have a passion for games, not only playing them, but I enjoy learning more about game engine design as well as techniques that push the limits of what is technically possible in gaming. On the other hand, the main appeal to game development for me personally is the ability to create a digital world without restrictions. Recently I have set the goal for myself to learn game development and more specifically Unity by creating a game for myself. Although I hope the game, *[Endless RPG](https://github.com/tibormester/EndlessRPG)*, will be a success eventually, for now, it is still a hobby and a means of practicing new skills. 

**Table Of Contents**

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


**Unity** 
**Endless RPG**

For this project, I have avoided using assets. In hindsight, this has been quite the delay as I have had to learn to create these assets through script, which is a lot harder than anticipated. However, it has been quite rewarding and has helped me better understand *Unity* as an engine. The idea of avoiding assets was primarily to make things easier for the procedural generation of the characters. The obvious approach in hindsight is to have assets for each body part and scale them a bit as well as pick randomly from a pool of them for variation. However, I decided to simply sketch them out as a bunch of quadrilaterals defining their dimensions at varying heights and quickly creating meshes from that data. This method gives me more control over the mesh data itself, but that level of control isn't necessary. Especially since a lot of runtime tweaks to the mesh will be done with shaders regardless and having each body part as a separate mesh instead of a skinned mesh might have been simpler for things like dismemberment... So all that said, I will likely maintain this workflow of sketching out models as basic geometric shapes through code and when this project reaches the polishing stage I will aim to hire an artist to create assets and refactor this code.
 
 Part of creating the mesh was learning that *Unity* doesn't seem to want people doing too much animating through script. Sure creating the mesh itself is fine and documented enough, but both the legacy and new animation systems are a struggle to get working without prebuilt animation assets. And even then they seem to lack libraries for generating more complex animation curves on the fly. As a result, I am setting out to simply ignore the animation systems and write my own self-contained animation components for objects that need it. Part of this is using IK specifically FABRIK and Trig for 2-bone IK. This will make it easier to incorporate more dynamic animations since it should come more naturally; however, I have started to notice it also leads to more convoluted systems without the easy-to-use state machine GUI. I hope to resolve this issue soon (As well as implement rotations, constraints, and blending/multi chains to my Fabrik algorithm).
 
https://github.com/tibormester/EndlessRPG/assets/67936278/d4d2cde1-c196-454d-ad3d-754eeb0c9c3c
  
**Character Controller**

So for a character, I have a rigid body with rotation locked and no gravity that is pushed around by forces. Although there is a box collider as a hitbox for the character, it remains floating above a pair of ray casts, one straight down, and another in the direction of motion (clamped to 45 degrees). These ray casts look for the ground and when found linearly phase out gravity while introducing a spring force with velocity dampening that aims to keep the boxcollider hoovering. The result is that going over minor bumps and debris is done seamlessly without constant raytracing for collisions to step over. The downside for some applications is that the character controller might feel slightly floaty and may bounce, but by tweaking dampening values and spring strength I was able to achieve a result that feels decent. Additionally, the responsiveness of the character controller was later fixed after I implemented forces that dampen velocity in non-movement input directions.
 
 All in all, there are a few of the very basic movement features: jumping/doubling jumping, turning the body towards movement while turning the head towards the camera, rotating to be normal to surfaces, and instant changes in directions and drag. This all creates a physics-based controller that feels pretty responsive, which is ideal. Implementing these features sounds simple, and it is; however, after starting this project and going through this phase a handful of times, no two attempts have been the same. Fine-tuning and tweaking decisions made on the character controller is a complex topic that will need more polish and is currently beyond my limited experience. (Animations are placeholder)

https://github.com/tibormester/EndlessRPG/assets/67936278/b5947b28-d26b-4ae0-8f54-376a636938ce
