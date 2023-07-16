import express from "express";
import http from "http";

const app = express();
app.use(express.json());
const server = http.createServer(app);

import cors from "cors";
app.use(cors());

import path, { dirname } from "path";
import { fileURLToPath } from "url";
const __dirname = dirname(fileURLToPath(import.meta.url));
const publicPath = path.join(__dirname, "public");
const port = process.env.PORT || 19611;
app.use(express.static(publicPath));

import routes from "./routes.js";
app.use("/", routes);

import { setupSockets } from "./sockets.js";
const io = setupSockets(server);

server.listen(port, () => {
    console.log(`listening on *:${port}`);
});
