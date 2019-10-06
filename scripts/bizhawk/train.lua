local actions = require "actions"
local mem = require "memory"
local reward = require "reward"
local socket = require("socket")

local tcp = assert(socket.tcp())
tcp:connect("127.0.0.1", 8001)

-- main loop
console.clear()
local playing = true
local inGame = false

while playing do

    -- Reset game
    if inGame == false then
        console.clear()
        print("start new episode")
        savestate.load('train.State')
        inGame = true
        emu.frameadvance()
        reward.init(mem.get_vitality())
        client.screenshottoclipboard()
    end

    done = 0
    tcp:send("0")
    -- Loop when playing
    while inGame do 
        if inGame == false then
            break
        end
                
        -- get actions
        action = nil
        while action == nil do
            action, status, partial = tcp:receive('*l')           
        end

        actions.process(tonumber(action)); 
        emu.frameadvance()

        client.screenshottoclipboard()
        rwd = reward.get_reward(mem.get_vitality()) 
           
        if mem.get_vitality() == 0 then
            print("lost")
            inGame = false
            done = 1            
        end
        tcp:send(rwd.." "..done)
        emu.frameadvance()
    end
    emu.frameadvance()
end

tcp:close()