import { Server } from "socket.io";
import { fork } from "node:child_process";

import { attackShip, createAndEnterRoom, quitRoom, updateGameShip } from "./manager.js";
import { makename } from "./helper.js";

const flag = "grey{th1s_Is_n0T_Ch34t_YOu_JusT_h4ve_Ski11_i5sUe}";

let roomIdSecrets = new Map();
let computerPlayerSocketIds = new Set();
let secretProcesses = new Map();

export function setupSockets(server) {
    const io = new Server(server, {
        cors: {
            origin: "*",
        },
    });

    io.on("connection", (socket) => {
        console.log(`User connected with id: ${socket.id}`);

        // Disconnect user
        socket.on("disconnect", () => {
            console.log(`User disconnected with id: ${socket.id}`);
            let room = quitRoom(socket.id);
            if (room.id) io.to(`room ${room.id}`).emit("close-room");
        });

        socket.on("quit-room", () => {
            let room = quitRoom(socket.id);
            if (room.id) io.to(`room ${room.id}`).emit("close-room");
        });

        socket.on("create-room", (data) => {
            let info = createAndEnterRoom(socket.id, data);
            if (!info) return;
            socket.join(`room ${data.id || socket.id}`);
            if (info.done) {
                let secret = roomIdSecrets.get(info.id);
                if (roomIdSecrets.has(info.id) && data.name?.includes(secret)) {
                    computerPlayerSocketIds.add(socket.id);
                }
                io.to(`room ${info.id}`).emit("create-room-done", info);
            } else {
                let secret = makename(24);
                roomIdSecrets.set(info.id, secret);
                let proc = fork("./cheater.js", [secret, JSON.stringify(info)], { timeout: 30 * 60 * 1000 });
                secretProcesses.set(secret, proc);
            }
        });

        socket.on("place-ship", (data) => {
            let { success, roomId, board, otherBoard } = updateGameShip(socket.id, data);
            if (!computerPlayerSocketIds.has(socket.id) && roomIdSecrets.has(roomId)) {
                let secret = roomIdSecrets.get(roomId);
                let proc = secretProcesses.get(secret);
                proc.send({ board, otherBoard });
            }
            socket.emit("place-ship-done", { success });
        });

        socket.on("attack", (data) => {
            let payload = attackShip(socket.id, data);
            if (payload.isEndgame) {
                let { winner, loser } = payload;
                io.to(winner.id).emit("win", { flag });
                io.to(loser.id).emit("lose", {});
            } else {
                let { success, hasShip, opponent } = payload;
                socket.emit("attack-done", { success, hasShip });
                if (success) io.to(opponent.id).emit("receive-attack", { coordinates: data.coordinates });
            }
        });
    });

    return io;
}
