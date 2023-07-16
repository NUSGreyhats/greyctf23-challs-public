import express from "express";
const router = express.Router();

import { Room } from "./room/Room.js";

// id => room
var rooms = {};
setTimeout(() => {
    let room = Object.keys(rooms);
    for (let key of room) {
        if (rooms[key].isClosed()) delete rooms[key];
    }
}, 30 * 60 * 1000);

import { makeid, makename } from "./helper.js";
router
    .get("/", (res, req) => {
        req.send("Hello World!");
    })

    .post("/room", (req, res) => {
        let roomName = makename(16);
        let roomId;
        do {
            roomId = makeid(1 << 30);
        } while (roomId in rooms);

        rooms[roomId] = new Room(roomId, roomName);
        console.log(`[LOG](/room) : ${Object.keys(rooms).length} rooms in use`);

        res.send({ roomId: roomId, roomName: roomName });
    })

    .get("/room/:id", (req, res) => {
        if (req.params.id in rooms) {
            res.send(rooms[req.params.id]);
        } else {
            res.status(404).send("Not found");
        }
    });

export default router;
