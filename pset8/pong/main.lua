Class = require 'class'
push = require 'push'

require 'Ball'
require 'Paddle'


-- set global definitions

WINDOW__WIDTH = 1280
WINDOW_HEIGHT = 720

VIRTUAL_WIDTH = 432
VIRTUAL_HEIGHT = 243

PADDLE_SPEED = 200

function love.load()
    math.randomseed(os.time())

    -- make sure text isnt blurry
    love.graphics.setDefaultFilter('nearest', 'nearest')
    -- title
    love.window.setTitle('Pong')

    -- set fonts
    smallFont = love.graphics.newFont('font.ttf', 8)
    scoreFont = love.graphics.newFont('font.ttf', 32)
    victoryFont = love.graphics.newFont('font.ttf', 24)

    -- set audiofiles
    sounds = {
        ['paddle_hit'] = love.audio.newSource('paddle_hit.wav', 'static'),
        ['point_scored'] = love.audio.newSource('point_scored.wav', 'static'),
        ['screen_hit'] = love.audio.newSource('screen_hit.wav', 'static')
    }

    -- declare variables
    player1Score = 0
    player2Score = 0

    servingPlayer = math.random(2) == 1 and 1 or 2
    winningPlayer = 0
    -- unless changed by pressing space the 2nd player is human (otherwise AI)
    player2 = 'human'
    gameState = 'start'

    -- declare objects
    paddle1 = Paddle(4, 20, 4, 20)
    paddle2 = Paddle(VIRTUAL_WIDTH - 10, VIRTUAL_HEIGHT - 30, 4, 20)
    ball = Ball(VIRTUAL_WIDTH / 2 - 2, VIRTUAL_HEIGHT / 2 - 2, 4, 4)

    -- set beginspeed
    if servingPlayer == 1 then
        ball.dx = 100
    else
        ball.dx = -100
    end

    -- set the window size
    push:setupScreen(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, WINDOW__WIDTH, WINDOW_HEIGHT, {
        fullscreen = false,
        vsync = true,
        resizable = true
    })
end

-- make sure the window resolution stays the same even if the user resizes
function love.resize(w,h)
    push:resize(w,h)
end

function love.update(dt)
    -- player 2 scores
    if ball.x < 0 then
        player2Score = player2Score + 1
        servingPlayer = 1
        sounds['point_scored']:play()
        ball:reset()
        if player2Score >= 10 then
            gameState = 'victory'
            winningPlayer = 2
        else
            gameState = 'serve'
        end
    end
    -- player 1 scores
    if ball.x >= VIRTUAL_WIDTH - 4 then
        player1Score = player1Score + 1
        servingPlayer = 2

        sounds['point_scored']:play()
        ball:reset()
        if player1Score >= 10 then
            gameState = 'victory'
            winningPlayer = 1
        else
            gameState = 'serve'
        end
    end

    if ball:collides(paddle1) then
    -- deflect ball to the right
        ball.dx = -ball.dx * 1.05
        sounds['paddle_hit']:play()
        -- change the vertical movement to make it less predictable
        if ball.dy < 0 then
            ball.dy = -math.random(10, 150)
        else
            ball.dy = math.random(10, 150)
        end

    end

    if ball:collides(paddle2) then
    -- deflect ball to the left
        ball.dx = -ball.dx * 1.05
        sounds['paddle_hit']:play()
        -- change the vertical movement to make it less predictable
        if ball.dy < 0 then
            ball.dy = -math.random(10, 150)
        else
            ball.dy = math.random(10, 150)
        end
    end

    if ball.y <= 0 then
        --deflect ball down and play the screen bounce sound
        ball.dy = -ball.dy
        ball.y = 0
        sounds['screen_hit']:play()
    end

    if ball.y >= VIRTUAL_HEIGHT - 4 then
        --deflect ball up and play the screen bounce sound
        ball.dy = -ball.dy
        ball.y = VIRTUAL_HEIGHT - 4
        sounds['screen_hit']:play()
    end

    -- see Paddle.lua, make sure the paddles move correctly
    paddle1:update(dt)
    paddle2:update(dt)

    -- Movement for paddle of player 1 with keyboardpressed
    if love.keyboard.isDown('w') then
        paddle1.dy = - PADDLE_SPEED

    elseif love.keyboard.isDown('s') then
        paddle1.dy = PADDLE_SPEED
    else
        paddle1.dy = 0
    end

    -- player 2 is either AI or multiplayer (functions at bottom)
    if player2 == 'AI' then
        playAI()
    else
        play2P()
    end

    -- make sure the ball moves properly (found in Ball.lua)
    if gameState == 'play' then
        ball:update(dt)
    end

end

function love.keypressed(key)
    -- quit game when 'esc' pressed
    if key == 'escape' then
        love.event.quit()
    elseif key == 'enter' or key == 'return' then
        if gameState == 'start' then
            gameState = 'serve'
        elseif gameState == 'serve' then
            gameState = 'play'
        elseif gameState == 'victory' then
            ball:reset()
            gameState = 'start'
            player1Score = 0
            player2Score = 0
        end
    end

    -- change player 2 to AI
    if gameState == 'start' then
        if player2 == 'human' then
            if key == 'space' then
                player2 = 'AI'
            end
        end
    end

end

function love.draw()
    push:apply('start')

    -- set color
    love.graphics.clear(45 / 255, 40 / 255, 52 / 255, 255 / 255)

    -- print screentext
    if gameState == 'start' then
        love.graphics.printf('Welcome to Pong!', 0 , 20, VIRTUAL_WIDTH, 'center')
        love.graphics.printf('Press Enter to play', 0, 32, VIRTUAL_WIDTH, 'center')
        love.graphics.printf('Press Space to play vs AI', 0, 44, VIRTUAL_WIDTH, 'center')
    elseif gameState == 'serve' then
        love.graphics.printf('Player '.. tostring(servingPlayer) .. ' serves', 0 , 20, VIRTUAL_WIDTH, 'center')
        love.graphics.printf('Press Enter to serve', 0, 32, VIRTUAL_WIDTH, 'center')
    elseif gameState == 'victory' then
        love.graphics.setFont(victoryFont)
        love.graphics.printf('Player '.. tostring(winningPlayer) .. ' wins', 0 , 20, VIRTUAL_WIDTH, 'center')
        love.graphics.setFont(smallFont)
        love.graphics.printf('Press Enter to reset', 0, 44, VIRTUAL_WIDTH, 'center')
    end

    -- print scores
    love.graphics.setFont(scoreFont)
    love.graphics.print(player1Score, VIRTUAL_WIDTH / 2 - 50, VIRTUAL_HEIGHT / 3)
    love.graphics.print(player2Score, VIRTUAL_WIDTH / 2 + 30, VIRTUAL_HEIGHT / 3)

    -- render rectangles and ball
    paddle1:render()
    paddle2:render()
    ball:render()

    -- display the fps in the top left
    displayFPS()

    push:apply('end')
end


function displayFPS()
    love.graphics.setColor(0, 1, 0, 1)
    love.graphics.setFont(smallFont)
    love.graphics.print('FPS: ' .. tostring (love.timer.getFPS()), 40, 20)
    love.graphics.setColor(1, 1, 1, 1)
end

-- set ai movement
function playAI()
    -- have the paddle move around the middle when the ball is moving to other player
    if ball.dx < 0 then
        if paddle2.y < VIRTUAL_HEIGHT / 2 - 20 then
            paddle2.dy = PADDLE_SPEED
        elseif paddle2.y > VIRTUAL_HEIGHT / 2 + 20 then
            paddle2.dy = -PADDLE_SPEED
        end
    end

    -- change the paddle movement depending on where the ball is
    if ball.dx > 0 then
        if ball.y < paddle2.y then
            paddle2.dy = -PADDLE_SPEED
        elseif ball.y > paddle2.y then
            paddle2.dy = PADDLE_SPEED
        elseif ball.y == paddle2.y then
            paddle2.dy = ball.dy
        end
    end
end

-- set multiplayer movement
function play2P()
        -- movement for player 2
    if love.keyboard.isDown('up') then
            paddle2.dy = -PADDLE_SPEED
    elseif love.keyboard.isDown('down') then
            paddle2.dy = PADDLE_SPEED
    else
            paddle2.dy = 0
    end
end