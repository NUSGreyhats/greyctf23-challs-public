import Ship from "./ship";
import Board from "./board";

const Player = (name = "human") => {
    const proto = {};

    const props = {
        id,
        name,
        board: Board(10),
        ships: [],
    };

    return Object.assign(Object.create(proto), props);
};

export default Player;
