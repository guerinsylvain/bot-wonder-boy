-- Reward module
local M = {}

local previous_score = 0
local previous_vitality = 0

function M.init(score, vitality)
    previous_score = score
    previous_vitality = vitality
end

function M.get_reward(score, vitality, level_position) 

    -- A large negative reward of -100 is given to the system for dying
    if vitality == 0 then
        previous_score = score
        return -100
    end

    -- A large positive reward of +100 is given for reaching the end of a level
    if level_position == 32 then
        previous_score = score
        return 100
    end 

    -- Grant small positive reward of +1 for increasing the game score
    if score > previous_score then
        previous_score = score
        return 1
    end

    -- A small negative reward of -1 is given for any other action. 
    -- Giving this constant negative reward will prevent the agent from remaining in one area 
    -- and will ultimately prevent it from dying due to running out of time in a level
    previous_score = score
    return -1
        
end

return M