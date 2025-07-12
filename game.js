const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game constants
const PADDLE_WIDTH = 100;
const PADDLE_HEIGHT = 15;
const BALL_SIZE = 15;
const BRICK_WIDTH = 75;
const BRICK_HEIGHT = 20;
const BRICK_ROWS = 5;
const BRICK_COLS = 10;

// Game objects
let paddle = { x: 350, y: 550, speed: 8 };
let ball = { x: 400, y: 300, dx: 4, dy: -4 };
let bricks = [];
let score = 0;
let lives = 3;
let gameOver = false;
let won = false;

// Colors
const colors = ['#ff0000', '#ffa500', '#ffff00', '#00ff00', '#0000ff'];

// Initialize game
function init() {
    createBricks();
    gameLoop();
}

function createBricks() {
    bricks = [];
    for (let row = 0; row < BRICK_ROWS; row++) {
        for (let col = 0; col < BRICK_COLS; col++) {
            bricks.push({
                x: col * (BRICK_WIDTH + 5) + 35,
                y: row * (BRICK_HEIGHT + 5) + 50,
                color: colors[row],
                destroyed: false
            });
        }
    }
}

function drawPaddle() {
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(paddle.x, paddle.y, PADDLE_WIDTH, PADDLE_HEIGHT);
    ctx.strokeStyle = '#00ffff';
    ctx.lineWidth = 2;
    ctx.strokeRect(paddle.x, paddle.y, PADDLE_WIDTH, PADDLE_HEIGHT);
}

function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, BALL_SIZE, 0, Math.PI * 2);
    ctx.fillStyle = '#ffffff';
    ctx.fill();
    ctx.strokeStyle = '#ffff00';
    ctx.lineWidth = 2;
    ctx.stroke();
}

function drawBricks() {
    bricks.forEach(brick => {
        if (!brick.destroyed) {
            ctx.fillStyle = brick.color;
            ctx.fillRect(brick.x, brick.y, BRICK_WIDTH, BRICK_HEIGHT);
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 1;
            ctx.strokeRect(brick.x, brick.y, BRICK_WIDTH, BRICK_HEIGHT);
        }
    });
}

function drawUI() {
    ctx.fillStyle = '#ffffff';
    ctx.font = '24px Arial';
    ctx.fillText(`Score: ${score}`, 10, 30);
    ctx.fillText(`Lives: ${lives}`, 10, 60);
    
    if (gameOver) {
        ctx.fillStyle = '#ff0000';
        ctx.font = '36px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('GAME OVER - Press R to Restart', 400, 300);
        ctx.textAlign = 'left';
    } else if (won) {
        ctx.fillStyle = '#00ff00';
        ctx.font = '36px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('YOU WIN! - Press R to Restart', 400, 300);
        ctx.textAlign = 'left';
    }
}

function update() {
    if (gameOver || won) return;
    
    // Move ball
    ball.x += ball.dx;
    ball.y += ball.dy;
    
    // Ball wall collisions
    if (ball.x <= BALL_SIZE || ball.x >= canvas.width - BALL_SIZE) {
        ball.dx = -ball.dx;
    }
    if (ball.y <= BALL_SIZE) {
        ball.dy = -ball.dy;
    }
    
    // Ball paddle collision
    if (ball.y + BALL_SIZE >= paddle.y && 
        ball.x >= paddle.x && 
        ball.x <= paddle.x + PADDLE_WIDTH) {
        ball.dy = -ball.dy;
        let hitPos = (ball.x - paddle.x) / PADDLE_WIDTH;
        ball.dx = (hitPos - 0.5) * 8;
    }
    
    // Ball brick collisions
    bricks.forEach(brick => {
        if (!brick.destroyed &&
            ball.x + BALL_SIZE >= brick.x &&
            ball.x - BALL_SIZE <= brick.x + BRICK_WIDTH &&
            ball.y + BALL_SIZE >= brick.y &&
            ball.y - BALL_SIZE <= brick.y + BRICK_HEIGHT) {
            brick.destroyed = true;
            ball.dy = -ball.dy;
            score += 10;
        }
    });
    
    // Ball falls off screen
    if (ball.y > canvas.height) {
        lives--;
        if (lives <= 0) {
            gameOver = true;
        } else {
            ball.x = 400;
            ball.y = 300;
            ball.dx = Math.random() > 0.5 ? 4 : -4;
            ball.dy = -4;
        }
    }
    
    // Check win condition
    if (bricks.every(brick => brick.destroyed)) {
        won = true;
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawPaddle();
    drawBall();
    drawBricks();
    drawUI();
}

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

function resetGame() {
    paddle.x = 350;
    ball.x = 400;
    ball.y = 300;
    ball.dx = Math.random() > 0.5 ? 4 : -4;
    ball.dy = -4;
    score = 0;
    lives = 3;
    gameOver = false;
    won = false;
    createBricks();
}

// Controls
const keys = {};
document.addEventListener('keydown', (e) => {
    keys[e.key] = true;
    if (e.key === 'r' || e.key === 'R') {
        if (gameOver || won) resetGame();
    }
});

document.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

function handleInput() {
    if (keys['ArrowLeft'] || keys['a'] || keys['A']) {
        if (paddle.x > 0) paddle.x -= paddle.speed;
    }
    if (keys['ArrowRight'] || keys['d'] || keys['D']) {
        if (paddle.x < canvas.width - PADDLE_WIDTH) paddle.x += paddle.speed;
    }
}

setInterval(handleInput, 16);

// Start game
init();