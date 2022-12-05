import {akaMakeMove, akaForfeitGame, akaPollGame, fbUser, akaAuthStateChanged, akaGetUser} from "./api.js"

// Row major board
var ROWS = 6;
var COLS = 7;

let game = {
    board: "",
    state: "MOVE_ONE",
    player_one: "",
    player_two: "",
}

let player_one = {
    username: ""
}

let player_two = {
    username: ""
}

let player_you = 1;

let your_move = 0;

let gameuuid = "";

// Onetime setup
function setGame() {
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            // JS
            // HTML
            let tile = document.createElement("div");
            tile.id = r.toString() + "-" + c.toString();
            tile.classList.add("tile");
            tile.addEventListener("click", makeMove);
            document.getElementById("board").append(tile);
        }
    }
}

function makeMove() {
    //get coords of that tile clicked
    let coords = this.id.split("-");
    let c = parseInt(coords[1]);
    console.log(c);
    // Make a move with current user 
    if (game.board.split(coords[1]).length - 1 < 6 && your_move) {
        akaMakeMove(gameuuid, fbUser().uid, c).then((g) => draw(g))
    }
}

function forfeitGame() {
    akaForfeitGame(gameuuid, fbUser().uid).then((g) => draw(g));
}

function pollGame() {
    akaPollGame(gameuuid, fbUser().uid).then((g) => draw(g));
}

function draw(g) {
    game = g;
    if (g) {
        console.log(g);

        // Draw players
        document.querySelector("#playerOne").innerHTML = player_one.username;
        document.querySelector("#playerTwo").innerHTML = player_two.username;

        // Draw state
        your_move = false;
        switch(g.state) {
            case "MOVE_ONE":
                if (player_you === 1) {
                    document.querySelector("#stateText").innerHTML = "Your move.";
                    your_move = true;
                } else {
                    document.querySelector("#stateText").innerHTML = "Their move.";
                }
                break;
            case "MOVE_TWO":
                if (player_you === 2) {
                    document.querySelector("#stateText").innerHTML = "Your move.";
                    your_move = true;
                } else {
                    document.querySelector("#stateText").innerHTML = "Their move.";
                }
                break;
            case "DRAW":
                document.querySelector("#stateText").innerHTML = "Draw.";
            case "WIN_ONE":
            case "FF_TWO":
            case "TIMEOUT_TWO":
                if (player_you === 1) {
                    document.querySelector("#stateText").innerHTML = "You Win!";
                } else {
                    document.querySelector("#stateText").innerHTML = "You Lose!";
                }
                break;
            case "WIN_TWO":
            case "FF_ONE":
            case "TIMEOUT_ONE":
                if (player_you === 2) {
                    document.querySelector("#stateText").innerHTML = "You Win!";
                } else {
                    document.querySelector("#stateText").innerHTML = "You Lose!";
                }
                break;
        }

        // Draw board
        drawBoard(g.board);

        // Cause another
        setTimeout(pollGame, 4000);

    } else {
        drawBoard("");
    }
}

function drawBoard(boardString) {

    // Clear existing
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            let tile = document.getElementById(`${r}-${c}`);
            tile.classList.remove("red-piece");
            tile.classList.remove("yellow-piece");
        }
    }

    let board = new Array(ROWS);
    for(let j = 0; j < ROWS; j++) {
        board[j] = new Array(COLS).fill(0);
    }
    // Loop through drops
    for(let i = 0; i < boardString.length; i++)
    {        
        // Column of drop
        let currColumn = parseInt(boardString[i]); 
        let player = (i % 2 === 0) ? 1 : 2;
        
        console.log(boardString);

        // Find row
        let currRow = -1;
        for(let j = ROWS - 1; j >= 0; j--)
        {
            // If row is empty
            if (board[j][currColumn] === 0) {
                currRow = j;
                
                break;
            }
        }

        // place player
        board[currRow][currColumn] = player;

        let tile = document.getElementById(currRow.toString() + "-" + currColumn.toString());
        if (player === 1) {
            tile.classList.add("red-piece");
        }
        else {
            tile.classList.add("yellow-piece");
        }
    }
}

akaAuthStateChanged((user) => {
    if (user) {

        // Set game
        setGame();
        gameuuid = sessionStorage.getItem("gameuuid");

        // Load game
        akaPollGame(gameuuid, fbUser().uid).then((game) => {

            // Load players
            akaGetUser(game.player_one).then((user) => {
                player_one = user;
                document.querySelector("#playerOne").innerHTML = player_one.username;
            });
            akaGetUser(game.player_two).then((user) => {
                player_two = user;
                document.querySelector("#playerOne").innerHTML = player_two.username;
            });

            // Update which is you
            if (game.player_one === fbUser().uid) {
                player_you = 1;
            } else {
                player_you = 2;
            }

            // draw board
            draw(game);
        })

    } else {
        window.location.href = "/login";
    }
});

document.querySelector("#forfeitButton").addEventListener("click", forfeitGame, false);