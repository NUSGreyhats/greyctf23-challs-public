const placeShipView = (() => {
    const boardEl = document.querySelector(".board__ship-placement");
    const shipsEl = [...document.querySelectorAll(".ship__wrapper")];

    const btnRotate = document.querySelector(".btn__rotate-ship");

    const generateSquareMarkup = (square) => `
            <div
              class="square square__empty ${square.hasShip ? "square__filled" : ""}"
              data-row="${square.row}"
              data-column="${square.column}"
              data-id="${square.id}"
            ></div>
  `;

    const renderBoard = (state) => {
        const markup = state.map((square) => generateSquareMarkup(square)).join("");

        boardEl.innerHTML = "";
        boardEl.insertAdjacentHTML("afterbegin", markup);
    };

    const renderShip = (ship) => {
        shipsEl.forEach((el) => el.classList.remove("ship__wrapper-active"));

        shipsEl.find((el) => el.dataset.ship === ship.name).classList.add("ship__wrapper-active");
    };

    const addHandlerFindShipSquares = (ship, handler) => {
        renderShip(ship);

        const squares = [...boardEl.querySelectorAll(".square")];

        squares.forEach((el) => {
            el.addEventListener("mouseenter", (e) => {
                const { row, column } = e.target.dataset;

                e.target.classList.add("square__placement-origin");

                const nextSquares = handler([+row, +column], ship);

                if (!nextSquares || nextSquares.length !== ship.size) return;

                nextSquares.forEach((id) => {
                    boardEl.querySelector(`.square[data-id="${id}"]`).classList.add("square__placement-adjacent");
                });
            });

            el.addEventListener("mouseleave", (e) => {
                e.target.classList.remove("square__placement-origin");
                squares.forEach((square) => square.classList.remove("square__placement-adjacent"));
            });
        });
    };

    const addHandlerRotateShip = (ship, handler) => {
        btnRotate.addEventListener("click", () => {
            handler(ship);
        });

        window.addEventListener("keydown", (e) => {
            if (e.key === " " || e.code === "Space") {
                e.preventDefault();
                handler(ship);
            }
        });
    };

    const addHandlerPlaceShip = (ship, handler) => {
        const squares = [...boardEl.querySelectorAll(".square")];

        squares.forEach((el) => {
            el.addEventListener("click", (e) => {
                const { row, column } = e.target.dataset;

                handler([+row, +column], ship);
            });
        });
    };

    return {
        renderBoard,
        addHandlerFindShipSquares,
        addHandlerRotateShip,
        addHandlerPlaceShip,
    };
})();

export default placeShipView;
