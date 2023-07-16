import { Player } from "./player/Player.js";
import { Room } from "./room/Room.js";

const rooms = new Map();
setTimeout(() => {
    let ids = rooms.keys();
    for (let id of ids) {
        if (rooms.get(id).isClosed()) {
            rooms.delete(id);
        }
    }
}, 30 * 60 * 1000);

export function createAndEnterRoom(socketId, data) {
    if (!data.name) return null;
    const currentPlayer = new Player(socketId, data.name);

    let room;
    if (rooms.has(data.id)) {
        room = rooms.get(data.id);
    } else {
        room = new Room(socketId, "Room " + socketId);
    }
    rooms.set(socketId, room);

    // Player `joinRoom` method will cause circular structure
    room.addPlayer(currentPlayer);
    console.log(`[LOG](createAndEnterRoom) : ${rooms.size} players joined`);

    return {
        done: room.isFull(),
        id: room.id,
        players: room.getPlayers(),
        board: room.game?.getPlayerBoard(currentPlayer),
        opponentBoard: room.game?.getOtherPlayerBoard(currentPlayer),
    };
}

export function quitRoom(socketId) {
    if (!rooms.has(socketId)) return {};
    let room = rooms.get(socketId);
    room.closeRoom();
    return room;
}

export function updateGameShip(socketId, { coordinates, ship }) {
    if (!rooms.has(socketId)) return { success: false };
    let room = rooms.get(socketId);
    let game = room.game;

    let player = room.getPlayers().find((p) => p.id === socketId);
    if (!player) return { success: false };

    try {
        coordinates = [coordinates[1] - 1, coordinates[0] - 1];
        let shipObj = player.ships.find((s) => s.name === ship.name);
        ship.__proto__ = shipObj.__proto__;
        let success = game.placeShip(player, ship, ...coordinates);
        return {
            success,
            roomId: room.id,
            board: game.getPlayerBoard(player),
            otherBoard: game.getOtherPlayerBoard(player),
        };
    } catch {
        return { success: false };
    }
}

export function attackShip(socketId, { coordinates }) {
    if (!rooms.has(socketId) || coordinates?.length !== 2) return false;
    let room = rooms.get(socketId);
    let game = room.game;

    let player = room.getPlayers().find((p) => p.id === socketId);
    let opponent = room.getPlayers().find((p) => p.id !== socketId);

    coordinates = [coordinates[1] - 1, coordinates[0] - 1];

    let payload = {
        success: false,
        hasShip: false,
        opponent,
        isEndgame: false,
        winner: null,
        loser: null,
    };

    if (!player || game.getCurrentPlayer().id !== player.id) return payload;

    try {
        payload.hasShip = game.attack(player, ...coordinates);
        // console.log(`[LOG](attackShip) : ${socketId} attack on ${coordinates}. ${payload.hasShip ? "HITS" : "MISSES"}`);
        payload.success = true;
        payload.isEndgame = game.isOver();
        if (payload.isEndgame) {
            payload.winner = game.getWinner();
            payload.loser = game.getLoser();
        }
    } catch {
        payload.success = false;
    } finally {
        return payload;
    }
}
