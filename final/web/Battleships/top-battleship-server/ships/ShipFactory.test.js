import { describe, test, expect } from "@jest/globals";
import {
  BATTLESHIP,
  CARRIER,
  CRUISER,
  DESTROYER,
  SUBMARINE,
  ShipFactory,
} from "./ShipFactory";
import { Ship } from "./Ship";
import { MAX_SHIP_SIZE, MIN_SHIP_SIZE } from "./sizes";
import { INVALID_SIZE, INVALID_NAME } from "./constants";

describe("ShipFactory", () => {
  describe("constructor", () => {
    test("should create a ship factory", () => {
      const shipFactory = new ShipFactory(1, "test");
      expect(shipFactory).toBeDefined();
      expect(shipFactory.size).toBe(1);
      expect(shipFactory.name).toBe("test");
    });
    test("should throw an error if the size is not provided", () => {
      expect(() => new ShipFactory()).toThrow(new Error(INVALID_SIZE));
    });
    test("should throw an error if the name is not provided", () => {
      expect(() => new ShipFactory(5)).toThrow(new Error(INVALID_NAME));
    });
    test("should throw an error if the size is not between 1 and 5", () => {
      expect(() => new ShipFactory(MIN_SHIP_SIZE - 1)).toThrow(
        new Error(INVALID_SIZE)
      );
      expect(() => new ShipFactory(MAX_SHIP_SIZE + 1)).toThrow(
        new Error(INVALID_SIZE)
      );
    });
  });

  describe("getSize", () => {
    const shipFactory = new ShipFactory(5, "test");
    test("should return the size of the ship", () => {
      expect(shipFactory.getSize()).toBe(5);
    });
  });

  describe("getName", () => {
    const shipFactory = new ShipFactory(5, "test");
    test("should return the name of the ship", () => {
      expect(shipFactory.getName()).toBe("test");
    });
  });

  describe("createShip", () => {
    const shipFactory = new ShipFactory(5, "test");
    test("should create a ship", () => {
      const ship = shipFactory.createShip();
      expect(ship).toBeDefined();
      expect(ship instanceof Ship).toBeTruthy();
      expect(ship.size).toBe(5);
      expect(ship.name).toBe("test");
      expect(ship.is_sunk).toBe(false);
      expect(ship.life).toBe(5);
    });
  });
});

describe("Default Ships", () => {
  describe("Carrier", () => {
    test("should create a ship with a size of 5", () => {
      expect(CARRIER.size).toBe(5);
    });
    test("should create a ship with a name of Carrier", () => {
      expect(CARRIER.name).toBe("Carrier");
    });
  });

  describe("Battleship", () => {
    test("should create a ship with a size of 4", () => {
      expect(BATTLESHIP.size).toBe(4);
    });
    test("should create a ship with a name of Battleship", () => {
      expect(BATTLESHIP.name).toBe("Battleship");
    });
  });

  describe("Cruiser", () => {
    test("should create a ship with a size of 3", () => {
      expect(CRUISER.size).toBe(3);
    });
    test("should create a ship with a name of Cruiser", () => {
      expect(CRUISER.name).toBe("Cruiser");
    });
  });

  describe("Submarine", () => {
    test("should create a ship with a size of 3", () => {
      expect(SUBMARINE.size).toBe(3);
    });
    test("should create a ship with a name of Submarine", () => {
      expect(SUBMARINE.name).toBe("Submarine");
    });
  });

  describe("Destroyer", () => {
    test("should create a ship with a size of 2", () => {
      expect(DESTROYER.size).toBe(2);
    });
    test("should create a ship with a name of Destroyer", () => {
      expect(DESTROYER.name).toBe("Destroyer");
    });
  });
});
