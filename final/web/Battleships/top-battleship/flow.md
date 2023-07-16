# Project: Battleship

## Course Objective:

Introduce Test-driven Development and incorporate it into workflow

## Flow

### Model

- Create ship factory function

  - Props: name, length, hitPoints, coordinates, orientation, and isSunk

  - Methods:

    - hit = increases the number of hits to ship
    - sinkShip = if hitPoints is equal to length, make isShipSunk true

- Create Gameboard factory

  - Props: gridSize(default 10), state,

  - Methods:

    - `placeShip` places ships at specific coordinates

      - check if entire ship can fit in that space

    - `createBoard` creates grid of squares with each square containing coordinates

      - `boardState` is an array which contains objects / nodes for each square

      ```
      let j = 1

      for (i < gridSize ; i++)

          let square = createSquare(column = i; row = j)

          j <= gridSize ?
      ```

    - `receiveAttack (row, col)`

      - if square contains a ship, hit() ship
      - square.isHit = true

    - `fill (row, col)` makes square.filled = true
    - `findSquareWithID`
    - `findSquareWithRowCol`
    - `explodeShip`

- Create Player factory

  - Props: name, isPlaying(Boolean), board, ships, isWinner, lastThreeMoves

  - Methods:
    - `attack (row, col)` places a mark on a set of coordinates
    - `generateMove` for computer
      - if Player === computer then generateMove()

- Create Square factory

  - Props: row, col, coordinates, isHit, hasShip, shipName,

- Create Game module
  - Props: Players[], currentPlayer
  - Methods:
    - `goToNextPlayer`
    - `checkWinner`
    - `sendAttack`

### game controller

game init()

- create Game() module

  - auto create two Player(), one ai, one human
  - set each player.board to Board(10)
  - wait for human to place ships
    - human.ships = [carrier(5), battleship(4), submarine(3), destroyer(3), patrolBoat(2)]
    - if human.ships.every(ship.coordinates === ship.length) end placement / return
  - when human finishes placing ships, computer generates ship placements
    - computer randomly chooses a coordinate, checks if that coordinate is free, then places ship
    - once all ships are placed, start game

- start game

  - game.setCurrentPlayer(human)

    - human.isPlaying = true
    - ai.isPlaying = false

  - \*\*click on board([row, col])

    - player.attack(opponent, [row, col])
      - let square = opponent.board.findSquareWithRowCol(row, col)
      - square.filled = true
      - if square.hasShip
        - let targetShip = opponent.ships.find(ship on square(row, col))
        - targetShip.getHit()
        - if targetShip.isSunk
          - board.explodeShip(targetShip.coordinates)
            - pops all squares around ship
          - if opponent.ships.every(ship.isSunk),
            - game.currentPlayer.isWinner
            - human/player.isWinner
            - game.gamePlay = false

  - then, game.setCurrentPlayer(ai)
    - human.isPlaying = false
    - ai.isPlaying = true
  - \*\*then, computer generates attack()

        - if ai.lastThreeMoves.some(square.isHit && square.hasShip && !square.shipName.isSunk), then checkX or checkY
        - let squareToAttack
        - let num = Math.random \* boardsize
        - squareToAttack = human.board.findSquareWithID(num)
        - if squareToAttack.isHit, squareToAttack = generateAttack() (recursion)
        - if !squareToAttack.isHit,

          - squareToAttack.isHit
          - human.receiveAttack([row, col])

            - do all the receive attack contents

          - ai.lastThreeMoves.shift();
          - ai.lastThreeMoves.push(squareToAttack);

  - repeat until winner is found
  - start new game
