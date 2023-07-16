import { CELL_OCCUPIED_ERROR, CELL_ALREADY_HIT_ERROR } from "./constants.js";

export class Cell {
    /**
     * The constructor of the Cell class within the board
     * @param {Ship | null} ship the ship that is in the cell. Defaults to null
     * @param {Boolean} isHit whether the cell has been hit or not. Defaults to false
     */
    constructor(ship = null, isHit = false) {
        this.ship = ship;
        this.isHit = isHit;
    }

    /**
     * Place a ship in the cell
     * @param {Ship} ship the ship to be placed in the cell
     * @returns {void}
     */
    placeShip(ship) {
        if (this.ship !== null) throw new Error(CELL_OCCUPIED_ERROR);
        this.ship = ship;
    }

    /**
     * Returns the ship that is in the cell
     * @returns {Ship | null} the ship that is in the cell
     */
    getShip() {
        return this.ship;
    }

    /**
     * Returns true if the cell has been hit and false otherwise
     * @returns {Boolean} whether the cell has been hit or not
     */
    wasHit() {
        return this.isHit;
    }

    /**
     * Hit the cell
     * @returns {void}
     */
    hit() {
        if (this.wasHit()) throw new Error(CELL_ALREADY_HIT_ERROR);
        this.isHit = true;
        if (this.ship !== null) this.ship.hit();
    }
}
