import { Game } from "./Game";
import { Player } from "../player/Player";
import { test, expect, describe } from "@jest/globals";
import { INVALID_PLAYERS } from "./constants";
import { DESTROYER } from "../ships/ShipFactory";

describe("Game", () => {
  const player1 = new Player(1, "test1");
  const player2 = new Player(2, "test2");
  const player3 = new Player(3, "test3");
  const ship = DESTROYER.createShip();

  describe("constructor", () => {
    test("should create a game with two players", () => {
      const game = new Game(player1, player2);
      expect(game.player1).toBe(player1);
      expect(game.player2).toBe(player2);
      expect(game.turn).toBe(1);
      expect(game.winner).toBeUndefined();
      expect(game.p1_board).toBeDefined();
      expect(game.p2_board).toBeDefined();
    });
    test("should throw an error if the first player is not provided", () => {
      expect(() => new Game()).toThrow(new Error(INVALID_PLAYERS));
    });
    test("should throw an error if the second player is not provided", () => {
      expect(() => new Game(player1)).toThrow(new Error(INVALID_PLAYERS));
    });
  });
  describe("getCurrentPlayer", () => {
    test("should return the first player if it is their turn", () => {
      const game = new Game(player1, player2);
      expect(game.getCurrentPlayer()).toBe(player1);
    });
    test("should return the second player if it is their turn", () => {
      const game = new Game(player1, player2);
      game.turn = 2;
      expect(game.getCurrentPlayer()).toBe(player2);
    });
  });
  describe("hasPlayer", () => {
    test("should return true if the player is in the game", () => {
      const game = new Game(player1, player2);
      expect(game.hasPlayer(player1)).toBeTruthy();
      expect(game.hasPlayer(player2)).toBeTruthy;
    });
    test("should return false if the player is not in the game", () => {
      const game = new Game(player1, player2);
      expect(game.hasPlayer(player3)).toBeFalsy();
    });
  });
  describe("endGameWithLoser", () => {
    test("should set the winner if there is no winner", () => {
      const game = new Game(player1, player2);
      game.endGameWithLoser(player1);
      expect(game.winner).toBe(player2);
    });
    test("should not set the winner if there is already a winner", () => {
      const game = new Game(player1, player2);
      game.endGameWithLoser(player1);
      game.endGameWithLoser(player2);
      expect(game.winner).toBe(player2);
    });
  });

  describe("endGameWithWinner", () => {
    test("should set the winner if there is no winner", () => {
      const game = new Game(player1, player2);
      game.endGameWithWinner(player1);
      expect(game.winner).toBe(player1);
    });
    test("should not set the winner if there is already a winner", () => {
      const game = new Game(player1, player2);
      game.endGameWithWinner(player1);
      game.endGameWithWinner(player2);
      expect(game.winner).toBe(player1);
    });
  });

  describe("isOver", () => {
    test("should return true if there is a winner", () => {
      const game = new Game(player1, player2);
      game.endGameWithWinner(player1);
      expect(game.isOver()).toBeTruthy();
    });
    test("should return false if there is no winner", () => {
      const game = new Game(player1, player2);
      expect(game.isOver()).toBeFalsy();
    });
  });

  describe("getWinner", () => {
    test("should return the winner if there is one", () => {
      const game = new Game(player1, player2);
      game.endGameWithWinner(player1);
      expect(game.getWinner()).toBe(player1);
    });
    test("should return undefined if there is no winner", () => {
      const game = new Game(player1, player2);
      expect(game.getWinner()).toBeUndefined();
    });
  });

  describe("placeShip", () => {
    test("should place a ship on the board of player 1", () => {
      const game = new Game(player1, player2);
      game.placeShip(player1, ship, 0, 0, 1);
      for (let i = 0; i < ship.length; i++) {
        expect(game.p1_board.board[i][0].ship).toBe(ship);
      }
    });
    test("should place a ship on the board of player 2", () => {
      const game = new Game(player1, player2);
      game.placeShip(player2, ship, 0, 0, 1);
      for (let i = 0; i < ship.length; i++) {
        expect(game.p2_board.board[i][0].ship).toBe(ship);
      }
    });
    test("should return false if the player is not in the game", () => {
      const game = new Game(player1, player2);
      expect(game.placeShip(player3, ship, 0, 0, 1)).toBeFalsy();
    });
    test("should return false if the game is over", () => {
      const game = new Game(player1, player2);
      game.endGameWithWinner(player1);
      expect(game.placeShip(player1, ship, 0, 0, 1)).toBeFalsy();
      expect(game.placeShip(player2, ship, 0, 0, 1)).toBeFalsy();
    });
  });

  describe("attack", () => {
    let game;
    beforeEach(() => {
      // Setup the game before each test
      game = new Game(player1, player2);
      game.placeShip(player1, ship, 0, 0, false);
      game.placeShip(player2, ship, 0, 0, false);
    });
    test("should attack the board of player 1 and switch to player 2's turn", () => {
      game.attack(player1, 0, 0);
      expect(game.p2_board.board[0][0]).toBeTruthy();
      expect(game.turn).toBe(2);
      expect(game.getCurrentPlayer()).toBe(player2);
    });
    test("should not allow player 2 to attack", () => {
      game.attack(player2, 0, 0);
      expect(game.p1_board.board[0][0].isHit).toBeFalsy();
      expect(game.turn).toBe(1);
      expect(game.getCurrentPlayer()).toBe(player1);
    });
    test("should not allow player 3 to attack", () => {
      game.attack(player3, 0, 0);
      expect(game.p1_board.board[0][0].isHit).toBeFalsy();
      expect(game.turn).toBe(1);
      expect(game.getCurrentPlayer()).toBe(player1);
    });
    test("should not allow attack and end the game if the ship is sunk", () => {
      expect(game.attack(player1, 0, 0)).toBeTruthy();
      expect(game.getCurrentPlayer()).toBe(player2);

      for (let i = 1; i < ship.length; ++i) {
        expect(game.attack(player2, i, 0)).toBeTruthy();
        expect(game.getCurrentPlayer()).toBe(player1);
        expect(game.attack(player1, i, 0)).toBeTruthy();
        expect(game.getCurrentPlayer()).toBe(player2);
      }
      expect(game.isOver()).toBeTruthy();
      expect(game.getWinner()).toBe(player1);
      expect(game.attack(game.getCurrentPlayer(), 2, 2)).toBeFalsy();
    });
    test("should not allow attack if out of bounds", () => {
      expect(game.attack(player1, 0, 10)).toBeFalsy();
      expect(game.attack(player1, 10, 0)).toBeFalsy();
      expect(game.attack(player1, 10, 10)).toBeFalsy();
    });
    test("should allow player 2 to attack on turn 2", () => {
      game.turn = 2;
      game.attack(player2, 0, 0);
      expect(game.p1_board.board[0][0].isHit).toBeTruthy();
      expect(game.turn).toBe(3);
      expect(game.getCurrentPlayer()).toBe(player1);
    });
  });
});
