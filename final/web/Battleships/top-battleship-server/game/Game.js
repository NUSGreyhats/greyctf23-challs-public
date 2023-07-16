import { Board } from "../board/Board.js";
import { INVALID_PLAYERS } from "./constants.js";

export class Game {
    /**
     * The constructor of the Battleship Game class
     * @param {Player} player1 The first player of the game
     * @param {Player} player2 The second player of the game
     */
    constructor(player1, player2) {
        if (player1 === undefined || player2 === undefined) throw new Error(INVALID_PLAYERS);

        this.player1 = player1;
        this.player2 = player2;
        this.turn = 1;
        this.p1_board = new Board();
        this.p2_board = new Board();
        this.winner = undefined;
    }

    /**
     * Returns the player whose turn it is.
     * @returns {Player}
     */
    getCurrentPlayer() {
        return this.turn % 2 === 1 ? this.player1 : this.player2;
    }

    /**
     * Returns true if the player is in the game.
     * @param {Player} player the player to check
     * @returns {bool}
     */
    hasPlayer(player) {
        return player === this.player1 || player === this.player2;
    }

    /**
     * Ends the game and sets the winner. Does nothing if there is already a winner.
     * @param {Player} loser the player who lost.
     */
    endGameWithLoser(loser) {
        if (this.winner !== undefined) return;
        this.winner = loser === this.player1 ? this.player2 : this.player1;
    }

    /**
     * Ends the game and sets the winner. Does nothing if there is already a winner.
     * @param {Player} winner the player who won.
     * @return {void}
     */
    endGameWithWinner(winner) {
        if (this.winner !== undefined) return;
        this.winner = winner;
    }

    isStart() {
        return !this.player1.hasShip() && !this.player2.hasShip();
    }

    /**
     * Returns true if the game is over.
     * @returns {bool}
     */
    isOver() {
        return this.winner !== undefined;
    }

    /**
     * Returns the winner of the game. Returns undefined if the game is not over.
     * @returns {Player | undefined}
     */
    getWinner() {
        return this.winner;
    }

    getLoser() {
        return this.player1 === this.winner ? this.player2 : this.player1;
    }

    /**
     *
     * @param {Player} player the player to get board of
     * @returns {Board} the board of the player, null if player is not in this game
     */
    getPlayerBoard(player) {
        return player === this.player1 ? this.p1_board : player === this.player2 ? this.p2_board : null;
    }

    /**
     *
     * @param {Player} player the player to NOT get board of
     * @returns {Board} the board of the other player, null if player is not in this game
     */
    getOtherPlayerBoard(player) {
        return player === this.player2 ? this.p1_board : player === this.player1 ? this.p2_board : null;
    }

    /**
     * Places a ship on the board of the player whose turn it is.
     * @param {Player} player the player who is placing the ship
     * @param {Ship} ship the ship to place
     * @param {number} x the x coordinate of the ship
     * @param {number} y the y coordinate of the ship
     * @returns {bool} true if the ship is placed successfully
     */
    placeShip(player, ship, x, y) {
        if (!this.hasPlayer(player)) return false;
        if (this.isOver()) return false;

        const board = this.getPlayerBoard(player);
        try {
            let success = board.placeShip(ship, x, y);
            player.removeShip(ship);
            return success;
        } catch {
            return false;
        }
    }

    /**
     * Attacks the board of the player whose turn it is.
     * @param {Player} player the player who is attacking
     * @param {number} x the x coordinate of the attack
     * @param {number} y the y coordinate of the attack
     * @returns {bool} true if the attack is a hit
     */
    attack(player, x, y) {
        if (!this.hasPlayer(player)) throw new Error();
        if (!this.isStart() || this.isOver()) throw new Error();
        if (player !== this.getCurrentPlayer()) throw new Error();
        const board = this.getOtherPlayerBoard(player);

        try {
            let isHit = board.makeGuess(x, y);
            ++this.turn;
            if (board.allShipsSunk()) this.endGameWithWinner(player);
            return isHit;
        } catch (e) {
            return false;
        }
    }
}
