-- Reward module
local M = {}

local previous_vitality = 0

function M.init(vitality)
    previous_vitality = vitality
end

function M.get_reward(vitality) 
    local reward = 0
    
    -- No reward if character is dead
    if vitality == 0 then
        return reward
    end

    -- If health has increased, it deserves also a reward
    if vitality > previous_vitality then
        reward = reward + ( (vitality - previous_vitality) * 1000)
    end

    previous_vitality = vitality
    return reward
end

return M