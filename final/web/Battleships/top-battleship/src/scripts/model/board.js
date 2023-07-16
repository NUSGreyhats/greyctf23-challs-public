/* eslint-disable no-return-assign */

const Square = (coordinates) => {
    const [row, column] = coordinates;

    return {
        row,
        column,
        coordinates,
        id: null,
        isHit: false,
        hasShip: false,
        shipName: "",
    };
};

const Board = (gridLength = 10) => {
    const size = gridLength ** 2;
    const dimension = gridLength;
    const state = [];

    const proto = {
        findSquareWithID(id) {
            return this.state.find((square) => square.id === id);
        },

        findSquareWithRowCol(coordinates) {
            return this.state.find((square) => square.row === coordinates[0] && square.column === coordinates[1]);
        },

        getValidSquaresToPlaceShipOn(origin, ship) {
            const [row, col] = origin;

            const targetSquares = [];

            for (let i = 0; i < ship.size; i++) {
                const coordinates = ship.is_vertical ? [+row + i, col] : [row, +col + i];
                const target = this.findSquareWithRowCol(coordinates);

                if (target && !target.hasShip) {
                    targetSquares.push(target);
                } else return false;
            }

            return targetSquares;
        },

        placeShip(coordinates, ship) {
            const targetSquares = this.getValidSquaresToPlaceShipOn(coordinates, ship);

            if (!targetSquares || !targetSquares.length) return false;

            targetSquares.forEach((square) => {
                square.shipName = ship.name;
                square.hasShip = true;
            });

            return true;
        },
    };

    const createBoard = () => {
        for (let i = 1; i <= gridLength; i++) {
            const row = i;
            let column = 1;

            for (let j = 1; j <= gridLength; j++) {
                column = j;

                const newSquare = Square([row, column]);
                state.push(newSquare);
            }
        }

        state.forEach((square, i) => (square.id = ++i));
    };

    createBoard();

    return Object.assign(Object.create(proto), {
        size,
        state,
        dimension,
    });
};

export default Board;
