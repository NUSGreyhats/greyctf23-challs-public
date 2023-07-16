import { Cell } from "./Cell.js";
import {
    BOARD_ALL_SUNK,
    BOARD_INVALID_POSITION,
    BOARD_OUT_OF_BOUNDS,
    BOARD_SIZE,
    CELL_ALREADY_HIT_ERROR,
} from "./constants.js";

export class Board {
    /**
     * The constructor of the Board class
     * @param {number} size The size of the board in size * size. Defaults to BOARD_SIZE
     */
    constructor(size = BOARD_SIZE) {
        this.size = size;
        this.ships = new Set();
        this.board = this.createBoard();
    }

    /**
     * Creates a 2D array of size * size.
     * @returns {Array<Array<Cell>>}
     */
    createBoard() {
        const board = [];
        const size = this.getSize();
        for (let i = 0; i < size; ++i) {
            const row = [];
            for (let j = 0; j < size; ++j) row.push(new Cell());
            board.push(row);
        }
        return board;
    }

    /**
     * Returns the size of the board
     * @returns {number}
     */
    getSize() {
        return this.size;
    }

    /**
     * Places a ship on the board
     * @param {Ship} ship The ship to be placed on the board
     * @param {number} x The x coordinate of the top right square of the ship
     * @param {number} y The y coordinate of the top right square of the ship
     * @param {boolean} isVertical Whether the ship is vertical or not
     */
    placeShip(ship, x, y) {
        // Check if the ship is out of bounds at each end
        if (
            this.isOutOfBounds(x, y) ||
            (!ship.is_vertical && this.isOutOfBounds(x + ship.size - 1, y)) ||
            (ship.is_vertical && this.isOutOfBounds(x, y + ship.size - 1))
        )
            throw new Error(BOARD_OUT_OF_BOUNDS);

        // Check if the ship overlaps with another ship
        if (!this.isValidPosition(x, y, ship)) throw new Error(BOARD_INVALID_POSITION);

        // Add the ship if it is valid
        this.ships.add(ship);
        const size = ship.size;
        if (ship.is_vertical) {
            for (let i = 0; i < size; ++i) this.board[x][y + i].placeShip(ship);
        } else {
            for (let i = 0; i < size; ++i) this.board[x + i][y].placeShip(ship);
        }
        return true;
    }

    /**
     * Returns true if the given coordinates are out of bounds
     * @param {number} x The x coordinate of the square
     * @param {number} y The y coordinate of the square
     */
    isOutOfBounds(x, y) {
        return x < 0 || x >= this.getSize() || y < 0 || y >= this.getSize();
    }

    /**
     * Returns true if the selected position is valid for placing a ship
     * @param {number} x The x coordinate of the square
     * @param {number} y The y coordinate of the square
     * @param {Ship} ship The ship to place
     * @returns {boolean}
     */
    isValidPosition(x, y, ship) {
        if (this.isOutOfBounds(x, y)) return false;
        return ship.is_vertical
            ? this.isValidVerticalPosition(x, y, ship.size)
            : this.isValidHorizontalPosition(x, y, ship.size);
    }

    /**
     * Returns true if is valid horizontal position
     * @param {number} x The x coordinate of the square
     * @param {number} y The y coordinate of the square
     * @param {number} size The size of the ship
     * @returns {boolean}
     */
    isValidHorizontalPosition(x, y, size) {
        if (this.isOutOfBounds(x, y) || this.isOutOfBounds(x + size - 1, y)) return false;
        for (let i = 0; i < size; ++i) {
            const cell = this.board[x + i][y];
            if (cell.getShip() !== null) return false;
        }
        return true;
    }

    /**
     * Returns true if is valid vertical position
     * @param {number} x The x coordinate of the square
     * @param {number} y The y coordinate of the square
     * @param {number} size The size of the ship
     * @returns {boolean}
     */
    isValidVerticalPosition(x, y, size) {
        if (this.isOutOfBounds(x, y) || this.isOutOfBounds(x, y + size - 1)) return false;
        for (let i = 0; i < size; ++i) {
            const cell = this.board[x][y + i];
            if (cell.getShip() !== null) return false;
        }
        return true;
    }

    /**
     * Player makes a guess on the board. Returns true if it is a hit, false if it is a miss
     * @param {number} x The x coordinate of the square
     * @param {number} y The y coordinate of the square
     * @returns {bool} if it is a hit or not
     */

    makeGuess(x, y) {
        if (this.isOutOfBounds(x, y)) throw new Error(BOARD_OUT_OF_BOUNDS);
        const curr_cell = this.board[x][y];
        if (curr_cell.wasHit()) throw new Error(CELL_ALREADY_HIT_ERROR);
        curr_cell.hit();
        return curr_cell.getShip() !== null;
    }

    /**
     * Returns true if all the ships have been sunk
     * @returns {boolean}
     */
    allShipsSunk() {
        for (const ship of this.ships) {
            if (!ship.isSunk()) return false;
        }
        return true;
    }
}
