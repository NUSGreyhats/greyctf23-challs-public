import View from "./view";

const gameView = (() => {
    const placeShipScreen = document.querySelector(".screen__ship-placement");
    const gameDisplayScreen = document.querySelector(".screen__game-display");

    const currentBoardEl = document.querySelector(".board__self");
    const otherBoardEl = document.querySelector(".board__opponent");
    const winnerOverlay = document.querySelector(".overlay__winner-display");

    const generateBoardMarkup = (square) => `
    <div class="square square__${square.isHit ? "damaged" : "base"} ${
        square.isHit && square.hasShip ? "square__has-ship" : ""
    }" data-row="${square.row}" data-column="${square.column}" data-id="${square.id}"></div>`;

    const renderBoard = (player, boardEl) => {
        const markup = player.board.state.map((square) => generateBoardMarkup(square)).join("");

        boardEl.innerHTML = `<span class="board__label">${player.name}'s domain</span>`;
        boardEl.insertAdjacentHTML("beforeend", markup);
    };

    const renderSelfBoard = (player) => {
        renderBoard(player, currentBoardEl);
    };

    const renderOpponentBoard = (player) => {
        renderBoard(player, otherBoardEl);
    };

    const displayScreen = (players) => {
        View.hideEl(placeShipScreen);
        View.unhideEl(gameDisplayScreen);

        const [human, computer] = players;

        renderBoard(human, currentBoardEl);
        renderBoard(computer, otherBoardEl);
    };

    const addHandlerAttackEnemy = (handler) => {
        const enemySquares = [...otherBoardEl.querySelectorAll(".square")];

        enemySquares.forEach((square) =>
            square.addEventListener("click", (e) => {
                const { row, column } = e.target.dataset;

                handler([+row, +column]);
            })
        );
    };

    const displayWinner = (player, isWin, message = "") => {
        View.unhideEl(winnerOverlay);

        winnerOverlay.querySelector(".message__winner-main").textContent = `The winner is ${player.name}!`;

        winnerOverlay.querySelector(".message__winner-sub").textContent = `${
            isWin
                ? `Congratulations! You have beat out the enemy. Your domain is in good hands. ${message}`
                : "Too bad! Now your domain has been overrun by the enemy!"
        }`;
    };

    return {
        displayScreen,
        renderBoard,
        renderSelfBoard,
        renderOpponentBoard,
        addHandlerAttackEnemy,
        displayWinner,
    };
})();

export default gameView;
