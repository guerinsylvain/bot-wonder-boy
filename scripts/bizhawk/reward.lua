-- Reward module
local M = {}

local previous_vitality = 0

function M.init(vitality)
    previous_vitality = vitality
end

function M.get_reward(vitality) 
    if previous_vitality == vitality then
        return 0
    else
        local reward = vitality - previous_vitality
        previous_vitality = vitality
        return reward
    end
end

return M