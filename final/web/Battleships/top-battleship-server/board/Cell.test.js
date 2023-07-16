import { describe, expect, test } from "@jest/globals";
import { Ship } from "../ships/Ship";
import { Cell } from "./Cell";
import { CELL_ALREADY_HIT_ERROR, CELL_OCCUPIED_ERROR } from "./constants";

describe("Cell", () => {
  const testShip = new Ship(1, "test");
  describe("constructor", () => {
    test("should create a cell with no ship by default", () => {
      const cell = new Cell();
      expect(cell.ship).toBeNull();
    });
    test("should create a cell with a ship", () => {
      const cell = new Cell(testShip);
      expect(cell.ship).toBe(testShip);
    });
    test("should create a cell that has not been hit by default", () => {
      const cell = new Cell();
      expect(cell.isHit).toBeFalsy();
    });
    test("should create a cell that has not been hit", () => {
      const cell = new Cell(null, false);
      expect(cell.isHit).toBeFalsy();
    });
    test("should create a cell that has been hit", () => {
      const cell = new Cell(null, true);
      expect(cell.isHit).toBeTruthy();
    });
  });

  describe("placeShip", () => {
    test("should place a ship in the cell", () => {
      const cell = new Cell();
      expect(cell.ship).toBeNull();
      cell.placeShip(testShip);
      expect(cell.ship).toBe(testShip);
    });
    test("should throw an error if the cell is already occupied", () => {
      const cell = new Cell(testShip);
      expect(() => cell.placeShip(testShip)).toThrow(
        new Error(CELL_OCCUPIED_ERROR)
      );
    });
  });

  describe("getShip", () => {
    test("should return the ship in the cell", () => {
      const cell = new Cell(testShip);
      expect(cell.getShip()).toBe(testShip);
    });
    test('should return "null" by default if the cell is empty', () => {
      const cell = new Cell();
      expect(cell.getShip()).toBeNull();
    });
    test("should return null if the cell is empty", () => {
      const cell = new Cell(null);
      expect(cell.getShip()).toBeNull();
    });
  });

  describe("isHit", () => {
    test("should return true if the cell has been hit", () => {
      const cell = new Cell(null, true);
      expect(cell.wasHit()).toBeTruthy();
    });
    test("should return false if the cell has not been hit", () => {
      const cell = new Cell(null, false);
      expect(cell.wasHit()).toBeFalsy();
    });
    test("should return false by default if the cell has not been hit", () => {
      const cell = new Cell();
      expect(cell.wasHit()).toBeFalsy();
    });
  });

  describe("hit", () => {
    test("should hit the cell", () => {
      const cell = new Cell(null, false);
      expect(cell.wasHit()).toBeFalsy();
      cell.hit();
      expect(cell.wasHit()).toBeTruthy();
    });
    test("should throw an error if the cell has already been hit", () => {
      const cell = new Cell(null, true);
      expect(() => cell.hit()).toThrow(new Error(CELL_ALREADY_HIT_ERROR));
    });
    test("should hit the ship in the cell", () => {
      const cell = new Cell(testShip, false);
      expect(cell.getShip().life).toBe(1);
      cell.hit();
      expect(cell.getShip().life).toBe(0);
    });
    afterEach(() => {
      testShip.reset();
    });
  });
});
