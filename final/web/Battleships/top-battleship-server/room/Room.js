import { INVALID_ID, INVALID_NAME, INVALID_ROOM_SIZE, ROOM_SIZE } from "./constants.js";
import { Game } from "../game/Game.js";

export class Room {
    /**
     * The constructor of the Room class
     * @param {String} id The id of the room
     * @param {String} name The name of the room
     * @param {number} room_size The size of the room
     */
    constructor(id, name, room_size = ROOM_SIZE) {
        if (id === undefined || id.length === 0) throw new Error(INVALID_ID);
        if (name === undefined || name.length === 0) throw new Error(INVALID_NAME);
        if (room_size < 2) throw new Error(INVALID_ROOM_SIZE);
        this.id = id;
        this.name = name;
        this.room_size = room_size;
        this.players = [];
        this.game = null;
        this.is_closed = false;
    }

    /**
     * Adds a player. Returns true if the addition is successful and false if the room is full.
     * @param {Player} player the player of the game
     * @returns {bool}
     */
    addPlayer(player) {
        if (this.is_closed || this.players.length >= this.room_size) return false;
        this.players.push(player);

        // Start the game when there are enough players
        if (this.players.length === this.room_size) this.game = new Game(this.players[0], this.players[1]);

        return true;
    }

    /**
     * Removes a player. Returns true if the removal is successful and false if the player is not in the room.
     * @param {Player} player the player to remove
     * @returns {bool}
     */
    removePlayer(player) {
        if (this.is_closed || this.players.length <= 0 || !this.players.includes(player)) return false;
        if (this.game !== null && this.game.hasPlayer(player)) this.game.endGameWithLoser(player);

        this.players = this.players.filter((p) => p.id !== player.id);
        this.closeRoom();
        return true;
    }

    /**
     * Returns the player with the given id.
     * @returns {Array<Player>} the players in the room
     */
    getPlayers() {
        return this.players;
    }

    /**
     * Closes the room.
     * @returns {void}
     */
    closeRoom() {
        for (const player of this.players) this.removePlayer(player);
        this.is_closed = true;
    }

    /**
     * Returns whether room is full.
     * @returns {Boolean}
     */
    isFull() {
        return this.players.length === this.room_size;
    }

    /**
     * Returns state of the room.
     * @returns {Boolean}
     */
    isClosed() {
        return this.is_closed;
    }
}
