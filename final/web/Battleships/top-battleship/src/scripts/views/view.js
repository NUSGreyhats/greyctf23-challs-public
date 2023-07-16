const View = (() => {
    const themeSwitcher = document.querySelector("#themeSwitch");

    const startScreen = document.querySelector(".screen__start");
    const waitingRoomScreen = document.querySelector(".screen__waiting-room");
    const placeShipScreen = document.querySelector(".screen__ship-placement");

    const btnStart = document.querySelector(".btn__start");
    const inputNameEl = document.querySelector(".input__player-name");
    const roomIdEl = document.querySelector(".input__room-id");

    const hideEl = (el) => {
        el.classList.add("hidden");
    };

    const unhideEl = (el) => {
        el.classList.remove("hidden");
    };

    const addHandlerToggleTheme = () => {
        themeSwitcher.addEventListener("change", (e) => {
            if (e.target.checked) {
                document.body.classList.add("dark-mode");
                localStorage.setItem("preferredTheme", "dark");
            } else {
                document.body.classList.remove("dark-mode");
                localStorage.setItem("preferredTheme", "light");
            }
        });
    };

    const setPageTheme = () => {
        const preferredTheme = localStorage.getItem("preferredTheme");

        if (!preferredTheme || preferredTheme === "light") {
            document.body.classList.remove("dark-mode");
            themeSwitcher.checked = false;
        } else if (preferredTheme === "dark") {
            document.body.classList.add("dark-mode");
            themeSwitcher.checked = true;
        }
    };

    const addHandlerStartGame = (handler) => {
        btnStart.addEventListener("click", (e) => {
            e.preventDefault();

            if (!inputNameEl.value) return;

            hideEl(startScreen);
            unhideEl(waitingRoomScreen);

            handler(inputNameEl.value, roomIdEl.value);
        });
    };

    const loadGameScreen = () => {
        hideEl(waitingRoomScreen);
        unhideEl(placeShipScreen);
    };

    return {
        hideEl,
        unhideEl,
        addHandlerToggleTheme,
        setPageTheme,
        addHandlerStartGame,
        loadGameScreen,
    };
})();

export default View;
