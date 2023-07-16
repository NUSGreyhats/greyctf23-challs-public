import { Ship } from "../ships/Ship.js";
import { INVALID_PLAYER_ID_ERROR, INVALID_PLAYER_NAME_ERROR } from "./constants.js";

export class Player {
    ships = [
        new Ship(5, "carrier"),
        new Ship(4, "battleship"),
        new Ship(3, "destroyer"),
        new Ship(3, "submarine"),
        new Ship(2, "patroller"),
    ];

    /**
     * The constructor of the Player class
     * @param {string} id the id of the player
     * @param {string} name the name of the player
     */
    constructor(id, name) {
        if (id === undefined || id.length === 0) throw new Error(INVALID_PLAYER_ID_ERROR);
        if (name === undefined || name.length === 0) throw new Error(INVALID_PLAYER_NAME_ERROR);
        this.id = id;
        this.name = name;
        this.room = null;
    }

    /**
     * Returns the id of the player
     * @returns {number}
     */
    getId() {
        return this.id;
    }

    /**
     * Returns the name of the player
     * @returns {string}
     */
    getName() {
        return this.name;
    }

    /**
     * Removes the ship from the player's possession
     */
    removeShip(ship) {
        this.ships = this.ships.filter((s) => s.getName() !== ship.name);
    }

    /**
     * Returns true if the player still has ships
     * @returns {Boolean}
     */
    hasShip() {
        return this.ships.length !== 0;
    }

    /**
     * Joins a room. Returns true if the join is successful and false if the room is full.
     * This method also removes the player from the current room.
     * @param {Room} room the room to join
     * @returns {bool} true if the join is successful
     */
    joinRoom(room) {
        if (room === null || this.room === room) return false;

        if (!room.addPlayer(this)) return false;

        this.room = room;
        return true;
    }

    /**
     * Leaves the current room. Returns true if the leave is successful and false if the player is not in a room.
     * @returns {bool} true if the leave is successful.
     */
    leaveRoom() {
        if (this.room === null) return false;
        this.room.removePlayer(this);
        this.room = null;
        return true;
    }
}
