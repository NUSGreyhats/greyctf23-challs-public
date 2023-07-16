import { describe, test, expect } from "@jest/globals";
import { Ship } from "./Ship";
import { INVALID_NAME, INVALID_SIZE } from "./constants";

describe("Ship", () => {
  describe("constructor", () => {
    test("should create a ship with a size and a name", () => {
      const ship = new Ship(5, "test");
      expect(ship.size).toBe(5);
      expect(ship.name).toBe("test");
      expect(ship.is_sunk).toBe(false);
      expect(ship.life).toBe(5);
    });
    test("should throw an error if the size is not provided", () => {
      expect(() => new Ship()).toThrow(new Error(INVALID_SIZE));
    });
    test("should throw an error if the name is not provided", () => {
      expect(() => new Ship(5)).toThrow(new Error(INVALID_NAME));
    });
  });

  describe("getSize", () => {
    const ship = new Ship(5, "test");
    test("should return the size of the ship", () => {
      expect(ship.getSize()).toBe(5);
    });
  });

  describe("getName", () => {
    const ship = new Ship(5, "test");
    test("should return the name of the ship", () => {
      expect(ship.getName()).toBe("test");
    });
  });

  describe("reset", () => {
    let ship;
    beforeEach(() => {
      ship = new Ship(5, "test");
      ship.hit();
      ship.hit();
      ship.hit();
    });
    test("should reset the ship", () => {
      ship.reset();
      expect(ship.is_sunk).toBeFalsy();
      expect(ship.life).toBe(5);
    });
  });

  describe("isSunk", () => {
    let ship;
    beforeEach(() => {
      ship = new Ship(5, "test");
    });
    test("should return false if the ship is not sunk", () => {
      expect(ship.isSunk()).toBeFalsy();
      for (let i = 0; i < 4; i++) {
        ship.hit();
        expect(ship.isSunk()).toBeFalsy();
      }
    });
    test("should return true if the ship is sunk", () => {
      for (let i = 0; i < 5; i++) {
        ship.hit();
      }
      expect(ship.isSunk()).toBeTruthy();
    });
  });

  describe("hit", () => {
    let ship;
    beforeEach(() => {
      ship = new Ship(5, "test");
    });

    test("should decrement the life of the ship", () => {
      ship.hit();
      expect(ship.life).toBe(4);
    });

    test('should set "is_sunk" to true if the ship is sunk', () => {
      for (let i = 0; i < 5; i++) {
        expect(ship.life).toBe(5 - i);
        expect(ship.is_sunk).toBeFalsy();
        ship.hit();
      }
      expect(ship.is_sunk).toBeTruthy();
      expect(ship.life).toBe(0);
    });
  });
});
