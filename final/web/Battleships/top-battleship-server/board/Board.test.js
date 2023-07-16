import { describe, expect, test } from "@jest/globals";
import { Board } from "./Board";
import { Ship } from "../ships/Ship";
import {
  BOARD_INVALID_POSITION,
  BOARD_OUT_OF_BOUNDS,
  BOARD_SIZE,
  CELL_ALREADY_HIT_ERROR,
} from "./constants";

describe("Board", () => {
  describe("constructor", () => {
    test("should create a board with the default size", () => {
      const board = new Board();
      expect(board.getSize()).toBe(BOARD_SIZE);
      expect(board.board.length).toBe(BOARD_SIZE);
      expect(board.board[0].length).toBe(BOARD_SIZE);
      expect(board.ships.size).toBe(0);
    });
    test('should create a board with the size "20"', () => {
      const board = new Board(20);
      expect(board.getSize()).toBe(20);
      expect(board.board.length).toBe(20);
      expect(board.board[0].length).toBe(20);
      expect(board.ships.size).toBe(0);
    });
  });
  describe("createBoard", () => {
    const board = new Board();
    test("should create a board with the default size", () => {
      const innerBoard = board.createBoard();

      expect(innerBoard.length).toBe(BOARD_SIZE);
      expect(innerBoard[0].length).toBe(BOARD_SIZE);

      for (let i = 0; i < BOARD_SIZE; ++i) {
        for (let j = 0; j < BOARD_SIZE; ++j) {
          const cell = innerBoard[i][j];
          expect(cell).toBeDefined();
          expect(cell.wasHit()).toBeFalsy();
          expect(cell.getShip()).toBeNull();
        }
      }
    });
  });
  describe("getSize", () => {
    const board = new Board();
    const customSize = 20;
    const boardWithCustomSize = new Board(customSize);
    test("should return the size of the board", () => {
      expect(board.getSize()).toBe(BOARD_SIZE);
    });
    test("should return the size of the custom board", () => {
      expect(boardWithCustomSize.getSize()).toBe(customSize);
    });
  });

  describe("placeShip", () => {
    let board;
    const ship = new Ship(3, "test");
    beforeEach(() => {
      board = new Board();
    });
    test("should place a ship on the board horizontally", () => {
      board.placeShip(ship, 0, 0, false);
      expect(board.ships.size).toBe(1);
      expect(board.ships.has(ship)).toBeTruthy();
    });
    test("should place a ship on the board vertically", () => {
      board.placeShip(ship, 0, 0, true);
      expect(board.ships.size).toBe(1);
      expect(board.ships.has(ship)).toBeTruthy();
    });
    test("should throw an error if the ship is out of bounds at the bottom left corner", () => {
      expect(() => board.placeShip(ship, 0, BOARD_SIZE - 1, false)).toThrow();
    });
    test("should throw an error if the ship is out of bounds at the top right corner", () => {
      expect(() => board.placeShip(ship, BOARD_SIZE - 1, 0, true)).toThrow();
    });
    test("should throw an error if the ship is out of bounds at the bottom right corner", () => {
      expect(() =>
        board.placeShip(ship, BOARD_SIZE - 1, BOARD_SIZE - 1, true)
      ).toThrow();
    });
    test('should throw an error if there already is a ship at the position "0, 0"', () => {
      board.placeShip(ship, 0, 0, false);
      expect(() => board.placeShip(ship, 0, 0, false)).toThrow(
        BOARD_INVALID_POSITION
      );
    });
    test('should throw an error if there already is a ship at the position "0, 1"', () => {
      board.placeShip(ship, 0, 0, false);
      expect(() => board.placeShip(ship, 1, 0, true)).toThrow(
        BOARD_INVALID_POSITION
      );
    });
  });

  describe("isOutOfBounds", () => {
    const board = new Board();
    test('should return "true" if the position is out of bounds', () => {
      expect(board.isOutOfBounds(0, BOARD_SIZE)).toBeTruthy();
      expect(board.isOutOfBounds(BOARD_SIZE, 0)).toBeTruthy();
      expect(board.isOutOfBounds(BOARD_SIZE, BOARD_SIZE)).toBeTruthy();
      expect(board.isOutOfBounds(-1, 0)).toBeTruthy();
      expect(board.isOutOfBounds(0, -1)).toBeTruthy();
      expect(board.isOutOfBounds(-1, -1)).toBeTruthy();
    });
    test('should return "false" if the position is not out of bounds', () => {
      for (let i = 0; i < BOARD_SIZE; ++i) {
        for (let j = 0; j < BOARD_SIZE; ++j) {
          expect(board.isOutOfBounds(i, j)).toBeFalsy();
        }
      }
    });
  });

  describe("isValidPosition", () => {
    const board = new Board();
    const ship = new Ship(3, "test");
    board.placeShip(ship, 0, 0, false);

    test('should return "true" if the position is valid', () => {
      expect(board.isValidPosition(0, 1, ship.getSize(), true)).toBeTruthy();
      expect(board.isValidPosition(0, 1, ship.getSize(), false)).toBeTruthy();
    });

    test('should return "false" if the position is not valid due to another ship', () => {
      for (let i = 0; i < ship.getSize(); ++i) {
        expect(board.isValidPosition(i, 0, 1, false)).toBeFalsy();
      }
    });

    test('should return "false" if the position is not valid due to being out of bounds', () => {
      expect(board.isValidPosition(0, BOARD_SIZE, 1, false)).toBeFalsy();
      expect(board.isValidPosition(BOARD_SIZE, 0, 1, true)).toBeFalsy();
      expect(
        board.isValidPosition(BOARD_SIZE, BOARD_SIZE, 1, true)
      ).toBeFalsy();
      expect(board.isValidPosition(-1, 0, 1, false)).toBeFalsy();
      expect(board.isValidPosition(0, -1, 1, true)).toBeFalsy();
      expect(board.isValidPosition(-1, -1, 1, true)).toBeFalsy();
    });
  });

  describe("isValidHorizontalPosition", () => {
    const board = new Board();
    const ship = new Ship(3, "test");
    board.placeShip(ship, 0, 0, false);

    test('should return "true" if the position is valid', () => {
      expect(
        board.isValidHorizontalPosition(0, 1, ship.getSize())
      ).toBeTruthy();
    });

    test('should return "false" if the position is not valid due to another ship', () => {
      for (let i = 0; i < ship.getSize(); ++i) {
        expect(board.isValidHorizontalPosition(i, 0, 1)).toBeFalsy();
      }
    });

    test('should return "false" if the position is not valid due to being out of bounds', () => {
      expect(board.isValidHorizontalPosition(0, BOARD_SIZE, 1)).toBeFalsy();
      expect(board.isValidHorizontalPosition(-1, 0, 1)).toBeFalsy();
      expect(board.isValidHorizontalPosition(-1, -1, 1)).toBeFalsy();
      expect(board.isValidHorizontalPosition(0, -1, 1)).toBeFalsy();
      expect(board.isValidHorizontalPosition(BOARD_SIZE, 0, 1)).toBeFalsy();
      expect(
        board.isValidHorizontalPosition(BOARD_SIZE, BOARD_SIZE, 1)
      ).toBeFalsy();
    });
  });

  describe("isValidVerticalPosition", () => {
    const board = new Board();
    const ship = new Ship(3, "test");
    board.placeShip(ship, 0, 0, true);

    test('should return "true" if the position is valid', () => {
      expect(board.isValidVerticalPosition(1, 0, ship.getSize())).toBeTruthy();
    });

    test('should return "false" if the position is not valid due to another ship', () => {
      for (let i = 0; i < ship.getSize(); ++i) {
        expect(board.isValidVerticalPosition(0, i, 1)).toBeFalsy();
      }
    });

    test('should return "false" if the position is not valid due to being out of bounds', () => {
      expect(board.isValidVerticalPosition(BOARD_SIZE, 0, 1)).toBeFalsy();
      expect(board.isValidVerticalPosition(0, BOARD_SIZE, 1)).toBeFalsy();
      expect(board.isValidVerticalPosition(-1, 0, 1)).toBeFalsy();
      expect(board.isValidVerticalPosition(0, -1, 1)).toBeFalsy();
      expect(board.isValidVerticalPosition(-1, -1, 1)).toBeFalsy();
      expect(
        board.isValidVerticalPosition(BOARD_SIZE, BOARD_SIZE, 1)
      ).toBeFalsy();
    });
  });

  describe("makeGuess", () => {
    let board, ship;
    beforeEach(() => {
      board = new Board();
      ship = new Ship(3, "test");
      board.placeShip(ship, 0, 0, true);
    });

    test("should return false if the guess is a miss", () => {
      // This tests for every square on the board that is not a ship
      for (let y = 0; y < BOARD_SIZE; ++y) {
        for (let x = 0; x < BOARD_SIZE; ++x) {
          if (x === 0 && y < 3) continue;
          expect(board.makeGuess(x, y)).toBeFalsy();
        }
      }
    });

    test("should return true if the guess is a hit", () => {
      // This tests for every square on the board that is a ship
      for (let i = 0; i < ship.getSize(); ++i) {
        expect(board.makeGuess(0, i)).toBeTruthy();
      }
    });

    test("should throw an error if the guess is out of bounds", () => {
      expect(() => board.makeGuess(0, BOARD_SIZE)).toThrowError(
        BOARD_OUT_OF_BOUNDS
      );
      expect(() => board.makeGuess(BOARD_SIZE, 0)).toThrowError(
        BOARD_OUT_OF_BOUNDS
      );
      expect(() => board.makeGuess(BOARD_SIZE, BOARD_SIZE)).toThrowError(
        BOARD_OUT_OF_BOUNDS
      );
      expect(() => board.makeGuess(-1, 0)).toThrowError(BOARD_OUT_OF_BOUNDS);
      expect(() => board.makeGuess(0, -1)).toThrowError(BOARD_OUT_OF_BOUNDS);
      expect(() => board.makeGuess(-1, -1)).toThrowError(BOARD_OUT_OF_BOUNDS);
    });

    test("should throw an error if the guess has already been made", () => {
      board.makeGuess(0, 0);
      expect(() => board.makeGuess(0, 0)).toThrowError(CELL_ALREADY_HIT_ERROR);
    });
  });

  describe("allShipsSunk", () => {
    let board, ship, ship2;
    beforeEach(() => {
      board = new Board();
      ship = new Ship(3, "test");
      ship2 = new Ship(2, "test2");
      board.placeShip(ship, 0, 0, true);
    });

    test("should return false if there are ships that have not been sunk", () => {
      expect(board.allShipsSunk()).toBeFalsy();
      board.makeGuess(0, 0);
      expect(board.allShipsSunk()).toBeFalsy();
      board.makeGuess(0, 1);
      expect(board.allShipsSunk()).toBeFalsy();
    });

    test('should return "true" if all ships have been sunk', () => {
      for (let i = 0; i < ship.getSize(); ++i) {
        board.makeGuess(0, i);
      }
      expect(board.allShipsSunk()).toBeTruthy();
    });

    test('should return "true" if all ships have been sunk and there are multiple ships', () => {
      board.placeShip(ship2, 0, 3, true);
      for (let i = 0; i < ship.getSize(); ++i) {
        board.makeGuess(0, i);
      }
      for (let i = 0; i < ship2.getSize(); ++i) {
        board.makeGuess(0, i + 3);
      }
      expect(board.allShipsSunk()).toBeTruthy();
    });

    test('should return "false" if all ships have been sunk except one', () => {
      board.placeShip(ship2, 0, 3, true);
      for (let i = 0; i < ship.getSize(); ++i) {
        board.makeGuess(0, i);
      }
      expect(board.allShipsSunk()).toBeFalsy();
    });
  });
});
