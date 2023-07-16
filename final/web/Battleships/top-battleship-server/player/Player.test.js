import { describe, expect, test } from "@jest/globals";
import { Player } from "./Player";
import { Room } from "../room/Room";
import {
  INVALID_PLAYER_ID_ERROR,
  INVALID_PLAYER_NAME_ERROR,
} from "./constants";
import { ROOM_SIZE } from "../room/constants";

describe("Player", () => {
  describe("constructor", () => {
    test("should create a player with an id and a name", () => {
      const player = new Player(1, "test");
      expect(player.id).toBe(1);
      expect(player.name).toBe("test");
    });
    test("should throw an error if the id is not provided", () => {
      expect(() => new Player()).toThrow(new Error(INVALID_PLAYER_ID_ERROR));
    });
    test("should throw an error if the name is not provided", () => {
      expect(() => new Player(1)).toThrow(new Error(INVALID_PLAYER_NAME_ERROR));
    });
    test("should throw an error if the name is empty", () => {
      expect(() => new Player(1, "")).toThrow(
        new Error(INVALID_PLAYER_NAME_ERROR)
      );
    });
  });

  describe("getId", () => {
    const player = new Player(1, "test");
    test("should return the id of the player", () => {
      expect(player.getId()).toBe(1);
    });
  });

  describe("getName", () => {
    const player = new Player(1, "test");
    test("should return the name of the player", () => {
      expect(player.getName()).toBe("test");
    });
  });

  describe("joinRoom", () => {
    test("should set the room of the player to the given room", () => {
      const player = new Player(1, "test");
      const room = new Room(1, "test");
      expect(player.joinRoom(room)).toBeTruthy();
      expect(room.getPlayers()).toContain(player);
      expect(player.room).toBe(room);
    });
    test("should not set the room of the player to the given room if the room is full", () => {
      const room = new Room(1, "test");
      for (let i = 0; i < ROOM_SIZE; ++i) {
        const player = new Player(i, "test");
        expect(player.joinRoom(room)).toBeTruthy();
      }
      const player = new Player(ROOM_SIZE, "test");
      expect(player.joinRoom(room)).toBeFalsy();
      expect(room.getPlayers()).not.toContain(player);
      expect(player.room).toBeNull();
    });
    test("should not be able to join a null room", () => {
      const player = new Player(1, "test");
      expect(player.joinRoom(null)).toBeFalsy();
      expect(player.room).toBeNull();
    });
  });
  describe("leaveRoom", () => {
    test("should set the room of the player to null", () => {
      const player = new Player(1, "test");
      const room = new Room(1, "test");
      expect(player.joinRoom(room)).toBeTruthy();
      expect(player.leaveRoom()).toBeTruthy();
      expect(room.getPlayers()).not.toContain(player);
      expect(player.room).toBeNull();
    });
    test("should not set the room of the player to null if the player is not in a room", () => {
      const player = new Player(1, "test");
      expect(player.leaveRoom()).toBeFalsy();
      expect(player.room).toBeNull();
    });
  });
});
