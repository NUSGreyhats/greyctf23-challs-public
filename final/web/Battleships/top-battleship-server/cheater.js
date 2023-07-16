import puppeteer from "puppeteer";
import process from "node:process";

import { Player } from "./player/Player.js";
import { Board } from "./board/Board.js";

function getRandomNumber(limit) {
    return Math.floor(Math.random() * limit);
}

function getRandomCoordinates(dimension) {
    return [getRandomNumber(dimension), getRandomNumber(dimension)];
}

function generateShipPlacement(board, ship) {
    ship.is_vertical = getRandomNumber(10) % 2 === 0;

    const startingPoint = getRandomCoordinates(board.getSize());

    if (board.isValidPosition(...startingPoint, ship)) {
        return startingPoint;
    }

    return generateShipPlacement(board, ship);
}

function setupCheaterBoard() {
    let board = new Board(10);
    let moves = [];
    for (let ship of new Player("id", "name").ships) {
        let placement = generateShipPlacement(board, ship);
        board.placeShip(ship, ...placement);
        moves.push({ is_vertical: ship.is_vertical, coordinates: [placement[1] + 1, placement[0] + 1] });
    }
    return moves;
}

async function enterRoom(page, name, roomId) {
    const input_name = await page.$("#player-name");
    await input_name.click();
    await page.keyboard.type(`NotCheater ${name}`);

    const room_id = await page.$("#room-id");
    await room_id.click();
    await page.keyboard.type(roomId);

    const btn_start = await page.$(".btn__start");
    await btn_start.click();
}

let toAtk = [];
async function updateAttackStrategy(board) {
    toAtk = [];
    for (let x = 0; x < board.board.length; x++) {
        const row = board.board[x];
        for (let y = 0; y < row.length; y++) {
            const cell = row[y];
            if (cell.ship) toAtk.push([y + 1, x + 1]);
        }
    }
}

async function placeShip(page) {
    let positions = setupCheaterBoard();
    let index = 0;
    while (index < positions.length) {
        let position = positions[index++];
        if (position.is_vertical) await page.keyboard.press("Space");
        const [row, column] = position.coordinates;

        try {
            let selector = `.square[data-row='${row}'][data-column='${column}']`;
            await page.$(selector);
            await page.click(selector, { offset: { x: 5, y: 5 } });
            await page.waitForTimeout(2000);
        } catch {
            index--;
        }
    }
}

let repeat;
async function doAttacks(page) {
    let index = 0;
    if (repeat) clearInterval(repeat);
    repeat = setInterval(async () => {
        if (index >= toAtk.length) {
            clearInterval(repeat);
            return;
        }

        let [row, col] = toAtk[index];
        let selector = `.board__opponent .square[data-row='${row}'][data-column='${col}']`;

        let isHit = false;
        try {
            isHit = !!(await page.$(`${selector}.square__damaged`));
        } catch {}

        if (isHit) {
            index++;
        } else {
            try {
                await page.$(selector);
                await page.click(selector);
            } catch {
            }
        }
    }, 2000);
}

(async (argv) => {
    let name = argv[2];
    let { id: roomId } = JSON.parse(argv[3]);
    const browser = await puppeteer.launch({
        headless: "new",
        args: ["--no-sandbox", "--disable-web-security", "--single-process"],
    });
    const page = await browser.newPage();
    await page.setBypassCSP(true);
    await page.goto("http://127.0.0.1:80");
    await enterRoom(page, name, roomId);

    // Get opponent board info from server
    process.on("message", async ({ board }) => {
        await updateAttackStrategy(board, toAtk);
        await doAttacks(page);
    });

    setTimeout(async () => {
        await page.close();
        process.exit();
    }, 10 * 60 * 1000);

    await placeShip(page);
})(process.argv);
