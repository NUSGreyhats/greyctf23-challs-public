import { INVALID_NAME, INVALID_SIZE } from "./constants.js";

export class Ship {
    /**
     * The constructor of the Ship class
     * @param {Number} size the size of the ship
     * @param {String} name the name of the ship
     */
    constructor(size, name) {
        if (size === undefined || size <= 0) throw new Error(INVALID_SIZE);
        if (name === undefined) throw new Error(INVALID_NAME);
        this.size = size;
        this.name = name;
        this.is_sunk = false;
        this.is_vertical = false;
        this.life = size;
    }

    /**
     * Returns the size of the ship
     * @returns {Number} the size of the ship
     */
    getSize() {
        return this.size;
    }

    /**
     * Returns the name of the ship
     * @returns {String} the name of the ship
     */
    getName() {
        return this.name;
    }

    /**
     * Reset the ship instance
     * @returns {void}
     */
    reset() {
        this.is_sunk = false;
        this.life = this.size;
    }

    /**
     * Returns true if the ship is sunk and false otherwise
     * @returns {Boolean} whether the ship is sunk or not
     */
    isSunk() {
        return this.is_sunk;
    }

    /**
     * Hit the ship
     * @returns {void}
     */
    hit() {
        --this.life;
        if (this.life === 0) this.is_sunk = true;
    }
}
