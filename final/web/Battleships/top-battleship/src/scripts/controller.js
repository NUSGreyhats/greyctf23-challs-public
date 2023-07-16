/* eslint-disable no-use-before-define */
// eslint-disable-next-line no-unused-vars
import styles from '../sass/main.scss';

import Board from "./model/board";

import View from "./views/view";
import placeShipView from "./views/placeShipView";
import gameView from "./views/gameView";

import { io } from "../../node_modules/socket.io/client-dist/socket.io";
let socket = io(`ws://${window.location.hostname}:19611`);

let currentPlayer;
let otherPlayer;
let currentShip;

const controlRotateShip = (ship) => {
    ship.is_vertical = !ship.is_vertical;
};

const controlAdjacentSquares = (origin, ship) => {
    const adjacentSquares = currentPlayer.board.getValidSquaresToPlaceShipOn(origin, ship);

    if (!adjacentSquares || adjacentSquares.some((square) => square.hasShip)) return false;

    return adjacentSquares.map((square) => square.id);
};

socket.on("win", (data) => {
    gameView.displayWinner(currentPlayer, true, data.flag);
});

socket.on("lose", (_) => {
    gameView.displayWinner(otherPlayer, false);
});

socket.on("receive-attack", (data) => {
    const attackedSquare = currentPlayer.board.findSquareWithRowCol(data.coordinates);
    attackedSquare.isHit = true;
    gameView.renderSelfBoard(currentPlayer);
});

const controlAttackEnemy = (coordinates) => {
    let target = otherPlayer.board.findSquareWithRowCol(coordinates);
    if (target.isHit) return;

    socket.emit("attack", { coordinates });

    socket.once("attack-done", (data) => {
        if (!data.success) return;
        target.isHit = true;
        if (data.hasShip !== null) target.hasShip = data.hasShip;

        gameView.renderOpponentBoard(otherPlayer);
        gameView.addHandlerAttackEnemy(controlAttackEnemy);
    });
};

const controlPlaceShip = (coordinates, ship) => {
    if (!currentPlayer.board.placeShip(coordinates, ship)) return;

    socket.emit("place-ship", { coordinates, ship });

    socket.once("place-ship-done", ({ success }) => {
        if (!success) return;

        currentPlayer.board.placeShip(coordinates, ship);
        placeShipView.renderBoard(currentPlayer.board.state);
        currentShip.isOnBoard = true;

        // Move to next ship not on board
        currentShip = currentPlayer.ships.find((targetShip) => !targetShip.isOnBoard);

        if (currentShip) {
            controlShipPlacement(currentShip);
        } else if (!currentShip) {
            localStorage.setItem("board", JSON.stringify(currentPlayer.board));
            gameView.displayScreen([currentPlayer, otherPlayer]);
            gameView.addHandlerAttackEnemy(controlAttackEnemy);
        }
    });
};

const controlShipPlacement = (ship) => {
    placeShipView.addHandlerFindShipSquares(ship, controlAdjacentSquares);
    placeShipView.addHandlerRotateShip(ship, controlRotateShip);
    placeShipView.addHandlerPlaceShip(ship, controlPlaceShip);
};

const controlStartGame = (name, roomId = "") => {
    socket.once("create-room-done", ({ players, board }) => {
        View.loadGameScreen();

        currentPlayer = players.find((p) => p.id === socket.id);
        otherPlayer = players.find((p) => p.id !== socket.id);
        currentShip = currentPlayer.ships[0];

        currentPlayer.board = Board(board.length);
        otherPlayer.board = Board(board.length);

        // Generate board placement screen
        placeShipView.renderBoard(currentPlayer.board.state);
        controlShipPlacement(currentShip);
    });

    // Quit room (for game restart)
    socket.emit("create-room", { name, id: roomId });
};

socket.on("close-room", () => {
    window.location.reload();
});

const init = () => {
    View.setPageTheme();
    View.addHandlerToggleTheme();
    View.addHandlerStartGame(controlStartGame);
};

init();
