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
local vitality = 0
local level_position = 0

while playing do

    -- Reset game
    if inGame == false then
        console.clear()
        print("start new episode")
        savestate.load('train.State')
        inGame = true
        emu.frameadvance()
        vitality = mem.get_vitality()
        level_position = mem.get_level_position()
        reward.init(mem.get_score(), vitality)
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

        -- repeat the action on the next 30 frames (half a second)
        for i = 30,1,-1 
        do 
            actions.process(tonumber(action)); 
            emu.frameadvance()
            vitality = mem.get_vitality()
            level_position = mem.get_level_position()
            if vitality == 0 or level_position == 32 then
                print("exiting loop"..i)
                break
            end
        end        

        client.screenshottoclipboard()
        vitality = mem.get_vitality()
        level_position = mem.get_level_position()
        rwd = reward.get_reward(mem.get_score(), vitality, level_position) 

        if vitality == 0 then
            print("lost")
            inGame = false
            done = 1            
        end

        if level_position == 32 then
            print("won")
            inGame = false
            done = 1            
        end

        tcp:send(rwd.." "..done.." "..level_position)
        if inGame == true then
            emu.frameadvance()
        end
    end
    -- emu.frameadvance()
end

tcp:close()