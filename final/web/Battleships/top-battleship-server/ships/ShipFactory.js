import { INVALID_SIZE, INVALID_NAME } from "./constants";
import { Ship } from "./Ship";
import { MAX_SHIP_SIZE, MIN_SHIP_SIZE } from "./sizes";

// Exported for testing purposes
export class ShipFactory {
  /**
   * The constructor of the Ship factory class
   * @param {number} size the size of the ship.
   * @param {String} name the name of the ship.
   */
  constructor(size, name) {
    if (size === undefined || size < MIN_SHIP_SIZE || size > MAX_SHIP_SIZE)
      throw new Error(INVALID_SIZE);
    if (name === undefined || name === "") throw new Error(INVALID_NAME);
    this.size = size;
    this.name = name;
  }

  /**
   * Returns the size of the ship.
   * @returns {number}
   */
  getSize() {
    return this.size;
  }

  /**
   * Returns the name of the ship
   * @returns {number}
   */
  getName() {
    return this.name;
  }

  /**
   * Create a new instance of the ship.
   * @returns {Ship}
   */
  createShip() {
    return new Ship(this.size, this.name);
  }
}

/// Create battleships
export const CARRIER = new ShipFactory(5, "Carrier");
export const BATTLESHIP = new ShipFactory(4, "Battleship");
export const CRUISER = new ShipFactory(3, "Cruiser");
export const SUBMARINE = new ShipFactory(3, "Submarine");
export const DESTROYER = new ShipFactory(2, "Destroyer");
