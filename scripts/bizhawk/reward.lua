-- Reward module
local M = {}

local previous_score = 0
local previous_vitality = 0

function M.init(score, vitality)
    previous_score = score
    previous_vitality = vitality
end

function M.get_reward(score, vitality) 
    local reward = 0

    -- Grant reward for score increase
    reward = score - previous_score
    previous_score = score

    -- Penality if more that one vitality is lost
    -- Will happen when touching a rock by example
    local vitalityDifference = previous_vitality - vitality
    if vitalityDifference > 1 then
        print(vitalityDifference)
        reward = reward - (100 * vitalityDifference)
    end
    previous_vitality = vitality
    
    return reward
end

return M