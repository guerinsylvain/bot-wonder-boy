-- Reward module
local M = {}

local previous_score = 0

function M.init(score)
    previous_score = score
end

function M.get_reward(score) 
    local reward = 0
    
    reward = score - previous_score
    previous_score = score
    
    return reward
end

return M