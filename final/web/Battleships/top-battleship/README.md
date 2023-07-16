## The Odin Project

# Project: Battleship game

[**Live version** of the game can be found here](https://renchester.github.io/top-battleship/)

This is a digital recreation of the classic **Battleship** game, where two players battle it out to sink all their opponent's ships first. Built with Javascript, HTML, and Sass.

This project served as a starting point to implement _test-driven development_. The functions / features involving the public interface were tested using **Jest** as the test runner.

### Improvements

At present, the computer player only randomly chooses squares when attacking.

The main focus for improving this game is to add an algorithm to make the computer player play 'naturally' like a human being would. This involves clicking the squares surrounding the previously clicked square if the square turns out to have a ship. Once one of the surrounding squares turns to have a ship as well, the computer would traverse that axis until the ship is sunken.

### Getting Started

In order to setup and work on this project on your own, you will need to:

1. Clone this project:  
   `git clone https://github.com/renchester/top-battleship.git`

2. Once you have cloned this project, you can install the required dependencies by using:  
   `npm install`

3. A live demo of the project can be started by using:  
   `npm start`

4. Distribution files can be produced using:  
   `npm run build`

### Deployed on GitHub Pages

Deployed on [GitHub Pages](https://pages.github.com/)

### Display

![Ship placement screen  (Light Mode)](/img/ship-placement-view-light-mode.png)
Ship placement screen (_Light Mode_)

![Game screen  (Dark Mode)](/img/game-view-dark-mode.png)
Game screen (_Dark Mode_)

---

Developed by **Renchester Ramos**
