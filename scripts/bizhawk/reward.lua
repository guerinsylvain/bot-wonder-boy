-- Reward module
local M = {}

local previous_score = 0
local previous_vitality = 0
local previous_level_position = 0

function M.init(score, vitality, level_position)
    previous_score = score
    previous_vitality = vitality
    previous_level_position = level_position
end

function M.get_reward(score, vitality, level_position, is_dead) 

    -- A large negative reward of -100 is given to the system for dying
    if vitality == 0 or is_dead then
        previous_vitality = vitality
        previous_score = score
        previous_level_position = level_position
        return -100
    end

    -- A large positive reward of +100 is given for reaching the end of a level
    if level_position >= (32 * 255) then
        previous_vitality = vitality
        previous_score = score
        previous_level_position = level_position
        return 100
    end 

    -- A positive reward of +20 if vitality has increased
    if vitality > previous_vitality then
        previous_vitality = vitality
        previous_score = score
        previous_level_position = level_position
        return 20
    end

    -- A negative reward of -20 if vitality has decreased of more than 1 unit
    if (previous_vitality-vitality) > 1 then
        previous_vitality = vitality
        previous_score = score
        previous_level_position = level_position
        return -20
    end

    -- Grant small positive reward of +1 for increasing the game score
    if score > previous_score then
        previous_vitality = vitality
        previous_score = score
        previous_level_position = level_position
        return 1
    end

    -- A negative reward of -5 to prevent the agent from remaining in one area 
    -- and will ultimately prevent it from dying due to running out of time in a level
    if previous_level_position == level_position then
        previous_vitality = vitality
        previous_score = score
        previous_level_position = level_position
        return -5
    end 

    -- A small negative reward of -1 is given for any other action. 
    previous_vitality = vitality
    previous_score = score
    previous_level_position = level_position
    return -1
        
end

return M