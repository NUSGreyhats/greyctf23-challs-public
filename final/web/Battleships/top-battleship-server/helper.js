import crypto from "crypto";

export const makeid = (size) => {
    return crypto.randomInt(0, size);
};

export const makename = (length) => {
    var result = [];
    var characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        let size = 4294967295;
        let rand = makeid(size) / size;
        result.push(characters.charAt(Math.floor(rand * charactersLength)));
    }
    return result.join("");
};
