import { Room } from "./Room";
import { INVALID_ID, INVALID_NAME, INVALID_ROOM_SIZE, ROOM_SIZE } from "./constants";
import { Game } from "../game/Game";
import { Player } from "../player/Player";
import { expect, test, describe } from "@jest/globals";

describe("Room", () => {
    describe("constructor", () => {
        test("should create a room with the given id, name and room_size", () => {
            const room = new Room("1", "room1", 2);
            expect(room.id).toBe("1");
            expect(room.name).toBe("room1");
            expect(room.room_size).toBe(2);
            expect(room.players).toEqual([]);
            expect(room.game).toBeNull();
        });
        test("should throw an error if the id is undefined or less than 0", () => {
            expect(() => new Room(undefined, "room1", 2)).toThrow(new Error(INVALID_ID));
            expect(() => new Room("", "room1", 2)).toThrow(new Error(INVALID_ID));
        });
        test("should throw an error if the name is undefined or empty", () => {
            expect(() => new Room("1", undefined, 2)).toThrow(new Error(INVALID_NAME));
            expect(() => new Room("1", "", 2)).toThrow(new Error(INVALID_NAME));
        });
        test("should throw an error if the room_size is undefined or less than 2", () => {
            expect(() => new Room("1", "room1", 1)).toThrow(new Error(INVALID_ROOM_SIZE));
            expect(() => new Room("1", "room1", -1)).toThrow(new Error(INVALID_ROOM_SIZE));
        });
        test("should create a room with the default room_size if the room_size is not given", () => {
            const room = new Room("1", "room1");
            expect(room.id).toBe("1");
            expect(room.name).toBe("room1");
            expect(room.room_size).toBe(ROOM_SIZE);
        });
    });

    describe("addPlayer", () => {
        test("should add a player to the room", () => {
            const room = new Room("1", "room1", 2);
            const player = { id: 1, name: "player1" };
            room.addPlayer(player);
            expect(room.players).toEqual([player]);
        });
        test("should not add a player to the room if the room is full", () => {
            const room = new Room("1", "room1", 2);
            const player1 = new Player("1", "player1");
            const player2 = new Player("2", "player2");
            const player3 = new Player("3", "player3");
            expect(room.addPlayer(player1)).toBeTruthy();
            expect(room.game).toBeNull();
            expect(room.addPlayer(player2)).toBeTruthy();
            expect(room.addPlayer(player3)).toBeFalsy();
            expect(room.players).toEqual([player1, player2]);
        });
        test("should start the game when there are 2 players", () => {
            const room = new Room("1", "room1", 2);
            const player1 = new Player("1", "player1");
            const player2 = new Player("2", "player2");
            room.addPlayer(player1);
            expect(room.game).toBeNull();
            room.addPlayer(player2);
            expect(room.game).toEqual(new Game(player1, player2));
        });
        test("should not be able to add players to the room if the room is closed", () => {
            const room = new Room("1", "room1", 2);
            const player = new Player("1", "player1");
            room.closeRoom();
            expect(room.is_closed).toBeTruthy();
            expect(room.addPlayer(player)).toBeFalsy();
        });
    });
    describe("removePlayer", () => {
        test("should remove a player from the room", () => {
            const room = new Room("1", "room1", 2);
            const player = new Player("1", "player1");
            expect(room.addPlayer(player)).toBeTruthy();
            expect(room.players).toEqual([player]);
            expect(room.removePlayer(player)).toBeTruthy();
            expect(room.players).toEqual([]);
        });
        test("should not remove a player from the room if the player is not in the room", () => {
            const room = new Room("1", "room1", 2);
            const player = new Player("1", "player1");
            const player2 = new Player("2", "player2");
            expect(room.addPlayer(player)).toBeTruthy();
            expect(room.players).toEqual([player]);
            expect(room.removePlayer(player2)).toBeFalsy();
            expect(room.players).toEqual([player]);
        });
        test("should stop the game when there is only 1 player left", () => {
            const room = new Room("1", "room1", 2);
            const player1 = new Player("1", "player1");
            const player2 = new Player("2", "player2");
            expect(room.addPlayer(player1)).toBeTruthy();
            expect(room.addPlayer(player2)).toBeTruthy();
            expect(room.game).toEqual(new Game(player1, player2));
            expect(room.removePlayer(player2));
            expect(room.game.winner).toBe(player1);
        });
        test("should not be able to remove players from the room if the room is closed", () => {
            const room = new Room("1", "room1", 2);
            const player = new Player("1", "player1");
            expect(room.addPlayer(player)).toBeTruthy();
            room.closeRoom();
            expect(room.is_closed).toBeTruthy();
            expect(room.removePlayer(player)).toBeFalsy();
        });
    });

    describe("getPlayers", (id) => {
        test("should return the players in the room", () => {
            const room = new Room("1", "room1", 2);
            const player1 = new Player("1", "player1");
            const player2 = new Player("2", "player2");
            expect(room.addPlayer(player1)).toBeTruthy();
            expect(room.addPlayer(player2)).toBeTruthy();
            expect(room.getPlayers()).toEqual([player1, player2]);
        });
        test("should return an empty array if there are no players in the room", () => {
            const room = new Room(1, "room1", 2);
            expect(room.getPlayers()).toEqual([]);
        });
    });

    describe("closeRoom", () => {
        test("should close the room", () => {
            const room = new Room("1", "room1", 2);
            room.closeRoom();
            expect(room.players).toEqual([]);
            expect(room.is_closed).toBeTruthy();
        });
    });
});
